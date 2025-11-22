from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.domain.listing import Listing
from core.repositories.listing_repository import ListingRepository
from infrastructure.database.models import ListingModel

class SqlAlchemyListingRepository(ListingRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: ListingModel) -> Listing:
        return Listing(
            id=model.id,
            asset_id=model.asset_id,
            exchange_id=model.exchange_id,
            ticker=model.ticker,
            currency=model.currency,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, domain: Listing) -> ListingModel:
        return ListingModel(
            asset_id=domain.asset_id,
            exchange_id=domain.exchange_id,
            ticker=domain.ticker,
            currency=domain.currency,
            is_active=domain.is_active
        )

    def create(self, listing: Listing) -> Listing:
        model = self._to_model(listing)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_domain(model)

    def get_by_id(self, listing_id: int) -> Optional[Listing]:
        stmt = select(ListingModel).where(ListingModel.id == listing_id)
        result = self.session.execute(stmt).scalar_one_or_none()
        if result:
            return self._to_domain(result)
        return None

    def list_all(self) -> List[Listing]:
        stmt = select(ListingModel)
        results = self.session.execute(stmt).scalars().all()
        return [self._to_domain(r) for r in results]

    def get_by_asset_id(self, asset_id: int) -> List[Listing]:
        stmt = select(ListingModel).where(ListingModel.asset_id == asset_id)
        results = self.session.execute(stmt).scalars().all()
        return [self._to_domain(r) for r in results]
