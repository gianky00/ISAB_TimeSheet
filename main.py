#!/usr/bin/env python3
"""
# SyncroJob - Sistema di Automazione Portale ISAB
Entry point principale dell'applicazione.
"""

import logging
import os
import shutil
import sys
import threading
import traceback
from pathlib import Path

from src.core.config_manager import CONFIG_DIR

# --- CRASH LOGGING SETUP ---
logger = logging.getLogger("crash_logger")


def handle_exception(exc_type, exc_value, exc_traceback):
    """Gestore globale per eccezioni non gestite (Thread Principale)."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.critical(f"UNHANDLED EXCEPTION (MainThread):\n{error_msg}")

    # Forza il flush immediato
    for handler in logger.handlers:
        handler.flush()

    try:
        log_file = CONFIG_DIR / "logs" / "crash.log"
        if log_file.exists():
            shutil.copy2(log_file, Path(__file__).parent / "crash.log")
    except Exception:
        pass


def handle_thread_exception(args):
    """Gestore globale per eccezioni nei thread secondari."""
    error_msg = "".join(
        traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)
    )
    logger.critical(f"UNHANDLED EXCEPTION (Thread: {args.thread.name}):\n{error_msg}")

    # Forza il flush
    for handler in logger.handlers:
        handler.flush()


def setup_crash_logging():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    # Setup Logger con Flush immediato
    handler = logging.FileHandler(log_dir / "crash.log", mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    clogger = logging.getLogger("crash_logger")
    if not clogger.handlers:
        clogger.addHandler(handler)
    clogger.setLevel(logging.INFO)

    # Installazione Hooks
    sys.excepthook = handle_exception
    threading.excepthook = handle_thread_exception  # Richiede Python 3.8+


setup_crash_logging()

# Ensure src is in path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


def main():
    import warnings

    # Suppress openpyxl "Unknown extension" warning
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

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
        QMessageBox.critical(None, "Errore GUI", f"Errore fatale durante l'avvio:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
