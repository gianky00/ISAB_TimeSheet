"""SyncroJob - Bot Execution Guard.

Gestisce i controlli pre-volo dei bot: licenza, aggiornamenti e integrità.
Centralizza la sicurezza dell'esecuzione.
"""

from src.application.services.logging import get_logger

logger = get_logger(__name__)


class ExecutionGuard:
    """Componente responsabile della validazione delle condizioni di esecuzione."""

    @staticmethod
    def check_environment() -> tuple[bool, str]:
        """Esegue i controlli preliminari (Licenza e Aggiornamenti).

        Returns:
          Tuple (esito, messaggio_errore).
        """
        try:
            from src.application.services.license_validator import verify_license
            # Rimosso run_update() sincrono: la risoluzione DNS (getaddrinfo) blocca il GIL su Windows
            # e causa il freeze della GUI. L'aggiornamento viene già gestito in background da AppInitializer.
        except Exception as e:
            logger.warning(f"Errore caricamento validatore: {e}")

        # 2. Validazione licenza reale
        valid, msg = verify_license()
        if not valid:
            logger.error(f"Validazione licenza fallita: {msg}")
            return False, msg

        return True, ""
