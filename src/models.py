from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from .database import Base
from sqlalchemy.sql import func

class Book(Base):
    __tablename__ = 'Book'
    __table_args__ = (
        UniqueConstraint('code', name='unique_component_commit'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False)
    etag = Column(String(20))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    published_date = Column(DateTime)
    type = Column(String(20))
    rating_count = Column(Integer)
    everage_count = Column(Integer)
    content_version = Column(String(50))
    language = Column(String(3))
    preview_link = Column(Text)
    info_link = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    image = relationship("Image", uselist=False, back_populates="book")
    available = relationship("Stock", uselist=False, back_populates="book")
    
class Image(Base):
    __tablename__ = 'Image'

    id = Column(Integer, primary_key=True, autoincrement=True)
    small_thumbnail = Column(Text)
    thumbnail = Column(Text)
    small = Column(Text)
    medium = Column(Text)
    large = Column(Text)
    extra_large = Column(Text)
    book_id = Column(Integer, ForeignKey('Book.id'))

    book = relationship("Book", uselist=False, back_populates="image")
    
class Stock(Base):
    __tablename__ = 'Stock'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False, default=1)
    available = Column(Integer, nullable=False, default=1)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    book_id = Column(Integer, ForeignKey('Book.id'))

    book = relationship("Book", uselist=False, back_populates="image")
