from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.domain.enums import AssetClass

@dataclass
class Asset:
    name: str
    asset_class: AssetClass
    id: Optional[int] = None
    isin: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name cannot be empty")
        # Ensure asset_class is a valid Enum member if it's passed as a string (optional, but good for safety)
        if isinstance(self.asset_class, str):
            try:
                self.asset_class = AssetClass(self.asset_class.upper())
            except ValueError:
                raise ValueError(f"Invalid asset class: {self.asset_class}")
