@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
cd ..

set VENV_PYTHON=.venv\Scripts\python.exe

echo ============================================================
echo 🚀 SYNCROJOB - RELEASE SHORTCUT
echo ============================================================
echo.
echo Scegli il tipo di release:
echo [1] Patch (1.0.x) - Default
echo [2] Minor (1.x.0)
echo [3] Major (x.0.0)
echo.
set /p TYPE_CHOICE="Scelta [1-3]: "

set BUMP_TYPE=patch
if "%TYPE_CHOICE%"=="2" set BUMP_TYPE=minor
if "%TYPE_CHOICE%"=="3" set BUMP_TYPE=major

echo.
echo Scegli la destinazione:
echo [1] Local Build Only (No Deploy) - Default
echo [2] Full Release + Deploy to Netlify
echo.
set /p MODE_CHOICE="Scelta [1-2]: "

set EXTRA_ARGS=
if "%MODE_CHOICE%"=="2" set EXTRA_ARGS=--deploy

echo.
echo Esecuzione: admin/release.py %BUMP_TYPE% %EXTRA_ARGS%
echo.
%VENV_PYTHON% admin/release.py %BUMP_TYPE% %EXTRA_ARGS%

pause
