"""
Módulo 04 - Normalização de Indicadores

Este módulo realiza:
1. Filtro de indicadores ativos (CONSIDERAR? = SIM)
2. Normalização de valores (0-100) por grupo de posição + competição
3. Tratamento de direção (CIMA vs BAIXO)

Converte: 04_normalize_indicators.ipynb → normalize_indicators.py
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

from . import get_base_dir


def normalize_column(series: pd.Series, direction: str = "CIMA") -> pd.Series:
    """
    Normaliza uma série de valores para o intervalo 0-100.

    Args:
        series: pd.Series com os valores a normalizar
        direction: 'CIMA' (maior é melhor) ou 'BAIXO' (menor é melhor)

    Returns:
        pd.Series normalizada (0-100)
    """
    min_val = series.min()
    max_val = series.max()

    # Evitar divisão por zero
    if max_val == min_val:
        return pd.Series([50.0] * len(series), index=series.index)

    # Normalização
    if direction == "CIMA":
        # Maior valor = 100
        normalized = (series - min_val) / (max_val - min_val) * 100
    else:  # BAIXO
        # Menor valor = 100
        normalized = (max_val - series) / (max_val - min_val) * 100

    return normalized


def run() -> bool:
    """
    Executa a normalização de indicadores.

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        print("=" * 70)
        print("ETAPA 4/6: NORMALIZAÇÃO DE INDICADORES")
        print("=" * 70)
        print()

        # Configurar diretórios
        BASE_DIR = get_base_dir()
        OUTPUT_DIR = BASE_DIR / "bases" / "outputs"

        # 1. Carregar Dados
        print("[1/5] Carregando dados...")
        df = pd.read_parquet(OUTPUT_DIR / "_temp_scouts_consolidated.parquet")
        df_weights = pd.read_parquet(OUTPUT_DIR / "_temp_weights_active.parquet")

        print(f"  ✓ Jogadores: {len(df)}")
        print(f"  ✓ Indicadores ativos: {len(df_weights)}")

        # 2. Identificar Indicadores Válidos
        print("\n[2/5] Identificando indicadores...")
        indicadores = df_weights["INDICADOR"].str.strip().tolist()
        indicadores_disponiveis = [ind for ind in indicadores if ind in df.columns]
        indicadores_faltantes = [ind for ind in indicadores if ind not in df.columns]

        print(f"  ✓ Indicadores disponíveis: {len(indicadores_disponiveis)}")
        if indicadores_faltantes:
            print(f"  ⚠ Indicadores faltantes: {len(indicadores_faltantes)}")

        # Criar mapeamento de direção
        direction_map = dict(zip(
            df_weights["INDICADOR"].str.strip(),
            df_weights["Melhor para"]
        ))

        # 3. Aplicar Normalização
        print("\n[3/5] Normalizando indicadores...")
        df_normalized = df.copy()

        # Criar coluna de grupo para normalização: posição + competição
        df_normalized["_norm_group"] = (
            df_normalized["mapped_position"].astype(str) + "_" +
            df_normalized["competition_id"].astype(str)
        )

        normalized_count = 0
        for idx, indicador in enumerate(indicadores_disponiveis, 1):
            if idx % 20 == 0:
                print(f"    {idx}/{len(indicadores_disponiveis)}...", end="\r")

            try:
                direction = direction_map.get(indicador, "CIMA")

                # Converter para numérico
                df_normalized[indicador] = pd.to_numeric(df_normalized[indicador], errors="coerce")

                # Normalizar POR GRUPO (posição + competição)
                df_normalized[f"{indicador}_norm"] = df_normalized.groupby("_norm_group")[indicador].transform(
                    lambda x: normalize_column(x, direction)
                )
                normalized_count += 1

            except Exception as e:
                # Continuar mesmo se houver erro em um indicador
                pass

        # Remover coluna auxiliar
        df_normalized.drop(columns=["_norm_group"], inplace=True)

        print(f"\r  ✓ Indicadores normalizados: {normalized_count}")

        # 4. Criar Mapeamento de Pesos
        print("\n[4/5] Criando mapeamento de pesos...")
        position_columns = ["GK", "RCB", "LCB", "CB", "RB", "LB", "DM", "CM", "AM", "LW", "RW", "CF"]
        available_pos_cols = [c for c in position_columns if c in df_weights.columns]

        weights_dict = {}
        for _, row in df_weights.iterrows():
            indicador = row["INDICADOR"].strip()
            if indicador in indicadores_disponiveis:
                weights_dict[indicador] = {}
                for pos in available_pos_cols:
                    weights_dict[indicador][pos] = row[pos] if pd.notna(row[pos]) else 0

        print(f"  ✓ Mapeamento criado para {len(weights_dict)} indicadores")

        # 5. Salvar Dados
        print("\n[5/5] Salvando dados...")

        df_normalized.to_parquet(OUTPUT_DIR / "_temp_scouts_normalized.parquet", index=False)

        with open(OUTPUT_DIR / "_temp_weights_map.json", "w") as f:
            json.dump(weights_dict, f)

        with open(OUTPUT_DIR / "_temp_indicators_available.json", "w") as f:
            json.dump(indicadores_disponiveis, f)

        print(f"  ✓ Dados normalizados salvos")
        print(f"  ✓ Mapeamento de pesos salvo")
        print(f"  ✓ Lista de indicadores salva")

        # Resumo final
        norm_cols = [c for c in df_normalized.columns if c.endswith("_norm")]
        print("\n" + "=" * 70)
        print("RESUMO")
        print("=" * 70)
        print(f"Jogadores: {len(df_normalized)}")
        print(f"Indicadores normalizados: {len(norm_cols)}")
        print(f"Colunas totais: {len(df_normalized.columns)}")
        print("=" * 70)
        print()

        return True

    except Exception as e:
        print(f"\n✗ ERRO na normalização: {str(e)}")
        raise


if __name__ == "__main__":
    run()
