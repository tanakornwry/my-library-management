from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas

class Book:
    def __init__(self, db: Session):
        self.db = db
    
    def getBook(self, **kwargs):
        if kwargs["book_id"] is not None:
            return crud.get_book(db=self.db, book_id=kwargs["book_id"])
        
        if kwargs["book_code"] is not None:
            return crud.get_book_by_code(db=self.db, book_id=kwargs["book_code"])
        
    def createBook(self, book: schemas.BookCreateRequest):
        book_existed = crud.get_book_by_code(db=self.db, book_code=book.detail.code)
        if book_existed:
            raise HTTPException(status_code=400, detail="Book code already registered")

        # Insert a book
        book_created = crud.create_book(db=self.db, book=book.detail)
        
        # Insert the book's image
        if book_created is not None:
            crud.create_imange(db=self.db, image=book.image, book_id=book_created.id)
            
        return crud.get_book(db=self.db, book_id=book_created.id)