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
        # 0. Setup Logging (CRITICAL: Prima di tutto il resto)
        AppInitializer._setup_logging()

        # 1. Licenza
        if not AppInitializer._check_license():
            sys.exit(1)

        # 2. Database
        if not AppInitializer._init_db():
            sys.exit(1)

        # 3. Sicurezza Telegram
        AppInitializer._init_telegram_security()

        return True

    @staticmethod
    def _setup_logging():
        """Configura il logging su file rotativo."""
        from logging.handlers import RotatingFileHandler
        from pathlib import Path
        from src.core import config_manager

        log_dir = Path(config_manager.get_logs_path())
        log_file = log_dir / "application.log"

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Handler Rotativo (5MB x 3 backup)
        handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        handler.setFormatter(formatter)

        # Root Logger config
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Evita duplicati se reload
        if not any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
            root_logger.addHandler(handler)
            logger.info(f"Logging inizializzato su: {log_file}")
        
        # Console Handler (opzionale, se non c'è già)
        if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            root_logger.addHandler(console)


    @staticmethod
    def _init_telegram_security():
        """Genera un codice di accoppiamento se Telegram non è configurato."""
        import random

        from src.core import config_manager

        config = config_manager.load_config()
        if not config.get("telegram_chat_id"):
            # Genera un codice a 6 cifre se non esiste già un pairing pendente
            if not config.get("telegram_pairing_code"):
                code = str(random.randint(100000, 999999))
                config_manager.set_config_value("telegram_pairing_code", code)
                logger.info(f"Generato nuovo pairing code Telegram: {code}")
            else:
                logger.info(
                    f"Pairing code Telegram esistente: {config.get('telegram_pairing_code')}"
                )

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
