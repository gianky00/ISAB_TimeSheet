"""
SyncroJob - App Initializer
Gestisce il ciclo di vita dell'avvio dell'applicazione.
Agnostico rispetto alla GUI (non importa PyQt direttamente nelle funzioni core).
"""

import logging
from collections.abc import Callable
from typing import Any, ClassVar

from src.core.logging import get_logger

logger = get_logger("AppInitializer")


class AppInitializer:
    """
    Orchestratore della sequenza di bootstrap dell'intero sistema.
    """

    _core_initialized = False
    _startup_alerts: ClassVar[list[tuple[str, str]]] = []

    @staticmethod
    def add_alert(severity: str, message: str) -> None:
        AppInitializer._startup_alerts.append((severity, message))

    @staticmethod
    def get_alerts() -> list[tuple[str, str]]:
        return AppInitializer._startup_alerts

    @staticmethod
    def initialize_core(progress_callback: Callable[[str, int], None] | None = None) -> bool:
        """Inizializzazione servizi fondamentali (Fase 1)."""

        def step(msg: str, perc: int) -> None:
            logger.info(f"[INIT CORE] {msg}")
            if progress_callback:
                progress_callback(msg, perc)

        try:
            if AppInitializer._core_initialized:
                return True

            step("Analisi variabili d'ambiente...", 2)
            step("Inizializzazione Sottosistema Logging...", 4)
            AppInitializer._setup_logging()

            step("Verifica dipendenze critiche (Pandas/Numpy)...", 7)
            import numpy
            import pandas

            logger.info(f"Engine: Pandas {pandas.__version__} | Numpy {numpy.__version__}")

            step("Validazione Path di Sistema...", 13)
            from src.core.config_manager import CONFIG_DIR

            CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            step("Verifica integrità WebDriver...", 19)
            from src.utils.resource_manager import ResourceManager

            ResourceManager.ensure_automation_driver()

            step("Caricamento Registry Bot...", 22)
            from src.bots import get_available_bots

            logger.info(f"Moduli bot rilevati: {len(get_available_bots())}")

            step("Verifica Identità Hardware (HWID)...", 25)
            from src.core.license_validator import get_hardware_id

            get_hardware_id()

            step("Handshake con Server Licenze...", 28)
            from src.core.license_updater import run_update

            with contextlib_suppress(Exception):
                run_update()

            step("Validazione Certificati di Licenza...", 31)
            from src.core.license_validator import LicenseStatus, get_detailed_license_status

            status, msg = get_detailed_license_status()
            if status != LicenseStatus.VALID:
                raise Exception(f"Licenza non valida: {msg}")

            step("Inizializzazione Engine SQLite3...", 34)
            from src.core.database import db_manager

            db_manager.init_db()

            AppInitializer._core_initialized = True
            step("Nucleo Sistema Operativo", 40)
            return True

        except Exception as e:
            if any(x in str(e) for x in ("REVOCATA", "Licenza non valida", "Errore Database")):
                raise
            logger.critical(f"Unexpected startup error: {e}", exc_info=True)
            raise Exception(f"Errore imprevisto durante l'avvio: {e}") from e

    @staticmethod
    def init_generator(mw_instance: Any, yield_callback: Callable[[], None] | None = None):
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

        for i, (idx, name) in enumerate(tasks):
            prog = base_prog + int((i / total) * 45)
            yield f"Caricamento {name}...", prog

            try:
                mw_instance.navigation_controller.get_panel(idx)
            except Exception as e:
                logger.error(f"Error loading panel {name}: {e}", exc_info=True)

            if yield_callback:
                yield_callback()

        yield "Sistema Pronto", 100

    @staticmethod
    def _setup_logging() -> None:
        try:
            from src.core.logging import configure_logging

            configure_logging()
        except Exception:
            logging.basicConfig(level=logging.INFO)


def contextlib_suppress(*exceptions):
    """Internal helper to avoid importing contextlib in core header."""
    from contextlib import suppress

    return suppress(*exceptions)
