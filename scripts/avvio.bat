@echo off
title SyncroJob - Avvio da sorgenti
cd /d "%~dp0"
cd ..

echo [INFO] Pulizia dei log di crash precedenti...
if exist crash.log del crash.log

echo =============================================
echo    SyncroJob - Avvio da codici sorgenti
echo =============================================
echo.

REM Verifica che Python sia installato
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato!
    echo Installa Python da https://www.python.org/downloads/
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
pip install -e . -q

echo.
echo [INFO] Avvio applicazione...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo [ERRORE] L'applicazione si e' chiusa con errore.
)

deactivate
