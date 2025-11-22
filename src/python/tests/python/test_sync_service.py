import pytest
from unittest.mock import MagicMock, patch
from core.services.asset_sync_service import AssetSyncService
from core.domain.asset import Asset
from core.domain.exchange import Exchange
from core.domain.listing import Listing
from core.domain.enums import AssetClass
from core.interfaces.market_data import MarketDataAsset

@pytest.fixture
def mock_asset_repo():
    repo = MagicMock()
    repo.upsert.side_effect = lambda x: Asset(id=1, name=x.name, asset_class=x.asset_class, isin=x.isin)
    return repo

@pytest.fixture
def mock_exchange_repo():
    repo = MagicMock()
    # Simulate finding an exchange
    repo.get_by_mic_code.return_value = Exchange(id=1, name="Test Exchange", mic_code="XNYS", currency="USD")
    return repo

@pytest.fixture
def mock_listing_repo():
    return MagicMock()

@pytest.fixture
def mock_market_data():
    provider = MagicMock()
    # Simulate returning data
    provider.get_assets_bulk.return_value = {
        "AAPL": MarketDataAsset(
            ticker="AAPL",
            name="Apple Inc.",
            currency="USD",
            asset_class="EQUITY",
            exchange_mic="NMS" # Should map to NASDAQ -> XNAS, but here we can test mapping logic or just mock what we expect
        )
    }
    return provider

def test_sync_assets(mock_asset_repo, mock_exchange_repo, mock_listing_repo, mock_market_data):
    service = AssetSyncService(mock_asset_repo, mock_exchange_repo, mock_listing_repo, mock_market_data)

    # Override the exchange mapping inside service for test if needed,
    # or ensure our mock returns what is needed.
    # In the code: 'NMS' -> 'XNAS'.
    # We need to ensure mock_exchange_repo.get_by_mic_code("XNAS") returns something.
    mock_exchange_repo.get_by_mic_code.side_effect = lambda mic: Exchange(id=1, name="Nasdaq", mic_code="XNAS", currency="USD") if mic == "XNAS" else None

    service.sync_assets(["AAPL"])

    mock_market_data.get_assets_bulk.assert_called_once_with(["AAPL"])
    mock_asset_repo.upsert.assert_called_once()
    mock_listing_repo.upsert.assert_called_once()

    # Verify correct data was passed
    created_listing = mock_listing_repo.upsert.call_args[0][0]
    assert created_listing.ticker == "AAPL"
    assert created_listing.exchange_id == 1

def test_seed_exchanges(mock_asset_repo, mock_exchange_repo, mock_listing_repo, mock_market_data):
    service = AssetSyncService(mock_asset_repo, mock_exchange_repo, mock_listing_repo, mock_market_data)

    exchanges = [{"name": "Test", "mic_code": "TEST", "currency": "USD"}]
    service.seed_exchanges(exchanges)

    mock_exchange_repo.upsert.assert_called_once()
