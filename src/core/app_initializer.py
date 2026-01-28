import logging
import logging.handlers
import sys
import time
import traceback
from typing import Callable, Optional

# Import leggeri
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger("AppInitializer")

class AppInitializer:
    """Gestisce la sequenza di avvio UNIFICATA (Core + GUI Preload)."""

    _core_initialized = False

    @staticmethod
    def initialize(status_callback: Optional[Callable[[str, int], None]] = None, mw_instance=None):
        """
        Esegue l'inizializzazione completa o il pre-caricamento della GUI.
        """
        
        def step(msg, prog):
            if status_callback:
                status_callback(msg, prog)
            logger.info(f"[INIT] {msg} ({prog}%)")

        try:
            # SE mw_instance non è fornito, facciamo il CORE INIT
            if not mw_instance and not AppInitializer._core_initialized:
                # --- FASE 1: CORE SYSTEM ---
                step("Inizializzazione Kernel SyncroJob...", 5)
                AppInitializer._setup_logging()
                
                step("Caricamento motori di analisi dati...", 10)
                import pandas
                import numpy
                
                step("Configurazione motori di automazione...", 15)
                import selenium
                
                # --- FASE 2: SICUREZZA & LICENZA ---
                step("Verifica identità hardware (HWID)...", 20)
                from src.core.license_validator import get_detailed_license_status, LicenseStatus
                from src.core.license_updater import run_update
                
                status, msg = get_detailed_license_status()
                if status != LicenseStatus.VALID:
                    step("Ripristino licenza tramite cloud...", 25)
                    run_update()

                step("Connessione al database di sistema...", 30)
                from src.core.database import db_manager
                db_manager.init_db()
                
                AppInitializer._core_initialized = True
                return True

            # SE mw_instance è fornito, facciamo il GUI PRELOAD
            elif mw_instance:
                from src.gui.main_window.page_index import PageIndex
                
                tasks = [
                    (PageIndex.DASHBOARD, "Dashboard & Analytics"),
                    (PageIndex.TIMBRATURE, "Timesheet Repository"),
                    (PageIndex.STRUMENTALE, "Asset Registry Module"),
                    (PageIndex.DATAEASE, "DataEase Sync Bridge"),
                    (PageIndex.ANAGRAFICHE, "HR Directory Service"),
                    (PageIndex.DIPENDENTI, "Employee Records"),
                    (PageIndex.AUTOMAZIONI, "Task Scheduler Engine"),
                    (PageIndex.LYRA, "Lyra Analysis Engine"),
                    (PageIndex.SETTINGS, "User Configuration")
                ]
                
                base_prog = 45
                for i, (idx, name) in enumerate(tasks):
                    prog = base_prog + int((i / len(tasks)) * 45)
                    step(f"Caricamento modulo: {name}...", prog)
                    mw_instance.navigation_controller.get_panel(idx)
                    # Piccola pausa per fluidità visiva
                    time.sleep(0.02)

                # --- FASE 5: SERVIZI ACCESSORI ---
                step("Avvio monitoraggio sicurezza Telegram...", 92)
                from src.core import config_manager
                config = config_manager.load_config()
                if not config.get("telegram_chat_id") and not config.get("telegram_pairing_code"):
                    import random
                    code = str(random.randint(100000, 999999))
                    config_manager.set_config_value("telegram_pairing_code", code)
                
                step("Sistema pronto. Accesso in corso...", 100)
                return True
            
            return True

        except Exception as e:
            logger.critical(f"Errore fatale startup: {e}")
            logger.error(traceback.format_exc())
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
