"""
Módulo 03 - Consolidação de Jogadores

Este módulo realiza:
1. Criação de chave única (player_id + competition_id + team_id)
2. Marcação de registro atual (v_current = True para mais recente)
3. Geração de colunas auxiliares (player_name com lógica de prioridade)

Converte: 03_consolidate_players.ipynb → consolidate_players.py
"""

import pandas as pd
from pathlib import Path

from . import get_base_dir


def run() -> bool:
    """
    Executa a consolidação de jogadores.

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        print("=" * 70)
        print("ETAPA 3/6: CONSOLIDAÇÃO DE JOGADORES")
        print("=" * 70)
        print()

        # Configurar diretórios
        BASE_DIR = get_base_dir()
        OUTPUT_DIR = BASE_DIR / "bases" / "outputs"

        # 1. Carregar Dados
        print("[1/4] Carregando dados...")
        df = pd.read_parquet(OUTPUT_DIR / "_temp_scouts_positions.parquet")
        print(f"  ✓ Dados carregados: {len(df)} registros")

        # 2. Criar Chave Única (player_id + competition_id + team_id)
        print("\n[2/4] Criando chave única...")
        df["unique_key"] = (
            df["player_id"].astype(str) + "_" +
            df["competition_id"].astype(str) + "_" +
            df["team_id"].astype(str)
        )

        print(f"  ✓ Total de registros: {len(df)}")
        print(f"  ✓ Chaves únicas: {df['unique_key'].nunique()}")

        duplicates_count = len(df) - df['unique_key'].nunique()
        if duplicates_count > 0:
            print(f"  ⚠ Registros duplicados: {duplicates_count}")

        # 3. Marcar Registro Atual (v_current)
        print("\n[3/4] Marcando registro atual...")

        if "player_season_most_recent_match" in df.columns:
            # Converter para datetime se necessário
            df["player_season_most_recent_match"] = pd.to_datetime(
                df["player_season_most_recent_match"], errors="coerce"
            )

            # Ordenar por data (mais recente primeiro)
            df = df.sort_values("player_season_most_recent_match", ascending=False)

            # Marcar o primeiro de cada grupo (mais recente) como v_current = True
            df["v_current"] = ~df.duplicated(subset="unique_key", keep="first")
        else:
            # Se não tiver a coluna de data, marcar o primeiro encontrado como atual
            df["v_current"] = ~df.duplicated(subset="unique_key", keep="first")

        print(f"  ✓ Registros atuais (v_current=True): {df['v_current'].sum()}")
        print(f"  ✓ Registros históricos (v_current=False): {(~df['v_current']).sum()}")

        # 4. Gerar Colunas Auxiliares
        print("\n[4/4] Gerando colunas auxiliares...")

        # Criar coluna auxiliar player_name com lógica de prioridade:
        # 1. player_known_name (prioridade máxima)
        # 2. player_name (vem do Excel original)
        # 3. first_name + last_name (somente se AMBOS existirem)
        # 4. somente first_name
        # 5. somente last_name

        df["player_name_final"] = None

        # Prioridade 1: player_known_name
        if "player_known_name" in df.columns:
            mask = df["player_known_name"].notna()
            df.loc[mask, "player_name_final"] = df.loc[mask, "player_known_name"]

        # Prioridade 2: player_name (do Excel original)
        if "player_name" in df.columns:
            mask = df["player_name_final"].isna() & df["player_name"].notna()
            df.loc[mask, "player_name_final"] = df.loc[mask, "player_name"]

        # Prioridade 3: first_name + last_name (somente se AMBOS existirem)
        if "player_first_name" in df.columns and "player_last_name" in df.columns:
            mask = (
                df["player_name_final"].isna() &
                df["player_first_name"].notna() &
                df["player_last_name"].notna()
            )
            df.loc[mask, "player_name_final"] = (
                df.loc[mask, "player_first_name"].astype(str) + " " +
                df.loc[mask, "player_last_name"].astype(str)
            )

        # Prioridade 4: somente first_name
        if "player_first_name" in df.columns:
            mask = df["player_name_final"].isna() & df["player_first_name"].notna()
            df.loc[mask, "player_name_final"] = df.loc[mask, "player_first_name"]

        # Prioridade 5: somente last_name
        if "player_last_name" in df.columns:
            mask = df["player_name_final"].isna() & df["player_last_name"].notna()
            df.loc[mask, "player_name_final"] = df.loc[mask, "player_last_name"]

        # Substituir a coluna player_name pela versão final
        df["player_name"] = df["player_name_final"]
        df.drop(columns=["player_name_final"], inplace=True)

        # Criar competition_name se não existir
        if "competition_name" not in df.columns and "source_file" in df.columns:
            df["competition_name"] = df["source_file"].str.replace(".xlsx", "", regex=False)

        print(f"  ✓ player_name gerado: {df['player_name'].notna().sum()} registros com nome")
        if df['player_name'].isna().sum() > 0:
            print(f"  ⚠ Registros SEM nome: {df['player_name'].isna().sum()}")

        # Salvar dados consolidados
        df.to_parquet(OUTPUT_DIR / "_temp_scouts_consolidated.parquet", index=False)
        print(f"  ✓ Dados salvos: _temp_scouts_consolidated.parquet")

        # Resumo final
        print("\n" + "=" * 70)
        print("RESUMO")
        print("=" * 70)
        print(f"Total de registros: {len(df)}")
        print(f"Registros atuais (v_current=True): {df['v_current'].sum()}")
        print(f"Registros históricos: {(~df['v_current']).sum()}")
        print(f"Chaves únicas: {df['unique_key'].nunique()}")
        print("=" * 70)
        print()

        return True

    except Exception as e:
        print(f"\n✗ ERRO na consolidação de jogadores: {str(e)}")
        raise


if __name__ == "__main__":
    # Permite testar módulo standalone
    run()
