import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# Carregar o parquet
df = pd.read_parquet(BASE_DIR / "bases" / "outputs" / "consolidated_overall.parquet")

print("Total de colunas:", len(df.columns))
print("Ultimas 5 colunas:", df.columns[-5:].tolist())

print("\nColuna highlight_color presente:", "highlight_color" in df.columns)
print("Coluna max_categories presente:", "max_categories" in df.columns)

print("\nDistribuicao de jogadores com categorias maximas:")
with_categories = df[df["max_categories"] != ""]
print(f"Total de jogadores com max_categories: {len(with_categories)}")
print("\nTop 10 combinacoes mais comuns:")
print(with_categories["max_categories"].value_counts().head(10))
