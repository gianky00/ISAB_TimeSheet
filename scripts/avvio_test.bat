@echo off
setlocal enabledelayedexpansion

REM ---------------------------------------------------------
REM SyncroJob Enterprise - Test Runner Wrapper
REM Assicura l'esecuzione tramite robust_tests.py nel .venv
REM ---------------------------------------------------------

cd /d "%~dp0\.."

echo [TEST] Inizializzazione ambiente...

set VENV_PYTHON=.venv\Scripts\python.exe
if not exist "!VENV_PYTHON!" (
    set VENV_PYTHON=python
    echo [WARNING] .venv non trovato, uso python di sistema.
)

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
