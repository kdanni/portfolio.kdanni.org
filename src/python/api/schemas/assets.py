from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.python.core.domain.enums import AssetClass

class AssetCreate(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the asset")
    asset_class: AssetClass = Field(..., description="The class of the asset")
    isin: Optional[str] = Field(None, max_length=12, description="International Securities Identification Number")
    is_active: bool = Field(True, description="Whether the asset is active")

class AssetResponse(BaseModel):
    id: int
    name: str
    asset_class: AssetClass
    isin: Optional[str]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
