@echo off
echo ==========================================
echo   SyncroJob Enterprise - Build Launcher
echo ==========================================

REM Verifica Poetry
where poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Poetry non trovato! Installalo o aggiungilo al PATH.
    pause
    exit /b 1
)

echo [INFO] Avvio procedura di build...
poetry run python "admin/Crea Setup/build_dist.py" %*

if %errorlevel% neq 0 (
    echo [ERROR] Build fallita. Vedi log per dettagli.
    pause
    exit /b 1
)

echo [SUCCESS] Build completata!
pause
