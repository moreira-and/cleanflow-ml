# infra/loaders/bcb_loader.py
from __future__ import annotations

import time
from typing import Any, Dict, Mapping, Optional, List

import requests
import pandas as pd

from src.domain.interfaces.repositories import IQuery
from src.infrastructure.config import YamlConfigProvider
from config.paths import DATASET_PARAMS_FILE
from config.logging_config import logger


class BcbLoader(IQuery):
    """
    Loader para dados do Banco Central (SGS API).
    Implementa contrato IQuery (get_by_id, list_all).
    """

    def __init__(
        self,
        start_date: str,
        end_date: str,
        *,
        sleep_seconds: float = 2.0,
        config: Optional[Mapping[str, str]] = None,
    ) -> None:
        self.start_date = pd.to_datetime(start_date, dayfirst=True)
        self.end_date = pd.to_datetime(end_date, dayfirst=True)
        self.sleep_seconds = sleep_seconds

        self._config: Dict[str, str] = dict(
            config or YamlConfigProvider(DATASET_PARAMS_FILE).get("bcb", {})
        )

    # ------------ IQuery ------------

    def get_by_id(self, ids: Optional[List[str]] = None) -> Mapping[str, Any]:
        requested = ids or list(self._config.keys())
        name_to_ticker = self._resolve_ids(requested)

        datasets: Dict[str, pd.DataFrame] = {}
        for name, ticker in name_to_ticker.items():
            logger.info(f"Downloading {name} ({ticker}) from BCB API...")
            try:
                df = self._request_bcb_series(ticker)
                if df is not None and not df.empty:
                    df.rename(columns={"valor": f"{name}_valor"}, inplace=True)
                    datasets[name] = df
                else:
                    logger.warning(f"No data returned for {name} ({ticker})")
            except Exception as e:
                logger.error(f"Error loading {name} ({ticker}): {e}", exc_info=True)

            if self.sleep_seconds:
                time.sleep(self.sleep_seconds)

        return datasets

    def list_all(self) -> List[str]:
        return list(self._config.keys())

    # ------------ Helpers ------------

    def _resolve_ids(self, ids: List[str]) -> Dict[str, str]:
        inverse = {ticker: name for name, ticker in self._config.items()}
        resolved: Dict[str, str] = {}
        for _id in ids:
            if _id in self._config:
                resolved[_id] = self._config[_id]  # name -> ticker
            elif _id in inverse:
                resolved[inverse[_id]] = _id  # ticker -> name
            else:
                resolved[_id] = _id  # fallback
        return resolved

    def _request_bcb_series(self, sgs_code: str) -> Optional[pd.DataFrame]:
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{sgs_code}/dados"
        params = {
            "formato": "json",
            "dataInicial": self.start_date.strftime("%d/%m/%Y"),
            "dataFinal": self.end_date.strftime("%d/%m/%Y"),
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                return None
            df = pd.DataFrame(data)
            df["data"] = pd.to_datetime(df["data"], dayfirst=True)
            return df.set_index("data")
        except Exception as e:
            logger.warning(f"Erro ao consultar API BCB: {e}", exc_info=True)
            return None
