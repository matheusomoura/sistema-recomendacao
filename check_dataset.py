from pathlib import Path
import pandas as pd

# Caminho base do projeto (onde está este arquivo)
BASE_DIR = Path(__file__).resolve().parent

# Caminho para a pasta data/ml-latest-small
data_dir = BASE_DIR / "data" / "ml-latest-small"

ratings_path = data_dir / "ratings.csv"
movies_path = data_dir / "movies.csv"

print("Caminho ratings.csv:", ratings_path)
print("Caminho movies.csv:", movies_path)

# Carrega os arquivos CSV
ratings = pd.read_csv(ratings_path)
movies = pd.read_csv(movies_path)

print("\nPrimeiras linhas de ratings.csv:")
print(ratings.head())

print("\nPrimeiras linhas de movies.csv:")
print(movies.head())

print("\nTotal de linhas em ratings:", len(ratings))
print("Total de linhas em movies:", len(movies))
