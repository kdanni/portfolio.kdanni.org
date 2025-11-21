import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    metadata = MetaData()

# Helper to get DB URL from environment or default
def get_db_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "assetmanager")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
