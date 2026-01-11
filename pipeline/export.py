"""
Módulo 06 - Exportação Final

Este módulo realiza:
1. Seleção de colunas finais
2. Exportação para parquet:
   - consolidated_overral.parquet (principais dados com scores)
   - consolidated_weights.parquet (tabela de pesos)
   - consolidated_context.parquet (metadados)
   - consolidated_normalized.parquet (valores normalizados)

Converte: 06_export.ipynb → export.py
"""

import pandas as pd
from pathlib import Path

from . import get_base_dir


def run() -> bool:
    """
    Executa a exportação final.

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        print("=" * 70)
        print("ETAPA 6/6: EXPORTAÇÃO FINAL")
        print("=" * 70)
        print()

        # Configurar diretórios
        BASE_DIR = get_base_dir()
        OUTPUT_DIR = BASE_DIR / "bases" / "outputs"

        # 1. Carregar Dados
        print("[1/4] Carregando dados...")
        df = pd.read_parquet(OUTPUT_DIR / "_temp_scouts_scored.parquet")
        df_weights = pd.read_parquet(OUTPUT_DIR / "_temp_weights_active.parquet")

        print(f"  ✓ Dados: {len(df)} jogadores, {len(df.columns)} colunas")
        print(f"  ✓ Pesos: {len(df_weights)} indicadores")

        # 2. Exportar consolidated_overral.parquet
        print("\n[2/4] Exportando consolidated_overral.parquet...")

        main_cols = [
            "player_id",
            "competition_id",
            "player_name",
            "competition_name",
            "team_name",
            "primary_position",
            "mapped_position",
            "position_group",
            "position_sub_group",
            "v_current",
            "overall_score",
            "rank_overall",
            "rank_position",
        ]

        # Adicionar colunas de score por categoria
        score_cols = [c for c in df.columns if c.startswith("score_")]
        main_cols.extend(score_cols)

        # Filtrar colunas disponíveis
        available_main_cols = [c for c in main_cols if c in df.columns]
        df_overall = df[available_main_cols].copy()
        df_overall = df_overall.sort_values("rank_overall")

        df_overall.to_parquet(OUTPUT_DIR / "consolidated_overral.parquet", index=False)
        size_mb = (OUTPUT_DIR / "consolidated_overral.parquet").stat().st_size / (1024 * 1024)
        print(f"  ✓ Exportado: {len(df_overall)} linhas, {len(df_overall.columns)} colunas ({size_mb:.2f} MB)")

        # 3. Exportar consolidated_weights.parquet
        print("\n[3/4] Exportando consolidated_weights.parquet...")
        df_weights.to_parquet(OUTPUT_DIR / "consolidated_weights.parquet", index=False)
        size_mb = (OUTPUT_DIR / "consolidated_weights.parquet").stat().st_size / (1024 * 1024)
        print(f"  ✓ Exportado: {len(df_weights)} indicadores ({size_mb:.2f} MB)")

        # 4. Exportar consolidated_context.parquet
        print("\n[4/4] Exportando consolidated_context.parquet...")

        context_cols = [
            "player_id",
            "competition_id",
            "unique_key",
            "source_file",
            "v_current",
            "player_season_most_recent_match",
        ]

        # Adicionar outras colunas de contexto disponíveis
        extra_context = [c for c in df.columns if any([
            "player_" in c.lower(),
            "team_" in c.lower(),
            "competition_" in c.lower(),
            "season" in c.lower(),
        ]) and not c.endswith("_norm") and c not in main_cols]

        context_cols.extend(extra_context)
        available_context_cols = list(set([c for c in context_cols if c in df.columns]))

        df_context = df[available_context_cols].copy()
        df_context.to_parquet(OUTPUT_DIR / "consolidated_context.parquet", index=False)
        size_mb = (OUTPUT_DIR / "consolidated_context.parquet").stat().st_size / (1024 * 1024)
        print(f"  ✓ Exportado: {len(df_context)} linhas, {len(df_context.columns)} colunas ({size_mb:.2f} MB)")

        # 5. Exportar consolidated_normalized.parquet
        print("\nExportando consolidated_normalized.parquet...")

        id_cols = ["player_id", "competition_id", "unique_key", "mapped_position", "v_current"]
        norm_cols = [c for c in df.columns if c.endswith("_norm")]

        normalized_cols = [c for c in id_cols if c in df.columns] + norm_cols
        df_normalized = df[normalized_cols].copy()

        df_normalized.to_parquet(OUTPUT_DIR / "consolidated_normalized.parquet", index=False)
        size_mb = (OUTPUT_DIR / "consolidated_normalized.parquet").stat().st_size / (1024 * 1024)
        print(f"  ✓ Exportado: {len(df_normalized)} linhas, {len(norm_cols)} indicadores normalizados ({size_mb:.2f} MB)")

        # Resumo final
        final_files = [
            "consolidated_overral.parquet",
            "consolidated_weights.parquet",
            "consolidated_context.parquet",
            "consolidated_normalized.parquet",
        ]

        print("\n" + "=" * 70)
        print("EXPORTAÇÃO CONCLUÍDA!")
        print("=" * 70)
        print("\nArquivos gerados em bases/outputs/:")
        for filename in final_files:
            filepath = OUTPUT_DIR / filename
            if filepath.exists():
                size_mb = filepath.stat().st_size / (1024 * 1024)
                print(f"  ✓ {filename} ({size_mb:.2f} MB)")

        print("=" * 70)
        print()

        return True

    except Exception as e:
        print(f"\n✗ ERRO na exportação: {str(e)}")
        raise


if __name__ == "__main__":
    run()
