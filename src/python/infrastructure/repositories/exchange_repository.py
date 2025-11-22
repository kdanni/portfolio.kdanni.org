from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert

from core.domain.exchange import Exchange
from core.repositories.exchange_repository import ExchangeRepository
from infrastructure.database.models import ExchangeModel

class SqlAlchemyExchangeRepository(ExchangeRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: ExchangeModel) -> Exchange:
        return Exchange(
            id=model.id,
            name=model.name,
            mic_code=model.mic_code,
            currency=model.currency,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, domain: Exchange) -> ExchangeModel:
        return ExchangeModel(
            name=domain.name,
            mic_code=domain.mic_code,
            currency=domain.currency,
            is_active=domain.is_active
        )

    def create(self, exchange: Exchange) -> Exchange:
        model = self._to_model(exchange)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_domain(model)

    def get_by_id(self, exchange_id: int) -> Optional[Exchange]:
        stmt = select(ExchangeModel).where(ExchangeModel.id == exchange_id)
        result = self.session.execute(stmt).scalar_one_or_none()
        if result:
            return self._to_domain(result)
        return None

    def list_all(self) -> List[Exchange]:
        stmt = select(ExchangeModel)
        results = self.session.execute(stmt).scalars().all()
        return [self._to_domain(r) for r in results]

    def upsert(self, exchange: Exchange) -> Exchange:
        model_data = {
            "name": exchange.name,
            "currency": exchange.currency,
            "is_active": exchange.is_active,
            "updated_at": func.now()
        }

        stmt = pg_insert(ExchangeModel).values(
            name=exchange.name,
            mic_code=exchange.mic_code,
            currency=exchange.currency,
            is_active=exchange.is_active
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[ExchangeModel.mic_code],
            set_=model_data
        ).returning(ExchangeModel)

        result = self.session.execute(stmt).scalar_one()
        self.session.commit()
        return self._to_domain(result)

    def get_by_mic_code(self, mic_code: str) -> Optional[Exchange]:
        stmt = select(ExchangeModel).where(ExchangeModel.mic_code == mic_code)
        result = self.session.execute(stmt).scalar_one_or_none()
        if result:
            return self._to_domain(result)
        return None
