import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.python.infrastructure.database.models import Base
from src.python.infrastructure.database.base import get_db_url
from src.python.core.domain.asset import Asset
from src.python.infrastructure.repositories.asset_repository import SqlAlchemyAssetRepository

# Use the same DB for now, but in real world we might use a separate test DB or schema
# For this POC, we will assume the docker DB is available for testing.
# WARNING: This will truncate tables in the dev DB!

@pytest.fixture(scope="module")
def db_engine():
    url = get_db_url()
    engine = create_engine(url)
    # Create tables if not exist (though alembic should have done it)
    # But for test isolation, let's drop and recreate
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine) # Cleanup

@pytest.fixture(scope="function")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def asset_repo(db_session):
    return SqlAlchemyAssetRepository(db_session)

def test_create_and_get_asset(asset_repo):
    asset = Asset(
        name="Apple Inc.",
        ticker="AAPL",
        asset_class="Equity"
    )

    created_asset = asset_repo.create(asset)

    assert created_asset.id is not None
    assert created_asset.name == "Apple Inc."
    assert created_asset.ticker == "AAPL"

    fetched_asset = asset_repo.get_by_id(created_asset.id)
    assert fetched_asset is not None
    assert fetched_asset.id == created_asset.id
    assert fetched_asset.ticker == "AAPL"

def test_get_by_ticker(asset_repo):
    asset = Asset(
        name="Microsoft Corp.",
        ticker="MSFT",
        asset_class="Equity"
    )
    asset_repo.create(asset)

    fetched_asset = asset_repo.get_by_ticker("MSFT")
    assert fetched_asset is not None
    assert fetched_asset.name == "Microsoft Corp."

def test_list_all(asset_repo):
    # Clean up previous tests is hard without transaction rollback fixture,
    # but we are in a proof of concept.
    # Since we use function scoped session, but the DB is module scoped and we commit in repo...
    # We might see data from previous tests if we don't clean up.
    # For simplicity, we just check if count increases.

    initial_count = len(asset_repo.list_all())

    asset = Asset(
        name="Google",
        ticker="GOOGL",
        asset_class="Equity"
    )
    asset_repo.create(asset)

    final_count = len(asset_repo.list_all())
    assert final_count == initial_count + 1

def test_unique_ticker_constraint(asset_repo):
    asset1 = Asset(name="Test", ticker="UNIQUE", asset_class="Equity")
    asset_repo.create(asset1)

    asset2 = Asset(name="Test2", ticker="UNIQUE", asset_class="Equity")

    with pytest.raises(Exception): # IntegrityError usually
        asset_repo.create(asset2)
