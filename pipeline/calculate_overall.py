"""
Módulo 05 - Cálculo de Scores Overall

Este módulo realiza:
1. Cálculo do score ponderado por posição
2. Cálculo de scores por categoria (CLASSIFICACAO RANKING)
3. Geração de rankings (geral e por posição)

Converte: 05_calculate_overall.ipynb → calculate_overall.py
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

from . import get_base_dir


POSITIONS = ["GK", "RCB", "LCB", "CB", "RB", "LB", "DM", "CM", "AM", "LW", "RW", "CF"]


def calculate_overall_score(row, weights_dict, position):
    """
    Calcula o score overall ponderado para um jogador em uma posição.

    Args:
        row: linha do DataFrame com dados do jogador
        weights_dict: dicionário com pesos por indicador e posição
        position: posição para aplicar os pesos

    Returns:
        float: score ponderado (0-100)
    """
    if position not in POSITIONS:
        return np.nan

    total_weight = 0
    weighted_sum = 0

    for indicador, pos_weights in weights_dict.items():
        norm_col = f"{indicador}_norm"

        if norm_col not in row.index:
            continue

        value = row[norm_col]
        if pd.isna(value):
            continue

        weight = pos_weights.get(position, 0)
        if weight == 0:
            continue

        weighted_sum += value * weight
        total_weight += weight

    if total_weight == 0:
        return np.nan

    return weighted_sum / total_weight


def calculate_category_score(row, indicadores, weights_dict, position):
    """
    Calcula o score ponderado para uma categoria específica.

    Args:
        row: linha do DataFrame
        indicadores: lista de indicadores da categoria
        weights_dict: dicionário com pesos
        position: posição do jogador

    Returns:
        float: score ponderado (0-100)
    """
    if position not in POSITIONS:
        return np.nan

    total_weight = 0
    weighted_sum = 0

    for indicador in indicadores:
        norm_col = f"{indicador}_norm"

        if norm_col not in row.index:
            continue

        value = row[norm_col]
        if pd.isna(value):
            continue

        weight = weights_dict.get(indicador, {}).get(position, 0)
        if weight == 0:
            continue

        weighted_sum += value * weight
        total_weight += weight

    if total_weight == 0:
        return np.nan

    return weighted_sum / total_weight


def run() -> bool:
    """
    Executa o cálculo de scores.

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        print("=" * 70)
        print("ETAPA 5/6: CÁLCULO DE SCORES")
        print("=" * 70)
        print()

        # Configurar diretórios
        BASE_DIR = get_base_dir()
        OUTPUT_DIR = BASE_DIR / "bases" / "outputs"

        # 1. Carregar Dados
        print("[1/4] Carregando dados...")
        df = pd.read_parquet(OUTPUT_DIR / "_temp_scouts_normalized.parquet")

        with open(OUTPUT_DIR / "_temp_weights_map.json", "r") as f:
            weights_dict = json.load(f)

        with open(OUTPUT_DIR / "_temp_indicators_available.json", "r") as f:
            indicadores_disponiveis = json.load(f)

        df_weights = pd.read_parquet(OUTPUT_DIR / "_temp_weights_active.parquet")

        print(f"  ✓ Jogadores: {len(df)}")
        print(f"  ✓ Indicadores com pesos: {len(weights_dict)}")

        # 2. Calcular Score Overall
        print("\n[2/4] Calculando scores overall...")
        scores = []
        for idx, row in df.iterrows():
            if (idx + 1) % 1000 == 0:
                print(f"    {idx + 1}/{len(df)}...", end="\r")

            position = row["mapped_position"]
            score = calculate_overall_score(row, weights_dict, position)
            scores.append(score)

        df["overall_score"] = scores
        valid_scores = df["overall_score"].notna().sum()
        print(f"\r  ✓ Scores calculados: {valid_scores} válidos de {len(df)}")

        # 3. Calcular Scores por Categoria e Subcategoria
        print("\n[3/4] Calculando scores por categoria e subcategoria...")

        # Criar mapeamentos indicador -> categoria e subcategoria
        indicador_categoria = dict(zip(
            df_weights["INDICADOR"].str.strip(),
            df_weights["CLASSIFICACAO RANKING"]
        ))

        indicador_subcategoria = dict(zip(
            df_weights["INDICADOR"].str.strip(),
            df_weights["SUBCLASSIFICACAO RANKING"]
        ))

        # Agrupar indicadores por categoria (CLASSIFICACAO)
        categorias_indicadores = {}
        for indicador in indicadores_disponiveis:
            categoria = indicador_categoria.get(indicador)
            if categoria:
                if categoria not in categorias_indicadores:
                    categorias_indicadores[categoria] = []
                categorias_indicadores[categoria].append(indicador)

        # Agrupar indicadores por subcategoria (SUBCLASSIFICACAO)
        subcategorias_indicadores = {}
        for indicador in indicadores_disponiveis:
            subcategoria = indicador_subcategoria.get(indicador)
            if subcategoria and pd.notna(subcategoria):
                if subcategoria not in subcategorias_indicadores:
                    subcategorias_indicadores[subcategoria] = []
                subcategorias_indicadores[subcategoria].append(indicador)

        # Calcular score por categoria (CLASSIFICACAO)
        for categoria, indicadores in categorias_indicadores.items():
            col_name = f"score_{categoria}"
            print(f"    {col_name}...", end="\r")

            scores_cat = []
            for idx, row in df.iterrows():
                position = row["mapped_position"]
                score = calculate_category_score(row, indicadores, weights_dict, position)
                scores_cat.append(score)

            df[col_name] = scores_cat

        print(f"\r  ✓ Scores por categoria (CLASSIFICACAO): {len(categorias_indicadores)} categorias")

        # Calcular score por subcategoria (SUBCLASSIFICACAO)
        for subcategoria, indicadores in subcategorias_indicadores.items():
            col_name = f"sub_score_{subcategoria}"
            print(f"    {col_name}...", end="\r")

            scores_subcat = []
            for idx, row in df.iterrows():
                position = row["mapped_position"]
                score = calculate_category_score(row, indicadores, weights_dict, position)
                scores_subcat.append(score)

            df[col_name] = scores_subcat

        print(f"\r  ✓ Scores por subcategoria (SUBCLASSIFICACAO): {len(subcategorias_indicadores)} subcategorias")

        # 4. Gerar Rankings
        print("\n[4/4] Gerando rankings...")

        # rank_position: ranking por posição (mapped_position)
        df["rank_position"] = df.groupby("mapped_position")["overall_score"].rank(ascending=False, method="min")

        # rank_overall: ranking por competition_id + position_group
        df["rank_overall"] = df.groupby(["competition_id", "position_group"])["overall_score"].rank(ascending=False, method="min")

        print(f"  ✓ Ranking por posição calculado (rank_position)")
        print(f"  ✓ Ranking overall por competição e grupo calculado (rank_overall)")

        # Salvar
        df.to_parquet(OUTPUT_DIR / "_temp_scouts_scored.parquet", index=False)
        print(f"  ✓ Dados salvos: _temp_scouts_scored.parquet")

        # Resumo final
        score_cols = [c for c in df.columns if c.startswith("score_") or c == "overall_score"]
        sub_score_cols = [c for c in df.columns if c.startswith("sub_score_")]
        print("\n" + "=" * 70)
        print("RESUMO")
        print("=" * 70)
        print(f"Total de jogadores: {len(df)}")
        print(f"Jogadores com score válido: {valid_scores}")
        print(f"Colunas de score (CLASSIFICACAO): {len(score_cols)}")
        print(f"Colunas de sub_score (SUBCLASSIFICACAO): {len(sub_score_cols)}")
        print(f"Total de colunas de score: {len(score_cols) + len(sub_score_cols)}")
        print("=" * 70)
        print()

        return True

    except Exception as e:
        print(f"\n✗ ERRO no cálculo de scores: {str(e)}")
        raise


if __name__ == "__main__":
    run()
