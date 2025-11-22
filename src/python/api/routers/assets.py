from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.assets import AssetCreate, AssetResponse
from core.domain.asset import Asset
from core.repositories.asset_repository import AssetRepository
from api.dependencies import get_asset_repository

router = APIRouter(
    prefix="/assets",
    tags=["assets"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    asset_in: AssetCreate,
    repository: AssetRepository = Depends(get_asset_repository)
):
    # Convert Pydantic model to Domain model
    domain_asset = Asset(
        name=asset_in.name,
        asset_class=asset_in.asset_class,
        isin=asset_in.isin,
        is_active=asset_in.is_active
    )
    created_asset = repository.create(domain_asset)
    return created_asset

@router.get("/{asset_id}", response_model=AssetResponse)
def read_asset(
    asset_id: int,
    repository: AssetRepository = Depends(get_asset_repository)
):
    asset = repository.get_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.get("/", response_model=List[AssetResponse])
def list_assets(
    repository: AssetRepository = Depends(get_asset_repository)
):
    assets = repository.list_all()
    return assets
