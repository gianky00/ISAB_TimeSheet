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
    """Gestore eccezioni globale per logging e copia del log."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

    try:
        log_file = CONFIG_DIR / "logs" / "crash.log"
        if log_file.exists():
            project_root = Path(__file__).parent
            dest_file = project_root / "crash.log"
            shutil.copy2(log_file, dest_file)
    except Exception as e:
        logger.error(f"Impossibile copiare il crash log nella root: {e}")

def setup_crash_logging():
    """Configura il logging per i crash e installa l'exception hook."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)

    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "crash.log"

    handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger("crash_logger")
    if not logger.handlers:
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    sys.excepthook = handle_exception


# Attiva logging immediatamente
setup_crash_logging()
print("[DEBUG] Logging setup")

# Ensure src is in path
if getattr(sys, "frozen", False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(base_path, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"[DEBUG] src_path: {src_path}")

def main():
    """Main entry point."""
    print("[DEBUG] main() start")
    from PyQt6.QtGui import QFont
    from PyQt6.QtWidgets import QApplication, QMessageBox

    print("[DEBUG] PyQt6 imported")
    from src.gui.styles import apply_theme
    print("[DEBUG] Styles imported")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    apply_theme(app, "light")
    print("[DEBUG] Theme applied")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    app.setApplicationName("SyncroJob")
    app.setOrganizationName("Giancarlo Allegretti")
    app.setApplicationVersion("1.0.0")

    # === LICENSE CHECK FLOW ===
    print("[DEBUG] License check...")
    try:
        from src.core.license_updater import check_emergency_grace_period, run_update
        from src.core.license_validator import (
            LicenseStatus,
            get_detailed_license_status,
            get_hardware_id,
        )

        status, msg = get_detailed_license_status()
        print(f"[DEBUG] Status: {status}")

        if status != LicenseStatus.VALID:
            run_update()
            status, msg = get_detailed_license_status()

    except Exception as e:
        print(f"[DEBUG] License error: {e}")
        QMessageBox.critical(None, "Errore Critico", f"Impossibile verificare la licenza.\n{e}")
        sys.exit(1)

    # === DATABASE INITIALIZATION ===
    print("[DEBUG] DB Init...")
    from src.core.database import db_manager
    try:
        db_manager.init_db()
        print("[DEBUG] DB Init OK")
    except Exception as e:
        print(f"[DEBUG] DB Init Error: {e}")
        QMessageBox.critical(
            None, 
            "Errore Database", 
            f"Impossibile inizializzare il database.\nL'applicazione verrà chiusa.\n\nErrore: {e}"
        )
        sys.exit(1)

    # === START GUI ===
    print("[DEBUG] GUI Start...")
    from src.gui.main_window import MainWindow
    try:
        print("[DEBUG] MainWindow instance...")
        window = MainWindow()
        print("[DEBUG] Show maximized...")
        window.showMaximized()
    except Exception as e:
        print(f"[DEBUG] GUI Error: {e}")
        import traceback
        traceback.print_exc()
        logger.critical("Errore avvio MainWindow", exc_info=True)
        QMessageBox.critical(None, "Errore GUI", f"Errore fatale durante l\'avvio dell\'interfaccia:\n{e}")
        sys.exit(1)

    print("[DEBUG] Executing app...")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()