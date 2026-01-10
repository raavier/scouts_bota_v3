"""
Script para executar notebooks da pipeline de dados

Uso:
    # Executar todos os notebooks
    python scripts/run_notebooks.py --all

    # Executar notebooks específicos
    python scripts/run_notebooks.py --notebooks 01 02 03

    # Executar a partir de um notebook específico
    python scripts/run_notebooks.py --from 03

    # Executar até um notebook específico
    python scripts/run_notebooks.py --to 04

    # Executar um range
    python scripts/run_notebooks.py --from 02 --to 05
"""

import argparse
import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Configurar encoding UTF-8 para stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent.parent
CODE_DIR = BASE_DIR / "code"

# Mapeamento de notebooks
NOTEBOOKS = {
    "01": "01_load_data.ipynb",
    "02": "02_prepare_positions.ipynb",
    "03": "03_consolidate_players.ipynb",
    "04": "04_normalize_indicators.ipynb",
    "05": "05_calculate_overall.ipynb",
    "06": "06_export.ipynb",
}

NOTEBOOK_NAMES = {
    "01": "Carregamento de Dados",
    "02": "Mapeamento de Posições",
    "03": "Consolidação de Jogadores",
    "04": "Normalização de Indicadores",
    "05": "Cálculo de Scores",
    "06": "Exportação Final",
}


def execute_notebook(notebook_path: Path, verbose: bool = True) -> Tuple[bool, str]:
    """
    Executa um notebook Jupyter

    Args:
        notebook_path: Caminho para o notebook
        verbose: Se True, imprime output detalhado

    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    try:
        # Carregar notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # Extrair células de código
        code_cells = [
            cell['source']
            for cell in notebook['cells']
            if cell['cell_type'] == 'code'
        ]

        # Juntar código
        code = '\n\n'.join([
            ''.join(source) if isinstance(source, list) else source
            for source in code_cells
        ])

        # Substituir display() por print() para melhor output em script
        code = code.replace('display(', 'print(')

        # Criar namespace para execução
        namespace = {'__name__': '__main__'}

        # Executar código
        if verbose:
            exec(code, namespace)
        else:
            # Suprimir output
            import io
            from contextlib import redirect_stdout, redirect_stderr
            f_out = io.StringIO()
            f_err = io.StringIO()
            with redirect_stdout(f_out), redirect_stderr(f_err):
                exec(code, namespace)

        return True, "Sucesso"

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        return False, error_msg


def get_notebooks_to_run(args) -> List[str]:
    """
    Determina quais notebooks executar baseado nos argumentos

    Returns:
        Lista de IDs de notebooks (ex: ["01", "02", "03"])
    """
    all_ids = sorted(NOTEBOOKS.keys())

    if args.all:
        return all_ids

    if args.notebooks:
        # Validar IDs fornecidos
        invalid = [nb for nb in args.notebooks if nb not in NOTEBOOKS]
        if invalid:
            print(f"ERRO: Notebooks inválidos: {', '.join(invalid)}")
            print(f"IDs válidos: {', '.join(all_ids)}")
            sys.exit(1)
        return sorted(args.notebooks)

    # Range: --from e/ou --to
    start_idx = 0
    end_idx = len(all_ids)

    if args.from_nb:
        if args.from_nb not in all_ids:
            print(f"ERRO: Notebook inicial inválido: {args.from_nb}")
            sys.exit(1)
        start_idx = all_ids.index(args.from_nb)

    if args.to_nb:
        if args.to_nb not in all_ids:
            print(f"ERRO: Notebook final inválido: {args.to_nb}")
            sys.exit(1)
        end_idx = all_ids.index(args.to_nb) + 1

    return all_ids[start_idx:end_idx]


def main():
    parser = argparse.ArgumentParser(
        description="Executa notebooks da pipeline de dados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Executar todos
  python scripts/run_notebooks.py --all

  # Executar notebooks específicos
  python scripts/run_notebooks.py --notebooks 01 02 03

  # Executar a partir do notebook 03
  python scripts/run_notebooks.py --from 03

  # Executar até o notebook 04
  python scripts/run_notebooks.py --to 04

  # Executar range (02 a 05)
  python scripts/run_notebooks.py --from 02 --to 05

  # Executar sem output detalhado
  python scripts/run_notebooks.py --all --quiet
        """
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Executar todos os notebooks'
    )

    parser.add_argument(
        '--notebooks',
        nargs='+',
        metavar='ID',
        help='IDs dos notebooks a executar (ex: 01 02 03)'
    )

    parser.add_argument(
        '--from',
        dest='from_nb',
        metavar='ID',
        help='Executar a partir deste notebook (inclusive)'
    )

    parser.add_argument(
        '--to',
        dest='to_nb',
        metavar='ID',
        help='Executar até este notebook (inclusive)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suprimir output detalhado dos notebooks'
    )

    parser.add_argument(
        '--continue-on-error',
        action='store_true',
        help='Continuar executando mesmo se houver erro'
    )

    args = parser.parse_args()

    # Validar argumentos
    if not any([args.all, args.notebooks, args.from_nb, args.to_nb]):
        parser.print_help()
        sys.exit(1)

    # Determinar notebooks a executar
    notebooks_to_run = get_notebooks_to_run(args)

    # Header
    print("=" * 70)
    print("EXECUÇÃO DE NOTEBOOKS - PIPELINE DE DADOS")
    print("=" * 70)
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Notebooks a executar: {len(notebooks_to_run)}\n")

    for nb_id in notebooks_to_run:
        print(f"  {nb_id}. {NOTEBOOK_NAMES[nb_id]}")

    print()

    # Executar notebooks
    results = []

    for i, nb_id in enumerate(notebooks_to_run, 1):
        nb_name = NOTEBOOKS[nb_id]
        nb_path = CODE_DIR / nb_name

        print(f"[{i}/{len(notebooks_to_run)}] Executando: {nb_id} - {NOTEBOOK_NAMES[nb_id]}")
        print(f"    Arquivo: {nb_name}")

        if not nb_path.exists():
            print(f"    ✗ ERRO: Arquivo não encontrado!")
            results.append((nb_id, False, "Arquivo não encontrado"))
            if not args.continue_on_error:
                break
            continue

        # Executar
        success, message = execute_notebook(nb_path, verbose=not args.quiet)
        results.append((nb_id, success, message))

        if success:
            print(f"    ✓ Concluído com sucesso")
        else:
            print(f"    ✗ ERRO: {message}")
            if not args.continue_on_error:
                break

        print()

    # Resumo
    print("=" * 70)
    print("RESUMO DA EXECUÇÃO")
    print("=" * 70)

    successful = sum(1 for _, success, _ in results if success)
    failed = sum(1 for _, success, _ in results if not success)

    for nb_id, success, message in results:
        status = "✓" if success else "✗"
        name = NOTEBOOK_NAMES[nb_id]
        print(f"  {status} {nb_id}. {name}")
        if not success:
            print(f"      Erro: {message}")

    print()
    print(f"Total executados: {len(results)}")
    print(f"Sucesso: {successful}")
    print(f"Falhas: {failed}")
    print(f"Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Status final
    if successful == len(notebooks_to_run):
        print("\n✓ TODOS OS NOTEBOOKS EXECUTADOS COM SUCESSO!")

        # Se executou todos, mostrar arquivos gerados
        if notebooks_to_run == sorted(NOTEBOOKS.keys()):
            print("\nArquivos gerados em bases/outputs/:")
            print("  - consolidated_overral.parquet")
            print("  - consolidated_weights.parquet")
            print("  - consolidated_context.parquet")
            print("  - consolidated_normalized.parquet")

        return 0
    else:
        print("\n✗ EXECUÇÃO INCOMPLETA - Verifique os erros acima")
        return 1


if __name__ == "__main__":
    sys.exit(main())
