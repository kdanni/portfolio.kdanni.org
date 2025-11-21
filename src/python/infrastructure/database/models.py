from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, CheckConstraint
from src.python.infrastructure.database.base import Base
import datetime

class AssetModel(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    ticker = Column(String(20), nullable=False, unique=True)
    asset_class = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Constraints for robust data integrity
    __table_args__ = (
        CheckConstraint("length(ticker) > 0", name="check_ticker_length"),
        CheckConstraint("length(name) > 0", name="check_name_length"),
    )

    def __repr__(self):
        return f"<Asset(id={self.id}, ticker='{self.ticker}', name='{self.name}')>"
