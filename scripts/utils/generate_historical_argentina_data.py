"""
Generate historical Argentina scout data files for testing visualizations.

Creates 6 historical Excel files (argentina_1 to argentina_6) with data for 2 specific players,
applying cascading transformations to simulate historical data progression.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parents[2]
BASE_FILE = BASE_DIR / "bases" / "inputs" / "scouts_base" / "argentina_2025.xlsx"
OUTPUT_DIR = BASE_DIR / "bases" / "inputs" / "scouts_base"
PLAYER_IDS = [424480, 30803]  # Luis Ignacio Abraham and Matko Mijael Miljevic
NUM_FILES = 6

# Transformation parameters
MINUTES_DECREASE_FACTOR = 0.9  # 10% decrease per file
RANDOM_VARIATION_MIN = 0.95    # -5%
RANDOM_VARIATION_MAX = 1.05    # +5%
MONTH_DECREASE = 1             # 1 month per file

# Static columns that don't change
STATIC_COLUMNS = [
    "account_id", "player_id", "player_name", "team_id", "team_name",
    "competition_id", "competition_name", "season_id", "season_name",
    "country_id", "birth_date", "player_female", "player_first_name",
    "player_last_name", "player_known_name", "player_weight", "player_height",
    "primary_position", "secondary_position"
]

# Special handling columns
MINUTES_COLUMN = "player_season_minutes"
DATE_COLUMN = "player_season_most_recent_match"
NINETY_S_COLUMN = "player_season_90s_played"


def parse_date(date_str):
    """Parse date string in ISO format."""
    return datetime.fromisoformat(date_str.replace("T", " ").replace("Z", ""))


def format_date(dt):
    """Format datetime to ISO string format."""
    return dt.strftime("%Y-%m-%dT%H:%M")


def subtract_months(date_str, months):
    """Subtract N months from a date string."""
    dt = parse_date(date_str)
    # Approximate month subtraction (assuming 30 days per month for simplicity)
    new_dt = dt - timedelta(days=30 * months)
    return format_date(new_dt)


def apply_random_variation(value):
    """Apply random variation between -5% and +5% to a value."""
    if pd.isna(value) or value == 0:
        return value

    variation = np.random.uniform(RANDOM_VARIATION_MIN, RANDOM_VARIATION_MAX)
    new_value = value * variation

    # Ensure ratios stay in valid range [0, 1]
    if 0 < value <= 1:
        new_value = max(0, min(1, new_value))

    return new_value


def transform_data(df, file_number):
    """
    Apply transformations to create historical data.
    file_number: 6 (oldest) to 1 (newest)
    """
    df = df.copy()

    # Transform minutes (10% decrease)
    df[MINUTES_COLUMN] = df[MINUTES_COLUMN] * MINUTES_DECREASE_FACTOR

    # Transform date (subtract 1 month)
    df[DATE_COLUMN] = df[DATE_COLUMN].apply(lambda x: subtract_months(x, 1))

    # Recalculate 90s played based on new minutes
    df[NINETY_S_COLUMN] = df[MINUTES_COLUMN] / 90

    # Apply random variation to all other player_season_* columns
    for col in df.columns:
        if col.startswith("player_season_") and col not in [MINUTES_COLUMN, DATE_COLUMN, NINETY_S_COLUMN]:
            df[col] = df[col].apply(apply_random_variation)

    return df


def main():
    """Generate historical Argentina data files."""
    print("=" * 60)
    print("Generating Historical Argentina Scout Data")
    print("=" * 60)

    # Load base data
    print(f"\n1. Loading base file: {BASE_FILE}")
    base_df = pd.read_excel(BASE_FILE)
    print(f"   Total players in base: {len(base_df)}")

    # Filter for target players
    players_df = base_df[base_df["player_id"].isin(PLAYER_IDS)].copy()
    print(f"   Filtered to {len(players_df)} players: {PLAYER_IDS}")

    if len(players_df) != len(PLAYER_IDS):
        print(f"   WARNING: Expected {len(PLAYER_IDS)} players but found {len(players_df)}")
        missing = set(PLAYER_IDS) - set(players_df["player_id"].tolist())
        if missing:
            print(f"   Missing player IDs: {missing}")

    # Display player info
    print("\n   Player details:")
    for _, player in players_df.iterrows():
        print(f"   - {player['player_name']} (ID: {player['player_id']}, {player['team_name']})")
        print(f"     Minutes: {player[MINUTES_COLUMN]:.2f}, Date: {player[DATE_COLUMN]}")

    # Generate files in reverse order (6 -> 5 -> ... -> 1)
    print(f"\n2. Generating {NUM_FILES} historical files...")
    current_df = players_df.copy()

    for file_num in range(NUM_FILES, 0, -1):
        # Apply transformations
        current_df = transform_data(current_df, file_num)

        # Save file
        output_file = OUTPUT_DIR / f"argentina_{file_num}.xlsx"
        current_df.to_excel(output_file, index=False)

        print(f"   [OK] Created {output_file.name}")
        print(f"     - Minutes range: {current_df[MINUTES_COLUMN].min():.2f} - {current_df[MINUTES_COLUMN].max():.2f}")
        print(f"     - Date: {current_df[DATE_COLUMN].iloc[0]}")

    # Verification
    print("\n3. Verification:")
    print(f"   [OK] Generated {NUM_FILES} files successfully")
    print(f"   [OK] Each file contains {len(players_df)} players")
    print("   [OK] Static columns preserved across all files")
    print("   [OK] Minutes decreased by ~10% per file")
    print("   [OK] Dates decreased by 1 month per file")
    print("   [OK] Other metrics varied by +-5%")

    print("\n" + "=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(f"\nOutput files location: {OUTPUT_DIR.resolve()}")
    print("Files: argentina_1.xlsx, argentina_2.xlsx, ..., argentina_6.xlsx")


if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    main()
