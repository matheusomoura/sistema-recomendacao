from pathlib import Path

from app.model import RecommenderModel


def build_model() -> RecommenderModel:
    base = Path("data/ml-latest-small")
    ratings = base / "ratings.csv"
    movies = base / "movies.csv"
    return RecommenderModel(ratings, movies)


def test_model_similarity():
    model = build_model()

    result = model.get_similar_movies(movie_id=1, top_n=5)

    assert len(result) == 5
    assert "movieId" in result.columns
    assert "title" in result.columns
    assert "similarity" in result.columns


def test_model_user_recommendation():
    model = build_model()

    result = model.recommend_for_user(user_id=1, top_n=5)

    assert len(result) == 5
    assert "movieId" in result.columns
    assert "title" in result.columns
    assert "score" in result.columns
