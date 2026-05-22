"""
SyncroJob - Changelog Worker
Worker asincrono per il caricamento e parsing del file changelog.json.
"""

import json
import logging
from pathlib import Path
from typing import Any

from PySide6.QtCore import QThread, Signal

from src.core.version import __version__

logger = logging.getLogger(__name__)


class ChangelogWorker(QThread):
    """
    Worker che legge il file changelog da disco e prepara i dati per il rendering.
    """

    finished_signal = Signal(list)  # Invia lista di release
    error_signal = Signal(str)

    def run(self) -> None:
        """Esegue l'I/O su disco in background."""
        try:
            logger.info("[ChangelogWorker] Lettura changelog.json...")
            changelog_path = Path(__file__).resolve().parent.parent.parent / "core" / "changelog.json"
            changelog_data: list[dict[str, Any]] = []

            if changelog_path.exists():
                try:
                    data = json.loads(changelog_path.read_text(encoding="utf-8"))
                    if isinstance(data, list):
                        changelog_data = data
                except Exception:
                    logger.exception("Impossibile decodificare il file changelog.json")

            if not changelog_data:
                changelog_data = [
                    {
                        "version": __version__,
                        "date": "2026-05-20",
                        "notes": [
                            "Release iniziale della versione corrente. Changelog in fase di indicizzazione."
                        ],
                    }
                ]

            self.finished_signal.emit(changelog_data)

        except Exception as e:
            logger.exception("Errore caricamento changelog")
            self.error_signal.emit(str(e))
