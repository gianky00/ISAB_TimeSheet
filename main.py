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


def setup_logging():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    # 1. Main App Logger (syncrojob.log)
    # Usa RotatingFileHandler per evitare file enormi (max 5MB, 3 backup)
    from logging.handlers import RotatingFileHandler

    app_log_file = log_dir / "syncrojob.log"
    app_handler = RotatingFileHandler(
        app_log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    app_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    # Configura il root logger (cattura tutto dai moduli src.*)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        root_logger.addHandler(app_handler)

    # 2. Crash Logger (crash.log) - Separato per errori fatali
    crash_handler = logging.FileHandler(
        log_dir / "crash.log", mode="w", encoding="utf-8"
    )
    crash_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    clogger = logging.getLogger("crash_logger")
    # Evita duplicazione se già configurato (es. reload)
    if not clogger.handlers:
        clogger.addHandler(crash_handler)
    clogger.setLevel(logging.INFO)
    clogger.propagate = False  # Non mandare i crash al root logger (opzionale)

    # Installazione Hooks
    sys.excepthook = handle_exception
    threading.excepthook = handle_thread_exception


setup_logging()

# Ensure src is in path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


def main():
    import warnings

    # Setup Icecream for debugging (DX)
    try:
        from icecream import ic

        ic.configureOutput(prefix="DEBUG| ", includeContext=True)
        import builtins

        builtins.ic = ic  # type: ignore
    except ImportError:
        pass

    # Suppress openpyxl "Unknown extension" warning
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

    from PyQt6.QtCore import QCoreApplication
    from PyQt6.QtWidgets import QApplication, QMessageBox

    if getattr(sys, "frozen", False):
        # Fix for Qt plugins path when frozen with PyInstaller 6+ and PyArmor
        exe_dir = os.path.dirname(sys.executable)
        # Struttura standard PyInstaller 6+: _internal/PyQt6/Qt6/plugins
        plugin_path = os.path.join(exe_dir, "_internal", "PyQt6", "Qt6", "plugins")
        if os.path.exists(plugin_path):
            QCoreApplication.addLibraryPath(plugin_path)

        # Fallback per icone se PROJECT_ROOT non è impostato correttamente in ResourceManager
        os.environ["QT_SVG_ICON_DIR"] = os.path.join(
            exe_dir, "_internal", "assets", "icons"
        )

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
