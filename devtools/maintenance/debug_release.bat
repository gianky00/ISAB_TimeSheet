@echo off
setlocal enabledelayedexpansion
title DEBUG - Release Script Test
cd /d "%~dp0"
cd ..

echo ============================================
echo [DEBUG] Test Release Script - Isolamento
echo ============================================
echo.
echo [1] Directory corrente: %CD%
echo [2] Python path: .venv\Scripts\python.exe
echo.

echo [3] Verifica esistenza file...
if exist .venv\Scripts\python.exe (echo     OK: python.exe trovato) else (echo     FAIL: python.exe NON trovato & goto end)
if exist admin\release.py (echo     OK: release.py trovato) else (echo     FAIL: release.py NON trovato & goto end)
if exist "admin\Crea Setup\build_dist.py" (echo     OK: build_dist.py trovato) else (echo     WARN: build_dist.py NON trovato)
echo.

echo [4] Test import moduli Python...
.venv\Scripts\python.exe -c "import sys; print('    Python version:', sys.version.split()[0])"
echo     Exit code: %errorlevel%
echo.

echo [5] Test singoli script della catena...
echo.
echo     --- pre_flight_check.py --help ---
.venv\Scripts\python.exe devtools/gui/pre_flight_check.py --help 2>&1 | findstr /i "usage error" || echo     (nessun output help)
echo     Exit code: %errorlevel%
echo.

echo     --- sync_requirements.py ---
.venv\Scripts\python.exe devtools/gui/sync_requirements.py
echo     Exit code: %errorlevel%
echo.

echo [6] Test COMPLETO release.py (con --no-git per sicurezza)...
echo ============================================
.venv\Scripts\python.exe devtools/gui/release.py auto --deploy --no-git
echo ============================================
echo.
echo [DEBUG] Exit code finale release.py: %errorlevel%
echo.

:end
echo ============================================
echo [DEBUG] Test completato
echo ============================================
pause
