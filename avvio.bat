@echo off
setlocal enableextensions enabledelayedexpansion

echo ==========================================
echo      AVVIO AUTOMATICO APPLICAZIONE
echo ==========================================
echo.

REM 1. Verifica Python
echo [1/5] Verifica installazione Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRORE] Python non trovato!
    echo Assicurati che Python sia installato e aggiunto alle variabili d'ambiente (PATH).
    goto :errore
)
python --version

REM 2. Verifica/Creazione Virtual Environment
set "VENV_DIR=venv"
if not exist "%VENV_DIR%" (
    echo [2/5] Creazione ambiente virtuale '%VENV_DIR%' in corso...
    python -m venv %VENV_DIR%
    if !errorlevel! neq 0 (
        echo [ERRORE] Impossibile creare l'ambiente virtuale.
        goto :errore
    )
    echo Ambiente creato con successo.
) else (
    echo [2/5] Ambiente virtuale '%VENV_DIR%' gia' esistente.
)

REM 3. Attivazione Virtual Environment
echo [3/5] Attivazione ambiente virtuale...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [ERRORE] File di attivazione non trovato: "%VENV_DIR%\Scripts\activate.bat"
    echo Prova a cancellare la cartella 'venv' e riavviare.
    goto :errore
)
call "%VENV_DIR%\Scripts\activate.bat"
if !errorlevel! neq 0 (
    echo [ERRORE] Attivazione fallita.
    goto :errore
)

REM 4. Installazione Dipendenze
if exist "requirements.txt" (
    echo [4/5] Controllo e installazione dipendenze...
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERRORE] Installazione delle dipendenze fallita.
        goto :errore
    )
) else (
    echo [4/5] File requirements.txt non trovato. Salto installazione.
)

REM 5. Avvio Applicazione
echo.
echo [5/5] Avvio applicazione (main.py)...
echo ==========================================
echo.
python main.py
if !errorlevel! neq 0 (
    echo.
    echo ==========================================
    echo [ERRORE] L'applicazione si e' chiusa in modo anomalo.
    goto :errore
)

echo.
echo ==========================================
echo Applicazione chiusa correttamente.
echo ==========================================
pause
exit /b 0

:errore
echo.
echo ==========================================
echo SI E' VERIFICATO UN ERRORE BLOCCANTE.
echo Leggi i messaggi sopra per i dettagli.
echo ==========================================
pause
exit /b 1
