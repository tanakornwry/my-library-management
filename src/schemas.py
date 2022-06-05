from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Base schemas
class BookBase(BaseModel):
    code: str
    etag: str = None
    isbn: str = None
    name: str
    description: Optional[str]
    published_date: Optional[datetime]
    type: Optional[str]
    rating_count: Optional[int]
    everage_count: Optional[int]
    content_version: Optional[str]
    language: Optional[str]
    preview_link: Optional[str]
    info_link: Optional[str]
    
class ImageBase(BaseModel):
    small_thumbnail: str
    thumbnail: str
    small: str
    medium: str
    large: str
    extra_large: str
    
class StockBase(BaseModel):
    qty: int
    available: int
    
class BorrowBase(BaseModel):
    customer_name: str
    created_at: datetime
    
    
    
# Create schemas
class BookCreate(BookBase):
    pass

class ImageCreate(ImageBase):
    pass

class StockCreate(StockBase):
    pass

class BorrowCreate(BorrowBase):
    pass

class BookCreateRequest(BaseModel):
    detail: BookCreate
    image: ImageCreate
    stock: StockCreate


# Response schemas
class Image(ImageBase):
    class Config:
        orm_mode = True

class Stock(StockBase):
    class Config:
        orm_mode = True

class Borrow(BorrowBase):
    id: int
    returned_at: datetime = None
    class Config:
        orm_mode = True

class BorrowResponse(BorrowBase):
    id: int
    book_id: int
    returned_at: datetime = None
    
    class Config:
        orm_mode = True

class Book(BookBase):
    id: int
    image: Image
    stock: Stock | None = None
    borrow_log: list[Borrow] = []
    
    class Config:
        orm_mode = True