from dataclasses import dataclass
from datetime import datetime

@dataclass
class Item:
    id: int
    content: str
    created_at: datetime
    next_review: datetime
    review_count: int
    ease_factor: float 