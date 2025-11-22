from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import app
from infrastructure.database.base import Base
from infrastructure.database.session import get_session
from core.domain.enums import AssetClass

# Setup in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_asset():
    response = client.post(
        "/assets/",
        json={
            "name": "Test Asset",
            "asset_class": "EQUITY",
            "isin": "US1234567890",
            "is_active": True
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Asset"
    assert data["asset_class"] == "EQUITY"
    assert "id" in data

def test_read_asset():
    # First create an asset
    create_response = client.post(
        "/assets/",
        json={
            "name": "Read Asset",
            "asset_class": "CASH",
            "isin": "US0987654321"
        },
    )
    asset_id = create_response.json()["id"]

    # Then read it
    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Read Asset"
    assert data["id"] == asset_id

def test_read_asset_not_found():
    response = client.get("/assets/99999")
    assert response.status_code == 404

def test_list_assets():
    # Clear DB (not needed for in-memory per test if we reset, but we are appending here)
    client.post(
        "/assets/",
        json={
            "name": "List Asset 1",
            "asset_class": "EQUITY"
        },
    )
    client.post(
        "/assets/",
        json={
            "name": "List Asset 2",
            "asset_class": "FIXED_INCOME"
        },
    )

    response = client.get("/assets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
