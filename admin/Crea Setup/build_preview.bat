@echo off
:: ============================================================================
:: SyncroJob - Build Preview Setup
:: Compila il setup di anteprima con Inno Setup (pochi secondi)
:: ============================================================================

echo.
echo  ================================================
echo   SyncroJob - Build Preview Setup
echo  ================================================
echo.

set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if not exist %ISCC% (
    echo [ERRORE] Inno Setup 6 non trovato in:
    echo   %ISCC%
    echo.
    echo Installa Inno Setup 6 da: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

echo [BUILD] Pulizia directory Setup...
if exist "%~dp0Setup\SyncroJob_Preview*.exe" del /Q "%~dp0Setup\SyncroJob_Preview*.exe"

echo [BUILD] Compilazione setup_preview.iss...
echo.

%ISCC% "%~dp0setup_preview.iss"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRORE] Compilazione fallita!
    pause
    exit /b 1
)

echo.
echo  ================================================
echo   BUILD COMPLETATA!
echo  ================================================
echo.
echo   Output: %~dp0Setup\SyncroJob_Preview_v*.exe
echo.
echo   Premi un tasto per avviare il setup di preview...
pause > nul

for %%F in ("%~dp0Setup\SyncroJob_Preview*.exe") do start "" "%%F"
