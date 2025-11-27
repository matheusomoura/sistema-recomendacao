from pathlib import Path
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from .model import RecommenderModel

# Caminhos dos arquivos de dados
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "ml-latest-small"

RATINGS_PATH = DATA_DIR / "ratings.csv"
MOVIES_PATH = DATA_DIR / "movies.csv"

# Inicializa modelo de recomendação
recommender = RecommenderModel(
    ratings_path=RATINGS_PATH,
    movies_path=MOVIES_PATH
)

app = FastAPI(
    title="Sistema de Recomendação - MovieLens",
    version="1.0.0"
)

# -----------------------------
# MODELOS Pydantic (entrada)
# -----------------------------

class RatingInput(BaseModel):
    movie_id: int
    rating: float


class NewUserInput(BaseModel):
    user_id: int
    ratings: List[RatingInput]


class NewMovieInput(BaseModel):
    movie_id: int
    title: str
    genres: str


# "Banco de dados" em memória (apenas para fins didáticos)
new_users: List[NewUserInput] = []
new_movies: List[NewMovieInput] = []


# -----------------------------
# ENDPOINTS EXISTENTES
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "API do Sistema de Recomendação – MovieLens",
        "endpoints": ["/similar/{movie_id}", "/user/{user_id}", "/add/user", "/add/item"]
    }


@app.get("/similar/{movie_id}")
def similar_movies(movie_id: int, top_n: int = 5):
    """
    Retorna filmes semelhantes ao movie_id informado.
    """
    try:
        result = recommender.get_similar_movies(movie_id=movie_id, top_n=top_n)
        return result.to_dict(orient="records")
    except Exception as e:
        return {"erro": str(e)}


@app.get("/user/{user_id}")
def user_recommendations(user_id: int, top_n: int = 5, min_rating: float = 4.0):
    """
    Retorna recomendações de filmes para um usuário específico.
    """
    try:
        result = recommender.recommend_for_user(
            user_id=user_id,
            top_n=top_n,
            min_rating=min_rating
        )
        return result.to_dict(orient="records")
    except ValueError as e:
        return {"erro": str(e)}
    except Exception as e:
        return {"erro": str(e)}


# -----------------------------
# NOVOS ENDPOINTS DA ETAPA 4
# -----------------------------

@app.post("/add/user")
def add_user(user: NewUserInput):
    """
    Recebe um novo usuário com suas avaliações.
    Os dados são armazenados em memória (new_users) apenas para demonstração.
    """
    new_users.append(user)
    return {
        "message": "Usuário recebido com sucesso.",
        "user_id": user.user_id,
        "total_usuarios_registrados": len(new_users)
    }


@app.post("/add/item")
def add_item(movie: NewMovieInput):
    """
    Recebe um novo filme (item) e armazena em memória (new_movies).
    """
    new_movies.append(movie)
    return {
        "message": "Filme recebido com sucesso.",
        "movie_id": movie.movie_id,
        "total_filmes_registrados": len(new_movies)
    }
