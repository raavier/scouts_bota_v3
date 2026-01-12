@echo off
REM ============================================================================
REM Script de execução do Streamlit App - Scouts Bota
REM ============================================================================

echo ========================================
echo   Scouts Bota - Gerenciador de Pesos
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.11 ou superior.
    pause
    exit /b 1
)

echo [1/3] Verificando dependencias...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Streamlit nao encontrado. Instalando dependencias...
    echo.
    pip install -r requirements_streamlit.txt
    if errorlevel 1 (
        echo.
        echo ERRO: Falha ao instalar dependencias!
        pause
        exit /b 1
    )
)

echo [2/3] Iniciando aplicacao Streamlit...
echo.
echo ========================================
echo   Abrindo navegador...
echo   URL: http://localhost:8501
echo ========================================
echo.
echo Para parar a aplicacao: pressione Ctrl+C
echo.

REM Executar Streamlit
streamlit run streamlit_app/app.py

pause
