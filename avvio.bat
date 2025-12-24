@echo off
title Bot TS - Avvio da sorgenti
cd /d "%~dp0"

echo =============================================
echo    Bot TS - Avvio da codici sorgenti
echo =============================================
echo.

REM Verifica che Python sia installato
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato!
    echo Installa Python da https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Controlla e installa dipendenze se necessario
if not exist "venv" (
    echo [INFO] Creazione ambiente virtuale...
    python -m venv venv
)

echo [INFO] Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo [INFO] Verifica dipendenze...
python.exe -m pip install --upgrade pip
pip install -r requirements.txt -q

echo.
echo [INFO] Avvio applicazione...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo [ERRORE] L'applicazione si e' chiusa con errore.
    pause
)

deactivate
