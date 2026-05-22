"""SyncroJob - Scarico Ore Controller.

Gestisce la logica di business, l'importazione e il calcolo dei totali per lo Scarico Ore.
"""

import logging
import time
from datetime import UTC, datetime

from PySide6.QtCore import QObject, QThread, Signal

from src.core.contabilita_manager import ContabilitaManager

logger = logging.getLogger(__name__)


class ScaricoOreWorker(QThread):
    """Worker thread per l'importazione asincrona di Scarico Ore.

    Inizializza il worker per l'importazione.

    Args:
      file_path: Percorso del file Excel dello Scarico Ore da importare.

    Attributes:
        finished_signal: Segnale emesso al completamento.
        progress_signal: Segnale per l'aggiornamento del progresso.
    """

    finished_signal = Signal(bool, str, int, int, float)
    progress_signal = Signal(str)

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path
        self.start_time: float = 0.0

    def run(self) -> None:
        """Esegue l'importazione nel thread separato con calcolo del progresso e dell'ETA.

        Inizializza il database e invoca il manager per il processing del file.
        """
        ContabilitaManager.init_db()
        self.start_time = time.time()
        try:
            total_rows = ContabilitaManager.scan_scarico_ore_rows(self.file_path)
        except Exception:
            total_rows = 1000

        def progress_cb(current: int, total: int) -> None:
            """Callback per l'aggiornamento dello stato di avanzamento e calcolo ETA."""
            real_total = max(total if total > 0 else total_rows, current)
            elapsed = time.time() - self.start_time
            if current > 0 and elapsed > 0:
                rate = current / elapsed
                remaining = real_total - current
                eta_sec = remaining / rate if rate > 0 else 0
                m, s = divmod(int(eta_sec), 60)
                percent = min(int((current / real_total) * 100), 99)
                self.progress_signal.emit(
                    f"Importazione: {percent}% completato ({current}/{real_total})   ETA: {m}m {s}s"
                )

        success, msg, added, removed = ContabilitaManager.import_scarico_ore(
            self.file_path, progress_callback=progress_cb
        )
        self.finished_signal.emit(success, msg, added, removed, time.time() - self.start_time)


class ScaricoOreController(QObject):
    """Controller centrale per il coordinamento dei dati di Scarico Ore.

    Inizializza il controller di Scarico Ore.
    """

    status_changed = Signal(str)
    update_finished = Signal(bool, str)

    def __init__(self) -> None:
        super().__init__()
        self.worker: ScaricoOreWorker | None = None

    def start_import(self, file_path: str) -> None:
        """Inizializza e avvia il thread di importazione asincrona.

        Args:
          file_path: Percorso del file Excel sorgente.
        """
        self.worker = ScaricoOreWorker(file_path)
        self.worker.progress_signal.connect(self.status_changed.emit)
        self.worker.finished_signal.connect(self._handle_finished)
        self.worker.start()

    def _handle_finished(self, success: bool, msg: str, added: int, removed: int, duration: float) -> None:
        """Gestisce il completamento del worker di importazione, formattando il report per la UI.

        Args:
          success: Esito dell'operazione.
          msg: Messaggio di errore o di stato.
          added: Numero di record aggiunti/aggiornati.
          removed: Numero di record rimossi.
          duration: Durata totale dell'operazione in secondi.
        """
        if success:
            ts = datetime.now(UTC).astimezone().strftime("%d/%m/%Y %H:%M")
            time_str = (
                f"{duration:.1f}s" if duration < 60 else f"{int(duration // 60)}m {int(duration % 60)}s"  # noqa: PLR2004
            )
            # Nota: I colori verranno gestiti dalla UI via HTML
            status = f"{ts} <b>+{added}</b> -{removed} ({time_str})"
            self.update_finished.emit(True, status)
        else:
            self.update_finished.emit(False, msg)

    @staticmethod
    def format_number(value: float) -> str:
        """Formatta un numero decimale rimuovendo gli zeri inutili.

        Args:
          value: Il valore numerico da formattare.

        Returns:
          str: Stringa formattata (es. '5' invece di '5.00').
        """
        return str(int(value)) if value % 1 == 0 else f"{value:.2f}"
