#!/usr/bin/env python3
"""
Bot TS - Sistema di Automazione Portale ISAB
Entry point principale dell'applicazione.
"""
import sys
import os
import logging
import traceback
import ctypes
from pathlib import Path

# --- CRASH LOGGING SETUP ---
def setup_crash_logging():
    """Configura il logging per intercettare crash all'avvio."""
    # 1. Definisci percorso log (User Profile per evitare problemi permessi)
    # Usa .bot_ts come standard
    log_dir = Path.home() / ".bot_ts"
    log_file = log_dir / "crash.log"

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Fallback se non si può creare la directory (raro in USERPROFILE)
        return

    # 2. Configura Logger
    # 'w' mode sovrascrive il file ad ogni avvio come richiesto
    logging.basicConfig(
        filename=str(log_file),
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Riduci verbosità per librerie rumorose
    for lib in ["matplotlib", "PIL", "urllib3", "selenium"]:
        logging.getLogger(lib).setLevel(logging.WARNING)

    logger = logging.getLogger("CrashLogger")
    logger.info(f"Crash Logger inizializzato. File: {log_file}")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Eseguibile: {sys.executable}")
    logger.info(f"Piattaforma: {sys.platform}")

    # 3. Redirect stdout/stderr
    class StreamToLogger:
        def __init__(self, logger, level):
            self.logger = logger
            self.level = level
            self.linebuf = ''

        def write(self, buf):
            for line in buf.rstrip().splitlines():
                self.logger.log(self.level, line.rstrip())

        def flush(self):
            # Il logger gestisce il flush su file
            pass

    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)

    # 4. Exception Hook globale
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

        # Mostra Popup (Solo Windows)
        if os.name == 'nt':
            try:
                error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                # Tronca messaggio troppo lungo per il popup
                short_msg = error_msg[-1000:] if len(error_msg) > 1000 else error_msg

                ctypes.windll.user32.MessageBoxW(
                    0,
                    f"L'applicazione ha riscontrato un errore critico:\n\n...{short_msg}\n\nIl log completo è stato salvato in:\n{log_file}",
                    "Errore Critico Bot TS",
                    0x10 | 0x10000 # MB_ICONHAND | MB_SETFOREGROUND
                )
            except Exception as e:
                logger.error(f"Impossibile mostrare popup errore: {e}")

    sys.excepthook = handle_exception
    logger.info("Exception hook installato.")

# Attiva logging immediatamente
setup_crash_logging()


# Ensure src is in path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = os.path.dirname(sys.executable)
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(base_path, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def main():
    """Main entry point."""
    # Import PyQt6 components
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont, QIcon
    from src.gui.styles import apply_theme
    import src.resources_rc
    
    # Create application first to allow message boxes
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    apply_theme(app, "light") # Default to light theme for now
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Set application metadata
    app.setApplicationName("Bot TS")
    app.setOrganizationName("Giancarlo Allegretti")
    app.setApplicationVersion("1.0.0")

    # === LICENSE CHECK FLOW ===
    try:
        from src.core.license_validator import get_detailed_license_status, LicenseStatus, get_hardware_id
        from src.core.license_updater import run_update, check_emergency_grace_period

        status, msg = get_detailed_license_status()

        # Se la licenza non è valida, proviamo a scaricarla di nuovo
        if status != LicenseStatus.VALID:
            print(f"[LICENZA] Stato: {status.name} ({msg}). Tentativo aggiornamento...")
            run_update() # Forza il download
            status, msg = get_detailed_license_status() # Ricontrolla

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
                    "L'applicazione continuerà a funzionare per il periodo rimanente."
                )
            else:
                # Blocco totale
                QMessageBox.critical(
                    None,
                    "Errore Licenza",
                    f"Licenza non valida e periodo di prova scaduto.\n\n"
                    f"Errore: {msg}\n"
                    f"ID Hardware: {hw_id}\n\n"
                    "L'applicazione verrà chiusa. Contatta l'amministratore."
                )
                sys.exit(1)

    except Exception as e:
        # Fallback di sicurezza in caso di crash del controllo licenza
        # Nota: questo viene catturato qui, ma se crasha prima (es. import) interviene l'excepthook
        QMessageBox.critical(
            None,
            "Errore Critico",
            f"Impossibile verificare la licenza.\n{e}"
        )
        sys.exit(1)

    # === START APP ===
    from src.gui.main_window import MainWindow
    
    window = MainWindow()
    window.showMaximized()
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
