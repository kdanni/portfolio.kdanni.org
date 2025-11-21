from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Listing:
    asset_id: int
    exchange_id: int
    ticker: str
    currency: str
    id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.ticker:
            raise ValueError("Ticker cannot be empty")
        if not self.asset_id:
            raise ValueError("Asset ID must be provided")
        if not self.exchange_id:
            raise ValueError("Exchange ID must be provided")
