import logging
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from infrastructure.database.session import get_session
from infrastructure.repositories.asset_repository import SqlAlchemyAssetRepository
from infrastructure.repositories.exchange_repository import SqlAlchemyExchangeRepository
from infrastructure.repositories.listing_repository import SqlAlchemyListingRepository
from infrastructure.services.market_data_service import YFinanceMarketDataProvider
from core.services.asset_sync_service import AssetSyncService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_market_data():
    logger.info("Starting market data seed...")

    # Create session manually since we are not in a request context
    # get_session is a generator, we need the sessionmaker or equivalent
    # Actually infrastructure.database.session.get_session yields a session.
    # We can just iterate it once.

    session_gen = get_session()
    session = next(session_gen)

    try:
        asset_repo = SqlAlchemyAssetRepository(session)
        exchange_repo = SqlAlchemyExchangeRepository(session)
        listing_repo = SqlAlchemyListingRepository(session)
        market_data = YFinanceMarketDataProvider()

        service = AssetSyncService(asset_repo, exchange_repo, listing_repo, market_data)

        # 1. Seed Exchanges
        # A small subset of major exchanges
        exchanges = [
            {"name": "New York Stock Exchange", "mic_code": "XNYS", "currency": "USD"},
            {"name": "NASDAQ Global Select Market", "mic_code": "XNAS", "currency": "USD"},
            {"name": "London Stock Exchange", "mic_code": "XLON", "currency": "GBP"},
            {"name": "Tokyo Stock Exchange", "mic_code": "XTKS", "currency": "JPY"},
            {"name": "Frankfurt Stock Exchange", "mic_code": "XFRA", "currency": "EUR"},
        ]
        service.seed_exchanges(exchanges)

        # 2. Seed Assets (Discovery)
        # Since we don't have a discovery API, we'll seed with a few popular tickers
        # covering different asset classes and exchanges.
        initial_tickers = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", # Tech (NASDAQ)
            "JPM", "V", "WMT", # NYSE
            "TSLA",
            "BTC-USD", "ETH-USD", # Crypto
            "SPY", "VOO", # ETFs
            "AZN.L", "HSBA.L", # LSE (Note: YFinance uses .L for London)
            # Note: We need to ensure our service maps 'AZN.L' -> LSE (XLON) correctly.
            # The current map in AssetSyncService might need adjustment for suffix-based mapping if we want to be robust,
            # but let's see what YFinance returns for exchange code for these.
        ]

        service.sync_assets(initial_tickers)

        logger.info("Market data seed completed successfully.")

    except Exception as e:
        logger.error(f"Seeding failed: {e}", exc_info=True)
    finally:
        session.close()

if __name__ == "__main__":
    seed_market_data()
