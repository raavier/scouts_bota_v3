"""
Módulo 02 - Preparação e Mapeamento de Posições

Este módulo realiza:
1. Carregamento dos dados da etapa anterior
2. Preenchimento de primary_position nulo
3. Aplicação do mapeamento de posições
4. Extração de position, position_group e position_sub_group
5. Validação das posições mapeadas

Converte: 02_prepare_positions.ipynb → prepare_positions.py
"""

import pandas as pd
import yaml
from pathlib import Path
from typing import Dict, Any

from . import get_base_dir


def map_position(original_position: str, position_mapping: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Mapeia uma posição original para a posição padronizada.

    Args:
        original_position: Posição original do jogador
        position_mapping: Dicionário de mapeamento de posições

    Returns:
        Dict com keys: position, position_group, position_sub_group
    """
    if pd.isna(original_position) or original_position == "":
        return {"position": None, "position_group": None, "position_sub_group": None}

    # Limpar espaços
    original_position = str(original_position).strip()

    # Buscar no mapeamento
    if original_position in position_mapping:
        return position_mapping[original_position]

    # Tentar case-insensitive
    for key, value in position_mapping.items():
        if key.lower() == original_position.lower():
            return value

    # Não encontrado
    return {"position": None, "position_group": None, "position_sub_group": None}


def run() -> bool:
    """
    Executa o mapeamento de posições.

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        print("=" * 70)
        print("ETAPA 2/6: MAPEAMENTO DE POSIÇÕES")
        print("=" * 70)
        print()

        # Configurar diretórios
        BASE_DIR = get_base_dir()
        CONFIG_DIR = BASE_DIR / "config"
        OUTPUT_DIR = BASE_DIR / "bases" / "outputs"

        # 1. Carregar Dados
        print("[1/4] Carregando dados...")
        df_scouts = pd.read_parquet(OUTPUT_DIR / "_temp_scouts_raw.parquet")
        print(f"  ✓ Scouts carregados: {len(df_scouts)} jogadores")

        with open(CONFIG_DIR / "positions.yaml", "r", encoding="utf-8") as f:
            positions_config = yaml.safe_load(f)

        position_mapping = positions_config["position_mapping"]
        print(f"  ✓ Mapeamentos de posição: {len(position_mapping)}")

        # Preencher primary_position nulo com texto padrão
        df_scouts['primary_position'] = df_scouts['primary_position'].fillna('Sem posição definida')

        # 2. Aplicar Mapeamento de Posições
        print("\n[2/4] Aplicando mapeamento de posições...")
        mapped = df_scouts["primary_position"].apply(lambda pos: map_position(pos, position_mapping))

        # Extrair as três colunas
        df_scouts["mapped_position"] = mapped.apply(lambda x: x["position"])
        df_scouts["position_group"] = mapped.apply(lambda x: x["position_group"])
        df_scouts["position_sub_group"] = mapped.apply(lambda x: x["position_sub_group"])

        print(f"  ✓ Mapeamento aplicado com sucesso")

        # 3. Validação das Posições
        print("\n[3/4] Validando posições...")

        # Posições esperadas
        EXPECTED_POSITIONS = {"GK", "CB", "RCB", "LCB", "RB", "LB", "DM", "CM", "AM", "LW", "RW", "CF"}
        mapped_positions = set(df_scouts["mapped_position"].dropna().unique())

        # Verificar se todas estão no conjunto esperado
        invalid_positions = mapped_positions - EXPECTED_POSITIONS
        if invalid_positions:
            print(f"  ⚠ POSIÇÕES INVÁLIDAS: {invalid_positions}")
        else:
            print(f"  ✓ Todas as posições são válidas")

        # Verificar posições não mapeadas
        unmapped = df_scouts[df_scouts["mapped_position"].isna()]
        if len(unmapped) > 0:
            print(f"  ⚠ Jogadores sem posição mapeada: {len(unmapped)}")
            # Não é erro crítico - geralmente jogadores com baixa minutagem
        else:
            print(f"  ✓ Todos os jogadores têm posição mapeada")

        # Distribuição de posições
        position_counts = df_scouts["mapped_position"].value_counts(dropna=False)
        print(f"\n  Distribuição de posições:")
        for pos, count in position_counts.head(5).items():
            print(f"    {pos}: {count}")

        # 4. Salvar Dados Processados
        print("\n[4/4] Salvando dados processados...")
        df_scouts.to_parquet(OUTPUT_DIR / "_temp_scouts_positions.parquet", index=False)
        print(f"  ✓ Dados salvos: _temp_scouts_positions.parquet")

        # Resumo final
        print("\n" + "=" * 70)
        print("RESUMO")
        print("=" * 70)
        print(f"Total de jogadores: {len(df_scouts)}")
        print(f"Jogadores com posição mapeada: {df_scouts['mapped_position'].notna().sum()}")
        print(f"Posições mapeadas encontradas: {len(mapped_positions)}")
        print("=" * 70)
        print()

        return True

    except Exception as e:
        print(f"\n✗ ERRO no mapeamento de posições: {str(e)}")
        raise


if __name__ == "__main__":
    # Permite testar módulo standalone
    run()
