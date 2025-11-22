from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from dataclasses import dataclass

@dataclass
class MarketDataAsset:
    ticker: str
    name: str
    currency: str
    asset_class: str
    isin: Optional[str] = None
    exchange_mic: Optional[str] = None

@dataclass
class MarketDataExchange:
    name: str
    mic_code: str
    currency: str

class MarketDataProvider(ABC):
    @abstractmethod
    def get_asset_details(self, ticker: str) -> Optional[MarketDataAsset]:
        """Fetch details for a single asset by ticker."""
        pass

    @abstractmethod
    def get_exchange_details(self, mic_code: str) -> Optional[MarketDataExchange]:
        """Fetch details for an exchange by MIC code."""
        pass

    @abstractmethod
    def get_assets_bulk(self, tickers: List[str]) -> Dict[str, Optional[MarketDataAsset]]:
        """Fetch details for multiple assets."""
        pass
