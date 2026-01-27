@echo off
echo ==========================================
echo   SyncroJob Enterprise - Build Launcher
echo ==========================================

@echo off
echo ==========================================
echo   SyncroJob Enterprise - Local Build
echo ==========================================
echo [INFO] Questo script ora utilizza la logica ufficiale di release.py
echo [INFO] Modalita': LOCAL BUILD (No Git Commit, No Deploy, Fast Check)

REM Configurazione Ambiente
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%.."

set "VENV_PYTHON=.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo [ERROR] Ambiente virtuale non trovato in: %VENV_PYTHON%
    echo Assicurati di aver installato le dipendenze con 'poetry install'.
    popd
    pause
    exit /b 1
)

REM Esegue release.py in modalità "solo build locale"
REM --no-git: Non crea commit o tag
REM --no-deploy: Non carica su Netlify
REM --skip-tests: Salta i test unitari per velocizzare (rimuovi se vuoi i test)
REM patch: usa un incremento di versione patch temporaneo (o usa 'auto')

"%VENV_PYTHON%" "admin/release.py" patch --no-git --skip-tests --force

if %errorlevel% neq 0 (
    echo [ERROR] Build fallita.
    popd
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Build Locale Completata!
echo Trovi l'installer in: admin\Crea Setup\Setup
popd
pause

if %errorlevel% neq 0 (
    echo [ERROR] Build fallita. Vedi log per dettagli.
    pause
    exit /b 1
)

echo [SUCCESS] Build completata!
pause
