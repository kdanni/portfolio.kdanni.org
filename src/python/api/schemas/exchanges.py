from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class ExchangeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    mic_code: str = Field(..., min_length=1, max_length=20)
    currency: str = Field(..., min_length=3, max_length=10)
    is_active: bool = True

class ExchangeResponse(BaseModel):
    id: int
    name: str
    mic_code: str
    currency: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
