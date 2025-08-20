import time
from typing import Dict, Optional
import pandas as pd
import pandas_datareader.data as pdr

from src.core.interfaces.dataset_loading_strategy import IDatasetLoadingStrategy
from src.infrastructure.config.market_config import MarketConfigFacade
from src.infrastructure.logging import logger


class DataReaderLoadingStrategy(IDatasetLoadingStrategy):
    """
    Strategy to load datasets from DataReader (FRED).
    Bottom Line Up Front (BLUF): If your pipeline ignores these sources,
    you are missing critical insights and exposing blind spots.
    """

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        self._config = MarketConfigFacade().datareader_codes

    def load(self) -> Dict[str, pd.DataFrame]:
        dr_data = {}

        for ticker, name in self._config.items():
            logger.info(
                f"[BLUF] Capturing {name} ({ticker}) from DataReader — "
                f"without this data, your analysis risks being incomplete."
            )
            df = self._load_single_ticker(ticker, name)
            if df is not None:
                dr_data[name] = df

            time.sleep(2)  # avoid overloading the API

        return dr_data

    def _load_single_ticker(self, ticker: str, name: str) -> Optional[pd.DataFrame]:
        try:
            df = pdr.DataReader(
                ticker, "fred", start=self.start_date, end=self.end_date
            )
            if df.empty:
                logger.warning(
                    f"[GAP] No data returned for {name} ({ticker}) — "
                    "ignoring this means missing a piece of the economic puzzle."
                )
                return None
            return df
        except Exception as e:
            logger.error(
                f"[FAILURE] Could not load {name} ({ticker}): {e} — "
                "delays here represent lost opportunities in decision-making.",
                exc_info=True,
            )
            return None
