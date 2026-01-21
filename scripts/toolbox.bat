@echo off
setlocal enabledelayedexpansion
title SyncroJob - Master Developer Toolbox (Enterprise Edition)
cd /d "%~dp0"
cd ..

:menu
cls
echo ============================================================
echo 🚀 SYNCROJOB - MASTER DEVELOPER TOOLBOX (ENTERPRISE)
echo ============================================================
echo.
echo [ QUALITY ^& INTEGRITY ]
echo  1. FULL CHECK (Qualita, Sicurezza, Deps, Test) - Rich UI
echo  2. FAST CHECK (Senza Test) - Rapido per commit
echo  3. ONLY TESTS (Pytest Suite)
echo  4. FIX STYLE  (Auto-fix Ruff)
echo.
echo [ DEEP TESTING ^& ARCHITECTURE ]
echo  5. MUTATION TEST (Mutmut - Lento ma profondo)
echo  6. COVERAGE HTML (Report Copertura)
echo  7. GEN DIAGRAM   (Genera schema architettura PNG)
echo.
echo [ DOCUMENTATION ]
echo  8. BUILD DOCS    (MkDocs - Genera sito statico)
echo  9. SERVE DOCS    (MkDocs - Anteprima live)
echo.
echo [ VERSIONING ^& DEPLOY ]
echo 10. COMMIT WIZARD (Commitizen - Guida al commit standard)
echo 11. BUMP VERSION  (Commitizen - Auto-incremento versione)
echo 12. RELEASE       (Legacy Release script)
echo 13. DEPLOY        (Release ^& Deploy to Netlify)
echo.
echo [ TOOLS ]
echo 14. INSPECTOR     (Universal Inspector)
echo 15. SECRETS       (Secrets Manager)
echo 16. PROFILING     (Scalene Performance)
echo 17. DB MAINTAIN   (SQLite Vacuum & Check)
echo 18. RAW METRICS   (Radon CC & MI)
echo 19. CLEAN CODE    (Eradicate - Remove commented code)
echo.
echo [ SYSTEM ]
echo 20. RUN APP       (Dev Mode - Icecream enabled)
echo 21. CLEAN         (Pulizia cache)
echo.
echo [q] ESCI
echo.
echo ============================================================

set /p choice="Scegli (1-21): "

set VENV_PYTHON=.venv\Scripts\python.exe
set VENV_BIN=.venv\Scripts

if not exist !VENV_PYTHON! (
    echo ❌ Errore: Ambiente virtuale .venv non trovato.
    pause
    goto menu
)

if "%choice%"=="1" (
    !VENV_PYTHON! admin/pre_flight_check.py
    pause
    goto menu
)

if "%choice%"=="2" (
    !VENV_PYTHON! admin/pre_flight_check.py --fast
    pause
    goto menu
)

if "%choice%"=="3" (
    !VENV_PYTHON! admin/pre_flight_check.py --test-only
    pause
    goto menu
)

if "%choice%"=="4" (
    !VENV_PYTHON! admin/pre_flight_check.py --fix --fast
    pause
    goto menu
)

if "%choice%"=="5" (
    echo [EXEC] Running Mutation Testing...
    !VENV_BIN!\mutmut run
    !VENV_BIN!\mutmut results
    pause
    goto menu
)

if "%choice%"=="6" (
    echo [EXEC] Generating Coverage Report...
    !VENV_BIN!\pytest --cov=src --cov-report=html
    start htmlcov/index.html
    pause
    goto menu
)

if "%choice%"=="7" (
    echo [EXEC] Generating Architecture Diagram...
    !VENV_PYTHON! docs/generate_architecture.py
    pause
    goto menu
)

if "%choice%"=="8" (
    echo [EXEC] Building Documentation...
    !VENV_BIN!\mkdocs build
    echo Docs generate in 'site/'
    pause
    goto menu
)

if "%choice%"=="9" (
    echo [EXEC] Serving Documentation at http://127.0.0.1:8000
    !VENV_BIN!\mkdocs serve
    goto menu
)

if "%choice%"=="10" (
    echo [INFO] Premi CTRL+F per interagire con il terminale se necessario.
    !VENV_BIN!\cz commit
    pause
    goto menu
)

if "%choice%"=="11" (
    echo [EXEC] Auto-bumping version and generating changelog...
    !VENV_BIN!\cz bump --changelog
    pause
    goto menu
)

if "%choice%"=="12" (
    !VENV_PYTHON! admin/release.py auto
    pause
    goto menu
)

if "%choice%"=="13" (
    !VENV_PYTHON! admin/release.py auto --deploy
    pause
    goto menu
)

if "%choice%"=="14" (
    !VENV_PYTHON! admin/universal_inspector.py
    goto menu
)

if "%choice%"=="15" (
    !VENV_PYTHON! admin/manage_secrets_gui.py
    goto menu
)

if "%choice%"=="16" (
    !VENV_BIN!\scalene.exe run --html --output profiling_report.html main.py
    pause
    goto menu
)

if "%choice%"=="17" (
    !VENV_PYTHON! admin/db_maintenance.py
    pause
    goto menu
)

if "%choice%"=="18" (
    echo [EXEC] Radon - Maintainability Index...
    !VENV_BIN!\radon mi src -s
    echo.
    echo [EXEC] Radon - Cyclomatic Complexity (Risk only)...
    !VENV_BIN!\radon cc src -a -nc --min B
    pause
    goto menu
)

if "%choice%"=="19" (
    echo [EXEC] Eradicate - Removing commented out code...
    !VENV_BIN!\pip install eradicate >nul
    !VENV_BIN!\eradicate -r -i src
    echo [INFO] Clean complete. Check git diff.
    pause
    goto menu
)

if "%choice%"=="20" (
    !VENV_PYTHON! main.py
    goto menu
)

if "%choice%"=="21" (
    !VENV_PYTHON! admin/clean_venv.py
    pause
    goto menu
)

if "%choice%"=="q" (
    exit /b 0
)

echo Scelta non valida.
pause
goto menu
