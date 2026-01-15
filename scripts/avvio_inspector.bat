@echo off
title Universal Inspector - Analisi Struttura Web
cd /d "%~dp0"
cd ..

echo =============================================
echo    UNIVERSAL INSPECTOR - Avvio Strumento
echo =============================================
echo.

:: Verifica ambiente virtuale
if not exist ".venv" (
    echo [ERRORE] Ambiente virtuale non trovato!
    echo Eseguire prima scripts\avvio.bat per configurare il sistema.
    pause
    exit /b 1
)

:: Attivazione ambiente virtuale
call .venv\Scripts\activate.bat

echo [INFO] Avvio Inspector...
echo.

python admin/universal_inspector.py

if errorlevel 1 (
    echo.
    echo [ERRORE] L'ispezione si e' chiusa con un problema.
    pause
)

deactivate
