@echo off
title SyncroJob - Avvio Profiling Scalene
cd /d "%~dp0"
cd ..

echo =============================================
echo    SyncroJob - Avvio con Profiling Scalene
echo =============================================
echo.

REM Avvio dell'applicazione con Scalene per il profiling
poetry run scalene run --html --output profiling_report.html main.py

if errorlevel 1 (
    echo.
    echo [ERRORE] L'applicazione o Scalene si sono chiusi con errore.
    pause
)

