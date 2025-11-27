import os
import sys

# adiciona a pasta raiz do projeto no caminho do Python
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# -------------------------------------------------------
# Teste 1: API está de pé
# -------------------------------------------------------
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sistema de Recomendação" in response.json()["message"]


# -------------------------------------------------------
# Teste 2: Filmes semelhantes
# -------------------------------------------------------
def test_similar_movies():
    response = client.get("/similar/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "movieId" in data[0]


# -------------------------------------------------------
# Teste 3: Recomendação para usuário
# -------------------------------------------------------
def test_recommend_user():
    response = client.get("/user/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "movieId" in data[0]
