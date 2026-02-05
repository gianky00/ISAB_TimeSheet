@echo off
setlocal enabledelayedexpansion
title SyncroJob - Master Developer Toolbox (Apex Edition)

:: Impostazione codepage UTF-8 per supportare emoji e caratteri Unicode
chcp 65001 >nul 2>&1

:: Forza Python a usare UTF-8 per input/output
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

cd /d "%~dp0"
cd ..

:: Impostazione Colori (Cyan)
color 0B

:menu
cls
echo.
echo  ========================================================================
echo    [#] SYNCROJOB - MASTER DEVELOPER TOOLBOX (APEX EDITION)
echo  ========================================================================
echo.
echo    [ 0. SYSTEM BOOTSTRAP AND SETUP ]
echo    ----------------------------------------------------------------------
echo     0. INIT SYSTEM     - Installa/Aggiorna tutte le librerie (Poetry)
echo.
echo    [ A. QUALITY AND SECURITY ENGINE ]
echo    ----------------------------------------------------------------------
echo     1. FULL AUDIT      - Analisi totale: Sicurezza, Tipi, Stile e Test
echo     2. FAST AUDIT      - Check completo saltando i test (Rapido)
echo     3. SMART CHECK     - ANALISI INCREMENTALE: Solo file modificati Git
echo     4. ONLY TESTS      - Esegue solo la suite unitaria di robustezza
echo     5. AUTO-FIX        - Sistema automaticamente errori di stile Ruff
echo     6. DASHBOARD       - Apre il report HTML dell'ultimo Audit
echo.
echo    [ B. SECURITY AND ARCHITECTURE ]
echo    ----------------------------------------------------------------------
echo     7. SECURITY SCAN   - Pip-audit: Verifica vulnerabilita CVE
echo     8. COVERAGE        - Genera report HTML di copertura del codice
echo     9. ARCHITECTURE    - Genera il diagramma delle classi (PNG)
echo.
echo    [ C. DOCUMENTATION AND KNOWLEDGE ]
echo    ----------------------------------------------------------------------
echo    10. BUILD DOCS      - Compila la documentazione MkDocs (Statica)
echo    11. SERVE DOCS      - Avvia il server live per vedere i manuali
echo.
echo    [ D. CI/CD, RELEASE AND DEPLOY ]
echo    ----------------------------------------------------------------------
echo    12. COMMIT WIZARD   - Guida al commit standard (Conventional Commits)
echo    13. VERSION BUMP    - Incrementa versione e genera Changelog
echo    14. FULL RELEASE    - Build EXE TOTALE (Certificazione Parita + Test)
echo    15. FAST RELEASE    - Build EXE rapida (Salta i test)
echo    16. FULL DEPLOY     - Release + Caricamento su server/distribuzione
echo.
echo    [ E. ENTERPRISE POWER TOOLS ]
echo    ----------------------------------------------------------------------
echo    17. SECRETS MGMT    - Gestore grafico delle chiavi e credenziali
echo    18. PERFORMANCE     - Profiling profondo (Scalene) per bottleneck
echo    19. DB MAINTAIN     - Ottimizzazione e Integrity Check SQLite
echo    20. RAW METRICS     - Complessita ciclotematica e indici tecnici
echo    21. CLEAN CODE      - Rimuove codice commentato e dead code
echo    22. DEPTY CHECK     - Verifica dipendenze inutilizzate (Deptry)
echo    23. PROJECT STATS   - Statistiche linee di codice e linguaggi
echo    27. DEP AUDIT       - Verifica isomorfismo dipendenze Sorgente/EXE
echo.
echo    [ F. SYSTEM AND RUN ]
echo    ----------------------------------------------------------------------
echo    24. RUN APP (DEV)   - Avvia l'app in modalita Sviluppo (Debug)
echo    25. CLEAN CACHE     - Pulisce .pyc, __pycache__ e temp files
echo    26. INSPECTOR       - Ispezione universale del sistema/log
echo.
echo    [ q. ESCI ]
echo.
echo  ========================================================================
echo.

set "choice="
set /p choice=" >> Seleziona un'operazione (0-27): "

set VENV_PYTHON=.venv\Scripts\python.exe
set VENV_BIN=.venv\Scripts

:: --- GESTIONE OPZIONE 0 (BOOTSTRAP) ---
if "%choice%"=="0" (
    echo [INFO] Avvio procedura di installazione/aggiornamento...
    where poetry >nul 2>nul
    if !errorlevel! neq 0 (
        echo [ERROR] Poetry non trovato! Tento installazione via PIP...
        "%VENV_PYTHON%" -m pip install -r requirements.txt
        pause
        goto menu
    )
    echo [INFO] Esecuzione Poetry Install...
    poetry install
    if !errorlevel! neq 0 (
        echo [WARNING] Poetry ha fallito. Tento recupero via PIP (Resilience Mode)...
        "%VENV_PYTHON%" -m pip install -r requirements.txt
    )
    pause
    goto menu
)

:: Verifica esistenza VENV
if not exist "%VENV_PYTHON%" (
    if /i not "%choice%"=="q" (
        echo.
        echo  [ERROR] Ambiente virtuale .venv non trovato!
        echo          Premi '0' per inizializzare il sistema.
        pause
    )
    if /i "%choice%"=="q" exit /b 0
    goto menu
)

:: --- LOGICA DI ESECUZIONE ---

if "%choice%"=="1" (
    "%VENV_PYTHON%" admin/pre_flight_check.py
    pause
    goto menu
)
if "%choice%"=="2" (
    "%VENV_PYTHON%" admin/pre_flight_check.py --fast
    pause
    goto menu
)
if "%choice%"=="3" (
    echo [INFO] Analisi incrementale...
    "%VENV_PYTHON%" admin/pre_flight_check.py --fast --inc
    pause
    goto menu
)
if "%choice%"=="4" (
    "%VENV_PYTHON%" admin/pre_flight_check.py --test-only
    pause
    goto menu
)
if "%choice%"=="5" (
    echo [INFO] Correzione automatica...
    "%VENV_PYTHON%" admin/pre_flight_check.py --fix --fast
    pause
    goto menu
)
if "%choice%"=="6" (
    if exist reports\preflight\dashboard.html (start reports\preflight\dashboard.html) else (echo [ERROR] Dashboard non trovata.)
    pause & goto menu
)
if "%choice%"=="7" (
    echo [INFO] Apex Security Scan (Bandit + Pip-Audit)...
    "%VENV_PYTHON%" admin/pre_flight_check.py --target security
    pause & goto menu
)
if "%choice%"=="8" (
    "%VENV_BIN%\pytest" --cov=src --cov-report=html
    start htmlcov/index.html
    pause & goto menu
)
if "%choice%"=="9" (
    "%VENV_PYTHON%" docs/generate_architecture.py
    pause
    goto menu
)
if "%choice%"=="10" (
    "%VENV_BIN%\mkdocs" build
    pause
    goto menu
)
if "%choice%"=="11" (
    "%VENV_BIN%\mkdocs" serve
    goto menu
)
if "%choice%"=="12" (
    "%VENV_BIN%\cz" commit
    pause
    goto menu
)
if "%choice%"=="13" (
    "%VENV_BIN%\cz" bump --changelog
    pause
    goto menu
)
if "%choice%"=="14" (
    "%VENV_PYTHON%" admin/release.py auto
    pause
    goto menu
)
if "%choice%"=="15" (
    "%VENV_PYTHON%" admin/release.py auto --skip-tests
    pause
    goto menu
)
if "%choice%"=="16" (
    "%VENV_PYTHON%" admin/release.py auto --deploy
    pause
    goto menu
)
if "%choice%"=="17" (
    "%VENV_PYTHON%" admin/manage_secrets_gui.py
    goto menu
)
if "%choice%"=="18" (
    echo [INFO] Avvio Profiling con cProfile (Massima Stabilita)...
    echo [NOTE] L'app potrebbe essere leggermente piu lenta durante il profiling.
    "%VENV_PYTHON%" -m cProfile -o profiling_report.prof main.py
    if exist profiling_report.prof (
        echo [INFO] Generazione report visuale con SnakeViz...
        echo [TIP] Se SnakeViz non si apre, installalo con: pip install snakeviz
        "%VENV_PYTHON%" -m snakeviz profiling_report.prof
    ) else (
        echo [ERROR] Profiling non generato.
    )
    pause
    goto menu
)
if "%choice%"=="19" (
    "%VENV_PYTHON%" admin/db_maintenance.py
    pause
    goto menu
)
if "%choice%"=="20" (
    echo [INFO] Apex Metrics (Radon MI + CC Parallel)...
    "%VENV_PYTHON%" admin/pre_flight_check.py --target metrics
    pause & goto menu
)
if "%choice%"=="21" (
    "%VENV_PYTHON%" admin/pre_flight_check.py --target clean
    pause
    goto menu
)
if "%choice%"=="22" (
    echo [INFO] Apex Dependency Check (Deptry)...
    "%VENV_PYTHON%" admin/pre_flight_check.py --target deps
    pause & goto menu
)
if "%choice%"=="23" (
    "%VENV_PYTHON%" admin/pre_flight_check.py --target stats
    pause
    goto menu
)
if "%choice%"=="24" (
    "%VENV_PYTHON%" main.py
    goto menu
)
if "%choice%"=="25" (
    "%VENV_PYTHON%" admin/clean_venv.py
    pause
    goto menu
)
if "%choice%"=="26" (
    "%VENV_PYTHON%" admin/universal_inspector.py
    goto menu
)
if "%choice%"=="27" (
    "%VENV_PYTHON%" admin/analyze_dependencies.py
    pause
    goto menu
)

if /i "%choice%"=="q" exit /b 0

echo.
echo  [WARNING] Scelta non valida.
timeout /t 2 >nul
goto menu
