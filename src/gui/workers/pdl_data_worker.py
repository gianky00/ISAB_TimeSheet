"""SyncroJob - PDL Data Worker.

Worker asincrono per il recupero dei dati PDL e il popolamento dinamico dei filtri.
Garantisce la fluidità della GUI durante le query SQL sul database PDL.
"""

import logging
from typing import Any

from PySide6.QtCore import QThread, Signal

from src.application.services.database import db_manager

logger = logging.getLogger(__name__)


class PDLDataWorker(QThread):
    """Worker per l'esecuzione di query PDL in background.

    Supporta sia il recupero dei dati tabellari che la query per i filtri.

    Inizializza il worker.

    Args:
      mode: 'fetch_data', 'update_areas', 'update_units' o 'initial_filters'.
      *args: Argomenti posizionali per la query.
      **kwargs: Argomenti nominali per il controller e i filtri.

    Attributes:
        data_ready: Segnale o attributo della classe.
        error_signal: Segnale o attributo della classe.
        filters_ready: Segnale o attributo della classe.
    """

    data_ready = Signal(list)  # Dati per la tabella o risultati generici
    filters_ready = Signal(str, list)  # (tipo_filtro, lista_valori)
    error_signal = Signal(str)

    def __init__(self, mode: str, *args: Any, **kwargs: Any) -> None:
        super().__init__()

        self.mode = mode
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """Esegue l'operazione richiesta in base al mode."""
        try:
            if self.mode == "fetch_data":
                self._fetch_pdl_data()
            elif self.mode == "initial_filters":
                self._fetch_initial_filters()
            elif self.mode == "update_areas":
                self._fetch_areas()
            elif self.mode == "update_units":
                self._fetch_units()
        except Exception as e:
            logger.exception(f"[PDLDataWorker] Errore in mode {self.mode}")
            self.error_signal.emit(str(e))

    def _fetch_pdl_data(self) -> None:
        """Delega al controller il recupero dati (eseguito in background)."""
        controller = self.kwargs.get("controller")
        filters = self.kwargs.get("filters")
        sort_col = self.kwargs.get("sort_col")
        sort_order = self.kwargs.get("sort_order", "DESC")

        if controller:
            data = controller.get_pdl_data(filters, sort_col, sort_order)
            self.data_ready.emit(data)

    def _fetch_initial_filters(self) -> None:
        """Recupera i gruppi iniziali dai PDL."""
        q = "SELECT DISTINCT SUBSTR(n_pdl, INSTR(n_pdl, '/') + 1) as grp FROM pdl WHERE n_pdl LIKE '%/%' ORDER BY grp"
        rows = db_manager.execute_query(db_manager.DB_PDL, q)
        results = [str(r[0]) for r in rows if r[0]]
        self.filters_ready.emit("groups", results)

    def _fetch_areas(self) -> None:
        """Recupera le aree filtrate per sito."""
        site = self.args[0] if self.args else "Tutti i siti"
        q = "SELECT DISTINCT area FROM pdl WHERE 1=1"
        p = []
        if site != "Tutti i siti":
            q += " AND sito = ?"
            p.append(site)
        q += " ORDER BY area"

        rows = db_manager.execute_query(db_manager.DB_PDL, q, tuple(p))
        results = [str(r[0]) for r in rows if r[0]]
        self.filters_ready.emit("areas", results)

    def _fetch_units(self) -> None:
        """Recupera le unità filtrate per sito e area."""
        site = self.args[0] if self.args else "Tutti i siti"
        area = self.args[1] if len(self.args) > 1 else "Tutte"

        q = "SELECT DISTINCT unita FROM pdl WHERE 1=1"
        p = []
        if site != "Tutti i siti":
            q += " AND sito = ?"
            p.append(site)
        if area != "Tutte":
            q += " AND area = ?"
            p.append(area)
        q += " ORDER BY unita"

        rows = db_manager.execute_query(db_manager.DB_PDL, q, tuple(p))
        results = [str(r[0]) for r in rows if r[0]]
        self.filters_ready.emit("units", results)
