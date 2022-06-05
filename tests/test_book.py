import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.main import app, get_db
from .testconf import get_sample_input, get_not_existed_book_id

try:
    load_dotenv()    
except:
    print("Can not read .env file")

SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL_TEST')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

sample_input = get_sample_input()

def test_create_book():
    response = client.post(
        "/book/",
        json = sample_input["json"]
    )
    
    assert response.status_code == 201, response.text

    data = response.json()
    assert "id" in data

    book_id = data["id"]    
    response = client.get(f"/book/{book_id}")
    assert response.status_code == 200, response.text
    
    data = response.json()
    assert data["code"] == sample_input["code"]
    
def test_create_duplicate_book():
    
    response = client.post(
        "/book/",
        json = sample_input["json"]
    )
    
    assert response.status_code == 406, response.text
    
def test_get_books():
    response = client.get(f"/book/?page=1&size50")
    assert response.status_code == 200, response.text

def test_not_found_book():
    book_id = get_not_existed_book_id()
    response = client.get(f"/book/{book_id}")
    assert response.status_code == 404, response.text