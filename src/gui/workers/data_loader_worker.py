"""
SyncroJob - Data Loader Worker
Worker generico per il caricamento asincrono di dati dal database o da API.
Previene il congelamento della UI durante operazioni pesanti di query o processamento.
"""

from typing import Any, Callable

from PyQt6.QtCore import QThread, pyqtSignal


class DataLoaderWorker(QThread):
    """
    Worker che esegue una funzione di recupero dati in un thread separato.
    Emette un segnale con il risultato al termine dell'operazione.
    """

    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, load_func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """
        Inizializza il worker.

        Args:
            load_func: La funzione da eseguire in background.
            *args: Argomenti posizionali per la funzione.
            **kwargs: Argomenti nominali per la funzione.
        """
        super().__init__()
        self.load_func = load_func
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """Esegue la funzione e notifica il risultato."""
        try:
            result = self.load_func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            self.error.emit(f"{e}\n{trace}")
