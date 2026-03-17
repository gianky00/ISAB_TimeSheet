"""
SyncroJob - App Initializer
Gestisce il ciclo di vita dell'avvio dell'applicazione, suddividendolo in fasi atomiche:
1. Inizializzazione del Nucleo (Database, Logging, Driver).
2. Caricamento Lazy dei Pannelli GUI.
3. Configurazione dello stile e dei metadati dell'applicazione.
Include meccanismi di yield per garantire la reattività dell'interfaccia durante il caricamento.
"""

from collections.abc import Callable
from typing import ClassVar

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src.core.logging import get_logger

logger = get_logger("AppInitializer")


def _yield() -> None:
    """Cede il controllo all'event loop di Qt per processare eventi pendenti e mantenere fluida la UI."""
    app = QApplication.instance()
    if app:
        app.processEvents()


class AppInitializer:
    """
    Orchestratore della sequenza di bootstrap dell'intero sistema.
    Fornisce metodi statici per la configurazione dei servizi core e il caricamento progressivo della GUI.
    """

    _core_initialized = False
    _startup_alerts: ClassVar[list[tuple[str, str]]] = []  # List of (severity, message)

    @staticmethod
    def add_alert(severity: str, message: str) -> None:
        """Aggiunge un avviso da mostrare all'utente all'avvio."""
        AppInitializer._startup_alerts.append((severity, message))

    @staticmethod
    def get_alerts() -> list[tuple[str, str]]:
        """Restituisce gli avvisi accumulati durante l'avvio."""
        return AppInitializer._startup_alerts

    @staticmethod
    def initialize_core(progress_callback: Callable[[str, int], None] | None = None) -> bool:
        """
        Esegue l'inizializzazione dei servizi fondamentali (Fase 1).
        Verifica la presenza delle librerie necessarie (Pandas, Selenium), configura il logging enterprise,
        connette il database e valida lo stato della licenza.

        Args:
            progress_callback: Funzione opzionale (msg, perc) per aggiornare lo splash screen.

        Returns:
            bool: True se l'inizializzazione core è terminata con successo, False altrimenti.
        """

        def step(msg: str, perc: int) -> None:
            """Logga un passo dell'inizializzazione e aggiorna il progresso se callback presente."""
            logger.info(f"[INIT CORE] {msg}")
            if progress_callback:
                progress_callback(msg, perc)

        try:
            if AppInitializer._core_initialized:
                return True

            step("Inizializzazione Nucleo Sistema", 5)
            try:
                AppInitializer._setup_logging()
            except Exception as e:
                logger.error(f"Failed to setup logging: {e}")

            step("Caricamento Motori Analisi Dati", 10)
            try:
                import numpy  # noqa
                import pandas  # noqa
                logger.info("Pandas/Numpy loaded successfully")
            except ImportError as e:
                msg = f"Librerie di analisi dati mancanti: {e}"
                logger.critical(f"CRITICAL: {msg}")
                raise Exception(msg) from e

            step("Configurazione Driver Automazione", 15)
            try:
                import selenium  # noqa
                from src.utils.resource_manager import ResourceManager

                # Pre-warming Webdriver (Verifica path e aggiornamento silente)
                ResourceManager.ensure_automation_driver()

                logger.info("Selenium loaded successfully")
            except ImportError as e:
                msg = f"Libreria Selenium mancante: {e}"
                logger.critical(f"CRITICAL: {msg}")
                raise Exception(msg) from e

            step("Pre-caricamento Motori Automazione", 20)
            try:
                # Importiamo preventivamente il factory dei bot per caricare tutti i sottomoduli
                from src.bots import create_bot, get_available_bots  # noqa
                logger.info("Automation bots engines pre-loaded")
            except Exception as e:
                logger.warning(f"Errore non-bloccante pre-caricamento bot: {e}")

            step("Verifica Integrità Hardware", 25)
            try:
                from src.core.license_updater import run_update
                from src.core.license_validator import (
                    LicenseStatus,
                    get_detailed_license_status,
                )

                step("Sincronizzazione Licenza Cloud", 30)
                try:
                    run_update()
                except Exception as update_err:
                    if "REVOCATA" in str(update_err):
                        raise
                    logger.warning(f"License update failed (non-blocking): {update_err}")

                status, msg = get_detailed_license_status()
                if status != LicenseStatus.VALID:
                    logger.critical(f"License check failed: {msg}")
                    raise Exception(f"Licenza non valida: {msg}")

            except Exception as e:
                # Blocchiamo SEMPRE l'avvio se la licenza non è valida o è stata revocata
                raise e

            step("Connessione Database Sistema", 35)
            try:
                from src.core.database import db_manager

                db_manager.init_db()
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.critical(f"Database initialization failed: {e}")
                raise Exception(f"Errore Database: {e}") from e

            AppInitializer._core_initialized = True
            step("Nucleo Inizializzato", 40)
            return True

        except Exception as e:
            # Se è un'eccezione esplicita di licenza o database che abbiamo già loggato e "formattato", la rilanciamo
            if any(x in str(e) for x in ("REVOCATA", "Licenza non valida", "Errore Database")):
                raise

            # Per errori imprevisti, logghiamo tutto e rilanciamo con un messaggio leggibile
            logger.critical(f"Unexpected startup error: {e}", exc_info=True)
            raise Exception(f"Errore imprevisto durante l'avvio: {e}") from e

    @staticmethod
    def init_generator(mw_instance):
        """
        Generatore Python per l'inizializzazione progressiva della GUI (Fase 2).
        Carica i pannelli principali in modalità differita per non bloccare lo splash screen.

        Args:
            mw_instance: Istanza di MainWindow su cui caricare i pannelli.

        Yields:
            tuple: (nome_task, percentuale_progresso).
        """
        from src.core import config_manager
        from src.gui.main_window.page_index import PageIndex

        tasks = [
            (PageIndex.DASHBOARD, "Preparazione Dashboard"),
            (PageIndex.AUTOMAZIONI, "Scheduler Attività"),
            (PageIndex.STORICO_ODA, "Archivio Storico OdA"),
            (PageIndex.TIMBRATURE, "Caricamento Repository Ore"),
            (PageIndex.STRUMENTALE, "Registro Asset Aziendali"),
            (PageIndex.NOTIFICATIONS, "Centro Notifiche"),
            (PageIndex.DATAEASE, "DataEase Sync Bridge"),
            (PageIndex.ANAGRAFICHE, "Directory Personale"),
            (PageIndex.SETTINGS, "Configurazione Utente"),
            (PageIndex.DIPENDENTI, "Gestione Schede Dipendenti"),
            (PageIndex.HELP, "Manuale Operativo"),
        ]

        import time

        from PyQt6.QtWidgets import QApplication

        base_prog = 45
        total = len(tasks)

        for i, (idx, name) in enumerate(tasks):
            prog = base_prog + int((i / total) * 45)
            yield name, prog

            start_time = time.perf_counter()
            logger.info(f"[UI STARTUP] Loading panel: {name}...")

            try:
                mw_instance.navigation_controller.get_panel(idx)
                elapsed = (time.perf_counter() - start_time) * 1000
                logger.info(f"[UI STARTUP] Panel {name} loaded in {elapsed:.2f}ms")
            except Exception as e:
                logger.error(f"Error loading panel {name}: {e}", exc_info=True)

            # Una sola chiamata per processare eventuali segnali interni dei widget
            QApplication.processEvents()

        yield "Monitoraggio Sicurezza Telegram", 94
        config = config_manager.load_config()
        if not config.get("telegram_chat_id") and not config.get("telegram_pairing_code"):
            import secrets

            code = str(secrets.randbelow(900000) + 100000)
            config_manager.set_config_value("telegram_pairing_code", code)

        yield "Sistema Pronto", 100

    @staticmethod
    def _setup_logging() -> None:
        """Configura il sistema di logging applicativo, tentando di attivare il modulo enterprise."""
        try:
            from src.core.logging import configure_logging

            configure_logging()
            import logging

            logging.getLogger().setLevel(logging.INFO)
        except Exception as e:
            import logging

            logging.basicConfig(
                level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            logging.getLogger().warning(f"Failed to initialize enterprise logging: {e}")

    @staticmethod
    def setup_app_style(app: QApplication) -> None:
        """
        Configura l'aspetto visivo e i metadati dell'applicazione.
        Imposta il tema Fusion, il font di sistema Segoe UI e la versione dell'app.

        Args:
            app: Istanza di QApplication da configurare.
        """
        from src.core.version import __version__

        app.setStyle("Fusion")
        from src.gui.styles import apply_theme

        apply_theme(app, "light")
        app.setFont(QFont("Segoe UI", 10))
        app.setApplicationName("SyncroJob")
        app.setApplicationVersion(__version__)
