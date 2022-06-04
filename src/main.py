from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, services
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# def greeting():
#     return "Library management system."

@app.get("/book/")
def get_book():
    return "Get all book"

@app.post("/book/", response_model=schemas.Book)
def create(book: schemas.BookCreateRequest, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    return book_class.createBook(book=book)

@app.get("/book/{book_id}", response_model=schemas.Book)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book