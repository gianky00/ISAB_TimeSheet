@echo off
title Bot TS - Reset Ambiente e Avvio
cd /d "%~dp0"

echo =============================================
echo    Bot TS - Reset Completo Ambiente
echo =============================================
echo.

echo [1/3] Rimozione ambiente virtuale esistente...
if exist "venv" (
    rmdir /s /q "venv"
    echo    - Cartella venv rimossa.
) else (
    echo    - Nessun ambiente venv trovato.
)

echo [2/3] Pulizia file cache Python (__pycache__)...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo    - Cache pulita.

echo [3/3] Riavvio tramite avvio.bat...
echo.
echo Il sistema ora ricostruira' l'ambiente da zero.
echo Questa operazione richiedera' alcuni minuti per scaricare le librerie.
echo.
pause

call avvio.bat
