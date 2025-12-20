@echo off
title Bot TS - Reset Ambiente e Avvio
cd /d "%~dp0"

echo =============================================
echo    Bot TS - Reset Completo Ambiente
echo =============================================
echo.

REM --- CHECK PER PROCESSI PYTHON ---
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [ATTENZIONE] Rilevati processi Python attivi.
    echo Chiudere eventuali finestre del bot aperte.
    echo.
    echo Premere un tasto per tentare di chiuderli forzatamente...
    pause
    taskkill /F /IM python.exe >nul 2>&1
)

echo [1/4] Rimozione ambiente virtuale esistente...
if exist "venv" (
    rmdir /s /q "venv"
    if exist "venv" (
        echo [ERRORE] Impossibile rimuovere la cartella 'venv'.
        echo Qualche file e' bloccato. Riavvia il PC o chiudi tutti i programmi.
        pause
        exit /b 1
    )
    echo    - Cartella venv rimossa correttamente.
) else (
    echo    - Nessun ambiente venv trovato.
)

echo [2/4] Pulizia file cache Python (__pycache__)...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo    - Cache pulita.

echo [3/4] Pulizia Cache WebDriver (Corregge WinError 193)...
if exist "%USERPROFILE%\.wdm" (
    rmdir /s /q "%USERPROFILE%\.wdm"
    echo    - Cache WebDriver (.wdm) rimossa.
) else (
    echo    - Nessuna cache WebDriver trovata.
)

echo [4/4] Riavvio tramite avvio.bat...
echo.
echo Il sistema ora ricostruira' l'ambiente da zero.
echo Verranno scaricati nuovamente i driver di Chrome.
echo.
pause

call avvio.bat
