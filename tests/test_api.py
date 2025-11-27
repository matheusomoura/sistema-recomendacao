from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_similar_movies():
    response = client.get("/similar/1?top_n=5")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]
    assert "movieId" in first
    assert "title" in first
    assert "similarity" in first


def test_recommend_user():
    response = client.get("/user/1?top_n=5&min_rating=4.0")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]
    assert "movieId" in first
    assert "title" in first
    assert "score" in first
