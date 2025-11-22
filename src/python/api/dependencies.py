from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.database.session import get_session
from core.repositories.asset_repository import AssetRepository
from infrastructure.repositories.asset_repository import SqlAlchemyAssetRepository
from core.repositories.exchange_repository import ExchangeRepository
from infrastructure.repositories.exchange_repository import SqlAlchemyExchangeRepository
from core.repositories.listing_repository import ListingRepository
from infrastructure.repositories.listing_repository import SqlAlchemyListingRepository

def get_asset_repository(session: Session = Depends(get_session)) -> AssetRepository:
    return SqlAlchemyAssetRepository(session)

def get_exchange_repository(session: Session = Depends(get_session)) -> ExchangeRepository:
    return SqlAlchemyExchangeRepository(session)

def get_listing_repository(session: Session = Depends(get_session)) -> ListingRepository:
    return SqlAlchemyListingRepository(session)
