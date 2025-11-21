from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Asset:
    name: str
    ticker: str
    asset_class: str
    id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        # Basic validation (business rules should go here)
        if not self.ticker:
            raise ValueError("Ticker cannot be empty")
        if not self.name:
            raise ValueError("Name cannot be empty")
