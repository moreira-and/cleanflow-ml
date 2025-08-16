# infra/loaders/yfinance_loader.py
from __future__ import annotations

import time
from typing import Any, Dict, Mapping, Optional, List

import pandas as pd
import yfinance as yf

from src.domain.interfaces.repositories import IQuery
from src.infrastructure.config import YamlConfigProvider
from config.paths import DATASET_PARAMS_FILE
from config.logging_config import logger


class YfinanceLoader(IQuery):
    """
    Infrastructure Layer loader implementing the IQuery interface.
    Preserves functionality from the previous loader (dates, interval, logging,
    and simple retries via sleep) under the new contract (get_by_id / list_all).
    """

    def __init__(
        self,
        start_date: str,
        end_date: str,
        *,
        interval: str = "1d",
        auto_adjust: bool = True,
        sleep_seconds: float = 2.0,
        config: Optional[Mapping[str, str]] = None,
    ) -> None:
        """
        :param start_date: Start date (YYYY-MM-DD)
        :param end_date: End date (YYYY-MM-DD)
        :param interval: Data interval, e.g., "1d", "1h", "5m"
        :param auto_adjust: Adjust prices for dividends and splits
        :param sleep_seconds: Sleep time between downloads (simple rate limiting)
        :param config: Optional mapping name->ticker; defaults to MarketConfigFacade
        """
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.auto_adjust = auto_adjust
        self.sleep_seconds = sleep_seconds

        self._config: Dict[str, str] = dict(
            config or YamlConfigProvider(DATASET_PARAMS_FILE).get("yfinance", {})
        )

    # ------------ IQuery ------------

    def get_by_id(self, ids: Optional[List[str]] = None) -> Mapping[str, Any]:
        """
        Fetch data from yfinance for the given IDs (or all if ids=None).
        IDs can be either 'name' (config key) or 'ticker' (config value).
        Returns: Dict[name, pd.DataFrame]
        """
        # fallback: sem ids -> todos
        requested = ids or list(self._config.keys())
        name_to_ticker = self._resolve_ids(requested)

        datasets: Dict[str, pd.DataFrame] = {}
        for name, ticker in name_to_ticker.items():
            logger.info(f"Downloading {name} ({ticker}) from yfinance...")
            try:
                df = yf.download(
                    ticker,
                    start=self.start_date,
                    end=self.end_date,
                    interval=self.interval,
                    auto_adjust=self.auto_adjust,
                    progress=False,
                    threads=False,
                )
                if isinstance(df, pd.DataFrame) and not df.empty:
                    df.columns = [
                        (
                            f"{name}_{col[0]}"
                            if isinstance(col, tuple)
                            else f"{name}_{col}"
                        )
                        for col in df.columns
                    ]
                    datasets[name] = df
                else:
                    logger.warning(f"No data returned for {ticker}")
            except Exception as e:
                logger.error(f"Error loading {ticker}: {e}")
            if self.sleep_seconds:
                time.sleep(self.sleep_seconds)

        return datasets

    def list_all(self) -> List[str]:
        """
        List all available IDs (logical names) from the configuration.
        """
        return list(self._config.keys())

    # ------------ Helpers ------------

    def _resolve_ids(self, ids: List[str]) -> Dict[str, str]:
        """
        Resolves provided IDs into a name -> ticker mapping.
        - If ID exists in config keys: treat as 'name'
        - If ID exists in config values: treat as 'ticker' and map to 'name'
        - Otherwise: fallback, use the raw ID as both name and ticker
        """
        inverse = {ticker: name for name, ticker in self._config.items()}
        resolved: Dict[str, str] = {}
        for _id in ids:
            if _id in self._config:
                resolved[_id] = self._config[_id]  # name -> ticker
            elif _id in inverse:
                resolved[inverse[_id]] = _id  # ticker -> name
            else:
                # fallback
                resolved[_id] = _id
        return resolved
