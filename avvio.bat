@echo off
setlocal

echo ==========================================
echo      AVVIO APPLICAZIONE ISAB
echo ==========================================
echo.

REM 1. Verifica Python
echo [1] Verifica installazione Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRORE] Python non trovato! Assicurati che sia installato e nel PATH.
    pause
    exit /b 1
)

REM 2. Setup Ambiente Virtuale
if not exist "venv" (
    echo [2] Creazione ambiente virtuale...
    python -m venv venv
) else (
    echo [2] Ambiente virtuale esistente.
)

REM 3. Attivazione e Dipendenze
echo [3] Attivazione ambiente e controllo dipendenze...
call venv\Scripts\activate.bat
if exist requirements.txt (
    pip install -r requirements.txt >nul
)

REM 4. Avvio Main
echo.
echo [4] Avvio interfaccia grafica...
echo ------------------------------------------
python main.py

REM 5. Gestione Chiusura
if %errorlevel% neq 0 (
    echo.
    echo ------------------------------------------
    echo [ERRORE] L'applicazione si e' chiusa con un errore.
) else (
    echo.
    echo ------------------------------------------
    echo Applicazione chiusa correttamente.
)

echo.
pause
