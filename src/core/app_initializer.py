import logging
import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMessageBox

from src.core.database import db_manager
from src.core.license_updater import check_emergency_grace_period, run_update
from src.core.license_validator import (
    LicenseStatus,
    get_detailed_license_status,
    get_hardware_id,
)
from src.gui.styles import apply_theme

logger = logging.getLogger("AppInitializer")


class AppInitializer:
    """Gestisce la sequenza di avvio dell'applicazione."""

    @staticmethod
    def initialize():
        """Esegue tutti i controlli necessari prima di mostrare la GUI."""
        # 1. Licenza
        if not AppInitializer._check_license():
            sys.exit(1)

        # 2. Database
        if not AppInitializer._init_db():
            sys.exit(1)

        return True

    @staticmethod
    def _check_license():
        try:
            status, msg = get_detailed_license_status()

            # Se la licenza non è valida o manca, tenta l'aggiornamento online
            if status != LicenseStatus.VALID:
                logger.info(
                    "Licenza non valida o mancante. Tentativo di aggiornamento online..."
                )
                run_update()
                status, msg = get_detailed_license_status()

            # Se ancora non è valida, prova ad attivare/verificare il periodo di grazia
            if status != LicenseStatus.VALID:
                logger.warning(f"Validazione licenza fallita ({status.value}): {msg}")
                grace_allowed, grace_msg, remaining = check_emergency_grace_period()
                hw_id = get_hardware_id()

                if grace_allowed:
                    logger.info(
                        f"Accesso consentito tramite periodo di grazia: {grace_msg}"
                    )
                    QMessageBox.warning(
                        None,
                        "Licenza - Modalità Provvisoria",
                        f"⚠️ {grace_msg}\n\nL'applicazione funzionerà in modalità limitata per {remaining} giorni.\nContatta l'assistenza fornendo il seguente ID:\n\nID Hardware: {hw_id}",
                    )
                    return True
                else:
                    logger.critical(f"Accesso negato: {grace_msg}")
                    QMessageBox.critical(
                        None,
                        "Errore Licenza",
                        f"Impossibile trovare una licenza valida e il periodo di grazia è scaduto.\n\n{msg}\n\nID Hardware: {hw_id}",
                    )
                    return False

            logger.info("Licenza verificata con successo.")
            return True
        except Exception as e:
            logger.error(f"Errore critico durante il controllo licenza: {e}")
            import traceback

            logger.error(traceback.format_exc())
            return False

    @staticmethod
    def _init_db():
        try:
            db_manager.init_db()
            return True
        except Exception as e:
            logger.critical(f"Errore DB: {e}")
            QMessageBox.critical(
                None, "Errore Database", f"Impossibile inizializzare il DB:\n{e}"
            )
            return False

    @staticmethod
    def setup_app_style(app):
        """Configura font e tema."""
        app.setStyle("Fusion")
        apply_theme(app, "light")
        app.setFont(QFont("Segoe UI", 10))
        app.setApplicationName("SyncroJob")
        app.setOrganizationName("Giancarlo Allegretti")
        app.setApplicationVersion("1.0.0")
