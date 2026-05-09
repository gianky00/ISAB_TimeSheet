@echo off
title SyncroJob
cd /d "%~dp0"
cd ..

set PYTHONUTF8=1

:: Verifica ambiente virtuale
if not exist ".venv" (
    echo [INFO] Creazione ambiente virtuale...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -e .
) else (
    call .venv\Scripts\activate.bat
)

echo [INFO] Avvio SyncroJob...
python main.py

if errorlevel 1 (
    echo.
    echo [ERRORE] Crash rilevato.
    pause
)
deactivate
