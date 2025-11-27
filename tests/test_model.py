import os
import sys

# adiciona a pasta raiz do projeto no caminho do Python
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path
from app.model import RecommenderModel


def test_model_similarity():
    base = Path("data/ml-latest-small")
    ratings = base / "ratings.csv"
    movies = base / "movies.csv"

    model = RecommenderModel(ratings, movies)

    result = model.get_similar_movies(movie_id=1, top_n=5)

    assert len(result) == 5
    assert "similarity" in result.columns


def test_model_user_recommendation():
    base = Path("data/ml-latest-small")
    ratings = base / "ratings.csv"
    movies = base / "movies.csv"

    model = RecommenderModel(ratings, movies)

    result = model.recommend_for_user(user_id=1, top_n=5)

    assert len(result) == 5
    assert "score" in result.columns
