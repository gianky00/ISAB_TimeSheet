@echo off
setlocal enabledelayedexpansion
title SyncroJob - Master Developer Toolbox
cd /d "%~dp0"
cd ..

:menu
cls
echo ============================================================
echo 🚀 SYNCROJOB - MASTER DEVELOPER TOOLBOX
echo ============================================================
echo.
echo [ QUALITY ^& INTEGRITY ]
echo  1. FULL CHECK (Qualita, Sicurezza, Test, Hook) - Pre-commit
echo  2. FAST CHECK (Qualita ^& Sicurezza senza Test)
echo  3. ONLY TESTS (Esecuzione completa suite di test)
echo  4. FIX STYLE  (Correzione automatica Ruff)
echo.
echo [ DEPLOYMENT ^& RELEASE ]
echo  5. RELEASE    (Auto-bump, Icons, Build ^& Tags)
echo  6. DEPLOY     (Release ^& Deploy to Netlify)
echo.
echo [ BOT DEVELOPMENT ]
echo  7. INSPECTOR  (Universal Inspector - Web Analysis UI)
echo  8. SECRETS    (Gestione API Keys ^& Secrets GUI)
echo  9. PROFILING  (Analisi performance con Scalene)
echo.
echo [ SYSTEM ]
echo 10. RUN APP    (Avvio applicazione in modalita Dev)
echo 11. CLEAN      (Pulizia ambiente virtuale ^& cache)
echo 12. SUPER AUDIT (Branch - Quality - Version - Merge)
echo.
echo [q] ESCI
echo.
echo ============================================================

set /p choice="Scegli un'operazione (1-12): "

set VENV_PYTHON=.venv\Scripts\python.exe
set VENV_BIN=.venv\Scripts

if not exist !VENV_PYTHON! (
    echo ❌ Errore: Ambiente virtuale .venv non trovato.
    pause
    goto menu
)

if "%choice%"=="1" (
    echo [EXEC] Full Pre-flight Check...
    !VENV_PYTHON! admin/pre_flight_check.py
    pause
    goto menu
)

if "%choice%"=="2" (
    echo [EXEC] Fast Quality Check...
    !VENV_PYTHON! admin/pre_flight_check.py --fast
    pause
    goto menu
)

if "%choice%"=="3" (
    echo [EXEC] Running Test Suite...
    !VENV_PYTHON! admin/pre_flight_check.py --test-only
    pause
    goto menu
)

if "%choice%"=="4" (
    echo [EXEC] Fixing style and formatting...
    !VENV_PYTHON! admin/pre_flight_check.py --fix --fast
    pause
    goto menu
)

if "%choice%"=="5" (
    echo [EXEC] Starting Automated Release...
    !VENV_PYTHON! admin/release.py auto
    pause
    goto menu
)

if "%choice%"=="6" (
    echo [EXEC] Starting Release with Cloud Deploy...
    !VENV_PYTHON! admin/release.py auto --deploy
    pause
    goto menu
)

if "%choice%"=="7" (
    echo [EXEC] Opening Universal Inspector...
    !VENV_PYTHON! admin/universal_inspector.py
    goto menu
)

if "%choice%"=="8" (
    echo [EXEC] Opening Secrets Manager...
    !VENV_PYTHON! admin/manage_secrets_gui.py
    goto menu
)

if "%choice%"=="9" (
    echo [EXEC] Starting Profiling...
    !VENV_BIN!\scalene.exe run --html --output profiling_report.html main.py
    pause
    goto menu
)

if "%choice%"=="10" (
    echo [EXEC] Launching Application...
    !VENV_PYTHON! main.py
    goto menu
)

if "%choice%"=="11" (
    echo [EXEC] Cleaning environment...
    !VENV_PYTHON! admin/clean_venv.py
    pause
    goto menu
)

if "%choice%"=="12" (
    echo [EXEC] Starting Super Audit Lifecycle...
    !VENV_PYTHON! admin/pre_flight_check.py --super-audit
    pause
    goto menu
)

if "%choice%"=="q" (
    exit /b 0
)

echo Scelta non valida.
pause
goto menu
