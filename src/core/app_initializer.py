"""
App Initializer con yield frequenti per animazioni fluide.
"""

import logging
import logging.handlers
import time
from typing import Callable, Optional

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

logger = logging.getLogger("AppInitializer")


def _yield():
    """Cede il controllo alla GUI per animazioni fluide."""
    app = QApplication.instance()
    if app:
        app.processEvents()


class AppInitializer:
    """Gestisce la sequenza di avvio."""

    _core_initialized = False

    @staticmethod
    def initialize(
        status_callback: Optional[Callable[[str, int], None]] = None, mw_instance=None
    ):
        """Esegue l'inizializzazione."""

        def step(msg, prog):
            """Report initialization progress step."""
            if status_callback:
                status_callback(msg, prog)
            logger.info(f"[INIT] {msg} ({prog}%)")

        try:
            if not mw_instance and not AppInitializer._core_initialized:
                # === FASE 1: MODULI CORE (può girare in thread) ===

                step("Inizializzazione Nucleo Sistema", 5)
                AppInitializer._setup_logging()

                step("Caricamento Motori Analisi Dati", 10)
                import pandas  # noqa
                import numpy  # noqa

                step("Configurazione Driver Automazione", 18)
                import selenium  # noqa

                step("Verifica Integrità Hardware", 22)
                from src.core.license_updater import run_update
                from src.core.license_validator import (
                    LicenseStatus,
                    get_detailed_license_status,
                )

                status, msg = get_detailed_license_status()
                if status != LicenseStatus.VALID:
                    step("Sincronizzazione Licenza Cloud", 26)
                    run_update()

                step("Connessione Database Sistema", 32)
                from src.core.database import db_manager

                db_manager.init_db()

                AppInitializer._core_initialized = True
                return True

            elif mw_instance:
                # === FASE 2: PRELOAD GUI (deve restare nel thread principale) ===
                from src.gui.main_window.page_index import PageIndex

                _yield()

                tasks = [
                    (PageIndex.DASHBOARD, "Preparazione Dashboard"),
                    (PageIndex.TIMBRATURE, "Caricamento Repository Ore"),
                    (PageIndex.STRUMENTALE, "Registro Asset Aziendali"),
                    (PageIndex.DATAEASE, "DataEase Sync Bridge"),
                    (PageIndex.ANAGRAFICHE, "Directory Personale"),
                    (PageIndex.DIPENDENTI, "Gestione Schede Dipendenti"),
                    (PageIndex.AUTOMAZIONI, "Scheduler Attività"),
                    (PageIndex.LYRA, "Motore Analisi Lyra"),
                    (PageIndex.SETTINGS, "Configurazione Utente"),
                ]

                base_prog = 45
                for i, (idx, name) in enumerate(tasks):
                    prog = base_prog + int((i / len(tasks)) * 45)
                    step(name, prog)
                    _yield()

                    # Carica il pannello
                    mw_instance.navigation_controller.get_panel(idx)
                    _yield()

                    # Micro-pausa per permettere refresh animazioni
                    time.sleep(0.008)
                    _yield()

                step("Monitoraggio Sicurezza Telegram", 94)
                _yield()
                from src.core import config_manager

                config = config_manager.load_config()
                if not config.get("telegram_chat_id") and not config.get(
                    "telegram_pairing_code"
                ):
                    import random

                    code = str(random.randint(100000, 999999))
                    config_manager.set_config_value("telegram_pairing_code", code)
                _yield()

                step("Sistema Pronto", 100)
                return True

            return True

        except Exception as e:
            logger.critical(f"Startup error: {e}")
            return False

    @staticmethod
    def _setup_logging():
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
    def setup_app_style(app):
        """Configure application style, theme, font and metadata."""
        from src.core.version import __version__

        app.setStyle("Fusion")
        from src.gui.styles import apply_theme

        apply_theme(app, "light")
        app.setFont(QFont("Segoe UI", 10))
        app.setApplicationName("SyncroJob")
        app.setApplicationVersion(__version__)
