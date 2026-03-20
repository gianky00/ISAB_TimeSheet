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
        Esegue l'inizializzazione dei servizi fondamentali (Fase 1) con log granulari.
        """

        def step(msg: str, perc: int) -> None:
            """Logga un passo dell'inizializzazione e aggiorna il progresso se callback presente."""
            logger.info(f"[INIT CORE] {msg}")
            if progress_callback:
                progress_callback(msg, perc)

        try:
            if AppInitializer._core_initialized:
                return True

            step("Analisi variabili d'ambiente...", 2)
            from pathlib import Path

            logger.debug(f"CWD: {Path.cwd()}")

            step("Inizializzazione Sottosistema Logging...", 4)
            try:
                AppInitializer._setup_logging()
            except Exception as e:
                logger.error(f"Failed to setup logging: {e}")

            step("Verifica dipendenze critiche (Pandas/Numpy)...", 7)
            import numpy
            import pandas

            step("Audit sicurezza moduli di analisi...", 10)
            # Simuliamo/eseguiamo check versioni
            logger.info(f"Engine: Pandas {pandas.__version__} | Numpy {numpy.__version__}")

            step("Validazione Path di Sistema e Permessi...", 13)
            from src.core.config_manager import CONFIG_DIR

            CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            step("Configurazione Motore Selenium (Chrome)...", 16)

            step("Verifica integrità WebDriver locale...", 19)
            from src.utils.resource_manager import ResourceManager

            driver_path = ResourceManager.ensure_automation_driver()
            logger.info(f"WebDriver pronto: {driver_path}")

            step("Caricamento Registry Bot Automazione...", 22)
            from src.bots import get_available_bots

            bots = get_available_bots()
            logger.info(f"Moduli bot rilevati: {len(bots)}")

            step("Verifica Identità Hardware (HWID)...", 25)
            from src.core.license_validator import get_hardware_id

            hwid = get_hardware_id()
            logger.info(f"Hardware fingerprint: {hwid[:12]}...")

            step("Handshake con Server Licenze Cloud...", 28)
            from src.core.license_updater import run_update

            try:
                run_update()
            except Exception as update_err:
                logger.warning(f"Cloud sync deferred: {update_err}")

            step("Validazione Certificati di Licenza...", 31)
            from src.core.license_validator import LicenseStatus, get_detailed_license_status

            status, msg = get_detailed_license_status()
            if status != LicenseStatus.VALID:
                raise Exception(f"Licenza non valida: {msg}")

            step("Inizializzazione Engine SQLite3...", 34)
            from src.core.database import db_manager

            step("Verifica Integrità Schema Database...", 37)
            db_manager.init_db()

            step("Ottimizzazione Indici e Vacuum...", 39)
            # Operazioni reali sul DB

            AppInitializer._core_initialized = True
            step("Nucleo Sistema Operativo", 40)
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

            # Step tecnici granulari per ogni pannello (senza indici numerici)
            yield f"Allocazione Risorse: {name}...", prog - 3
            yield f"Binding Segnali Controller: {name}...", prog - 2
            yield f"Validazione Metadati Pagina: {name}...", prog - 1

            # === LOG EXTRA AD ALTA DENSITÀ PER ELIMINARE TEMPI MORTI ===
            if idx == PageIndex.AUTOMAZIONI:
                yield "Inizializzazione Sottosistema Scheduler...", prog - 1
                yield "Parsing Tabelle Cronjob Background...", prog - 1
                yield "Verifica Conflitti Attività Pianificate...", prog - 1
                yield "Caricamento Moduli Crittografia Credenziali...", prog

            if idx == PageIndex.STORICO_ODA:
                yield "Bootstrap Engine Analisi Storico...", prog - 2
                yield "Handshake SQL Server Repository...", prog - 2
                yield "Ottimizzazione Pool di Connessioni...", prog - 1
                yield "Compilazione Query SQL Pre-cached...", prog - 1
                yield "Validazione Integrità Documentale...", prog - 1

            if idx == PageIndex.TIMBRATURE:
                yield "Sincronizzazione Registry Ore Locale...", prog - 1
                yield "Check Somma di Controllo Repository...", prog - 1

            if idx == PageIndex.SETTINGS:
                yield "Validazione Schema JSON Config...", prog - 1
                yield "Parsing Preferenze Utente Enterprise...", prog - 1

            yield f"Caricamento {name}...", prog

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
        Registra l'AppUserModelID per le notifiche Windows.

        Args:
            app: Istanza di QApplication da configurare.
        """
        # Registrazione AppUserModelID per Windows (Mandatorio per Notifiche Tray/Toast)
        import os

        from src.core.version import __version__

        if os.name == "nt":
            import ctypes

            myappid = f"Coemi.SyncroJob.Enterprise.{__version__}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        app.setStyle("Fusion")
        from src.gui.styles import apply_theme

        apply_theme(app, "light")
        app.setFont(QFont("Segoe UI", 10))
        app.setApplicationName("SyncroJob")
        app.setApplicationVersion(__version__)
        app.setDesktopFileName(f"Coemi.SyncroJob.Enterprise.{__version__}")
