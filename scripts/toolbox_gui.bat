@echo off
:: SyncroJob Developer Toolbox GUI Launcher
title SyncroJob - Developer Toolbox GUI

cd /d "%~dp0"
cd ..

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Ambiente virtuale non trovato!
    echo Esegui prima: poetry install
    pause
    exit /b 1
)

echo Avvio Developer Toolbox GUI...
".venv\Scripts\python.exe" admin/developer_toolbox_gui.py %*
