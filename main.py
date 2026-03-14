"""
Processador de Scouts - Botafogo
Entry point principal para o executável

Este script executa toda a pipeline de processamento:
1. Carregamento de dados
2. Mapeamento de posições
3. Consolidação de jogadores
4. Normalização de indicadores
5. Cálculo de scores
6. Cálculo de tendências
7. Exportação final
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
import io
import warnings

# Suprimir warnings que poluem a saída
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*openpyxl.*")
warnings.filterwarnings("ignore", message=".*Workbook.*")
warnings.filterwarnings("ignore", message=".*fragmented.*")
warnings.filterwarnings("ignore", message=".*PerformanceWarning.*")

# Configurar encoding UTF-8 para stdout (importante no Windows)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def print_progress_bar(current: int, total: int, step_name: str, bar_length: int = 40):
    """
    Exibe uma barra de progresso visual no console.

    Args:
        current: Etapa atual (1-indexed)
        total: Total de etapas
        step_name: Nome da etapa atual
        bar_length: Comprimento da barra em caracteres
    """
    percent = current / total
    filled_length = int(bar_length * percent)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    percent_str = f"{percent * 100:.0f}%"

    print(f"\n┌{'─' * (bar_length + 10)}┐")
    print(f"│  [{bar}] {percent_str:>4}  │")
    print(f"└{'─' * (bar_length + 10)}┘")
    print(f"  Etapa {current}/{total}: {step_name}")
    print()


def setup_logging():
    """Configura logging para arquivo log.txt (somente arquivo, sem stdout)"""
    log_file = Path(__file__).parent / "log.txt"

    # Configurar logging apenas para arquivo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8', mode='w'),
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
            calculate_trends,
            export
        )

        # Definir etapas
        steps = [
            ("Carregamento de Dados", load_data.run),
            ("Mapeamento de Posições", prepare_positions.run),
            ("Consolidação de Jogadores", consolidate_players.run),
            ("Normalização de Indicadores", normalize_indicators.run),
            ("Cálculo de Scores", calculate_overall.run),
            ("Cálculo de Tendências", calculate_trends.run),
            ("Exportação Final", export.run),
        ]

        # Executar pipeline
        total_steps = len(steps)
        for step_num, (name, func) in enumerate(steps, 1):
            try:
                print_progress_bar(step_num, total_steps, name)
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

        # Verificar se há nacionalidades pendentes
        base_dir = Path(__file__).parent
        pending_file = base_dir / "bases" / "outputs" / "_pending_nationalities.txt"
        if pending_file.exists():
            with open(pending_file, "r") as f:
                pending_count = int(f.read().strip())
            print()
            print("!" * 70)
            print("⚠ ATENÇÃO: NACIONALIDADES PENDENTES")
            print("!" * 70)
            print(f"  Existem {pending_count} código(s) de país sem nacionalidade definida.")
            print("  Edite o arquivo: bases/inputs/business/nacionalidades.xlsx")
            print("  Procure por linhas com nationality = 'PENDENTE' e preencha.")
            print("!" * 70)

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
