import pandas as pd
import sys
import io

# Configurar encoding UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Carregar dados
df = pd.read_parquet('bases/outputs/consolidated_overral.parquet')

# IDs de exemplo da imagem
sample_ids = [523978, 520106, 445998, 419029, 196875, 410697, 406907]

print("="*80)
print("VERIFICAÇÃO: Jogadores agora têm 'Sem posição definida'")
print("="*80)

players = df[df['player_id'].isin(sample_ids)]

for i, (_, p) in enumerate(players.iterrows(), 1):
    print(f"\n{i}. Player ID: {p['player_id']}")
    print(f"   Nome: {p['player_name']}")
    print(f"   Primary Position: {p['primary_position']}")
    print(f"   Mapped Position: {p['mapped_position']}")
    print(f"   Overall Score: {p['overall_score']}")
    print(f"   Time: {p['team_name']}")
    print(f"   Competição: {p['competition_name']}")

# Estatísticas gerais
print("\n" + "="*80)
print("ESTATÍSTICAS GERAIS")
print("="*80)

sem_posicao = df[df['primary_position'] == 'Sem posição definida']
print(f"\nTotal de jogadores com 'Sem posição definida': {len(sem_posicao)}")
print(f"Percentual: {len(sem_posicao)/len(df)*100:.2f}%")

# Verificar se ainda há None
null_positions = df[df['primary_position'].isna()]
print(f"\nJogadores com primary_position nulo: {len(null_positions)}")

print("\n" + "="*80)
print("CONCLUSÃO")
print("="*80)
if len(sem_posicao) > 0 and len(null_positions) == 0:
    print("✓ Correção aplicada com sucesso!")
    print(f"  {len(sem_posicao)} jogadores agora têm 'Sem posição definida'")
    print("  Esses jogadores aparecem na tabela mas sem overall_score")
else:
    print("✗ Ainda há problemas na correção")
