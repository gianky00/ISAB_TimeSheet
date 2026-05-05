@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo   SyncroJob - Rilevamento Hardware ID (HWID)
echo ====================================================
echo.

:: Esegue lo script python per ottenere l'HWID normalizzato
for /f "tokens=*" %%i in ('python "%~dp0get_hwid.py"') do set HWID=%%i

if "%HWID%"=="NON_TROVATO" (
    echo [ERRORE] Impossibile rilevare il Seriale del Disco.
    pause
    exit /b 1
)

echo Il tuo Hardware ID e':
echo.
echo   !HWID!
echo.
echo ----------------------------------------------------
echo [INFO] L'ID e' stato copiato negli appunti.
echo [INFO] Incollalo nel Generatore Licenze.
echo ----------------------------------------------------

:: Copia negli appunti
echo | set /p="!HWID!" | clip

echo.
echo Premi un tasto per uscire...
pause > nul
