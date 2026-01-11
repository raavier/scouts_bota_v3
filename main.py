"""
Processador de Scouts - Botafogo
Entry point principal para o executável

Este script executa toda a pipeline de processamento:
1. Carregamento de dados
2. Mapeamento de posições
3. Consolidação de jogadores
4. Normalização de indicadores
5. Cálculo de scores
6. Exportação final
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
import io

# Configurar encoding UTF-8 para stdout (importante no Windows)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def setup_logging():
    """Configura logging para arquivo log.txt"""
    log_file = Path(__file__).parent / "log.txt"

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8', mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger(__name__)


def validate_directories():
    """Valida a existência das pastas necessárias"""
    base_dir = Path(__file__).parent

    required_dirs = [
        base_dir / "bases" / "inputs" / "scouts_base",
        base_dir / "bases" / "inputs" / "business",
        base_dir / "config",
    ]

    missing = []
    for dir_path in required_dirs:
        if not dir_path.exists():
            missing.append(str(dir_path))

    if missing:
        print("\n✗ ERRO: Pastas necessárias não encontradas:\n")
        for path in missing:
            print(f"  - {path}")
        print("\nVerifique a estrutura de arquivos e tente novamente.")
        return False

    # Verificar se há arquivos Excel
    scouts_dir = base_dir / "bases" / "inputs" / "scouts_base"
    xlsx_files = list(scouts_dir.glob("*.xlsx"))

    if not xlsx_files:
        print(f"\n✗ ERRO: Nenhum arquivo .xlsx encontrado em:\n  {scouts_dir}")
        print("\nAdicione os arquivos de scouts e tente novamente.")
        return False

    # Verificar base_peso.xlsx
    weights_file = base_dir / "bases" / "inputs" / "business" / "base_peso.xlsx"
    if not weights_file.exists():
        print(f"\n✗ ERRO: Arquivo base_peso.xlsx não encontrado em:\n  {weights_file}")
        return False

    return True


def main():
    """Função principal"""
    logger = setup_logging()

    print("=" * 70)
    print("PROCESSADOR DE SCOUTS - BOTAFOGO")
    print("=" * 70)
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        # Validar estrutura de pastas
        if not validate_directories():
            return 1

        # Importar módulos da pipeline
        from pipeline import (
            load_data,
            prepare_positions,
            consolidate_players,
            normalize_indicators,
            calculate_overall,
            export
        )

        # Definir etapas
        steps = [
            ("Carregamento de Dados", load_data.run),
            ("Mapeamento de Posições", prepare_positions.run),
            ("Consolidação de Jogadores", consolidate_players.run),
            ("Normalização de Indicadores", normalize_indicators.run),
            ("Cálculo de Scores", calculate_overall.run),
            ("Exportação Final", export.run),
        ]

        # Executar pipeline
        for name, func in steps:
            try:
                result = func()
                if not result:
                    print(f"\n✗ ERRO: Etapa '{name}' retornou False")
                    return 1
            except Exception as e:
                logger.error(f"Erro na etapa '{name}': {str(e)}", exc_info=True)
                print(f"\n✗ ERRO na etapa '{name}':")
                print(f"  {type(e).__name__}: {str(e)}")
                print("\nVerifique o arquivo log.txt para mais detalhes.")
                return 1

        # Sucesso!
        print("=" * 70)
        print("✓ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print(f"\nArquivos gerados em: bases/outputs/")
        print("  - consolidated_overall.parquet")
        print("  - consolidated_weights.parquet")
        print("  - consolidated_context.parquet")
        print("  - consolidated_normalized.parquet")
        print()
        print(f"Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        return 0

    except KeyboardInterrupt:
        print("\n\n✗ Processamento interrompido pelo usuário")
        return 1
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        print(f"\n✗ ERRO INESPERADO:")
        print(f"  {type(e).__name__}: {str(e)}")
        print("\nVerifique o arquivo log.txt para mais detalhes.")
        return 1


if __name__ == "__main__":
    exit_code = main()

    # Pausar para ver resultado (útil quando executado via .bat)
    print("\nPressione Enter para sair...")
    try:
        input()
    except:
        pass

    sys.exit(exit_code)
