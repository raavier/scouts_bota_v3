"""
Script de Build - Python Embeddable

Este script:
1. Baixa Python 3.11 Embeddable para Windows
2. Instala dependências em libs/
3. Configura sys.path
4. Cria estrutura final para distribuição

Resultado: dist/BotafogoScouts/ pronto para uso
"""

import os
import sys
import urllib.request
import zipfile
import shutil
import subprocess
from pathlib import Path

# Configurações
PYTHON_VERSION = "3.11.9"
PYTHON_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"
BASE_DIR = Path(__file__).parent
DIST_DIR = BASE_DIR / "dist" / "BotafogoScouts"
PYTHON_EMBED_DIR = DIST_DIR / "python-embed"
LIBS_DIR = DIST_DIR / "libs"


def download_python_embeddable():
    """Baixa Python Embeddable"""
    print("\n[1/6] Baixando Python Embeddable...")
    print(f"  URL: {PYTHON_URL}")

    zip_path = BASE_DIR / "python-embed.zip"

    if zip_path.exists():
        print("  [OK] Arquivo ja existe, pulando download")
    else:
        print("  Baixando... (pode levar alguns minutos)")
        urllib.request.urlretrieve(PYTHON_URL, zip_path)
        print("  [OK] Download concluido")

    return zip_path


def extract_python_embeddable(zip_path):
    """Extrai Python Embeddable"""
    print("\n[2/6] Extraindo Python Embeddable...")

    # Limpar pasta anterior
    if PYTHON_EMBED_DIR.exists():
        shutil.rmtree(PYTHON_EMBED_DIR)

    PYTHON_EMBED_DIR.mkdir(parents=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(PYTHON_EMBED_DIR)

    print(f"  [OK] Extraído para: {PYTHON_EMBED_DIR}")


def configure_sys_path():
    """Configura python311._pth para incluir libs/"""
    print("\n[3/6] Configurando sys.path...")

    # Python 3.11 -> python311._pth
    pth_file = PYTHON_EMBED_DIR / "python311._pth"

    if not pth_file.exists():
        print(f"  [ERRO] Arquivo nao encontrado: {pth_file}")
        return

    # Ler conteúdo atual
    with open(pth_file, 'r') as f:
        content = f.read()

    # Remover linha "import site" se existir (descomentá-la)
    content = content.replace('#import site', 'import site')
    if 'import site' not in content:
        content += '\nimport site\n'

    # Adicionar libs/ ao path
    content += '\n../libs\n'
    content += '..\n'  # Pasta raiz (BotafogoScouts/)

    # Escrever de volta
    with open(pth_file, 'w') as f:
        f.write(content)

    print("  [OK] sys.path configurado")


def install_get_pip():
    """Instala get-pip.py no Python Embeddable"""
    print("\n[4/6] Instalando pip...")

    # Baixar get-pip.py
    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_path = PYTHON_EMBED_DIR / "get-pip.py"

    print("  Baixando get-pip.py...")
    urllib.request.urlretrieve(get_pip_url, get_pip_path)

    # Executar get-pip.py
    python_exe = PYTHON_EMBED_DIR / "python.exe"
    cmd = [
        str(python_exe),
        str(get_pip_path),
        "--no-warn-script-location",
        f"--target={LIBS_DIR}"
    ]

    print("  Instalando pip...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  [ERRO] Erro ao instalar pip:")
        print(result.stderr)
        return False

    print("  [OK] pip instalado")
    return True


def install_dependencies():
    """Instala dependências do projeto"""
    print("\n[5/6] Instalando dependências...")

    python_exe = PYTHON_EMBED_DIR / "python.exe"
    requirements = BASE_DIR / "requirements.txt"

    if not requirements.exists():
        print("  [ERRO] requirements.txt não encontrado")
        return False

    # Instalar dependências
    cmd = [
        str(python_exe),
        "-m", "pip",
        "install",
        "-r", str(requirements),
        "--no-warn-script-location",
        f"--target={LIBS_DIR}"
    ]

    print("  Instalando pandas, openpyxl, pyarrow, pyyaml...")
    print("  (pode levar alguns minutos)")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  [ERRO] Erro ao instalar dependências:")
        print(result.stderr)
        return False

    print("  [OK] Dependências instaladas")
    return True


def copy_project_files():
    """Copia arquivos do projeto para dist/"""
    print("\n[6/6] Copiando arquivos do projeto...")

    # Arquivos e pastas a copiar
    items_to_copy = [
        "main.py",
        "pipeline/",
        "bases/",
        "config/",
        "ProcessarScouts.bat",
        "LEIA-ME.txt",
    ]

    for item in items_to_copy:
        src = BASE_DIR / item
        dst = DIST_DIR / item

        if not src.exists():
            print(f"  [AVISO] Item não encontrado: {item}")
            continue

        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  [OK] Pasta copiada: {item}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  [OK] Arquivo copiado: {item}")

    print("\n  [OK] Arquivos copiados")


def cleanup():
    """Remove arquivos temporários"""
    print("\nLimpando arquivos temporários...")

    temp_files = [
        BASE_DIR / "python-embed.zip",
        PYTHON_EMBED_DIR / "get-pip.py",
    ]

    for file in temp_files:
        if file.exists():
            file.unlink()
            print(f"  [OK] Removido: {file.name}")


def main():
    print("=" * 70)
    print("BUILD SCRIPT - PYTHON EMBEDDABLE")
    print("=" * 70)

    try:
        # Baixar Python
        zip_path = download_python_embeddable()

        # Extrair
        extract_python_embeddable(zip_path)

        # Configurar sys.path
        configure_sys_path()

        # Instalar pip
        if not install_get_pip():
            return 1

        # Instalar dependências
        if not install_dependencies():
            return 1

        # Copiar arquivos do projeto
        copy_project_files()

        # Limpar temporários
        cleanup()

        # Sucesso!
        print("\n" + "=" * 70)
        print("[OK] BUILD CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print(f"\nPasta de distribuição criada em:")
        print(f"  {DIST_DIR}")
        print("\nPara testar:")
        print(f"  cd {DIST_DIR}")
        print(f"  ProcessarScouts.bat")
        print("\nPara distribuir:")
        print(f"  Comprima a pasta '{DIST_DIR.name}' em um arquivo .zip")
        print("=" * 70)

        return 0

    except Exception as e:
        print(f"\n[ERRO] ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
