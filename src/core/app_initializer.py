import logging
import logging.handlers
import sys
import traceback
from typing import Callable, Optional

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
    def initialize(status_callback: Optional[Callable[[str, int], None]] = None):
        """
        Esegue tutti i controlli necessari prima di mostrare la GUI.
        
        Args:
            status_callback: Funzione(messaggio, progresso) per aggiornare la UI di caricamento.
        """
        def update(msg, prog):
            if status_callback:
                status_callback(msg, prog)
            logger.info(f"[INIT] {msg} ({prog}%)")

        try:
            # 0. Setup Logging
            update("Configurazione sistema di logging...", 20)
            AppInitializer._setup_logging()

            # 1. Licenza
            update("Verifica licenza in corso...", 40)
            if not AppInitializer._check_license(status_callback):
                return False

            # 2. Database
            update("Inizializzazione database locale...", 70)
            if not AppInitializer._init_db():
                return False

            # 3. Sicurezza Telegram
            update("Sincronizzazione sicurezza Telegram...", 90)
            AppInitializer._init_telegram_security()

            update("Avvio applicazione...", 100)
            return True

        except Exception as e:
            logger.critical(f"Errore fatale inizializzazione: {e}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(None, "Errore Inizializzazione", 
                                f"Si è verificato un errore durante l'avvio:\n{e}")
            return False

    @staticmethod
    def _setup_logging():
        """Configura il logging su file rotativo."""
        from pathlib import Path
        from src.core import config_manager

        log_dir = Path(config_manager.get_logs_path())
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "application.log"

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        if not any(
            isinstance(h, logging.handlers.RotatingFileHandler)
            for h in root_logger.handlers
        ):
            root_logger.addHandler(handler)

    @staticmethod
    def _init_telegram_security():
        """Genera un codice di accoppiamento se Telegram non è configurato."""
        import random
        from src.core import config_manager

        config = config_manager.load_config()
        if not config.get("telegram_chat_id"):
            if not config.get("telegram_pairing_code"):
                code = str(random.randint(100000, 999999))
                config_manager.set_config_value("telegram_pairing_code", code)

    @staticmethod
    def _check_license(status_callback=None):
        try:
            status, msg = get_detailed_license_status()

            if status != LicenseStatus.VALID:
                if status_callback:
                    status_callback("Tentativo ripristino licenza online...", 50)
                run_update()
                status, msg = get_detailed_license_status()

            if status != LicenseStatus.VALID:
                grace_allowed, grace_msg, remaining = check_emergency_grace_period()
                hw_id = get_hardware_id()

                if grace_allowed:
                    return True
                else:
                    QMessageBox.critical(
                        None,
                        "Errore Licenza",
                        f"Licenza non valida.\n\n{msg}\n\nID Hardware: {hw_id}",
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
            return False

    @staticmethod
    def setup_app_style(app):
        """Configura font e tema."""
        from src.core.version import __version__
        app.setStyle("Fusion")
        apply_theme(app, "light")
        app.setFont(QFont("Segoe UI", 10))
        app.setApplicationName("SyncroJob")
        app.setOrganizationName("Giancarlo Allegretti")
        app.setApplicationVersion(__version__)
