class SyncroJobError(Exception):
    """Base exception for all SyncroJob errors."""


class BrowserInitError(SyncroJobError, RuntimeError):
    """Eccezione sollevata quando l'inizializzazione del browser fallisce."""

    def __init__(self, message: str = "Page or Context not initialized") -> None:
        super().__init__(message)


class StartupError(SyncroJobError):
    """Eccezione sollevata durante l'avvio dell'applicazione."""


class LicenseError(SyncroJobError):
    """Eccezione sollevata per problemi relativi alla licenza."""


class BotError(SyncroJobError):
    """Base exception for bot execution errors."""


class AutomationError(BotError):
    """Errore durante l'automazione Selenium/Playwright."""


class DatabaseError(SyncroJobError):
    """Errore nelle operazioni sul database."""


class ConfigError(SyncroJobError):
    """Errore nella configurazione o nei percorsi."""
