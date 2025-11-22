from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.domain.asset import Asset
from core.repositories.asset_repository import AssetRepository
from infrastructure.database.models import AssetModel

class SqlAlchemyAssetRepository(AssetRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: AssetModel) -> Asset:
        return Asset(
            id=model.id,
            name=model.name,
            asset_class=model.asset_class,
            isin=model.isin,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, domain: Asset) -> AssetModel:
        return AssetModel(
            name=domain.name,
            asset_class=domain.asset_class,
            isin=domain.isin,
            is_active=domain.is_active
        )

    def create(self, asset: Asset) -> Asset:
        model = self._to_model(asset)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_domain(model)

    def get_by_id(self, asset_id: int) -> Optional[Asset]:
        stmt = select(AssetModel).where(AssetModel.id == asset_id)
        result = self.session.execute(stmt).scalar_one_or_none()
        if result:
            return self._to_domain(result)
        return None

    def list_all(self) -> List[Asset]:
        stmt = select(AssetModel)
        results = self.session.execute(stmt).scalars().all()
        return [self._to_domain(r) for r in results]

    # Removed get_by_ticker since ticker is no longer on Asset
