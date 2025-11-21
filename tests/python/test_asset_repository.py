import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from src.python.infrastructure.database.models import Base, ExchangeModel, ListingModel
from src.python.infrastructure.database.base import get_db_url
from src.python.core.domain.asset import Asset
from src.python.core.domain.enums import AssetClass
from src.python.core.domain.listing import Listing
from src.python.infrastructure.repositories.asset_repository import SqlAlchemyAssetRepository
from src.python.infrastructure.repositories.listing_repository import SqlAlchemyListingRepository

@pytest.fixture(scope="module")
def db_engine():
    url = get_db_url()
    engine = create_engine(url)
    # Drop and recreate tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def exchange(db_session):
    stmt = select(ExchangeModel).where(ExchangeModel.mic_code == "XNAS")
    existing = db_session.execute(stmt).scalar_one_or_none()
    if existing:
        return existing

    exchange = ExchangeModel(
        name="NASDAQ",
        mic_code="XNAS",
        currency="USD"
    )
    db_session.add(exchange)
    db_session.commit()
    db_session.refresh(exchange)
    return exchange

@pytest.fixture
def asset_repo(db_session):
    return SqlAlchemyAssetRepository(db_session)

@pytest.fixture
def listing_repo(db_session):
    return SqlAlchemyListingRepository(db_session)

def test_create_asset_and_listing(asset_repo, listing_repo, exchange):
    # 1. Create Asset (Instrument)
    asset = Asset(
        name="Apple Inc.",
        asset_class=AssetClass.EQUITY,
        isin="US0378331005"
    )
    created_asset = asset_repo.create(asset)

    assert created_asset.id is not None
    assert created_asset.name == "Apple Inc."
    assert created_asset.asset_class == AssetClass.EQUITY
    assert created_asset.isin == "US0378331005"

    # 2. Create Listing
    listing = Listing(
        asset_id=created_asset.id,
        exchange_id=exchange.id,
        ticker="AAPL",
        currency="USD"
    )
    created_listing = listing_repo.create(listing)

    assert created_listing.id is not None
    assert created_listing.ticker == "AAPL"
    assert created_listing.asset_id == created_asset.id
    assert created_listing.exchange_id == exchange.id

    # 3. Retrieve Listing
    fetched_listing = listing_repo.get_by_ticker_and_exchange("AAPL", exchange.id)
    assert fetched_listing is not None
    assert fetched_listing.asset_id == created_asset.id

def test_multiple_listings_for_asset(asset_repo, listing_repo, exchange, db_session):
    # Create another exchange
    exchange_lse = ExchangeModel(
        name="London Stock Exchange",
        mic_code="XLON",
        currency="GBP"
    )
    db_session.add(exchange_lse)
    db_session.commit()

    # Create Asset
    asset = Asset(
        name="Rio Tinto",
        asset_class=AssetClass.EQUITY
    )
    created_asset = asset_repo.create(asset)

    # Listing 1 (LSE)
    listing1 = Listing(
        asset_id=created_asset.id,
        exchange_id=exchange_lse.id,
        ticker="RIO",
        currency="GBP"
    )
    listing_repo.create(listing1)

    # Listing 2 (NASDAQ - assuming dual listed for test)
    listing2 = Listing(
        asset_id=created_asset.id,
        exchange_id=exchange.id,
        ticker="RIO",
        currency="USD"
    )
    listing_repo.create(listing2)

    listings = listing_repo.list_by_asset(created_asset.id)
    assert len(listings) == 2

    currencies = {l.currency for l in listings}
    assert "USD" in currencies
    assert "GBP" in currencies

def test_unique_ticker_per_exchange(asset_repo, listing_repo, exchange):
    asset = Asset(name="Test Corp", asset_class=AssetClass.EQUITY)
    created_asset = asset_repo.create(asset)

    listing1 = Listing(
        asset_id=created_asset.id,
        exchange_id=exchange.id,
        ticker="UNIQUE",
        currency="USD"
    )
    listing_repo.create(listing1)

    # Try to create same ticker on same exchange
    listing2 = Listing(
        asset_id=created_asset.id,
        exchange_id=exchange.id,
        ticker="UNIQUE",
        currency="USD"
    )

    with pytest.raises(Exception):
        listing_repo.create(listing2)
