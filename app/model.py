from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderModel:
    """
    Modelo de recomendação baseado em Filtragem Colaborativa por Itens
    usando similaridade de cosseno.
    """

    def __init__(self, ratings_path: Path, movies_path: Path):
        # Carrega dados
        self.ratings = pd.read_csv(ratings_path)
        self.movies = pd.read_csv(movies_path)

        # Cria matriz usuário x filme (userId x movieId)
        user_item = self.ratings.pivot_table(
            index="userId",
            columns="movieId",
            values="rating"
        )

        self.user_item = user_item

        # Matriz filme x usuário (para similaridade entre filmes)
        item_user = user_item.T  # transposta
        item_user = item_user.fillna(0.0)

        self.item_user = item_user

        # Calcula matriz de similaridade entre filmes
        sim_matrix = cosine_similarity(self.item_user)

        self.sim_matrix = pd.DataFrame(
            sim_matrix,
            index=self.item_user.index,
            columns=self.item_user.index
        )

    # -------------------------------------------------------------
    # 1) Filmes semelhantes a um filme específico
    # -------------------------------------------------------------
    def get_similar_movies(self, movie_id: int, top_n: int = 5) -> pd.DataFrame:
        """
        Retorna os top_n filmes mais semelhantes ao movie_id informado.
        """

        if movie_id not in self.sim_matrix.index:
            raise ValueError(f"movie_id {movie_id} não encontrado na matriz de similaridade.")

        # Similaridade desse filme com todos os outros
        scores = self.sim_matrix[movie_id].sort_values(ascending=False)

        # Remove ele mesmo
        scores = scores.drop(labels=[movie_id])

        # Pega os top_n
        top_ids = scores.head(top_n).index

        # Junta com os dados dos filmes
        result = self.movies[self.movies["movieId"].isin(top_ids)].copy()
        result["similarity"] = scores.loc[top_ids].values

        # Ordena por similaridade (maior primeiro)
        result = result.sort_values(by="similarity", ascending=False)

        return result[["movieId", "title", "genres", "similarity"]]

    # -------------------------------------------------------------
    # 2) Recomendações para um usuário específico
    # -------------------------------------------------------------
    def recommend_for_user(
        self,
        user_id: int,
        top_n: int = 5,
        min_rating: float = 4.0
    ) -> pd.DataFrame:
        """
        Gera recomendações de filmes para um usuário, com base
        nas notas que ele já deu e na similaridade entre os filmes.
        """

        if user_id not in self.user_item.index:
            raise ValueError(f"user_id {user_id} não encontrado na matriz usuário x filme.")

        # Notas do usuário
        user_ratings = self.user_item.loc[user_id].dropna()

        if user_ratings.empty:
            raise ValueError("Usuário não possui avaliações suficientes.")

        # Filmes que ele avaliou bem (acima de min_rating)
        liked = user_ratings[user_ratings >= min_rating]

        # Se não houver nada acima do min_rating, pega os 5 melhores avaliados
        if liked.empty:
            liked = user_ratings.sort_values(ascending=False).head(5)

        # Acumula score para cada filme usando similaridade ponderada pela nota
        scores = pd.Series(dtype=float)

        for movie_id, rating in liked.items():
            if movie_id not in self.sim_matrix.columns:
                continue

            sims = self.sim_matrix[movie_id]

            # soma ponderada: similaridade * nota
            scores = scores.add(sims * rating, fill_value=0.0)

        # Remove filmes que o usuário já avaliou
        scores = scores.drop(index=user_ratings.index, errors="ignore")

        # Se não sobrar nada, retorna vazio
        if scores.empty:
            return pd.DataFrame(columns=["movieId", "title", "genres", "score"])

        # Pega top_n
        top_ids = scores.sort_values(ascending=False).head(top_n).index

        result = self.movies[self.movies["movieId"].isin(top_ids)].copy()
        result["score"] = scores.loc[top_ids].values

        # Ordena por score
        result = result.sort_values(by="score", ascending=False)

        return result[["movieId", "title", "genres", "score"]]
