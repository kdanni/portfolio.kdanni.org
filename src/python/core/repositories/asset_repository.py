from abc import ABC, abstractmethod
from typing import Optional, List
from src.python.core.domain.asset import Asset

class AssetRepository(ABC):
    @abstractmethod
    def create(self, asset: Asset) -> Asset:
        """Creates a new asset."""
        pass

    @abstractmethod
    def get_by_id(self, asset_id: int) -> Optional[Asset]:
        """Retrieves an asset by its ID."""
        pass

    @abstractmethod
    def list_all(self) -> List[Asset]:
        """Lists all assets."""
        pass
