from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class UserGiftListRequest(BaseModel):
    list_type: str
    number_of_items: int
    gender_of_gifts: str
    price_range: str
class ItemDescription(BaseModel):
    description: str
    price_range: str

class GiftItem(BaseModel):
    description: str
    price: str
    link: HttpUrl
    rating: Optional[float]

class AgentItem(BaseModel):
    link: HttpUrl
    price: str
    rating: Optional[float]

class StoredItem(BaseModel):
    description: str
    agent_items: List[AgentItem]
