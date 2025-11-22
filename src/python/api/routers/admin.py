from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from infrastructure.database.session import get_session
from infrastructure.repositories.asset_repository import SqlAlchemyAssetRepository
from infrastructure.repositories.exchange_repository import SqlAlchemyExchangeRepository
from infrastructure.repositories.listing_repository import SqlAlchemyListingRepository
from infrastructure.services.market_data_service import YFinanceMarketDataProvider
from core.services.asset_sync_service import AssetSyncService

router = APIRouter()

class SyncRequest(BaseModel):
    tickers: List[str]

def get_sync_service(session: Session = Depends(get_session)) -> AssetSyncService:
    asset_repo = SqlAlchemyAssetRepository(session)
    exchange_repo = SqlAlchemyExchangeRepository(session)
    listing_repo = SqlAlchemyListingRepository(session)
    market_data = YFinanceMarketDataProvider()
    return AssetSyncService(asset_repo, exchange_repo, listing_repo, market_data)

# Helper function to run sync in background with its own session management if needed,
# but since BackgroundTasks runs in the same process, we need to be careful with session scope.
# FastAPI dependency injection sessions are closed after the request.
# So we should probably instantiate a fresh service/session inside the background task wrapper.

def run_sync_task(tickers: List[str]):
    # Create a new session for the background task
    session_gen = get_session()
    session = next(session_gen)
    try:
        asset_repo = SqlAlchemyAssetRepository(session)
        exchange_repo = SqlAlchemyExchangeRepository(session)
        listing_repo = SqlAlchemyListingRepository(session)
        market_data = YFinanceMarketDataProvider()
        service = AssetSyncService(asset_repo, exchange_repo, listing_repo, market_data)

        service.sync_assets(tickers)
    except Exception as e:
        print(f"Background sync failed: {e}")
    finally:
        session.close()

@router.post("/sync", status_code=202)
def trigger_sync(
    request: SyncRequest,
    background_tasks: BackgroundTasks
):
    """
    Triggers an asynchronous sync of assets for the provided tickers.
    """
    if not request.tickers:
        raise HTTPException(status_code=400, detail="No tickers provided")

    background_tasks.add_task(run_sync_task, request.tickers)
    return {"message": f"Sync triggered for {len(request.tickers)} tickers"}
