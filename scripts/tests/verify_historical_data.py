"""Verify the generated historical Argentina data files."""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
BASE_PATH = BASE_DIR / "bases" / "inputs" / "scouts_base"
FILES = ["argentina_2025", "argentina_6", "argentina_5", "argentina_4",
         "argentina_3", "argentina_2", "argentina_1"]
PLAYER_IDS = [424480, 30803]

print("=" * 80)
print("Verification of Historical Argentina Data Files")
print("=" * 80)

for player_id in PLAYER_IDS:
    print(f"\nPlayer ID: {player_id}")
    print("-" * 80)
    print(f"{'File':<18} {'Minutes':<12} {'90s_played':<12} {'Date':<20} {'np_xg_90':<12}")
    print("-" * 80)

    for file_name in FILES:
        file_path = BASE_PATH / f"{file_name}.xlsx"
        df = pd.read_excel(file_path)
        player = df[df["player_id"] == player_id]

        if len(player) > 0:
            player = player.iloc[0]
            print(f"{file_name:<18} "
                  f"{player['player_season_minutes']:<12.2f} "
                  f"{player['player_season_90s_played']:<12.4f} "
                  f"{player['player_season_most_recent_match']:<20} "
                  f"{player['player_season_np_xg_90']:<12.6f}")
        else:
            print(f"{file_name:<18} [NOT FOUND]")

# Check static columns consistency
print("\n" + "=" * 80)
print("Checking Static Columns Consistency")
print("=" * 80)

static_cols = ["player_name", "team_name", "competition_name", "birth_date"]
for player_id in PLAYER_IDS:
    print(f"\nPlayer ID: {player_id}")
    base_file = BASE_PATH / "argentina_2025.xlsx"
    base_df = pd.read_excel(base_file)
    base_player = base_df[base_df["player_id"] == player_id].iloc[0]

    print(f"  Name: {base_player['player_name']}")
    print(f"  Team: {base_player['team_name']}")
    print(f"  Competition: {base_player['competition_name']}")

    # Verify all files have same static values
    all_consistent = True
    for file_name in FILES[1:]:  # Skip base file
        file_path = BASE_PATH / f"{file_name}.xlsx"
        df = pd.read_excel(file_path)
        player = df[df["player_id"] == player_id].iloc[0]

        for col in static_cols:
            if str(player[col]) != str(base_player[col]):
                print(f"  [WARNING] {col} differs in {file_name}: {player[col]} vs {base_player[col]}")
                all_consistent = False

    if all_consistent:
        print("  [OK] All static columns consistent across files")

print("\n" + "=" * 80)
print("Verification Complete!")
print("=" * 80)
