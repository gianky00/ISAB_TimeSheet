import logging
import logging.handlers
import sys
import time
import traceback
from typing import Callable, Optional

# Import leggeri
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMessageBox, QApplication

logger = logging.getLogger("AppInitializer")


def _yield_to_gui():
    """Cede il controllo alla GUI per mantenere le animazioni fluide."""
    app = QApplication.instance()
    if app:
        app.processEvents()


class AppInitializer:
    """Gestisce la sequenza di avvio con log puliti e sintetici."""

    _core_initialized = False

    @staticmethod
    def initialize(status_callback: Optional[Callable[[str, int], None]] = None, mw_instance=None):
        """
        Esegue l'inizializzazione con log diretti.
        Cede frequentemente il controllo alla GUI per animazioni fluide.
        """

        def step(msg, prog):
            if status_callback:
                status_callback(msg, prog)
            logger.info(f"[INIT] {msg} ({prog}%)")
            _yield_to_gui()

        try:
            if not mw_instance and not AppInitializer._core_initialized:
                # --- FASE 1: CORE ---
                step("Kernel System", 5)
                AppInitializer._setup_logging()
                _yield_to_gui()

                step("Data Analysis Engines", 10)
                _yield_to_gui()
                import pandas
                _yield_to_gui()
                import numpy
                _yield_to_gui()

                step("Automation Drivers", 15)
                _yield_to_gui()
                import selenium
                _yield_to_gui()

                # --- FASE 2: SICUREZZA ---
                step("Hardware Identity (HWID)", 20)
                _yield_to_gui()
                from src.core.license_validator import get_detailed_license_status, LicenseStatus
                _yield_to_gui()
                from src.core.license_updater import run_update
                _yield_to_gui()

                status, msg = get_detailed_license_status()
                _yield_to_gui()
                if status != LicenseStatus.VALID:
                    step("Cloud License Recovery", 25)
                    run_update()
                    _yield_to_gui()

                step("System Database", 30)
                _yield_to_gui()
                from src.core.database import db_manager
                _yield_to_gui()
                db_manager.init_db()
                _yield_to_gui()

                AppInitializer._core_initialized = True
                return True

            elif mw_instance:
                from src.gui.main_window.page_index import PageIndex
                _yield_to_gui()

                tasks = [
                    (PageIndex.DASHBOARD, "Dashboard & Analytics"),
                    (PageIndex.TIMBRATURE, "Timesheet Repository"),
                    (PageIndex.STRUMENTALE, "Asset Registry"),
                    (PageIndex.DATAEASE, "DataEase Sync Bridge"),
                    (PageIndex.ANAGRAFICHE, "HR Directory"),
                    (PageIndex.DIPENDENTI, "Employee Records"),
                    (PageIndex.AUTOMAZIONI, "Task Scheduler"),
                    (PageIndex.LYRA, "Lyra Analysis Engine"),
                    (PageIndex.SETTINGS, "User Configuration")
                ]

                base_prog = 45
                for i, (idx, name) in enumerate(tasks):
                    prog = base_prog + int((i / len(tasks)) * 45)
                    step(name, prog)
                    _yield_to_gui()
                    mw_instance.navigation_controller.get_panel(idx)
                    _yield_to_gui()
                    # Micro-pausa per permettere alle animazioni di aggiornarsi
                    time.sleep(0.01)
                    _yield_to_gui()

                # --- FASE 5: SERVIZI ---
                step("Telegram Security Monitor", 92)
                _yield_to_gui()
                from src.core import config_manager
                config = config_manager.load_config()
                _yield_to_gui()
                if not config.get("telegram_chat_id") and not config.get("telegram_pairing_code"):
                    import random
                    code = str(random.randint(100000, 999999))
                    config_manager.set_config_value("telegram_pairing_code", code)
                _yield_to_gui()

                step("System Ready", 100)
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
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
        handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        if not any(isinstance(h, logging.handlers.RotatingFileHandler) for h in root_logger.handlers):
            root_logger.addHandler(handler)

    @staticmethod
    def setup_app_style(app):
        from src.core.version import __version__
        app.setStyle("Fusion")
        from src.gui.styles import apply_theme
        apply_theme(app, "light")
        app.setFont(QFont("Segoe UI", 10))
        app.setApplicationName("SyncroJob")
        app.setApplicationVersion(__version__)
