from abc import ABC, abstractmethod
from typing import List, Optional

from core.domain.exchange import Exchange

class ExchangeRepository(ABC):
    @abstractmethod
    def create(self, exchange: Exchange) -> Exchange:
        """Creates a new exchange."""
        pass

    @abstractmethod
    def get_by_id(self, exchange_id: int) -> Optional[Exchange]:
        """Retrieves an exchange by its ID."""
        pass

    @abstractmethod
    def list_all(self) -> List[Exchange]:
        """Lists all exchanges."""
        pass
