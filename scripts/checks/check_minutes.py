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
print(f"JOGADORES SEM POSIÇÃO MAPEADA - ANÁLISE DE MINUTAGEM")
print("="*80)
print(f"Total: {len(no_pos)} jogadores\n")

if 'player_season_minutes' in no_pos.columns:
    minutes = no_pos['player_season_minutes']

    print(f"Estatísticas de minutagem:")
    print(f"  Média: {minutes.mean():.1f} minutos")
    print(f"  Mediana: {minutes.median():.1f} minutos")
    print(f"  Mínimo: {minutes.min():.1f} minutos")
    print(f"  Máximo: {minutes.max():.1f} minutos")

    print(f"\nDistribuição por faixas:")
    print(f"  0-90 min (1 jogo): {(minutes <= 90).sum()} jogadores ({(minutes <= 90).sum()/len(no_pos)*100:.1f}%)")
    print(f"  91-450 min (1-5 jogos): {((minutes > 90) & (minutes <= 450)).sum()} jogadores ({((minutes > 90) & (minutes <= 450)).sum()/len(no_pos)*100:.1f}%)")
    print(f"  451-900 min (5-10 jogos): {((minutes > 450) & (minutes <= 900)).sum()} jogadores ({((minutes > 450) & (minutes <= 900)).sum()/len(no_pos)*100:.1f}%)")
    print(f"  901+ min (10+ jogos): {(minutes > 900).sum()} jogadores ({(minutes > 900).sum()/len(no_pos)*100:.1f}%)")

    print("\n" + "="*80)
    print("EXEMPLOS DE JOGADORES (15 primeiros)")
    print("="*80)

    examples = no_pos[['player_name', 'team_name', 'competition_name', 'player_season_minutes']].head(15)
    for i, (idx, row) in enumerate(examples.iterrows(), 1):
        print(f"{i:2d}. {row['player_name']:30s} | {row['team_name']:25s} | {row['player_season_minutes']:6.0f} min | {row['competition_name']}")

    # Comparar com jogadores que TÊM posição
    print("\n" + "="*80)
    print("COMPARAÇÃO: Jogadores COM posição mapeada")
    print("="*80)

    with_pos = df[df['mapped_position'].notna()]
    minutes_with_pos = with_pos['player_season_minutes']

    print(f"Total: {len(with_pos)} jogadores\n")
    print(f"Estatísticas de minutagem:")
    print(f"  Média: {minutes_with_pos.mean():.1f} minutos")
    print(f"  Mediana: {minutes_with_pos.median():.1f} minutos")
    print(f"  Mínimo: {minutes_with_pos.min():.1f} minutos")
    print(f"  Máximo: {minutes_with_pos.max():.1f} minutos")

    print(f"\n" + "="*80)
    print("CONCLUSÃO")
    print("="*80)
    print(f"Jogadores SEM posição têm em média {minutes.mean():.0f} minutos")
    print(f"Jogadores COM posição têm em média {minutes_with_pos.mean():.0f} minutos")
    print(f"Diferença: {minutes_with_pos.mean() - minutes.mean():.0f} minutos a mais para quem tem posição")
