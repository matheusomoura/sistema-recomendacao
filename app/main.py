from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.model import RecommenderModel


app = FastAPI(
    title="Sistema de Recomendação - MovieLens",
    description="API do trabalho final | Desenvolvimento de Sistemas de IA",
    version="1.0.0",
)

# ----------------------------------------------------------------------
# Instancia única do modelo de recomendação
# ----------------------------------------------------------------------
BASE_DIR = Path("data/ml-latest-small")

recommender = RecommenderModel(
    ratings_path=BASE_DIR / "ratings.csv",
    movies_path=BASE_DIR / "movies.csv",
)

# "Banco" em memória só para demonstrar os endpoints de criação
fake_users_db: Dict[int, Dict] = {}
fake_items_db: Dict[int, Dict] = {}


# ----------------------------------------------------------------------
# Schemas Pydantic para os endpoints de POST/PUT
# ----------------------------------------------------------------------
class NewUserInput(BaseModel):
    userId: int
    name: str


class NewMovieInput(BaseModel):
    movieId: int
    title: str
    genres: str


class RatingInput(BaseModel):
    userId: int
    movieId: int
    rating: float


# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------
@app.get("/")
def root():
    """Endpoint raiz: mostra status da API."""
    return {"status": "ok", "message": "API de recomendação ativa"}


@app.get("/similar/{movie_id}")
def similar_movies(movie_id: int, top_n: int = 5):
    """
    Retorna filmes similares ao movie_id informado.
    """
    try:
        result = recommender.get_similar_movies(movie_id=movie_id, top_n=top_n)
        return result.to_dict(orient="records")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/user/{user_id}")
def user_recommendations(user_id: int, top_n: int = 5, min_rating: float = 4.0):
    """
    Retorna recomendações personalizadas para um usuário.
    """
    try:
        result = recommender.recommend_for_user(
            user_id=user_id,
            top_n=top_n,
            min_rating=min_rating,
        )
        return result.to_dict(orient="records")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ------------------------- NOVOS ENDPOINTS -----------------------------


@app.post("/add/user")
def add_user(user: NewUserInput):
    """
    Adiciona um novo usuário.
    Obs.: aqui está apenas em memória, para fins didáticos do trabalho.
    """
    if user.userId in fake_users_db:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado.")

    fake_users_db[user.userId] = user.dict()
    return {
        "message": "Usuário adicionado com sucesso.",
        "user": fake_users_db[user.userId],
    }


@app.post("/add/item")
def add_item(item: NewMovieInput):
    """
    Adiciona um novo filme (item).
    Também fica apenas em memória, não altera o CSV original.
    """
    if item.movieId in fake_items_db:
        raise HTTPException(status_code=400, detail="Filme já cadastrado.")

    fake_items_db[item.movieId] = item.dict()
    return {
        "message": "Filme adicionado com sucesso.",
        "item": fake_items_db[item.movieId],
    }


@app.put("/update/rating")
def update_rating(payload: RatingInput):
    """
    Atualiza as preferências de um usuário (nota para um filme).
    Isso realmente altera a matriz de ratings em memória
    e reconstrói o modelo de recomendação.
    """
    try:
        recommender.update_rating(
            user_id=payload.userId,
            movie_id=payload.movieId,
            rating=payload.rating,
        )
        return {"message": "Avaliação registrada/atualizada com sucesso."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # fallback genérico para não quebrar a API
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar rating: {e}")
