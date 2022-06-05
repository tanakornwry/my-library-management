from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas

class Book:
    def __init__(self, db: Session):
        self.db = db
    
    def getBook(self, **kwargs):
        if "book_id" in kwargs:
            return crud.get_book(db=self.db, book_id=kwargs["book_id"])
        
        if "book_code" in kwargs:
            return crud.get_book_by_code(db=self.db, book_code=kwargs["book_code"])
        
    def getBooks(self, **kwargs):
        books = crud.get_books(db=self.db)
        return books
        
    def createBook(self, book: schemas.BookCreateRequest):
        # Insert a book
        book_created = crud.create_book(db=self.db, book=book.detail)
        
        if book_created is not None:
            # Insert the book's image
            crud.create_imange(db=self.db, image=book.image, book_id=book_created.id)
            
            # Insert the book's stock
            crud.create_stock(db=self.db, stock=book.stock, book_id=book_created.id)
            
        return crud.get_book(db=self.db, book_id=book_created.id)
    
    def getBookStock(self, book_id: int):
        return crud.get_book_stock(db=self.db, book_id=book_id)

    def getBorrowLog(self, borrow_log_id):
        return crud.get_borrow_log(db=self.db, borrow_log_id=borrow_log_id)
        
    def borrowBook(self, book_id: int, borrow: schemas.BorrowCreate):
        # Insert borrow log record
        borrow_created = crud.create_borrow_log(db=self.db, borrow=borrow, book_id=book_id)
        if borrow_created is not None:
            # Update the book's stock
            stock = crud.get_book_stock(db=self.db, book_id=book_id)
            crud.update_stock_available(db=self.db, book_id=book_id, available=stock.available-1)
        
        return borrow_created

    def returnBook(self, borrow_log_id: int):
        returned = crud.update_book_return(db=self.db, borrow_log_id=borrow_log_id)
        if returned is not None:
            stock = crud.get_book_stock(db=self.db, book_id=returned.book_id)
            crud.update_stock_available(db=self.db, book_id=returned.book_id, available=stock.available+1)

        return returned
        