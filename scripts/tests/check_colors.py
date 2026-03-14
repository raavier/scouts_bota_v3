import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# Carregar o parquet
df = pd.read_parquet(BASE_DIR / "bases" / "outputs" / "consolidated_overall.parquet")

# Filtrar jogadores
position_group = "Extremo - Direita"
competition_id = 12

filtered = df[
    (df["position_group"] == position_group) &
    (df["competition_id"] == competition_id) &
    (df["highlight_color"] != "#FFFFFF")
]

print(f"Position Group: {position_group}")
print(f"Competition ID: {competition_id}")
print(f"\nTotal de jogadores destacados: {len(filtered)}")
print("\n" + "=" * 120)

if len(filtered) > 0:
    cols = ["player_name", "team_name", "overall_score", "score_OFFENSIVE",
            "score_DGP", "score_PASS", "score_DEFENSIVE", "highlight_color", "max_categories"]

    # Verificar quais colunas existem
    available_cols = [c for c in cols if c in filtered.columns]

    print(f"\n{'Player':<30} {'Team':<25} {'Overall':<10} {'Off':<8} {'DGP':<8} {'Pass':<8} {'Def':<8} {'Color':<10} {'Max Categories'}")
    print("=" * 150)

    for _, row in filtered[available_cols].iterrows():
        print(f"{str(row['player_name']):<30} "
              f"{str(row['team_name']):<25} "
              f"{row.get('overall_score', 0):<10.2f} "
              f"{row.get('score_OFFENSIVE', 0):<8.2f} "
              f"{row.get('score_DGP', 0):<8.2f} "
              f"{row.get('score_PASS', 0):<8.2f} "
              f"{row.get('score_DEFENSIVE', 0):<8.2f} "
              f"{row['highlight_color']:<10} "
              f"{row.get('max_categories', '')}")

    print("\n" + "=" * 120)
    print("\nVerificando máximos do grupo:")
    group_data = df[(df["position_group"] == position_group) & (df["competition_id"] == competition_id)]

    print(f"Max overall_score: {group_data['overall_score'].max():.2f}")
    if "score_OFFENSIVE" in group_data.columns:
        print(f"Max score_OFFENSIVE: {group_data['score_OFFENSIVE'].max():.2f}")
    if "score_DGP" in group_data.columns:
        print(f"Max score_DGP: {group_data['score_DGP'].max():.2f}")
    if "score_PASS" in group_data.columns:
        print(f"Max score_PASS: {group_data['score_PASS'].max():.2f}")
    if "score_DEFENSIVE" in group_data.columns:
        print(f"Max score_DEFENSIVE: {group_data['score_DEFENSIVE'].max():.2f}")
else:
    print("\nNenhum jogador destacado encontrado neste grupo.")
