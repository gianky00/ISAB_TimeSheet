#!/usr/bin/env python3
"""
Bot TS - Sistema di Automazione Portale ISAB
Entry point principale dell'applicazione.
"""
import sys
import os

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
    
    # Create application first to allow message boxes
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
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
