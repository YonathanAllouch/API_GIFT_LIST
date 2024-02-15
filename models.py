from pydantic import BaseModel, Field
from typing import List, Optional

class GiftItem(BaseModel):
    name: str
    price_range: str  # Example: "50-100"
    description: Optional[str] = None

class GiftList(BaseModel):
    event_type: str
    items: List[GiftItem]
