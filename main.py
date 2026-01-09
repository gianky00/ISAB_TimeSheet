#!/usr/bin/env python3
"""
# SyncroJob - Sistema di Automazione Portale ISAB
Entry point principale dell'applicazione.
"""
import logging
import os
import shutil
import sys
from pathlib import Path

from src.core.config_manager import CONFIG_DIR

# --- CRASH LOGGING SETUP ---
logger = logging.getLogger("crash_logger")

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))
    try:
        log_file = CONFIG_DIR / "logs" / "crash.log"
        if log_file.exists():
            shutil.copy2(log_file, Path(__file__).parent / "crash.log")
    except Exception:
        pass

def setup_crash_logging():
    if not CONFIG_DIR.exists(): CONFIG_DIR.mkdir(parents=True)
    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    handler = logging.FileHandler(log_dir / "crash.log", mode='w', encoding='utf-8')
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    clogger = logging.getLogger("crash_logger")
    if not clogger.handlers: clogger.addHandler(handler)
    clogger.setLevel(logging.INFO)
    sys.excepthook = handle_exception

setup_crash_logging()

# Ensure src is in path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if src_path not in sys.path: sys.path.insert(0, src_path)

def main():
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from src.core.app_initializer import AppInitializer
    from src.gui.main_window import MainWindow

    app = QApplication(sys.argv)
    AppInitializer.setup_app_style(app)

    if not AppInitializer.initialize():
        sys.exit(1)

    try:
        window = MainWindow()
        window.showMaximized()
        sys.exit(app.exec())
    except Exception as e:
        logger.critical("Errore fatale GUI", exc_info=True)
        QMessageBox.critical(None, "Errore GUI", f"Errore fatale durante l\'avvio:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()