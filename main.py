#!/usr/bin/env python3
"""
# SyncroJob - Sistema di Automazione Portale ISABEntry point principale dell'applicazione.
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
    # Prima logga l'eccezione come al solito
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

    # Ora copia il file di log nella root del progetto
    try:
        log_file = CONFIG_DIR / "logs" / "crash.log"
        if log_file.exists():
            # Costruisce il percorso di destinazione nella root del progetto
            # __file__ si riferisce a main.py, .parent ci dà la root
            project_root = Path(__file__).parent
            dest_file = project_root / "crash.log"

            shutil.copy2(log_file, dest_file)
            logger.info(f"Copia del crash log salvata in: {dest_file}")
    except Exception as e:
        logger.error(f"Impossibile copiare il crash log nella root: {e}")

def setup_crash_logging():
    """Configura il logging per i crash e installa l'exception hook."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)

    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "crash.log"

    # Configurazione del logger
    # 'w' per sovrascrivere a ogni avvio, così abbiamo solo il log del crash più recente
    handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger("crash_logger")
    if not logger.handlers:
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Log delle informazioni di sistema all'avvio
    logger.info(f"Crash Logger inizializzato. File: {log_file}")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Eseguibile: {sys.executable}")
    logger.info(f"Piattaforma: {sys.platform}")

    # Installa il gestore di eccezioni globale
    sys.excepthook = handle_exception
    logger.info("Exception hook installato.")


# Attiva logging immediatamente
setup_crash_logging()
print("[DEBUG] Crash logging setup complete")

# Ensure src is in path
if getattr(sys, "frozen", False):
    # Running as compiled executable
    base_path = os.path.dirname(sys.executable)
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(base_path, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"[DEBUG] base_path: {base_path}")
print(f"[DEBUG] src_path: {src_path}")

def main():
    """Main entry point."""
    print("[DEBUG] Entering main()")
    # Import PyQt6 components
    try:
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QApplication, QMessageBox
        print("[DEBUG] PyQt6 imports successful")
    except Exception as e:
        print(f"[DEBUG] PyQt6 imports failed: {e}")
        return

    try:
        from src.gui.styles import apply_theme
        print("[DEBUG] src.gui.styles import successful")
    except Exception as e:
        print(f"[DEBUG] src.gui.styles import failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Create application first to allow message boxes
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    apply_theme(app, "light")  # Default to light theme for now

    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Set application metadata
    app.setApplicationName("SyncroJob")
    app.setOrganizationName("Giancarlo Allegretti")
    app.setApplicationVersion("1.0.0")

    # === LICENSE CHECK FLOW ===
    print("[DEBUG] Starting license check")
    try:
        from src.core.license_updater import check_emergency_grace_period, run_update
        from src.core.license_validator import (
            LicenseStatus,
            get_detailed_license_status,
            get_hardware_id,
        )

        status, msg = get_detailed_license_status()
        print(f"[DEBUG] License status: {status}, msg: {msg}")

        # Se la licenza non è valida, proviamo a scaricarla di nuovo
        if status != LicenseStatus.VALID:
            print(f"[LICENZA] Stato: {status.name} ({msg}). Tentativo aggiornamento...")
            run_update()  # Forza il download
            status, msg = get_detailed_license_status()  # Ricontrolla

        # Se ancora non valida, gestiamo i casi
        if status != LicenseStatus.VALID:

            # Verifichiamo il periodo di grazia (3 giorni)
            grace_allowed, grace_msg, days_left = check_emergency_grace_period()

            hw_id = get_hardware_id()

            if grace_allowed:
                # Avviso grazia attiva
                QMessageBox.warning(
                    None,
                    "Licenza non trovata - Modalità Provvisoria",
                    f"Licenza non rilevata o non valida.\n\n"
                    f"{grace_msg}\n\n"
                    f"ID Hardware: {hw_id}\n\n"
                    "Contatta l'amministratore per ottenere una licenza valida.\n"
                    "L'applicazione continuerà a funzionare per il periodo rimanente.",
                )
            else:
                # Blocco totale
                QMessageBox.critical(
                    None,
                    "Errore Licenza",
                    f"Licenza non valida e periodo di prova scaduto.\n\n"
                    f"Errore: {msg}\n"
                    f"ID Hardware: {hw_id}\n\n"
                    "L'applicazione verrà chiusa. Contatta l'amministratore.",
                )
                sys.exit(1)

    except Exception as e:
        # Fallback di sicurezza in caso di crash del controllo licenza
        # Nota: questo viene catturato qui, ma se crasha prima (es. import) interviene l'excepthook
        print(f"[DEBUG] License check exception: {e}")
        QMessageBox.critical(None, "Errore Critico", f"Impossibile verificare la licenza.\n{e}")
        sys.exit(1)

    # === START APP ===
    print("[DEBUG] Importing db_manager and MainWindow")
    try:
        from src.core.database import db_manager
        print("[DEBUG] db_manager imported")
        from src.gui.main_window import MainWindow
        print("[DEBUG] MainWindow imported")
    except Exception as e:
        print(f"[DEBUG] Import failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Inizializza schema database (Contabilità, Timbrature, ecc.)
    try:
        print("[DEBUG] Initializing database")
        db_manager.init_db()
        print("[DEBUG] Database initialized")
    except Exception as e:
        print(f"[DATABASE] Errore inizializzazione: {e}")

    try:
        print("[DEBUG] Creating MainWindow instance")
        window = MainWindow()
        print("[DEBUG] Showing MainWindow")
        window.showMaximized()
    except Exception as e:
        print(f"[DEBUG] Failed to create or show MainWindow: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Run event loop
    print("[DEBUG] Entering event loop")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
