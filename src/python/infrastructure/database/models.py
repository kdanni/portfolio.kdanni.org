from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, CheckConstraint, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from src.python.infrastructure.database.base import Base
import datetime
from src.python.core.domain.enums import AssetClass

class ExchangeModel(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    mic_code = Column(String(20), nullable=False, unique=True)
    currency = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint("length(mic_code) > 0", name="check_mic_code_length"),
        CheckConstraint("length(name) > 0", name="check_exchange_name_length"),
    )

    def __repr__(self):
        return f"<Exchange(id={self.id}, mic_code='{self.mic_code}', name='{self.name}')>"

class AssetModel(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    asset_class = Column(Enum(AssetClass), nullable=False)
    isin = Column(String(12), unique=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    listings = relationship("ListingModel", backref="asset", cascade="all, delete-orphan")

    # Constraints for robust data integrity
    __table_args__ = (
        CheckConstraint("length(name) > 0", name="check_name_length"),
    )

    def __repr__(self):
        return f"<Asset(id={self.id}, name='{self.name}')>"

class ListingModel(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    exchange_id = Column(Integer, ForeignKey("exchanges.id"), nullable=False)
    ticker = Column(String(20), nullable=False)
    currency = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    exchange = relationship("ExchangeModel", backref="listings")

    __table_args__ = (
        CheckConstraint("length(ticker) > 0", name="check_ticker_length"),
        UniqueConstraint('ticker', 'exchange_id', name='uq_listing_ticker_exchange'),
    )

    def __repr__(self):
        return f"<Listing(id={self.id}, ticker='{self.ticker}', exchange_id={self.exchange_id})>"
