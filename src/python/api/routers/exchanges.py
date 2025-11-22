from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.exchanges import ExchangeCreate, ExchangeResponse
from core.domain.exchange import Exchange
from core.repositories.exchange_repository import ExchangeRepository
from api.dependencies import get_exchange_repository

router = APIRouter(
    prefix="/exchanges",
    tags=["exchanges"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ExchangeResponse, status_code=status.HTTP_201_CREATED)
def create_exchange(
    exchange_in: ExchangeCreate,
    repository: ExchangeRepository = Depends(get_exchange_repository)
):
    domain_exchange = Exchange(
        name=exchange_in.name,
        mic_code=exchange_in.mic_code,
        currency=exchange_in.currency,
        is_active=exchange_in.is_active
    )
    # Note: Exceptions from unique constraints are currently handled by the global exception handler (if any)
    # or will result in a 500 error. In a more complete implementation, we'd catch IntegrityError here.
    created_exchange = repository.create(domain_exchange)
    return created_exchange

@router.get("/{exchange_id}", response_model=ExchangeResponse)
def read_exchange(
    exchange_id: int,
    repository: ExchangeRepository = Depends(get_exchange_repository)
):
    exchange = repository.get_by_id(exchange_id)
    if exchange is None:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return exchange

@router.get("/", response_model=List[ExchangeResponse])
def list_exchanges(
    repository: ExchangeRepository = Depends(get_exchange_repository)
):
    exchanges = repository.list_all()
    return exchanges
