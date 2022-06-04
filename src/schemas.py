from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ImageBase(BaseModel):
    small_thumbnail: str
    thumbnail: str
    small: str
    medium: str
    large: str
    extra_large: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    code: str
    etag: str
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

class BookCreateRequest(BaseModel):
    detail: BookBase
    image: Image
    
class BookCreate(BaseModel):
    pass

class Book(BookBase):
    id: int
    image: Image

    class Config:
        orm_mode = True