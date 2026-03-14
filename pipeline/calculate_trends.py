"""
Módulo 05.5 - Cálculo de Tendências

Este módulo realiza:
1. Análise de tendência de overall_score usando regressão linear
2. Cálculo de variação percentual vs período anterior
3. Análise de tendência de rankings (overall e position)
4. Identificação de períodos com dados insuficientes
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import yaml

from . import get_base_dir


def load_config():
    """Carrega configurações do arquivo config.yaml"""
    base_dir = get_base_dir()
    config_file = base_dir / "config" / "config.yaml"

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config.get('trends', {
        'enabled': True,
        'time_window_months': 3,
        'min_periods_required': 2,
        'stable_threshold': 0.05
    })


def calculate_linear_regression(x, y):
    """
    Calcula regressão linear simples.

    Args:
        x: array de valores X (tempo)
        y: array de valores Y (scores)

    Returns:
        dict com slope, intercept, ou None se dados insuficientes
    """
    if len(x) < 2 or len(y) < 2:
        return None

    # Remover NaN
    mask = ~(np.isnan(x) | np.isnan(y))
    x_clean = x[mask]
    y_clean = y[mask]

    if len(x_clean) < 2:
        return None

    # Calcular regressão linear usando fórmulas básicas
    n = len(x_clean)
    x_mean = np.mean(x_clean)
    y_mean = np.mean(y_clean)

    numerator = np.sum((x_clean - x_mean) * (y_clean - y_mean))
    denominator = np.sum((x_clean - x_mean) ** 2)

    if denominator == 0:
        return None

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean

    return {
        'slope': slope,
        'intercept': intercept
    }


def calculate_months_span(dates):
    """
    Calcula o span temporal em meses entre a data mais antiga e mais recente.

    Args:
        dates: lista de datas (datetime)

    Returns:
        float: span em meses
    """
    if len(dates) < 2:
        return 0.0

    dates_clean = [d for d in dates if pd.notna(d)]
    if len(dates_clean) < 2:
        return 0.0

    oldest = min(dates_clean)
    newest = max(dates_clean)

    # Calcular diferença em dias e converter para meses
    days_diff = (newest - oldest).days
    months_span = days_diff / 30.44  # média de dias por mês

    return round(months_span, 2)


def classify_direction(value, threshold):
    """
    Classifica direção baseado em um valor e threshold.

    Args:
        value: valor numérico
        threshold: limite para considerar estável

    Returns:
        "up", "down", "stable", ou None
    """
    if value is None or pd.isna(value):
        return None

    if abs(value) < threshold:
        return "stable"
    elif value > 0:
        return "up"
    else:
        return "down"


def calculate_trend_for_player(player_records, config):
    """
    Calcula tendências para um único jogador.

    Args:
        player_records: DataFrame com todos os registros do jogador (histórico + atual)
                       Deve estar ordenado por data (mais antigo primeiro)
        config: Dict com configurações de tendência

    Returns:
        dict com colunas de tendência
    """
    # Inicializar resultado com valores padrão
    result = {
        'trend_overall_slope': None,
        'trend_overall_direction': None,
        'trend_overall_change_pct': None,
        'trend_overall_periods_used': 0,
        'trend_overall_months_span': 0.0,
        'trend_rank_overall_change': None,
        'trend_rank_overall_direction': None,
        'trend_rank_position_change': None,
        'trend_rank_position_direction': None,
    }

    # Verificar se tem dados suficientes
    if len(player_records) < 1:
        return result

    # Se tem apenas 1 registro (sem histórico), retornar valores padrão
    if len(player_records) == 1:
        return result

    # Ordenar por data (mais antigo primeiro)
    player_records = player_records.sort_values('player_season_most_recent_match')

    # Filtrar últimos N meses (se configurado)
    time_window_months = config.get('time_window_months', 3)
    if time_window_months > 0:
        cutoff_date = player_records.iloc[-1]['player_season_most_recent_match'] - timedelta(days=time_window_months * 30.44)
        player_records = player_records[player_records['player_season_most_recent_match'] >= cutoff_date]

    # Recalcular quantidade de períodos após filtro
    n_periods = len(player_records)

    if n_periods < 1:
        return result

    # Atualizar períodos usados e span temporal
    result['trend_overall_periods_used'] = n_periods - 1  # Não conta o registro atual
    result['trend_overall_months_span'] = calculate_months_span(
        player_records['player_season_most_recent_match'].tolist()
    )

    # Se tem apenas 1 período no window, não pode calcular tendências
    if n_periods == 1:
        return result

    # Pegar registro atual (último) e anterior
    current_record = player_records.iloc[-1]
    previous_record = player_records.iloc[-2]

    # Calcular variação percentual (atual vs anterior)
    if pd.notna(current_record.get('overall_score')) and pd.notna(previous_record.get('overall_score')):
        if previous_record['overall_score'] != 0:
            change_pct = ((current_record['overall_score'] - previous_record['overall_score']) /
                         previous_record['overall_score']) * 100
            result['trend_overall_change_pct'] = round(change_pct, 2)

    # Calcular mudança de rankings
    if pd.notna(current_record.get('rank_overall')) and pd.notna(previous_record.get('rank_overall')):
        # Mudança positiva = subiu posições (rank menor é melhor)
        rank_change = int(previous_record['rank_overall'] - current_record['rank_overall'])
        result['trend_rank_overall_change'] = rank_change
        result['trend_rank_overall_direction'] = classify_direction(rank_change, 0)

    if pd.notna(current_record.get('rank_position')) and pd.notna(previous_record.get('rank_position')):
        rank_change = int(previous_record['rank_position'] - current_record['rank_position'])
        result['trend_rank_position_change'] = rank_change
        result['trend_rank_position_direction'] = classify_direction(rank_change, 0)

    # Calcular regressão linear (requer mínimo de períodos)
    min_periods = config.get('min_periods_required', 2)
    if n_periods >= min_periods:
        # Preparar dados para regressão
        x = np.arange(n_periods)  # 0, 1, 2, ..., N-1
        y = player_records['overall_score'].values

        # Calcular regressão
        regression = calculate_linear_regression(x, y)

        if regression is not None:
            slope = regression['slope']
            result['trend_overall_slope'] = round(slope, 4)

            # Classificar direção baseado no slope
            threshold = config.get('stable_threshold', 0.05)
            result['trend_overall_direction'] = classify_direction(slope, threshold)

    return result


def run() -> bool:
    """
    Executa o cálculo de tendências.

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        print("=" * 70)
        print("ETAPA 5.5/6: CÁLCULO DE TENDÊNCIAS")
        print("=" * 70)
        print()

        # Configurar diretórios
        BASE_DIR = get_base_dir()
        OUTPUT_DIR = BASE_DIR / "bases" / "outputs"

        # Carregar configurações
        print("[1/4] Carregando configurações...")
        config = load_config()

        if not config.get('enabled', True):
            print("  ⚠ Cálculo de tendências desabilitado no config.yaml")
            print("  ⚠ Pulando esta etapa...")
            return True

        time_window = config.get('time_window_months', 3)
        min_periods = config.get('min_periods_required', 2)
        print(f"  ✓ Time window: {time_window} meses")
        print(f"  ✓ Mínimo de períodos para regressão: {min_periods}")

        # Carregar dados scored
        print("\n[2/4] Carregando dados...")
        df = pd.read_parquet(OUTPUT_DIR / "_temp_scouts_scored.parquet")
        print(f"  ✓ Dados carregados: {len(df)} registros")

        # Converter data para datetime se necessário
        if not pd.api.types.is_datetime64_any_dtype(df['player_season_most_recent_match']):
            df['player_season_most_recent_match'] = pd.to_datetime(
                df['player_season_most_recent_match'], errors='coerce'
            )

        # Calcular tendências para cada unique_key
        print("\n[3/4] Calculando tendências...")

        # Inicializar colunas de tendência com valores padrão
        trend_columns = [
            'trend_overall_slope', 'trend_overall_direction', 'trend_overall_change_pct',
            'trend_overall_periods_used', 'trend_overall_months_span',
            'trend_rank_overall_change', 'trend_rank_overall_direction',
            'trend_rank_position_change', 'trend_rank_position_direction'
        ]

        for col in trend_columns:
            df[col] = None

        # Processar por unique_key
        unique_keys = df['unique_key'].unique()
        processed = 0
        with_trends = 0

        for key in unique_keys:
            # Filtrar todos os registros deste jogador (histórico + atual)
            player_records = df[df['unique_key'] == key].copy()

            # Calcular tendências
            trends = calculate_trend_for_player(player_records, config)

            # Atualizar APENAS o registro atual (v_current = True)
            current_mask = (df['unique_key'] == key) & (df['v_current'] == True)

            if current_mask.any():
                for col, value in trends.items():
                    df.loc[current_mask, col] = value

                # Contar quantos têm tendências calculadas
                if trends['trend_overall_periods_used'] > 0:
                    with_trends += 1

            processed += 1
            if processed % 1000 == 0:
                print(f"    {processed}/{len(unique_keys)}...", end='\r')

        print(f"  ✓ Tendências calculadas: {processed} jogadores")
        print(f"  ✓ Jogadores com dados históricos: {with_trends}")
        print(f"  ✓ Jogadores sem histórico: {processed - with_trends}")

        # Salvar dados com tendências
        print("\n[4/4] Salvando dados...")
        df.to_parquet(OUTPUT_DIR / "_temp_scouts_with_trends.parquet", index=False)
        print(f"  ✓ Dados salvos: _temp_scouts_with_trends.parquet")

        # Resumo final
        print("\n" + "=" * 70)
        print("RESUMO")
        print("=" * 70)
        print(f"Total de jogadores: {processed}")
        print(f"Jogadores com tendências: {with_trends}")
        print(f"Novas colunas adicionadas: {len(trend_columns)}")
        print("=" * 70)
        print()

        return True

    except Exception as e:
        print(f"\n✗ ERRO no cálculo de tendências: {str(e)}")
        raise


if __name__ == "__main__":
    # Permite testar módulo standalone
    run()
