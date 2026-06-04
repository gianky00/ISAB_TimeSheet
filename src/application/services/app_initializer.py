"""SyncroJob - App Initializer.

Gestisce il ciclo di vita dell'avvio dell'applicazione.
Agnostico rispetto alla GUI (non importa PyQt direttamente nelle funzioni core).
"""

import logging
import sys
import time
from collections.abc import Callable
from typing import Any, ClassVar

import numpy
import pandas

from src.application.services.exceptions import StartupError
from src.application.services.initialization.license_verifier import LicenseVerifier
from src.application.services.initialization.migration_engine import DatabaseMigrationEngine
from src.application.services.logging import configure_logging, get_logger
from src.application.services.paths import CONFIG_DIR
from src.infrastructure.bots import get_available_bots
from src.infrastructure.utils.resource_manager import ResourceManager

logger = get_logger("AppInitializer")


class AppInitializer:
    """Orchestratore della sequenza di bootstrap dell'intero sistema."""

    _core_initialized = False
    _startup_alerts: ClassVar[list[tuple[str, str]]] = []

    @staticmethod
    def add_alert(severity: str, message: str) -> None:
        """Registra un avviso (alert) da mostrare all'avvio dell'applicazione."""
        AppInitializer._startup_alerts.append((severity, message))

    @staticmethod
    def get_alerts() -> list[tuple[str, str]]:
        """Restituisce la lista degli avvisi accumulati durante l'inizializzazione."""
        return AppInitializer._startup_alerts

    @staticmethod
    def initialize_core(progress_callback: Callable[[str, int], None] | None = None) -> bool:
        """Inizializzazione servizi fondamentali (Fase 1)."""
        if AppInitializer._core_initialized:
            return True

        def step(msg: str, perc: int) -> None:
            """Propaga lo stato avanzamento dell'inizializzazione core."""
            logger.info(f"[INIT CORE] {msg}")
            if progress_callback:
                progress_callback(msg, perc)

        try:
            step("Inizializzazione Sottosistema Logging...", 4)
            AppInitializer._setup_logging()

            AppInitializer._verify_environment(step)
            LicenseVerifier.verify_license(step)
            DatabaseMigrationEngine.initialize_database(step)

            step("Ottimizzazione motori di automazione (Playwright/PDF/Excel)...", 38)
            AppInitializer._preload_heavy_modules()

            AppInitializer._core_initialized = True
            step("Nucleo Sistema Operativo", 40)
        except Exception as e:
            if any(x in str(e) for x in ("REVOCATA", "Licenza non valida", "Errore Database")):
                raise
            logger.critical(f"Unexpected startup error: {e}", exc_info=True)
            raise StartupError(f"Startup error: {e}") from e
        else:
            return True

    @staticmethod
    def _verify_environment(step: Callable[[str, int], None]) -> None:
        """Verifica dipendenze e ambiente."""
        step("Verifica dipendenze critiche (Pandas/Numpy)...", 7)
        logger.info(f"Engine: Pandas {pandas.__version__} | Numpy {numpy.__version__}")

        step("Validazione Path di Sistema...", 13)
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        step("Verifica integrità WebDriver...", 19)
        ResourceManager.ensure_automation_driver()

        step("Caricamento Registry Bot...", 22)
        logger.info(f"Moduli bot rilevati: {len(get_available_bots())}")

    @staticmethod
    def init_generator(mw_instance: Any, yield_callback: Callable[[], None] | None = None) -> Any:
        """Generatore per l'inizializzazione progressiva della GUI (Fase 2)."""
        tasks = [
            (0, "Preparazione Dashboard"),
            (1, "Scheduler Attività"),
            (10, "Archivio Storico OdA"),
            (3, "Caricamento Repository Ore"),
            (4, "Registro Asset Aziendali"),
            (9, "Centro Notifiche"),
            (5, "DataEase Sync Bridge"),
            (6, "Directory Personale"),
            (7, "Configurazione Utente"),
            (11, "Gestione Schede Dipendenti"),
            (8, "Manuale Operativo"),
            (12, "Consuntivo"),
        ]

        base_prog = 45
        total = len(tasks)
        gen_start = time.perf_counter()

        for i, (idx, name) in enumerate(tasks):
            prog = base_prog + int((i / total) * 45)
            yield f"Caricamento {name}...", prog

            t0 = time.perf_counter()
            try:
                mw_instance.navigation_controller.get_panel(idx)
            except Exception as e:
                logger.error(f"Error loading panel {name}: {e}", exc_info=True)
            elapsed = time.perf_counter() - t0
            logger.info(f"[PERF] Panel '{name}' (idx={idx}) loaded in {elapsed:.2f}s")

            if yield_callback:
                yield_callback()

        total_elapsed = time.perf_counter() - gen_start
        logger.info(f"[PERF] init_generator total: {total_elapsed:.2f}s")
        yield "Sistema Pronto", 100

    @staticmethod
    def _preload_heavy_modules() -> None:
        """Pre-carica in memoria i moduli e le librerie esterne più pesanti per garantire prestazioni istantanee a runtime."""
        logger.info("[INIT CORE] Pre-caricamento moduli pesanti per prestazioni Zero-Lag...")
        try:
            # 1. Motori di automazione ed I/O
            import fitz  # noqa: F401, PLC0415
            import openpyxl  # noqa: F401, PLC0415
            import playwright.sync_api  # noqa: F401, PLC0415
            import psutil  # noqa: F401, PLC0415

            # 2. Moduli core del bot scarico TS
            from src.infrastructure.bots.portale_fornitori.scarico_ts.bot import (  # noqa: PLC0415
                ScaricaTSBot,  # noqa: F401
            )
            from src.infrastructure.bots.portale_fornitori.scarico_ts.playwright_bot import (  # noqa: PLC0415
                PlaywrightScaricaTSBot,  # noqa: F401
            )

            # 3. Riscaldamento preventivo Playwright e Chromium (Antivirus Warming)
            logger.info("[INIT CORE] Riscaldamento motori di automazione (Antivirus Warming)...")
            import os  # noqa: PLC0415
            from pathlib import Path  # noqa: PLC0415

            if getattr(sys, "frozen", False):
                bundle_dir = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(sys.executable).parent
                drivers_pw_path = bundle_dir / "drivers" / "ms-playwright"
                if drivers_pw_path.exists():
                    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(drivers_pw_path)

            # 4. Riscaldamento WMI (psutil) e Pulizia Preventiva
            logger.info("[INIT CORE] Riscaldamento sottosistema processi (WMI/psutil)...")
            from src.infrastructure.utils.helpers import cleanup_bot_processes  # noqa: PLC0415

            cleanup_bot_processes()

            from playwright.sync_api import sync_playwright  # noqa: PLC0415

            pw = sync_playwright().start()
            try:
                browser = pw.chromium.launch(headless=True)
                browser.close()
            finally:
                pw.stop()

            logger.info("[INIT CORE] Pre-caricamento e riscaldamento completati con successo.")
        except Exception as e:
            logger.warning(f"[INIT CORE] Avvertimento nel pre-caricamento/riscaldamento moduli: {e}")

    @staticmethod
    def _setup_logging() -> None:
        """Configura il sottosistema di logging caricando le impostazioni dal config."""
        try:
            configure_logging()
        except Exception:
            logging.basicConfig(level=logging.INFO)
