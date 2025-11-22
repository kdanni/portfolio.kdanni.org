from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.base import get_db_url

# Create the engine using the URL from base.py
engine = create_engine(get_db_url())

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """
    Generator function to get a database session.
    Usage:
        session = next(get_session())
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
