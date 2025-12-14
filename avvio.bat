@echo off
setlocal

set "VENV_DIR=venv"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python non trovato! Assicurati che Python sia installato e aggiunto al PATH.
    pause
    exit /b 1
)

REM Check if venv exists, if not create it
if not exist "%VENV_DIR%" (
    echo Creazione ambiente virtuale in corso...
    python -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo Errore nella creazione dell'ambiente virtuale.
        pause
        exit /b 1
    )
    echo Ambiente virtuale creato.
)

REM Activate venv
call "%VENV_DIR%\Scripts\activate.bat"

REM Install requirements
if exist "requirements.txt" (
    echo Verifica e installazione dipendenze...
    pip install -r requirements.txt
) else (
    echo ATTENZIONE: File requirements.txt non trovato.
)

REM Run the application
echo Avvio applicazione...
python main.py

REM Deactivate (optional, as script ends)
deactivate

pause
