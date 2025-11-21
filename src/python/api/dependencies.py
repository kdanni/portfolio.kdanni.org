from fastapi import Depends
from sqlalchemy.orm import Session
from src.python.infrastructure.database.session import get_session
from src.python.core.repositories.asset_repository import AssetRepository
from src.python.infrastructure.repositories.asset_repository import SqlAlchemyAssetRepository

def get_asset_repository(session: Session = Depends(get_session)) -> AssetRepository:
    return SqlAlchemyAssetRepository(session)
