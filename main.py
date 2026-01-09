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

# Ensure src is in path
if getattr(sys, "frozen", False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(base_path, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


def main():
    """Main entry point."""
    from PyQt6.QtGui import QFont
    from PyQt6.QtWidgets import QApplication, QMessageBox

    from src.gui.styles import apply_theme

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    apply_theme(app, "light")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    app.setApplicationName("SyncroJob")
    app.setOrganizationName("Giancarlo Allegretti")
    app.setApplicationVersion("1.0.0")

    # === LICENSE CHECK FLOW ===
    try:
        from src.core.license_updater import check_emergency_grace_period, run_update
        from src.core.license_validator import (
            LicenseStatus,
            get_detailed_license_status,
            get_hardware_id,
        )

        status, msg = get_detailed_license_status()

        if status != LicenseStatus.VALID:
            run_update()
            status, msg = get_detailed_license_status()

        if status != LicenseStatus.VALID:
            grace_allowed, grace_msg, days_left = check_emergency_grace_period()
            hw_id = get_hardware_id()

            if grace_allowed:
                QMessageBox.warning(
                    None,
                    "Licenza non trovata - Modalità Provvisoria",
                    f"Licenza non rilevata o non valida.\n\n{grace_msg}\n\nID Hardware: {hw_id}",
                )
            else:
                QMessageBox.critical(
                    None,
                    "Errore Licenza",
                    f"Licenza non valida e periodo di prova scaduto.\n\nErrore: {msg}\nID Hardware: {hw_id}",
                )
                sys.exit(1)

    except Exception as e:
        QMessageBox.critical(None, "Errore Critico", f"Impossibile verificare la licenza.\n{e}")
        sys.exit(1)

    # === DATABASE INITIALIZATION ===
    from src.core.database import db_manager
    try:
        db_manager.init_db()
    except Exception as e:
        QMessageBox.critical(
            None, 
            "Errore Database", 
            f"Impossibile inizializzare il database.\nL'applicazione verrà chiusa.\n\nErrore: {e}"
        )
        sys.exit(1)

    # === START GUI ===
    from src.gui.main_window import MainWindow
    try:
        window = MainWindow()
        window.showMaximized()
    except Exception as e:
        logger.critical("Errore avvio MainWindow", exc_info=True)
        QMessageBox.critical(None, "Errore GUI", f"Errore fatale durante l'avvio dell'interfaccia:\n{e}")
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
