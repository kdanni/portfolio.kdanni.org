from abc import ABC, abstractmethod
from typing import List, Optional

from core.domain.listing import Listing

class ListingRepository(ABC):
    @abstractmethod
    def create(self, listing: Listing) -> Listing:
        """Creates a new listing."""
        pass

    @abstractmethod
    def get_by_id(self, listing_id: int) -> Optional[Listing]:
        """Retrieves a listing by its ID."""
        pass

    @abstractmethod
    def list_all(self) -> List[Listing]:
        """Lists all listings."""
        pass

    @abstractmethod
    def get_by_asset_id(self, asset_id: int) -> List[Listing]:
        """Retrieves listings for a specific asset."""
        pass
