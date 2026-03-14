"""
Módulo 01 - Carregamento de Dados

Este módulo realiza:
1. Carregamento das configurações YAML
2. Carregamento de todos os arquivos de scouts
3. Carregamento da tabela de pesos
4. Validação da estrutura dos dados
5. Salvamento de arquivos temporários para próximas etapas

Converte:01_load_data.ipynb → load_data.py
"""

import pandas as pd
import yaml
from pathlib import Path
from typing import Tuple

from . import get_base_dir


def run() -> bool:
    """
    Executa o carregamento de dados.

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        print("=" * 70)
        print("ETAPA 1/6: CARREGAMENTO DE DADOS")
        print("=" * 70)
        print()

        # Configurar diretórios
        BASE_DIR = get_base_dir()
        CONFIG_DIR = BASE_DIR / "config"
        INPUTS_DIR = BASE_DIR / "bases" / "inputs"
        OUTPUT_DIR = BASE_DIR / "bases" / "outputs"

        # Criar pasta de outputs se não existir
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # 1. Carregar Configurações
        print("[1/5] Carregando configurações...")
        with open(CONFIG_DIR / "config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        with open(CONFIG_DIR / "positions.yaml", "r", encoding="utf-8") as f:
            positions_config = yaml.safe_load(f)

        print(f"  ✓ Configurações carregadas: {config['app']['name']} v{config['app']['version']}")

        # 2. Carregar Arquivos de Scouts
        print("\n[2/5] Carregando arquivos de scouts...")
        SCOUTS_DIR = INPUTS_DIR / "scouts_base"

        scout_files = list(SCOUTS_DIR.glob("*.xlsx"))
        if not scout_files:
            raise FileNotFoundError(
                f"Nenhum arquivo .xlsx encontrado em: {SCOUTS_DIR}\n"
                "Por favor, adicione arquivos de scouts na pasta inputs/scouts_base/"
            )

        print(f"  ✓ Arquivos encontrados: {len(scout_files)}")

        dfs_scouts = []
        for file_path in scout_files:
            print(f"    - {file_path.name}...", end=" ")
            df = pd.read_excel(file_path)
            df["source_file"] = file_path.name
            dfs_scouts.append(df)
            print(f"{len(df)} jogadores")

        df_scouts = pd.concat(dfs_scouts, ignore_index=True)
        print(f"  ✓ Total: {len(df_scouts)} jogadores carregados")

        # 3. Carregar Mapeamento de Nacionalidades
        print("\n[3/6] Carregando mapeamento de nacionalidades...")
        NATIONALITY_FILE = INPUTS_DIR / "business" / "nacionalidades.xlsx"

        if NATIONALITY_FILE.exists():
            df_nationality = pd.read_excel(NATIONALITY_FILE)

            # Detectar country_ids novos que não estão no arquivo
            existing_ids = set(df_nationality['country_id'].unique())
            all_ids = set(df_scouts['country_id'].dropna().unique())
            new_ids = all_ids - existing_ids

            # Se há novos country_ids, adicionar ao arquivo com "PENDENTE"
            if new_ids:
                print(f"  ⚠ Novos country_ids detectados: {sorted(new_ids)}")
                new_rows = []
                for cid in new_ids:
                    # Pegar um jogador de exemplo para esse country_id
                    sample = df_scouts[df_scouts['country_id'] == cid].iloc[0]
                    new_rows.append({
                        'country_id': int(cid),
                        'nationality': 'PENDENTE',
                        'player_example': sample.get('player_name', ''),
                        'team_example': sample.get('team_name', '')
                    })

                # Adicionar novas linhas ao DataFrame
                df_new = pd.DataFrame(new_rows)
                df_nationality = pd.concat([df_nationality, df_new], ignore_index=True)
                df_nationality = df_nationality.sort_values('country_id')

                # Salvar arquivo atualizado
                df_nationality.to_excel(NATIONALITY_FILE, index=False)
                print(f"  ✓ Arquivo nacionalidades.xlsx atualizado com {len(new_ids)} novos códigos")

            # Fazer merge com scouts para adicionar coluna nationality
            df_scouts = df_scouts.merge(
                df_nationality[['country_id', 'nationality']],
                on='country_id',
                how='left'
            )

            # Contar pendências (nationality = "PENDENTE" ou vazio)
            pending_mask = (df_scouts['nationality'] == 'PENDENTE') | (df_scouts['nationality'].isna())
            pending_count = pending_mask.sum()
            pending_ids = df_scouts[pending_mask]['country_id'].unique()

            if pending_count > 0:
                print(f"  ⚠ {pending_count} jogadores com nacionalidade PENDENTE (country_ids: {sorted(pending_ids)})")
                # Salvar arquivo de controle para aviso no final
                with open(OUTPUT_DIR / "_pending_nationalities.txt", "w") as f:
                    f.write(f"{len(pending_ids)}")
            else:
                # Remover arquivo de controle se não há pendências
                pending_file = OUTPUT_DIR / "_pending_nationalities.txt"
                if pending_file.exists():
                    pending_file.unlink()

            mapped_count = (~pending_mask).sum()
            print(f"  ✓ Nacionalidades mapeadas: {mapped_count} de {len(df_scouts)} jogadores")
        else:
            print(f"  ⚠ Arquivo de nacionalidades não encontrado: {NATIONALITY_FILE}")
            df_scouts['nationality'] = None

        # 4. Carregar Tabela de Pesos
        print("\n[4/6] Carregando tabela de pesos...")
        WEIGHTS_FILE = INPUTS_DIR / "business" / "base_peso.xlsx"

        if not WEIGHTS_FILE.exists():
            raise FileNotFoundError(
                f"Arquivo de pesos não encontrado: {WEIGHTS_FILE}\n"
                "Certifique-se de que o arquivo base_peso.xlsx está em inputs/business/"
            )

        df_weights = pd.read_excel(WEIGHTS_FILE)
        df_weights_active = df_weights[df_weights["CONSIDERAR?"] == "SIM"].copy()

        print(f"  ✓ Tabela de pesos carregada: {df_weights.shape}")
        print(f"  ✓ Indicadores ativos: {len(df_weights_active)}")
        print(f"  ✓ Indicadores ignorados: {len(df_weights) - len(df_weights_active)}")

        # 4. Validação dos Dados
        print("\n[5/6] Validando dados...")

        # Verificar indicadores
        indicadores_pesos = set(df_weights_active["INDICADOR"].str.strip())
        colunas_scouts = set(df_scouts.columns)
        indicadores_match = indicadores_pesos.intersection(colunas_scouts)
        indicadores_missing = indicadores_pesos - colunas_scouts

        print(f"  ✓ Indicadores na tabela de pesos: {len(indicadores_pesos)}")
        print(f"  ✓ Indicadores encontrados nos scouts: {len(indicadores_match)}")

        if indicadores_missing:
            print(f"  ⚠ Indicadores faltantes: {len(indicadores_missing)}")
            # Não é erro crítico, apenas aviso

        # 5. Salvar Dados Carregados
        print("\n[6/6] Salvando dados intermediários...")

        # Converter colunas string (mantém NaN como NaN)
        string_cols = [
            'season_name', 'competition_name', 'team_name', 'player_name',
            'player_first_name', 'player_last_name', 'player_known_name',
            'primary_position', 'source_file', 'nationality'
        ]

        for col in string_cols:
            if col in df_scouts.columns:
                mask = df_scouts[col].notna()
                df_scouts.loc[mask, col] = df_scouts.loc[mask, col].astype(str)

        # Salvar scouts
        df_scouts.to_parquet(OUTPUT_DIR / "_temp_scouts_raw.parquet", index=False)

        # Converter colunas string da tabela de pesos
        weights_string_cols = [
            'INDICADOR', 'CLASSIFICACAO RANKING', 'SUBCLASSIFICACAO RANKING',
            'CONSIDERAR?', 'ESPECIAL?', 'Melhor para', 'tipo_agreg',
            'Explicação indicador'
        ]

        for col in weights_string_cols:
            if col in df_weights_active.columns:
                mask = df_weights_active[col].notna()
                df_weights_active.loc[mask, col] = df_weights_active.loc[mask, col].astype(str)

        # Salvar pesos
        df_weights_active.to_parquet(OUTPUT_DIR / "_temp_weights_active.parquet", index=False)

        print(f"  ✓ Scouts salvos: _temp_scouts_raw.parquet")
        print(f"  ✓ Pesos salvos: _temp_weights_active.parquet")

        # Resumo final
        print("\n" + "=" * 70)
        print("RESUMO")
        print("=" * 70)
        print(f"Total de jogadores: {len(df_scouts)}")
        print(f"Total de colunas: {len(df_scouts.columns)}")
        print(f"Arquivos processados: {len(scout_files)}")
        print(f"Indicadores ativos: {len(df_weights_active)}")
        print("=" * 70)
        print()

        return True

    except Exception as e:
        print(f"\n✗ ERRO no carregamento de dados: {str(e)}")
        raise


if __name__ == "__main__":
    # Permite testar módulo standalone
    run()
