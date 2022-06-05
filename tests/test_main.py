from tests.testconf import test_app

def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Services": "Library management system v1"}