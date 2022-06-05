from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
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

@app.get("/")
def greeting():
    return "Library management system."

@app.get("/book/", response_model=Page[schemas.Book])
def get_book(db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    return paginate(book_class.getBooks())
    
add_pagination(app)

@app.post("/book/", response_model=schemas.Book)
def create(book: schemas.BookCreateRequest, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    if book_class.getBook(book_code=book.detail.code):
        raise HTTPException(status_code=400, detail="Book code already registered")
        
    return book_class.createBook(book=book)

@app.get("/book/{book_id}", response_model=schemas.Book)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    book_detail = book_class.getBook(book_id=book_id)
    if book_detail is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_detail

@app.post("/book/{book_id}/borrow", response_model=schemas.BorrowResponse)
def create(book_id: int, borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    if book_class.getBook(book_id=book_id) is None:
        raise HTTPException(status_code=400, detail="Not found the book ID {}".format(book_id))
    
    book_stock = book_class.getBookStock(book_id=book_id)
    if book_stock.available < 1 :
        raise HTTPException(status_code=406, detail="The book ID {} is not availabled".format(book_id))

    db_borrow = book_class.borrowBook(book_id=book_id, borrow=borrow)
    return db_borrow

@app.put("/book/{borrow_id}")
def create(borrow_id: int, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    borrow_log_record = book_class.getBorrowLog(borrow_log_id=borrow_id)
    if borrow_log_record is None:
        raise HTTPException(status_code=400, detail="Not found record ID {}".format(borrow_id))
    
    if borrow_log_record.returned_at is not None:
        raise HTTPException(status_code=406, detail="Record ID {} has been returned already".format(borrow_id))
        
    
    if book_class.returnBook(borrow_log_id=borrow_id) is not None:
        return {"success": True}
    else:
        return {"success": False}
