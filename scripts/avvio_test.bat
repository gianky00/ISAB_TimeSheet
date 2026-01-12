@echo off
REM Spostati nella root del progetto (cartella genitore di scripts)
cd /d "%~dp0.."

echo Avvio test robusti...

REM Check for venv
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe tests/run_robust_tests.py --reset %*
) else (
    echo [WARNING] .venv not found, using system python...
    python tests/run_robust_tests.py --reset %*
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Errore durante i test.
    pause
) else (
    echo.
    echo Test completati con successo.
    pause
)
