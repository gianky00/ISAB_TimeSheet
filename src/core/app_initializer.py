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
            if status != LicenseStatus.VALID:
                run_update()
                status, msg = get_detailed_license_status()

            if status != LicenseStatus.VALID:
                grace_allowed, grace_msg, _ = check_emergency_grace_period()
                hw_id = get_hardware_id()
                if grace_allowed:
                    QMessageBox.warning(
                        None,
                        "Licenza - Modalità Provvisoria",
                        f"{grace_msg}\n\nID: {hw_id}",
                    )
                    return True
                else:
                    QMessageBox.critical(
                        None,
                        "Errore Licenza",
                        f"Licenza non valida.\n\n{msg}\nID: {hw_id}",
                    )
                    return False
            return True
        except Exception as e:
            logger.error(f"Errore licenza: {e}")
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
