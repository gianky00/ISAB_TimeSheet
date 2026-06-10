@echo off
:: SyncroJob Developer Toolbox GUI Launcher
:: Avvio silente tramite pythonw.exe

cd /d "%~dp0"
set PYTHONUTF8=1

if not exist ".venv\Scripts\pythonw.exe" (
    echo [ERROR] Ambiente virtuale o pythonw.exe non trovato!
    echo Esegui prima: uv sync
    pause
    exit /b 1
)

:: Avvio silente: non apre finestre CMD extra e non blocca quella corrente
start /b "" ".venv\Scripts\pythonw.exe" "devtools\gui\developer_toolbox_gui.py" %*
