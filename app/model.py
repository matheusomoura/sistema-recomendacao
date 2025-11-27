from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderSystem:
    """
    Sistema de recomendação baseado em filtragem colaborativa por itens.

    Ideia:
    - Usamos as notas (ratings) dos usuários para os filmes.
    - Construímos uma matriz usuário x filme.
    - Calculamos a similaridade entre filmes (itens) usando cosseno.
    - Para recomendar:
        * Para um filme: pegamos os mais parecidos com ele.
        * Para um usuário: olhamos os filmes que ele avaliou bem
          e combinamos as similaridades para sugerir novos filmes.
    """

    def __init__(self):
        # Descobre o caminho base do projeto (sistema-recomendacao)
        base_dir = Path(__file__).resolve().parents[1]
        data_dir = base_dir / "data" / "ml-latest-small"

        ratings_path = data_dir / "ratings.csv"
        movies_path = data_dir / "movies.csv"

        # Carrega dados
        self.ratings = pd.read_csv(ratings_path)
        self.movies = pd.read_csv(movies_path)

        # Garante tipos adequados
        self.ratings["userId"] = self.ratings["userId"].astype(int)
        self.ratings["movieId"] = self.ratings["movieId"].astype(int)

        # Monta matriz usuário x filme (linhas = usuários, colunas = filmes)
        self.user_item_matrix = self._build_user_item_matrix()

        # Calcula a matriz de similaridade entre filmes
        self.item_similarity, self.movie_id_to_idx, self.idx_to_movie_id = (
            self._build_item_similarity()
        )

    # ------------------------------------------------------------------
    # Construção da matriz usuário x item
    # ------------------------------------------------------------------
    def _build_user_item_matrix(self) -> pd.DataFrame:
        """
        Cria uma tabela onde:
          - cada linha é um usuário
          - cada coluna é um filme (movieId)
          - cada célula é a nota (rating) que o usuário deu ao filme
        """
        user_item = self.ratings.pivot_table(
            index="userId",
            columns="movieId",
            values="rating",
            fill_value=0.0,  # onde não tem nota, colocamos 0
        )
        return user_item

    # ------------------------------------------------------------------
    # Similaridade entre filmes (itens)
    # ------------------------------------------------------------------
    def _build_item_similarity(self):
        """
        Calcula a similaridade de cosseno entre filmes.

        - Pegamos a matriz usuário x filme.
        - Transpomos para filme x usuário.
        - Aplicamos cosine_similarity para obter:
            matriz [num_filmes x num_filmes]
        """
        # Transpõe: agora linhas = filmes, colunas = usuários
        item_matrix = self.user_item_matrix.T

        # Guarda o mapeamento de índice para movieId
        movie_ids = item_matrix.index.to_list()
        movie_id_to_idx = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}
        idx_to_movie_id = {idx: movie_id for movie_id, idx in movie_id_to_idx.items()}

        # Converte para numpy array
        item_matrix_np = item_matrix.values

        # Similaridade de cosseno entre linhas (filmes)
        similarity_matrix = cosine_similarity(item_matrix_np)

        return similarity_matrix, movie_id_to_idx, idx_to_movie_id

    # ------------------------------------------------------------------
    # Recomendar filmes semelhantes a um filme específico
    # ------------------------------------------------------------------
    def recommend_similar_movies(self, movie_id: int, top_n: int = 5) -> pd.DataFrame:
        """
        Retorna os 'top_n' filmes mais parecidos com o filme informado.

        :param movie_id: ID do filme de referência (coluna movieId do movies.csv)
        :param top_n: quantidade de recomendações
        """
        if movie_id not in self.movie_id_to_idx:
            raise ValueError(f"movie_id {movie_id} não encontrado na base.")

        movie_idx = self.movie_id_to_idx[movie_id]

        # Similaridades desse filme com todos os outros
        sim_scores = self.item_similarity[movie_idx]

        # Ordena pela similaridade (maior -> menor)
        # ignorando o próprio filme (idx diferente)
        similar_indices = np.argsort(sim_scores)[::-1]  # ordem decrescente
        similar_indices = [idx for idx in similar_indices if idx != movie_idx]

        # Pega os top_n
        top_indices = similar_indices[:top_n]

        # Converte índices de volta para movieId
        similar_movie_ids = [self.idx_to_movie_id[idx] for idx in top_indices]

        # Junta com o dataframe de filmes
        result = self.movies[self.movies["movieId"].isin(similar_movie_ids)].copy()

        # Adiciona coluna com a similaridade
        result["similarity"] = [
            sim_scores[self.movie_id_to_idx[movie_id_sim]]
            for movie_id_sim in similar_movie_ids
        ]

        # Ordena do mais similar para o menos similar
        result = result.sort_values(by="similarity", ascending=False)

        return result[["movieId", "title", "genres", "similarity"]]

    # ------------------------------------------------------------------
    # Recomendar filmes para um usuário com base nas notas dele
    # ------------------------------------------------------------------
    def recommend_for_user(
        self,
        user_id: int,
        top_n: int = 5,
        min_rating: float = 4.0,
    ) -> pd.DataFrame:
        """
        Recomenda filmes para um usuário baseado nas notas que ele deu.

        Estratégia:
        - Pegamos os filmes que o usuário avaliou com nota >= min_rating.
        - Para cada um desses filmes, olhamos a similaridade com outros filmes.
        - Somamos as similaridades, criando uma espécie de "score" para cada filme.
        - Removemos os filmes que o usuário já assistiu.
        - Retornamos os top_n com maior score.

        :param user_id: ID do usuário (coluna userId de ratings.csv)
        :param top_n: quantidade de recomendações
        :param min_rating: nota mínima para considerar que ele "gostou" de um filme
        """
        if user_id not in self.user_item_matrix.index:
            raise ValueError(f"user_id {user_id} não encontrado na base.")

        # Filmes que o usuário avaliou
        user_ratings = self.ratings[self.ratings["userId"] == user_id]

        # Considera apenas filmes com nota >= min_rating
        liked_movies = user_ratings[user_ratings["rating"] >= min_rating]

        if liked_movies.empty:
            raise ValueError(
                f"Usuário {user_id} não tem filmes avaliados com nota >= {min_rating}."
            )

        # Lista de movieIds que o usuário já viu
        seen_movie_ids = set(user_ratings["movieId"].tolist())

        # Vetor para acumular os scores
        scores = np.zeros(self.item_similarity.shape[0])

        # Para cada filme que o usuário gostou:
        for _, row in liked_movies.iterrows():
            movie_id = int(row["movieId"])
            rating = float(row["rating"])

            if movie_id not in self.movie_id_to_idx:
                continue

            movie_idx = self.movie_id_to_idx[movie_id]

            # Similaridade desse filme para todos os outros
            sim_vector = self.item_similarity[movie_idx]

            # Soma ponderada pela nota (opcional)
            scores += sim_vector * rating

        # Zera o score dos filmes que o usuário já viu
        for seen_id in seen_movie_ids:
            if seen_id in self.movie_id_to_idx:
                seen_idx = self.movie_id_to_idx[seen_id]
                scores[seen_idx] = 0.0

        # Pega os índices com maiores scores
        recommended_indices = np.argsort(scores)[::-1][:top_n]
        recommended_movie_ids = [self.idx_to_movie_id[idx] for idx in recommended_indices]

        # Monta dataframe de resultado
        result = self.movies[self.movies["movieId"].isin(recommended_movie_ids)].copy()
        result["score"] = [
            scores[self.movie_id_to_idx[movie_id]] for movie_id in recommended_movie_ids
        ]

        # Ordena por score
        result = result.sort_values(by="score", ascending=False)

        return result[["movieId", "title", "genres", "score"]]
