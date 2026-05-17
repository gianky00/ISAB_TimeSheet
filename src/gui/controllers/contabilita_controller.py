"""
SyncroJob - Contabilita Controller
Gestore della logica di interfaccia per il modulo Contabilità.
Separa la gestione dei dati e dei worker dalla visualizzazione (ContabilitaPanel).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from src.core.contabilita_worker import ContabilitaWorker
from src.core.database.repositories import ContabilitaRepository

if TYPE_CHECKING:
    from src.gui.panels.contabilita_panel import ContabilitaPanel

logger = logging.getLogger(__name__)


class ContabilitaController(QObject):
    """
    Controller dedicato al modulo Contabilità.
    Gestisce l'orchestrazione dei dati, l'avvio dei worker di importazione
    e la comunicazione tra la logica di business e la UI.
    """

    # Segnali per aggiornare la UI
    status_updated = Signal(str)  # Messaggio di stato HTML
    import_finished = Signal(bool, str)  # success, message
    data_refreshed = Signal()  # Notifica che i dati sono stati ricaricati

    def __init__(self, panel: ContabilitaPanel) -> None:
        super().__init__(panel)
        self.panel = panel
        self.repository = ContabilitaRepository()
        self.worker: ContabilitaWorker | None = None
        self._last_status_html = "Pronto"

    def get_available_years(self) -> list[int]:
        """Recupera gli anni disponibili tramite repository."""
        return self.repository.get_available_years()

    def start_import_process(self) -> None:
        """Avvia il processo di importazione asincrona dei file Excel."""
        if self.worker and self.worker.isRunning():
            logger.warning("Importazione già in corso.")
            return

        from src.core.config_manager import get_config_value

        # Recupero path da config
        path_contabilita = get_config_value("contabilita_path", "")
        path_giornaliere = get_config_value("giornaliere_path", "")
        path_programmate = get_config_value("attivita_programmate_path", "")
        path_certificati = get_config_value("certificati_campione_path", "")

        self.worker = ContabilitaWorker(
            path_contabilita, path_giornaliere, path_programmate, path_certificati
        )

        # Connessione segnali worker
        self.worker.progress_signal.connect(self._handle_worker_status)
        self.worker.finished_signal.connect(self._handle_worker_finished)

        self.worker.start()
        self.status_updated.emit("<b>Inizializzazione importazione...</b>")

    def _handle_worker_status(self, message: str) -> None:
        """Gestisce gli aggiornamenti di stato dal worker."""
        self._last_status_html = message
        self.status_updated.emit(message)

    def _handle_worker_finished(
        self, success: bool, message: str, added: int, removed: int, duration: float
    ) -> None:
        """Gestisce la chiusura del worker."""
        self.import_finished.emit(success, message)
        if success:
            self.data_refreshed.emit()

    def handle_search(self, text: str) -> None:
        """Gestisce la logica di ricerca delegandola al pannello attivo."""
        # Nota: In una scomposizione più profonda, anche i tab avrebbero i loro controller
        # Per ora manteniamo la delega al widget corrente del panel
        self.panel._on_search_changed(text)

    def update_selection_stats(self, count: int, total_hours: float) -> None:
        """Aggiorna le etichette delle statistiche di selezione nel pannello."""
        self.panel.selection_count_label.setText(str(count))
        self.panel.selection_sum_label.setText(f"{total_hours:.2f}")
