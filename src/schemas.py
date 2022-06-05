from importlib.resources import path
from fastapi import Query
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Required

# Base schemas
class BookBase(BaseModel):
    code: str
    etag: str | None = None
    isbn: str | None = None
    name: str
    description: str | None = None
    published_date: datetime | None = None
    type: str | None = None
    rating_count: int | None = None
    everage_count: int | None = None
    content_version: str | None = None
    language: Optional[str] = "TH" 
    preview_link: str | None = None
    info_link: str | None = None
    
class ImageBase(BaseModel):
    small_thumbnail: str | None = None
    thumbnail: str | None = None
    small: str | None = None
    medium: str | None = None
    large: str | None = None
    extra_large: str | None = None
    
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
    image: Image | None = None
    stock: Stock | None = None
    borrow_log: list[Borrow] = []
    
    class Config:
        orm_mode = True