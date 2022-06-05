from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session
from src import models, schemas, services
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/book/", response_model=Page[schemas.Book])
def get_book(db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    return paginate(book_class.getBooks())
    
add_pagination(router)

@router.post("/book/", response_model=schemas.Book, status_code=201)
def create_book(book: schemas.BookCreateRequest, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    if book_class.getBook(book_code=book.detail.code):
        raise HTTPException(status_code=406, detail="Book code already registered")
        
    return book_class.createBook(book=book)

@router.get("/book/{book_id}", response_model=schemas.Book)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    book_detail = book_class.getBook(book_id=book_id)
    if book_detail is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_detail

@router.post("/book/{book_id}/borrow", response_model=schemas.BorrowResponse, status_code=201)
def create_borrow(book_id: int, borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    if book_class.getBook(book_id=book_id) is None:
        raise HTTPException(status_code=404, detail="Not found the book ID {}".format(book_id))
    
    book_stock = book_class.getBookStock(book_id=book_id)
    if book_stock.available < 1 :
        raise HTTPException(status_code=406, detail="The book ID {} is not availabled".format(book_id))

    db_borrow = book_class.borrowBook(book_id=book_id, borrow=borrow)
    return db_borrow

@router.put("/book/{borrow_id}")
def book_return(borrow_id: int, db: Session = Depends(get_db)):
    book_class = services.Book(db=db)
    borrow_log_record = book_class.getBorrowLog(borrow_log_id=borrow_id)
    if borrow_log_record is None:
        raise HTTPException(status_code=404, detail="Not found record ID {}".format(borrow_id))
    
    if borrow_log_record.returned_at is not None:
        raise HTTPException(status_code=406, detail="Record ID {} has been returned already".format(borrow_id))
        
    
    if book_class.returnBook(borrow_log_id=borrow_id) is not None:
        return {"success": True}
    else:
        return {"success": False}