"""
App Initializer con yield frequenti per animazioni fluide.
"""

import logging
import logging.handlers

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
    def initialize_core():
        """Esegue l'inizializzazione del nucleo (Fase 1)."""

        def step(msg):
            logger.info(f"[INIT CORE] {msg}")

        try:
            if AppInitializer._core_initialized:
                return True

            step("Inizializzazione Nucleo Sistema")
            AppInitializer._setup_logging()

            step("Caricamento Motori Analisi Dati")
            import pandas  # noqa
            import numpy  # noqa

            step("Configurazione Driver Automazione")
            import selenium  # noqa

            step("Verifica Integrità Hardware")
            from src.core.license_updater import run_update
            from src.core.license_validator import (
                LicenseStatus,
                get_detailed_license_status,
            )

            status, msg = get_detailed_license_status()
            if status != LicenseStatus.VALID:
                step("Sincronizzazione Licenza Cloud")
                run_update()

            step("Connessione Database Sistema")
            from src.core.database import db_manager

            db_manager.init_db()

            AppInitializer._core_initialized = True
            return True

        except Exception as e:
            logger.critical(f"Startup error: {e}")
            return False

    @staticmethod
    def init_generator(mw_instance):
        """Generatore per l'inizializzazione GUI a step (Fase 2)."""

        from src.core import config_manager
        from src.gui.main_window.page_index import PageIndex

        # IMPORTANT: PageIndex enum values (corrected to match current definition)
        # DASHBOARD=0, AUTOMAZIONI=1, LYRA=2, TIMBRATURE=3, STRUMENTALE=4,
        # DATAEASE=5, ANAGRAFICHE=6, SETTINGS=7, HELP=8, NOTIFICATIONS=9,
        # STORICO_ODA=10, DIPENDENTI=11

        tasks = [
            (PageIndex.DASHBOARD, "Preparazione Dashboard"),
            (PageIndex.AUTOMAZIONI, "Scheduler Attività"),
            (PageIndex.LYRA, "Motore Analisi Lyra"),
            (PageIndex.TIMBRATURE, "Caricamento Repository Ore"),
            (PageIndex.STRUMENTALE, "Registro Asset Aziendali"),
            (PageIndex.DATAEASE, "DataEase Sync Bridge"),
            (PageIndex.ANAGRAFICHE, "Directory Personale"),
            (PageIndex.SETTINGS, "Configurazione Utente"),
            (PageIndex.DIPENDENTI, "Gestione Schede Dipendenti"),
        ]

        base_prog = 45
        total = len(tasks)

        for i, (idx, name) in enumerate(tasks):
            prog = base_prog + int((i / total) * 45)
            # Yield control to main loop
            yield name, prog

            # Heavy task - load panel with error handling
            try:
                import logging

                logger = logging.getLogger("AppInitializer")
                logger.info(f"Loading panel {name} (index {idx})...")
                mw_instance.navigation_controller.get_panel(idx)
                logger.info(f"Panel {name} loaded successfully")
            except Exception as e:
                import logging

                logger = logging.getLogger("AppInitializer")
                logger.error(
                    f"Error loading panel {name} (index {idx}): {e}", exc_info=True
                )
                # Continue anyway - app should still work without this panel

        yield "Monitoraggio Sicurezza Telegram", 94
        config = config_manager.load_config()
        if not config.get("telegram_chat_id") and not config.get(
            "telegram_pairing_code"
        ):
            import random

            code = str(random.randint(100000, 999999))
            config_manager.set_config_value("telegram_pairing_code", code)

        yield "Sistema Pronto", 100

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
