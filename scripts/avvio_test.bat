@echo off
setlocal enabledelayedexpansion

REM ---------------------------------------------------------
REM SyncroJob Enterprise - Test Runner Wrapper
REM Assicura l'esecuzione tramite robust_tests.py nel .venv
REM ---------------------------------------------------------

cd /d "%~dp0\.."

echo [TEST] Inizializzazione ambiente...

REM Verifica che Python sia installato
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python non trovato!
    pause
    exit /b 1
)

:: Controllo se esiste l'ambiente virtuale
if not exist ".venv" (
    echo [INFO] Ambiente virtuale non trovato. Creazione in corso...
    python -m venv .venv
)

set VENV_PYTHON=.venv\Scripts\python.exe

echo [INFO] Verifica dipendenze...
"!VENV_PYTHON!" -m pip install --upgrade pip -q
"!VENV_PYTHON!" -m pip install -e . -q

echo.
echo [TEST] Avvio Robust Test Runner...
echo.

"!VENV_PYTHON!" tests/run_robust_tests.py %*

if errorlevel 1 (
    echo.
    echo [ERROR] Test falliti o interrotti.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Esecuzione completata.
pause
