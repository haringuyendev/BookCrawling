from pydantic import BaseModel
from typing import Optional

class BookCreateDTO(BaseModel):
    title: str
    price: str
    availability: str
    product_url: str
    star_rating: int
    publisher_country: Optional[str] = ""
    
class BookResponseDTO(BookCreateDTO):
    created_date: Optional[str] = None
