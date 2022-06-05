from fastapi import FastAPI
from .routers import book
from src import models
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
        
app.include_router(book.router)

@app.get("/")
async def root():
    return {"Services": "Library management system v1"}