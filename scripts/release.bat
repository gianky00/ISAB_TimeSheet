@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
cd ..

set VENV_PYTHON=.venv\Scripts\python.exe

echo ============================================================
echo 🔍 SYNCROJOB - PRE-FLIGHT CHECK
echo ============================================================
%VENV_PYTHON% admin/pre_flight_check.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Pre-Flight Check Fallito. Rilascio annullato.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ============================================================
echo 🚀 SYNCROJOB - RELEASE SHORTCUT
echo ============================================================
echo.
echo Scegli il tipo di release:
echo [1] Rileva Automaticamente (Basato sui commit) - Default
echo [2] Patch (1.0.x)
echo [3] Minor (1.x.0)
echo [4] Major (x.0.0)
echo.
set /p TYPE_CHOICE="Scelta [1-4]: "

set BUMP_TYPE=auto
if "%TYPE_CHOICE%"=="2" set BUMP_TYPE=patch
if "%TYPE_CHOICE%"=="3" set BUMP_TYPE=minor
if "%TYPE_CHOICE%"=="4" set BUMP_TYPE=major

echo.
echo Scegli la destinazione:
echo [1] Local Build Only (No Deploy) - Default
echo [2] Full Release + Deploy to Netlify
echo.
set /p MODE_CHOICE="Scelta [1-2]: "

set EXTRA_ARGS=
if "%MODE_CHOICE%"=="2" set EXTRA_ARGS=%EXTRA_ARGS% --deploy

echo.
echo Vuoi eseguire i test prima del rilascio?
echo [1] Si (Consigliato) - Default
echo [2] No (Salta test)
echo.
set /p TEST_CHOICE="Scelta [1-2]: "

if "%TEST_CHOICE%"=="2" set EXTRA_ARGS=%EXTRA_ARGS% --skip-tests

echo.
echo Esecuzione: admin/release.py %BUMP_TYPE% %EXTRA_ARGS%
echo.
%VENV_PYTHON% admin/release.py %BUMP_TYPE% %EXTRA_ARGS%

pause
