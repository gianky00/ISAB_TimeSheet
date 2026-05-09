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
            AppInitializer._verify_license(step)
            AppInitializer._init_databases(step)

            AppInitializer._core_initialized = True
            step("Nucleo Sistema Operativo", 40)
        except Exception as e:
            if any(x in str(e) for x in ("REVOCATA", "Licenza non valida", "Errore Database")):
                raise
            logger.critical(f"Unexpected startup error: {e}", exc_info=True)
            raise Exception(f"Errore imprevisto durante l'avvio: {e}") from e  # noqa: TRY002, TRY003
        else:
            return True

    @staticmethod
    def _verify_environment(step: Callable[[str, int], None]) -> None:
        """Verifica dipendenze e ambiente."""
        step("Verifica dipendenze critiche (Pandas/Numpy)...", 7)
        import numpy  # noqa: PLC0415
        import pandas  # noqa: PLC0415

        logger.info(f"Engine: Pandas {pandas.__version__} | Numpy {numpy.__version__}")

        step("Validazione Path di Sistema...", 13)
        from src.core.paths import CONFIG_DIR  # noqa: PLC0415

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        step("Verifica integrita' WebDriver...", 19)
        from src.utils.resource_manager import ResourceManager  # noqa: PLC0415

        ResourceManager.ensure_automation_driver()

        step("Caricamento Registry Bot...", 22)
        from src.bots import get_available_bots  # noqa: PLC0415

        logger.info(f"Moduli bot rilevati: {len(get_available_bots())}")

    @staticmethod
    def _verify_license(step: Callable[[str, int], None]) -> None:
        """Verifica HWID e stato licenza."""
        step("Verifica Identit  Hardware (HWID)...", 25)
        from src.core.license_validator import get_hardware_id  # noqa: PLC0415

        get_hardware_id()

        step("Handshake con Server Licenze in Background...", 28)
        import threading  # noqa: PLC0415

        from src.core.license_updater import run_update  # noqa: PLC0415

        def _async_handshake() -> None:
            try:
                run_update()
            except Exception as handshake_err:
                if "REVOCATA" in str(handshake_err):
                    logger.critical("Licenza REVOCATA rilevata dal background thread!")
                    AppInitializer._trigger_revocation_shutdown()
                else:
                    logger.warning(f"Errore handshake licenza (non bloccante): {handshake_err}")

        threading.Thread(target=_async_handshake, daemon=True).start()

        step("Validazione Certificati di Licenza (Cache Locale)...", 31)
        from src.core.license_validator import (  # noqa: PLC0415
            LicenseStatus,
            get_detailed_license_status,
        )

        status, msg = get_detailed_license_status()
        if status != LicenseStatus.VALID:
            raise Exception(f"Licenza non valida: {msg}")  # noqa: TRY002, TRY003

    @staticmethod
    def _init_databases(step: Callable[[str, int], None]) -> None:
        """Inizializzazione database."""
        step("Inizializzazione Engine SQLite3...", 34)
        try:
            from src.core.database import db_manager  # noqa: PLC0415

            db_manager.init_db()
        except Exception as e:
            logger.exception("Errore inizializzazione database", e)  # noqa: TRY401, PLE1205
            raise

    @staticmethod
    def init_generator(mw_instance: Any, yield_callback: Callable[[], None] | None = None) -> Any:
        """Generatore per l'inizializzazione progressiva della GUI (Fase 2)."""
        import time  # noqa: PLC0415

        tasks = [
            (0, "Preparazione Dashboard"),
            (1, "Scheduler Attivita'"),
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
    def _trigger_revocation_shutdown() -> None:
        """Blocca immediatamente l'app quando il server conferma la revoca della licenza.

        Viene chiamato dal background thread: usa QTimer.singleShot(0) per
        eseguire il dialog e il sys.exit sul main thread Qt (thread-safe).
        """

        def _force_shutdown() -> None:
            import sys  # noqa: PLC0415

            from PySide6.QtWidgets import QApplication, QMessageBox  # noqa: PLC0415

            app = QApplication.instance()
            if app:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Licenza Revocata")
                msg.setText(
                    "La licenza di questo software  stata REVOCATA dal server.\n\n"
                    "L'applicazione verr  chiusa immediatamente.\n"
                    "Contattare l'amministratore per assistenza."
                )
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
            sys.exit(1)

        try:
            from PySide6.QtCore import QTimer  # noqa: PLC0415

            QTimer.singleShot(0, _force_shutdown)
        except Exception:
            import sys  # noqa: PLC0415

            sys.exit(1)

    @staticmethod
    def _setup_logging() -> None:
        """Configura il sottosistema di logging caricando le impostazioni dal config."""
        try:
            from src.core.logging import configure_logging  # noqa: PLC0415

            configure_logging()
        except Exception:
            logging.basicConfig(level=logging.INFO)
