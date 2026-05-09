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
    pause
    exit /b 1
)

:: Controllo se esiste l'ambiente virtuale
if not exist ".venv" (
    echo [INFO] Ambiente virtuale non trovato. Creazione in corso...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRORE] Impossibile creare l'ambiente virtuale.
        pause
        exit /b 1
    )
)

:: Attivazione ambiente virtuale
if not exist ".venv\Scripts\activate.bat" (
    echo [ERRORE] Ambiente virtuale corrotto. Elimina la cartella .venv e riprova.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat

echo [INFO] Verifica ambiente e dipendenze...

:: Logica "Fast Start": se il pacchetto e' gia' installato, evita pip install
pip show syncrojob >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Pacchetto gia' installato (Fast Start).
) else (
    echo [INFO] Installazione pacchetto in corso...
    pip install -e . --no-deps --timeout 15
)

:: Verifica minima dipendenze critiche (PySide6)
pip show PySide6 >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installazione dipendenze mancanti...
    pip install .
)

echo.
echo [INFO] Avvio applicazione...
echo.

:: Avvio con variabili d'ambiente per forzare UTF-8
set PYTHONUTF8=1
python main.py

if errorlevel 1 (
    echo.
    echo [ERRORE] L'applicazione si e' chiusa in modo anomalo.
    if exist logs\crash.txt (
        echo [INFO] Controlla il file logs\crash.txt per i dettagli.
    )
    pause
)

deactivate
