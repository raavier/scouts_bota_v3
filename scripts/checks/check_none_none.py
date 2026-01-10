import pandas as pd

# Carregar arquivo consolidado
df = pd.read_parquet('bases/outputs/consolidated_overral.parquet')

print(f'Total registros: {len(df)}')
print(f'Registros com "None None": {len(df[df["player_name"] == "None None"])}')
print(f'Registros com player_name nulo: {df["player_name"].isna().sum()}')

print('\n' + '='*60)
print('Exemplo: Jogador 410697 (competition_id=12)')
print('='*60)

player = df[(df['player_id'] == 410697) & (df['competition_id'] == 12)]

if len(player) > 0:
    print(f'player_name: {player["player_name"].iloc[0]}')
    print(f'team_name: {player["team_name"].iloc[0]}')
    print(f'mapped_position: {player["mapped_position"].iloc[0]}')
    print(f'overall_score: {player["overall_score"].iloc[0]:.2f}')
else:
    print('Jogador não encontrado!')

# Estatísticas gerais
print('\n' + '='*60)
print('Estatísticas de player_name')
print('='*60)
print(f'Nomes válidos: {df["player_name"].notna().sum()}')
print(f'Nomes nulos: {df["player_name"].isna().sum()}')
print(f'Nomes "None None": {(df["player_name"] == "None None").sum()}')
print(f'Nomes "nan": {(df["player_name"] == "nan").sum()}')
