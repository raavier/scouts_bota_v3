import pandas as pd
import sys
import io

# Configurar encoding UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Carregar dados
df = pd.read_parquet('bases/outputs/consolidated_overral.parquet')

# Jogadores sem posição mapeada
no_pos = df[df['mapped_position'].isna()]

print("="*80)
print(f"JOGADORES SEM POSIÇÃO MAPEADA: {len(no_pos)}")
print("="*80)

# Verificar primary_position desses jogadores
print("\nPosições originais (primary_position):")
print(no_pos['primary_position'].value_counts())

# Verificar se primary_position é nulo
print(f"\nJogadores com primary_position nulo: {no_pos['primary_position'].isna().sum()}")
print(f"Jogadores com primary_position não nulo: {no_pos['primary_position'].notna().sum()}")

# Mostrar alguns exemplos
print("\n" + "="*80)
print("PRIMEIROS 15 JOGADORES SEM POSIÇÃO MAPEADA")
print("="*80)

for i, (idx, row) in enumerate(no_pos.head(15).iterrows()):
    print(f"\n{i+1}. Player ID: {row['player_id']}")
    print(f"   Nome: {row['player_name']}")
    print(f"   Primary Position: {row['primary_position']}")
    print(f"   Mapped Position: {row['mapped_position']}")
    print(f"   Time: {row['team_name']}")
    print(f"   Competição: {row['competition_name']}")

# Carregar dados da etapa anterior para entender o problema
print("\n" + "="*80)
print("INVESTIGANDO DADOS BRUTOS")
print("="*80)

df_raw = pd.read_parquet('bases/outputs/_temp_scouts_raw.parquet')

# Verificar um dos jogadores problemáticos
player_id = 523978
player_raw = df_raw[df_raw['player_id'] == player_id]

if len(player_raw) > 0:
    print(f"\nExemplo: Player ID {player_id} nos dados BRUTOS")
    print(f"  player_name: {player_raw['player_name'].iloc[0]}")
    print(f"  primary_position: {player_raw['primary_position'].iloc[0]}")
    print(f"  team_name: {player_raw['team_name'].iloc[0]}")

# Carregar dados após mapeamento de posição
df_positions = pd.read_parquet('bases/outputs/_temp_scouts_positions.parquet')
player_pos = df_positions[df_positions['player_id'] == player_id]

if len(player_pos) > 0:
    print(f"\nExemplo: Player ID {player_id} APÓS MAPEAMENTO")
    print(f"  player_name: {player_pos['player_name'].iloc[0]}")
    print(f"  primary_position: {player_pos['primary_position'].iloc[0]}")
    print(f"  mapped_position: {player_pos['mapped_position'].iloc[0]}")
    print(f"  team_name: {player_pos['team_name'].iloc[0]}")
