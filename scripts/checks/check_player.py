import pandas as pd

# Carregar Excel
excel_file = 'bases/inputs/scouts_base/italy_1.xlsx'
df = pd.read_excel(excel_file)

print(f'Total de registros no Excel: {len(df)}')
print(f'Total de colunas: {len(df.columns)}')

# Mostrar primeiras colunas
print(f'\nPrimeiras 10 colunas:')
for i, col in enumerate(df.columns[:10]):
    print(f'  {i+1}. {col}')

# Buscar colunas com 'id' ou 'player'
id_cols = [c for c in df.columns if 'id' in c.lower() or 'player' in c.lower()]
print(f'\nColunas com "id" ou "player":')
for col in id_cols:
    print(f'  - {col}')

# Tentar encontrar a coluna correta de ID
player_id_col = None
for col in df.columns:
    if 'player' in col.lower() and 'id' in col.lower():
        player_id_col = col
        break

if player_id_col:
    print(f'\nUsando coluna: {player_id_col}')
    player = df[df[player_id_col] == 410697]

    print(f'\nJogador encontrado: {len(player) > 0}')

    if len(player) > 0:
        # Colunas com 'name'
        name_cols = [c for c in df.columns if 'name' in c.lower()]
        print(f'\nColunas relacionadas a nome:')
        for col in name_cols:
            print(f'  - {col}')

        print(f'\n{"="*60}')
        print(f'DADOS DO JOGADOR (player_id=410697, competition_id=12)')
        print(f'{"="*60}')

        for col in name_cols:
            val = player[col].iloc[0]
            print(f'{col}: {val}')

        # Buscar outras colunas importantes
        other_cols = ['Team Name', 'Primary Position', 'Competition Id']
        for col in other_cols:
            if col in df.columns:
                print(f'{col}: {player[col].iloc[0]}')
    else:
        print('Jogador não encontrado no Excel')
else:
    print('Coluna de Player ID não encontrada!')
