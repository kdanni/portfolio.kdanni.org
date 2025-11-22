from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.listings import ListingCreate, ListingResponse
from core.domain.listing import Listing
from core.repositories.listing_repository import ListingRepository
from api.dependencies import get_listing_repository

router = APIRouter(
    prefix="/listings",
    tags=["listings"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
def create_listing(
    listing_in: ListingCreate,
    repository: ListingRepository = Depends(get_listing_repository)
):
    domain_listing = Listing(
        asset_id=listing_in.asset_id,
        exchange_id=listing_in.exchange_id,
        ticker=listing_in.ticker,
        currency=listing_in.currency,
        is_active=listing_in.is_active
    )
    # Note: Foreign key violations and unique constraint violations should be handled here
    # but for this iteration, we rely on the database layer to enforce them.
    created_listing = repository.create(domain_listing)
    return created_listing

@router.get("/{listing_id}", response_model=ListingResponse)
def read_listing(
    listing_id: int,
    repository: ListingRepository = Depends(get_listing_repository)
):
    listing = repository.get_by_id(listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.get("/", response_model=List[ListingResponse])
def list_listings(
    repository: ListingRepository = Depends(get_listing_repository)
):
    listings = repository.list_all()
    return listings

@router.get("/asset/{asset_id}", response_model=List[ListingResponse])
def list_listings_by_asset(
    asset_id: int,
    repository: ListingRepository = Depends(get_listing_repository)
):
    listings = repository.get_by_asset_id(asset_id)
    return listings
