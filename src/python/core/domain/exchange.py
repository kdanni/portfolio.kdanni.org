from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Exchange:
    name: str
    mic_code: str
    currency: str
    id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.mic_code:
            raise ValueError("MIC code cannot be empty")
        if not self.name:
            raise ValueError("Name cannot be empty")
