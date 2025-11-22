import logging
from typing import List, Optional

from core.domain.asset import Asset
from core.domain.exchange import Exchange
from core.domain.listing import Listing
from core.domain.enums import AssetClass
from core.repositories.asset_repository import AssetRepository
from core.repositories.exchange_repository import ExchangeRepository
from core.repositories.listing_repository import ListingRepository
from core.interfaces.market_data import MarketDataProvider, MarketDataAsset

logger = logging.getLogger(__name__)

class AssetSyncService:
    def __init__(
        self,
        asset_repository: AssetRepository,
        exchange_repository: ExchangeRepository,
        listing_repository: ListingRepository,
        market_data_provider: MarketDataProvider
    ):
        self.asset_repo = asset_repository
        self.exchange_repo = exchange_repository
        self.listing_repo = listing_repository
        self.market_data = market_data_provider

    def seed_exchanges(self, exchanges_data: List[dict]) -> None:
        """
        Seeds the database with exchanges from a provided list.
        exchanges_data: List of dicts with keys 'name', 'mic_code', 'currency'
        """
        logger.info(f"Seeding {len(exchanges_data)} exchanges")
        for ex_data in exchanges_data:
            exchange = Exchange(
                name=ex_data['name'],
                mic_code=ex_data['mic_code'],
                currency=ex_data['currency']
            )
            self.exchange_repo.upsert(exchange)
        logger.info("Exchange seeding complete")

    def sync_assets(self, tickers: List[str]) -> None:
        """
        Syncs assets and listings for the given list of tickers.
        """
        logger.info(f"Syncing {len(tickers)} assets...")

        # Fetch bulk data
        market_data_map = self.market_data.get_assets_bulk(tickers)

        for ticker, data in market_data_map.items():
            if not data:
                logger.warning(f"No data found for ticker {ticker}")
                continue

            try:
                self._process_asset_data(data)
            except Exception as e:
                logger.error(f"Failed to process asset {ticker}: {e}", exc_info=True)

        logger.info("Asset sync complete")

    def _process_asset_data(self, data: MarketDataAsset) -> None:
        # 1. Resolve Exchange
        # We need to map the market data exchange to our DB exchange.
        # YFinance gives us exchange codes like 'NMS' (Nasdaq), 'NYQ' (NYSE).
        # We need a mapping strategy. For now, we'll try to look up by MIC or fallback to a default if unknown.
        # Since we don't have a robust mapping table yet, we might skip or create a placeholder if we want.
        # BETTER APPROACH: We assume the caller knows which Exchange (MIC) these tickers belong to if they are passed in context,
        # but here we just have a list of tickers.
        # YFinance `exchange` field is tricky.

        # Simplification for this task:
        # If we can't find the exchange by MIC (assuming data.exchange_mic IS a mic or we have a map),
        # we might default to 'XNYS' or 'XNAS' for US stocks if ambiguous, or skip.

        # Let's try to map some common YF codes to MIC
        yf_to_mic = {
            'NMS': 'XNAS', # NASDAQ Global Select
            'NGM': 'XNAS', # NASDAQ Global Market
            'NCM': 'XNAS', # NASDAQ Capital Market
            'NYQ': 'XNYS', # NYSE
            'LSE': 'XLON', # London Stock Exchange
            # Add more as needed
        }

        mic_code = yf_to_mic.get(data.exchange_mic, data.exchange_mic) # Fallback to itself if not found

        exchange = self.exchange_repo.get_by_mic_code(mic_code)

        if not exchange:
            # If exchange doesn't exist, we can't create a Listing linked to it.
            # We could auto-create the exchange, but that risks creating garbage exchanges.
            # For now, log and skip.
            logger.warning(f"Exchange {data.exchange_mic} (mapped to {mic_code}) not found in DB. Skipping {data.ticker}")
            return

        # 2. Upsert Asset
        # Map string asset class to Enum
        try:
            # Ensure asset_class matches Enum string values
            # The MarketDataAsset already tries to map to Enum value string
            asset_class_enum = AssetClass(data.asset_class)
        except ValueError:
            logger.warning(f"Invalid asset class {data.asset_class} for {data.ticker}. Defaulting to STOCK.")
            asset_class_enum = AssetClass.STOCK

        asset = Asset(
            name=data.name,
            asset_class=asset_class_enum,
            isin=data.isin
        )

        # Check if ISIN exists to decide upsert logic in repo (handled by repo upsert)
        saved_asset = self.asset_repo.upsert(asset)

        # 3. Upsert Listing
        listing = Listing(
            asset_id=saved_asset.id,
            exchange_id=exchange.id,
            ticker=data.ticker,
            currency=data.currency
        )

        self.listing_repo.upsert(listing)
        logger.info(f"Successfully synced {data.ticker} ({saved_asset.name}) on {exchange.mic_code}")
