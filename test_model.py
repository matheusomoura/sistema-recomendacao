from app.model import RecommenderSystem


def main():
    # Inicializa o sistema de recomendação
    print("Carregando modelo de recomendação...")
    recommender = RecommenderSystem()
    print("Modelo carregado com sucesso!\n")

    # ----------------------------------------------------
    # 1) Teste: filmes parecidos com um filme específico
    # ----------------------------------------------------
    example_movie_id = 1  # Toy Story (1995) no MovieLens
    print(f"Filmes semelhantes ao movieId={example_movie_id}:\n")
    similar_movies = recommender.recommend_similar_movies(
        movie_id=example_movie_id,
        top_n=5,
    )
    print(similar_movies.to_string(index=False))

    # ----------------------------------------------------
    # 2) Teste: recomendações para um usuário específico
    # ----------------------------------------------------
    example_user_id = 1
    print(f"\n\nRecomendações para o userId={example_user_id}:\n")
    user_recs = recommender.recommend_for_user(
        user_id=example_user_id,
        top_n=5,
        min_rating=4.0,
    )
    print(user_recs.to_string(index=False))


if __name__ == "__main__":
    main()
