from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class ListingCreate(BaseModel):
    asset_id: int
    exchange_id: int
    ticker: str = Field(..., min_length=1, max_length=20)
    currency: str = Field(..., min_length=3, max_length=10)
    is_active: bool = True

class ListingResponse(BaseModel):
    id: int
    asset_id: int
    exchange_id: int
    ticker: str
    currency: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
