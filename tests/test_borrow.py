import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.main import app, get_db
from tests.testconf import get_sample_input, get_not_existed_book_id

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

borrow_id = int()

def test_create_borrow():
    response = client.post(
        "/book/",
        json = sample_input["json"]
    )    
    data = response.json()
    
    response = client.post(
        "/book/{}/borrow".format(data["id"]),
        json = {"customer_name": "test man", "created_at": "2022-06-05T12:54:31.567Z"}
    )
    assert response.status_code == 201, response.text

    borrow_data = response.json()
    global borrow_id
    borrow_id = borrow_data["id"]
    assert borrow_data["returned_at"] == None

def test_create_borrow_not_found_book():
    book_id = get_not_existed_book_id()
    response = client.post(
        "/book/{}/borrow".format(book_id),
        json = {"customer_name": "test man", "created_at": "2022-06-05T12:54:31.567Z"}
    )
    assert response.status_code == 404, response.text
    
def test_book_return():
    response = client.put(
        "/book/{}".format(borrow_id)
    )
    
    assert response.status_code == 200, response.text