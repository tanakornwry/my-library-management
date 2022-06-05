from email.mime import image
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_code(db: Session, book_code: str):
    return db.query(models.Book).filter(models.Book.code == book_code).first()

def get_book_stock(db: Session, book_id: int):
    return db.query(models.Stock).filter(models.Stock.book_id == book_id).first()

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

def create_stock(db: Session, stock: schemas.StockCreate, book_id: int):
    db_stock = models.Stock(**stock.dict(), book_id=book_id)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)

    return db_stock

def update_stock_available(db: Session, book_id: int, available: int):
    db_stock = db.query(models.Stock).filter(models.Stock.book_id == book_id).first()
    db_stock.available = available
    db.commit()
    db.refresh(db_stock)

    return db_stock

def create_borrow_log(db: Session, borrow: schemas.BorrowCreate, book_id: int):
    db_borrow = models.Borrow_log(**borrow.dict(), book_id=book_id)
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)

    return db_borrow

def get_borrow_log(db: Session, borrow_log_id: int):
    return db.query(models.Borrow_log).filter(models.Borrow_log.id == borrow_log_id).first()
    
def update_book_return(db: Session, borrow_log_id: int):
    db_borrow = db.query(models.Borrow_log).filter(models.Borrow_log.id == borrow_log_id).first()
    db_borrow.returned_at = func.now()
    db.commit()
    db.refresh(db_borrow)
    
    return db_borrow