"""Check historical data in consolidated output."""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

df = pd.read_parquet(BASE_DIR / "bases" / "outputs" / "consolidated_overall.parquet")

# Check current records for test players
current = df[(df["v_current"] == True) & (df["player_id"].isin([30803, 424480]))].sort_values("player_id")

print("Registros ATUAIS (v_current=True):")
print()
print(current[["player_id", "player_name", "player_season_minutes",
               "player_season_most_recent_match", "v_current"]].to_string(index=False))

print("\n\nTOTAL DE REGISTROS POR JOGADOR:")
for pid in [30803, 424480]:
    total = len(df[df["player_id"] == pid])
    hist_count = len(df[(df["player_id"] == pid) & (df["v_current"] == False)])
    curr_count = len(df[(df["player_id"] == pid) & (df["v_current"] == True)])
    name = df[df["player_id"] == pid].iloc[0]["player_name"]
    print(f"  {name} (ID {pid}): {total} registros ({curr_count} atual + {hist_count} historicos)")

print("\n" + "=" * 70)
print("RESUMO")
print("=" * 70)
print(f"Total de registros no output: {len(df)}")
print(f"Registros atuais: {len(df[df['v_current'] == True])}")
print(f"Registros historicos: {len(df[df['v_current'] == False])}")
print("=" * 70)
