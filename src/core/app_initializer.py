"""
App Initializer con yield frequenti per animazioni fluide.
"""


from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src.core.logging import get_logger

logger = get_logger("AppInitializer")


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
            try:
                AppInitializer._setup_logging()
            except Exception as e:
                logger.error(f"Failed to setup logging: {e}")
                # Continue with fallback logging

            step("Caricamento Motori Analisi Dati")
            try:
                import numpy  # noqa
                import pandas  # noqa
                logger.info("Pandas/Numpy loaded successfully")
            except ImportError as e:
                logger.critical(f"CRITICAL: Missing data analysis libraries: {e}")
                return False
            except Exception as e:
                logger.critical(f"Error loading data engines: {e}")
                return False

            step("Configurazione Driver Automazione")
            try:
                import selenium  # noqa
                logger.info("Selenium loaded successfully")
            except ImportError as e:
                logger.critical(f"CRITICAL: Missing selenium library: {e}")
                return False

            step("Verifica Integrità Hardware")
            try:
                from src.core.license_updater import run_update
                from src.core.license_validator import (
                    LicenseStatus,
                    get_detailed_license_status,
                )

                status, _msg = get_detailed_license_status()
                logger.info(f"License status: {status}")
                if status != LicenseStatus.VALID:
                    step("Sincronizzazione Licenza Cloud")
                    run_update()
            except Exception as e:
                logger.error(f"License check failed: {e}")
                # We might want to continue or stop here depending on business rules
                # For now, let's keep going if it's not a critical import error

            step("Connessione Database Sistema")
            try:
                from src.core.database import db_manager
                db_manager.init_db()
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.critical(f"Database initialization failed: {e}")
                return False

            AppInitializer._core_initialized = True
            logger.info("Core initialization completed successfully")
            return True

        except Exception as e:
            logger.critical(f"Unexpected startup error: {e}", exc_info=True)
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
                logger.info(f"Loading panel {name} (index {idx})...")
                mw_instance.navigation_controller.get_panel(idx)
                logger.info(f"Panel {name} loaded successfully")
            except Exception as e:
                logger.error(f"Error loading panel {name} (index {idx}): {e}", exc_info=True)
                # Continue anyway - app should still work without this panel

        yield "Monitoraggio Sicurezza Telegram", 94
        config = config_manager.load_config()
        if not config.get("telegram_chat_id") and not config.get("telegram_pairing_code"):
            import secrets

            code = str(secrets.randbelow(900000) + 100000)
            config_manager.set_config_value("telegram_pairing_code", code)

        yield "Sistema Pronto", 100

    @staticmethod
    def _setup_logging():
        """Configura il sistema di logging enterprise."""
        try:
            from src.core.logging import configure_logging

            # Configura il nuovo sistema enterprise
            configure_logging()

            # Reindirizza anche i logger standard per compatibilità
            import logging

            logging.getLogger().setLevel(logging.INFO)

        except Exception as e:
            # Fallback al logging base se il nuovo sistema fallisce
            import logging

            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            logging.getLogger().warning(f"Failed to initialize enterprise logging: {e}")

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
