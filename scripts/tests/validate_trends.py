"""Validar cálculo de tendências para jogadores de teste."""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

df = pd.read_parquet(BASE_DIR / "bases" / "outputs" / "consolidated_overall.parquet")

print("=" * 80)
print("VALIDAÇÃO DE TENDÊNCIAS - JOGADORES DE TESTE")
print("=" * 80)

# Filtrar jogadores de teste (APENAS REGISTROS ATUAIS)
test_players = df[(df["player_id"].isin([30803, 424480])) & (df["v_current"] == True)].copy()

for player_id in [30803, 424480]:
    player = test_players[test_players["player_id"] == player_id].iloc[0]

    print(f"\n{'='*80}")
    print(f"Jogador: {player['player_name']} (ID: {player_id})")
    print(f"Time: {player['team_name']}")
    print(f"Posição: {player['primary_position']}")
    print(f"{'='*80}")

    # Overall score
    print(f"\n[Overall Score]")
    print(f"  Score atual: {player['overall_score']:.2f}")

    # Tendências
    print(f"\n[Tendências - Overall]")
    print(f"  Períodos usados: {player['trend_overall_periods_used']}")
    print(f"  Span temporal: {player['trend_overall_months_span']:.2f} meses")
    print(f"  Slope (inclinação): {player['trend_overall_slope']}")
    print(f"  Direção: {player['trend_overall_direction']}")
    print(f"  Mudança %: {player['trend_overall_change_pct']}")

    # Tendências de ranking
    print(f"\n[Tendências - Rankings]")
    print(f"  Ranking overall atual: {player['rank_overall']}")
    print(f"  Mudança ranking overall: {player['trend_rank_overall_change']}")
    print(f"  Direção: {player['trend_rank_overall_direction']}")

    print(f"\n  Ranking position atual: {player['rank_position']}")
    print(f"  Mudança ranking position: {player['trend_rank_position_change']}")
    print(f"  Direção: {player['trend_rank_position_direction']}")

# Verificar jogador sem histórico
print(f"\n\n{'='*80}")
print("VERIFICAÇÃO: Jogador SEM Histórico")
print(f"{'='*80}")

no_history = df[(df["v_current"] == True) & (~df["player_id"].isin([30803, 424480]))].iloc[0]

print(f"\nJogador: {no_history['player_name']} (ID: {no_history['player_id']})")
print(f"  trend_overall_periods_used: {no_history['trend_overall_periods_used']}")
print(f"  trend_overall_months_span: {no_history['trend_overall_months_span']}")
print(f"  trend_overall_slope: {no_history['trend_overall_slope']}")
print(f"  trend_overall_direction: {no_history['trend_overall_direction']}")
print(f"  trend_overall_change_pct: {no_history['trend_overall_change_pct']}")

# Estatísticas gerais
print(f"\n\n{'='*80}")
print("ESTATÍSTICAS GERAIS")
print(f"{'='*80}")

trends_calculated = df[df["trend_overall_periods_used"] > 0]
print(f"\nTotal de jogadores: {len(df[df['v_current'] == True])}")
print(f"Jogadores com tendências: {len(trends_calculated)}")
print(f"Jogadores sem tendências: {len(df[df['v_current'] == True]) - len(trends_calculated)}")

# Distribuição de direções
print(f"\nDistribuição de direções de tendência:")
if len(trends_calculated) > 0:
    print(trends_calculated["trend_overall_direction"].value_counts())
else:
    print("  Nenhum jogador com tendência calculada")

print(f"\n{'='*80}")
