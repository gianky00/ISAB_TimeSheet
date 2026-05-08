class BrowserInitError(RuntimeError):
    """Eccezione sollevata quando l'inizializzazione del browser fallisce."""

    def __init__(self, message: str = "Page or Context not initialized") -> None:
        super().__init__(message)
