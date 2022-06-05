import random
import pytest
from starlette.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client
    
    
def random_string(length):  
    sample_string = 'ABCDEFGHLMNOPQRSTUVWXYZ1234567890' 
    return ''.join((random.choice(sample_string)) for x in range(length)) 

def get_sample_input():
    code = random_string(20)
    crate_book_input = {
                        "detail": {
                            "code": code,
                            "etag": "string",
                            "isbn": "string",
                            "name": "string",
                            "description": "string",
                            "published_date": "2022-06-05T11:37:46.739Z",
                            "type": "string",
                            "rating_count": 0,
                            "everage_count": 0,
                            "content_version": "string",
                            "language": "TH",
                            "preview_link": "string",
                            "info_link": "string"
                        },
                        "image": {
                            "small_thumbnail": "string",
                            "thumbnail": "string",
                            "small": "string",
                            "medium": "string",
                            "large": "string",
                            "extra_large": "string"
                        },
                        "stock": {
                            "qty": 5,
                            "available": 5
                        }
                    }

    return dict(json = crate_book_input, code = code)

def get_not_existed_book_id():
    return "90000000000"