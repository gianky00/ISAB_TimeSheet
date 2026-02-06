@echo off
cd /d "%~dp0"

echo Avvio test applicazione...
echo.

REM Prova ad avviare Python
python --version
if errorlevel 1 (
    echo ERRORE: Python non trovato
    pause
    exit /b 1
)

echo.
echo Avvio main.py...
python main.py 2>&1

if errorlevel 1 (
    echo.
    echo ERRORE durante esecuzione
    pause
)
