from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert

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

    def upsert(self, asset: Asset) -> Asset:
        model_data = {
            "name": asset.name,
            "asset_class": asset.asset_class,
            "isin": asset.isin,
            "is_active": asset.is_active,
            "updated_at": func.now()
        }

        # We need to decide what constraint to use for conflict.
        # ISIN is unique but nullable. Name is not unique.
        # If ISIN is present, use it.
        # However, `pg_insert` needs a specific constraint.
        # If ISIN is None, we might just insert new asset or rely on a "soft" deduplication in the service layer.
        # For now, we assume upsert is mostly for ISIN-based updates or we treat it as create if no ISIN.

        if asset.isin:
            stmt = pg_insert(AssetModel).values(
                name=asset.name,
                asset_class=asset.asset_class,
                isin=asset.isin,
                is_active=asset.is_active
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=[AssetModel.isin],
                set_=model_data
            ).returning(AssetModel)

            result = self.session.execute(stmt).scalar_one()
            self.session.commit()
            return self._to_domain(result)
        else:
             # If no ISIN, try to find by name and asset_class as a fallback "identity"
             # This is not perfect as names can change, but better than blind duplicates for things like Crypto
             stmt = select(AssetModel).where(
                 AssetModel.name == asset.name,
                 AssetModel.asset_class == asset.asset_class,
                 AssetModel.isin == None
             )
             existing = self.session.execute(stmt).scalar_one_or_none()

             if existing:
                 # Update existing
                 existing.is_active = asset.is_active
                 # name/class are same
                 existing.updated_at = func.now()
                 self.session.commit()
                 self.session.refresh(existing)
                 return self._to_domain(existing)
             else:
                 return self.create(asset)
