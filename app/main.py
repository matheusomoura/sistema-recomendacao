from fastapi import FastAPI
from app.model import RecommenderSystem

app = FastAPI(
    title="Sistema de Recomendação - MovieLens",
    description="API do trabalho final | IA",
    version="1.0.0"
)

# Carregar modelo uma única vez
recommender = RecommenderSystem()


@app.get("/")
def root():
    return {
        "message": "API do Sistema de Recomendação está funcionando!",
        "endpoints": {
            "/similar/{movie_id}": "Recomenda filmes semelhantes",
            "/user/{user_id}": "Recomenda filmes para um usuário"
        }
    }


@app.get("/similar/{movie_id}")
def similar_movies(movie_id: int, top_n: int = 5):
    try:
        result = recommender.recommend_similar_movies(movie_id, top_n)
        return result.to_dict(orient="records")
    except ValueError as e:
        return {"erro": str(e)}


@app.get("/user/{user_id}")
def user_recommendations(user_id: int, top_n: int = 5, min_rating: float = 4.0):
    try:
        result = recommender.recommend_for_user(user_id, top_n, min_rating)
        return result.to_dict(orient="records")
    except ValueError as e:
        return {"erro": str(e)}
