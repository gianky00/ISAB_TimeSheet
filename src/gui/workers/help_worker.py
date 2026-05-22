"""SyncroJob - Help Worker.

Worker asincrono per il caricamento dei contenuti della guida.
Garantisce la fluidità della GUI durante la preparazione della documentazione.
"""

import logging
from collections.abc import Callable

from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)


class HelpWorker(QThread):
    """Worker che prepara le sezioni della documentazione in background."""

    finished_signal = Signal(list)
    error_signal = Signal(str)

    def __init__(self, section_loaders: list[tuple[str, Callable[[], str], str]]) -> None:
        """Inizializza il worker con la lista dei loader.

        Args:
          section_loaders: Lista di (Titolo, FunzioneLoader, IconKey).
        """
        super().__init__()
        self.section_loaders = section_loaders

    def run(self) -> None:
        """Esegue i loader di documentazione in background."""
        try:
            logger.info("[HelpWorker] Caricamento documentazione...")
            sections = []
            for title, loader_func, icon_key in self.section_loaders:
                content = loader_func()
                sections.append((title, content, icon_key))

            self.finished_signal.emit(sections)
            logger.info(f"[HelpWorker] Documentazione caricata ({len(sections)} sezioni).")

        except Exception as e:
            logger.exception("[HelpWorker] Errore durante il caricamento help")
            self.error_signal.emit(str(e))
