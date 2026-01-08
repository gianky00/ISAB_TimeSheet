@echo off
title SyncroJob - Avvio da sorgenti
cd /d "%~dp0"
cd ..

echo =============================================
echo    SyncroJob - Avvio da codici sorgenti
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

:: Controllo se esiste l'ambiente virtuale
if not exist ".venv" (
    echo [INFO] Ambiente virtuale non trovato. Creazione in corso...
    python -m venv .venv
)

:: Attivazione ambiente virtuale
call .venv\Scripts\activate.bat

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
