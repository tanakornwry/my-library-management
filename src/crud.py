from email.mime import image
from sqlalchemy.orm import Session

from . import models, schemas

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_code(db: Session, book_code: str):
    return db.query(models.Book).filter(models.Book.code == book_code).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return db_book

def create_imange(db: Session, image: schemas.ImageCreate, book_id: int):
    db_imgage = models.Image(**image.dict(), book_id=book_id)
    db.add(db_imgage)
    db.commit()
    db.refresh(db_imgage)

    return db_imgage