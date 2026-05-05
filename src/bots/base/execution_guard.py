"""
SyncroJob - Bot Execution Guard
Gestisce i controlli pre-volo dei bot: licenza, aggiornamenti e integrità.
Centralizza la sicurezza dell'esecuzione.
"""

import logging

from src.core.license_updater import run_update
from src.core.license_validator import verify_license

logger = logging.getLogger(__name__)


class ExecutionGuard:
    """
    Componente responsabile della validazione delle condizioni di esecuzione.
    """

    @staticmethod
    def check_environment() -> tuple[bool, str]:
        """
        Esegue i controlli preliminari (Licenza e Aggiornamenti).
        
        Returns:
            Tuple (esito, messaggio_errore).
        """
        try:
            # 1. Verifica/Esegue aggiornamenti licenza silenti
            run_update()
        except Exception as e:
            if "REVOCATA" in str(e):
                logger.error("Licenza revocata rilevata durante pre-check.")
                return False, f"ACCESSO NEGATO: {e}"
            logger.warning("Errore silente durante run_update: %s", e)

        # 2. Validazione licenza reale
        valid, msg = verify_license()
        if not valid:
            logger.error("Validazione licenza fallita: %s", msg)
            return False, msg

        return True, ""
