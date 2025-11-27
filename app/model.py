from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderModel:
    """
    Modelo de recomendação baseado em Filtragem Colaborativa por Itens.
    Usa o dataset MovieLens (ratings.csv + movies.csv).
    """

    def __init__(self, ratings_path: Path | str, movies_path: Path | str) -> None:
        self.ratings_path = Path(ratings_path)
        self.movies_path = Path(movies_path)

        self.ratings_df: pd.DataFrame | None = None
        self.movies_df: pd.DataFrame | None = None
        self.user_item_matrix: pd.DataFrame | None = None
        self.item_similarity_df: pd.DataFrame | None = None

        self.load_data()
        self.build_model()

    # ------------------------------------------------------------------
    # Carregamento e preparação dos dados
    # ------------------------------------------------------------------
    def load_data(self) -> None:
        """Carrega os arquivos CSV de ratings e filmes."""
        self.ratings_df = pd.read_csv(self.ratings_path)
        self.movies_df = pd.read_csv(self.movies_path)

    def build_model(self) -> None:
        """Monta a matriz usuário x filme e calcula a similaridade entre itens."""
        if self.ratings_df is None:
            raise ValueError("Ratings ainda não foram carregados.")

        # matriz usuário x filme (userId nas linhas, movieId nas colunas)
        user_item = self.ratings_df.pivot_table(
            index="userId",
            columns="movieId",
            values="rating",
            aggfunc="mean",
        ).fillna(0.0)

        self.user_item_matrix = user_item

        # similaridade de cosseno entre filmes (colunas)
        similarity_matrix = cosine_similarity(user_item.T)
        self.item_similarity_df = pd.DataFrame(
            similarity_matrix,
            index=user_item.columns,
            columns=user_item.columns,
        )

    # ------------------------------------------------------------------
    # Recomendação de filmes similares
    # ------------------------------------------------------------------
    def get_similar_movies(
        self,
        movie_id: int,
        top_n: int = 5,
        min_rating: float = 0.0,
    ) -> pd.DataFrame:
        """
        Retorna filmes similares a um filme de referência, com base na similaridade de cosseno.
        """
        if self.item_similarity_df is None or self.movies_df is None:
            raise ValueError("Modelo ainda não foi construído.")

        if movie_id not in self.item_similarity_df.index:
            raise ValueError(f"movieId {movie_id} não encontrado na matriz de similaridade.")

        # vetor de similaridade para o filme escolhido
        movie_similarities = self.item_similarity_df[movie_id]

        # remove o próprio filme e ordena por similaridade decrescente
        movie_similarities = movie_similarities.drop(movie_id).sort_values(ascending=False)

        # aplica filtro opcional (não usamos min_rating aqui, mas mantemos assinatura)
        top_similar = movie_similarities.head(top_n)

        movies_info = self.movies_df.set_index("movieId").loc[top_similar.index]

        result = movies_info.copy()
        result["similarity"] = top_similar.values

        return result.reset_index()[["movieId", "title", "genres", "similarity"]]

    # ------------------------------------------------------------------
    # Recomendação personalizada por usuário
    # ------------------------------------------------------------------
    def recommend_for_user(
        self,
        user_id: int,
        top_n: int = 5,
        min_rating: float = 4.0,
    ) -> pd.DataFrame:
        """
        Gera recomendações de filmes para um usuário específico.
        O score é um somatório ponderado pela similaridade com os filmes avaliados.
        """
        if (
            self.user_item_matrix is None
            or self.item_similarity_df is None
            or self.movies_df is None
        ):
            raise ValueError("Modelo ainda não foi construído.")

        if user_id not in self.user_item_matrix.index:
            raise ValueError(f"userId {user_id} não encontrado na base.")

        user_ratings = self.user_item_matrix.loc[user_id]

        # filmes que o usuário já avaliou
        rated_movies = user_ratings[user_ratings >= min_rating]
        if rated_movies.empty:
            raise ValueError(
                f"Usuário {user_id} não possui avaliações com nota mínima {min_rating}."
            )

        scores = pd.Series(0.0, index=self.user_item_matrix.columns)

        # acumula o score de cada filme com base nas similaridades
        for movie_id, rating in rated_movies.items():
            scores += self.item_similarity_df[movie_id] * float(rating)

        # remove os filmes já avaliados
        scores = scores.drop(rated_movies.index, errors="ignore")

        # pega o top_n
        scores = scores.sort_values(ascending=False).head(top_n)

        movies_info = self.movies_df.set_index("movieId").loc[scores.index]

        result = movies_info.copy()
        result["score"] = scores.values

        return result.reset_index()[["movieId", "title", "genres", "score"]]

    # ------------------------------------------------------------------
    # Atualização de preferências (endpoint /update/rating)
    # ------------------------------------------------------------------
    def update_rating(self, user_id: int, movie_id: int, rating: float) -> None:
        """
        Atualiza (ou insere) a avaliação de um usuário para um filme
        e reconstrói o modelo em memória.
        """
        if self.ratings_df is None:
            raise ValueError("Ratings ainda não foram carregados.")

        # remove, se já existir avaliação desse user para esse filme
        mask = ~(
            (self.ratings_df["userId"] == user_id)
            & (self.ratings_df["movieId"] == movie_id)
        )
        self.ratings_df = self.ratings_df[mask]

        new_row = {
            "userId": user_id,
            "movieId": movie_id,
            "rating": float(rating),
            "timestamp": int(pd.Timestamp.utcnow().timestamp()),
        }

        self.ratings_df = pd.concat(
            [self.ratings_df, pd.DataFrame([new_row])],
            ignore_index=True,
        )

        # reconstrói a matriz e as similaridades com o novo dado
        self.build_model()
