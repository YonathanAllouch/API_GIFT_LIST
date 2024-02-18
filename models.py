from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class GiftItemGPT(BaseModel):
    description: str
    price_range: str

class SerpApiItem(BaseModel):
    description: str
    actual_price: str
    link: HttpUrl  # HttpUrl type ensures the link is a valid URL
    rating: Optional[float] = None

class FinalGiftItem(BaseModel):
    description: str
    best_option: SerpApiItem

class GiftList(BaseModel):
    event_type: str
    items: List[GiftItemGPT]

