"""
Módulo 06 - Exportação Final

Este módulo realiza:
1. Seleção de colunas finais
2. Exportação para parquet:
   - consolidated_overall.parquet (principais dados com scores)
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

        # 2. Exportar consolidated_overall.parquet
        print("\n[2/4] Exportando consolidated_overall.parquet...")

        main_cols = [
            "unique_key",
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
            # Informações pessoais
            "birth_date",
            "player_weight",
            "player_height",
            "country_id",
            # Informações de disponibilidade
            "player_season_minutes",
            "player_season_appearances",
            "player_season_starting_appearances",
            "player_season_average_minutes",
            "player_season_most_recent_match",
            "player_season_90s_played",
            "player_season_360_minutes",
        ]

        # Adicionar colunas de score por categoria (CLASSIFICACAO)
        score_cols = [c for c in df.columns if c.startswith("score_") and not c.startswith("sub_score_")]
        main_cols.extend(score_cols)

        # Adicionar colunas de sub_score por subcategoria (SUBCLASSIFICACAO)
        sub_score_cols = [c for c in df.columns if c.startswith("sub_score_")]
        main_cols.extend(sub_score_cols)

        # Filtrar colunas disponíveis
        available_main_cols = [c for c in main_cols if c in df.columns]
        df_overall = df[available_main_cols].copy()

        # Calcular idade a partir da birth_date
        if "birth_date" in df_overall.columns:
            from datetime import datetime
            current_date = datetime.now()
            df_overall["player_age"] = df_overall["birth_date"].apply(
                lambda x: (current_date - pd.to_datetime(x)).days // 365 if pd.notna(x) else None
            )

        # Calcular coluna de cor baseada nos máximos por competition_id + position_group
        print("  Calculando coluna de cores...")

        # Mapear nomes das colunas de score para as categorias corretas
        score_mapping = {}
        for col in df_overall.columns:
            if col.startswith("score_"):
                category = col.replace("score_", "").lower()
                score_mapping[category] = col

        # Calcular máximos por grupo (competition_id + position_group)
        grouped = df_overall.groupby(["competition_id", "position_group"])

        # Definir ordem de prioridade para as cores
        color_priority = [
            ("overall_score", "#E6E6E6"),
            (score_mapping.get("offensive", None), "#E2EFDA"),
            (score_mapping.get("dgp", None), "#C7B8E7"),
            (score_mapping.get("pass", None), "#F0E199"),
            (score_mapping.get("defensive", None), "#EFB5B9"),
        ]

        # Filtrar apenas as colunas que existem
        color_priority = [(col, color) for col, color in color_priority if col and col in df_overall.columns]

        def get_color(row):
            """Determina a cor baseada no score máximo do grupo"""
            # Se position_group é None, retornar branco
            if pd.isna(row["position_group"]):
                return "#FFFFFF"

            group_key = (row["competition_id"], row["position_group"])

            # Verificar se o grupo existe
            try:
                group_data = grouped.get_group(group_key)
            except KeyError:
                return "#FFFFFF"

            # Verificar cada score na ordem de prioridade
            for score_col, color in color_priority:
                if pd.notna(row[score_col]):
                    max_score = group_data[score_col].max()
                    if row[score_col] == max_score:
                        return color

            return "#FFFFFF"  # cor padrão se nenhuma condição for atendida

        df_overall["highlight_color"] = df_overall.apply(get_color, axis=1)
        print(f"  ✓ Coluna highlight_color adicionada")

        # Calcular coluna com todas as categorias máximas
        print("  Calculando categorias máximas...")

        # Mapeamento de colunas para nomes amigáveis
        category_names = {
            "overall_score": "Overall",
            score_mapping.get("offensive", None): "Offensive",
            score_mapping.get("dgp", None): "DGP",
            score_mapping.get("pass", None): "Pass",
            score_mapping.get("defensive", None): "Defensive",
        }

        # Filtrar apenas as colunas que existem
        category_names = {col: name for col, name in category_names.items() if col and col in df_overall.columns}

        def get_max_categories(row):
            """Retorna todas as categorias em que o jogador é máximo no grupo"""
            # Se position_group é None, retornar vazio
            if pd.isna(row["position_group"]):
                return ""

            group_key = (row["competition_id"], row["position_group"])

            # Verificar se o grupo existe
            try:
                group_data = grouped.get_group(group_key)
            except KeyError:
                return ""

            max_categories = []

            # Verificar todas as categorias
            for score_col, category_name in category_names.items():
                if pd.notna(row[score_col]):
                    max_score = group_data[score_col].max()
                    if row[score_col] == max_score:
                        max_categories.append(category_name)

            return ", ".join(max_categories) if max_categories else ""

        df_overall["max_categories"] = df_overall.apply(get_max_categories, axis=1)
        print(f"  ✓ Coluna max_categories adicionada")

        df_overall = df_overall.sort_values("rank_overall")

        df_overall.to_parquet(OUTPUT_DIR / "consolidated_overall.parquet", index=False)
        size_mb = (OUTPUT_DIR / "consolidated_overall.parquet").stat().st_size / (1024 * 1024)
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
            "consolidated_overall.parquet",
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
