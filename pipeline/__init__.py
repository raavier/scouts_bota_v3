"""
Pipeline de processamento de dados de scouts

Este pacote contém os módulos que substituem os notebooks Jupyter originais,
permitindo empacotamento como executável standalone.
"""

from pathlib import Path
import sys


def get_base_dir() -> Path:
    """
    Detecta o diretório base do projeto automaticamente.

    Funciona tanto quando rodando como script Python normal quanto quando
    empacotado como executável (PyInstaller ou Python Embeddable).

    Returns:
        Path: Diretório base do projeto

    Examples:
        >>> base = get_base_dir()
        >>> config_dir = base / "config"
        >>> inputs_dir = base / "bases" / "inputs"
    """
    if getattr(sys, 'frozen', False):
        # Rodando como executável empacotado (PyInstaller)
        # sys.executable aponta para o .exe
        return Path(sys.executable).parent
    else:
        # Rodando como script Python normal
        # __file__ é pipeline/__init__.py
        # parent = pipeline/, parent.parent = v3/
        return Path(__file__).parent.parent


__all__ = ['get_base_dir']
