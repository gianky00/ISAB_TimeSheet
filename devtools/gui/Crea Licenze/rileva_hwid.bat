@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo   SyncroJob - Rilevamento Hardware ID (HWID)
echo ====================================================
echo.

:: Rilevamento tramite PowerShell (Standalone)
:: La logica e' identica al validator: Serial Number del Disco, altrimenti UUID Sistema.
:: Applica la normalizzazione: strip e rstrip('.')

set "PS_CMD=$id = (Get-CimInstance -Class Win32_DiskDrive | Select-Object -ExpandProperty SerialNumber | Where-Object { $_ } | Select-Object -First 1); if (-not $id) { $id = (Get-CimInstance -Class Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID) }; if ($id) { $id.Trim().TrimEnd('.') } else { 'NON_TROVATO' }"

for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command "%PS_CMD%"`) do set HWID=%%i

if "!HWID!"=="NON_TROVATO" (
    echo [ERRORE] Impossibile rilevare un ID Hardware valido.
    echo Assicurati di eseguire come amministratore se necessario.
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

:: Copia negli appunti (usa set /p per evitare il newline finale)
echo | set /p="!HWID!" | clip

echo.
echo Premi un tasto per uscire...
pause > nul
