"""License Verifier.

Gestisce la verifica formale del file di licenza e della firma HWID,
l'handshake asincrono con il server licenze e lo spegnimento forzato in caso di revoca.
"""

import sys
import threading
from collections.abc import Callable

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from src.application.services.exceptions import LicenseError
from src.application.services.license_updater import run_update
from src.application.services.license_validator import (
    LicenseStatus,
    get_detailed_license_status,
    get_hardware_id,
)
from src.application.services.logging import get_logger

logger = get_logger("LicenseVerifier")


class LicenseVerifier:
    """Gestore e verificatore del sottosistema di licenze dell'applicazione."""

    @staticmethod
    def verify_license(step_callback: Callable[[str, int], None]) -> None:
        """Esegue il controllo formale della validità della licenza e dell'HWID."""
        step_callback("Verifica Identità Hardware (HWID)...", 25)
        get_hardware_id()

        step_callback("Handshake con Server Licenze in Background...", 28)

        def _async_handshake() -> None:
            try:
                run_update()
            except Exception as handshake_err:
                if "REVOCATA" in str(handshake_err):
                    logger.critical("Licenza REVOCATA rilevata dal background thread!")
                    LicenseVerifier._trigger_revocation_shutdown()
                else:
                    logger.warning(f"Errore handshake licenza (non bloccante): {handshake_err}")

        threading.Thread(target=_async_handshake, daemon=True).start()

        step_callback("Validazione Certificati di Licenza (Cache Locale)...", 31)
        status, msg = get_detailed_license_status()
        if status != LicenseStatus.VALID:
            raise LicenseError(f"Licenza non valida: {msg}")

    @staticmethod
    def _trigger_revocation_shutdown() -> None:
        """Esegue lo spegnimento immediato dell'applicazione per licenza revocata.

        Garantisce la thread-safety usando QTimer.singleShot(0) sul main thread Qt.
        """

        def _force_shutdown() -> None:
            app = QApplication.instance()
            if app:
                try:
                    from src.gui.dialogs.confirmation_dialog import ConfirmationDialog  # noqa: PLC0415

                    ConfirmationDialog.show_error(
                        None,
                        "Licenza Revocata",
                        "La licenza di questo software è stata REVOCATA dal server.\n\n"
                        "L'applicazione verrà chiusa immediatamente.\n"
                        "Contattare l'amministratore per assistenza.",
                    )
                except Exception:
                    logger.exception("Errore nel mostrare il dialog di revoca")
            sys.exit(1)

        try:
            QTimer.singleShot(0, _force_shutdown)
        except Exception:
            sys.exit(1)
