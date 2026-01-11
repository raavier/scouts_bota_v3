@echo off
chcp 65001 >nul
cls

echo ==========================================
echo PROCESSADOR DE SCOUTS - BOTAFOGO
echo ==========================================
echo.

REM Verificar se Python Embeddable existe
if exist "python-embed\python.exe" (
    echo Usando Python Embeddable...
    python-embed\python.exe main.py
) else if exist "python.exe" (
    echo Usando Python local...
    python.exe main.py
) else (
    echo Python não encontrado!
    echo.
    echo Instale o Python ou execute build_embeddable.py primeiro.
    echo.
    pause
    exit /b 1
)

echo.
pause
