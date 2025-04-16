from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    price: str
    availability: str
    product_url: str
    star_rating: int
    publisher_country: str = ""
    is_deleted:int = 0
    deleted_date:Optional[datetime] = None
    created_date:Optional[datetime] = None
    updated_date:Optional[datetime] = None

def serialize_books(book_list):
    return [book.dict() if hasattr(book, "dict") else book.__dict__ for book in book_list]
