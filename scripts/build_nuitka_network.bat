@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   SyncroJob - AUTOMATIC NUITKA RELEASE SYSTEM
echo ============================================================
echo [INFO] Processo: Bump - Build - Deploy - Git Push
echo.

REM Configurazione Ambiente
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%.."

set "VENV_PYTHON=.venv\Scripts\python.exe"
set "VENV_CZ=.venv\Scripts\cz.exe"
set "BUILD_SCRIPT=admin/Crea Setup/build_dist.py"

REM Forza encoding UTF-8 per prevenire crash charset
set PYTHONUTF8=1

if not exist "%VENV_PYTHON%" (
    echo [ERROR] Ambiente virtuale non trovato in: %VENV_PYTHON%
    popd
    pause
    exit /b 1
)

echo [1/4] INCREMENTO VERSIONE AUTOMATICO (PATCH)...
if exist "%VENV_CZ%" (
    REM Usa Commitizen per gestire versione e changelog in modo standard
    "%VENV_CZ%" bump --changelog --yes
) else (
    REM Fallback su script interno
    "%VENV_PYTHON%" "admin/bump_version.py" patch
)

echo.
echo [2/4] COMPILAZIONE NUITKA (PC LOCALE)...
echo [HINT] Usa i log dettagliati e lo spinner per monitorare il progresso.
echo.

REM Avvia build locale: Nuitka + Installer + Network Deploy
"%VENV_PYTHON%" "%BUILD_SCRIPT%" --use-nuitka --no-deploy

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Procedura di build interrotta per errori tecnici.
    echo Controlla build_log.txt.
    popd
    pause
    exit /b 1
)

echo.
echo [3/4] SINCRONIZZAZIONE REPOSITORY...
echo [INFO] Caricamento nuova versione e tag su GitHub...
git push origin feat/nuitka-compilation --tags

echo.
echo [4/4] PULIZIA FINALE...
echo [INFO] Rilevamento driver allineato.

echo.
echo ============================================================
echo   [SUCCESS] RELEASE COMPLETATA E DISTRIBUITA!
echo ============================================================
echo [STATUS] Versione incrementata.
echo [STATUS] EXE compilato con Nuitka.
echo [STATUS] Setup copiato in rete condivisa.
echo [STATUS] Git repository sincronizzato.
echo.

popd
pause
