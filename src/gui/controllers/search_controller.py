"""
SyncroJob - Search Controller (Refactored)
Controller per la ricerca universale asincrona con debouncing.
Garantisce la fluidit  della GUI delegando le query al SearchWorker.
"""

import logging
from typing import Any

from PySide6.QtCore import QObject, QPoint, QTimer
from PySide6.QtWidgets import QMenu

from src.gui.workers.search_worker import SearchWorker

logger = logging.getLogger(__name__)


class SearchController(QObject):
    """Controller per la ricerca universale e la navigazione ai risultati."""

    def __init__(self, main_window: Any) -> None:
        """
        Inizializza il controller di ricerca.

        Args:
          main_window: Riferimento alla finestra principale per navigazione e posizionamento menu.
        """
        super().__init__()
        self.mw = main_window
        self.worker: SearchWorker | None = None

        # Timer per il debouncing (attende 300ms di inattivitàprima di cercare)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._execute_async_search)
        self._last_query = ""

    def perform_search(self, query: str) -> None:
        """
        Avvia il processo di ricerca con debouncing.

        Args:
          query: La stringa digitata dall'utente.
        """
        query = query.strip()
        if not query or len(query) < 2:
            self._last_query = ""
            return

        self._last_query = query
        self.search_timer.start(300)

    def _execute_async_search(self) -> None:
        """Crea e avvia il worker per la ricerca asincrona."""
        if not self._last_query:
            return

        # Interrompe in modo sicuro eventuali ricerche precedenti ancora in corso
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.results_ready.disconnect()  # Previene update da vecchi thread

        self.worker = SearchWorker(self._last_query, parent=self)
        self.worker.results_ready.connect(self._show_results_menu)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def _show_results_menu(self, results: dict[str, Any]) -> None:
        """
        Costruisce e mostra il menu contestuale con i risultati della ricerca.

        Args:
          results: Dizionario dei risultati prodotto dal SearchService.
        """
        results_menu = QMenu(self.mw)
        results_menu.setStyleSheet(
            """
      QMenu { background-color: white; border: 1px solid #dee2e6; padding: 5px; min-width: 450px; }
      QMenu::item { padding: 8px 25px; font-size: 13px; }
      QMenu::item:selected { background-color: #0d6efd; color: white; }
      QMenu::separator { height: 1px; background: #e9ecef; margin: 5px 0; }
    """
        )

        found_count = 0
        found_count += self._add_oda_matches(results.get("oda", []), results_menu)
        found_count += self._add_storico_oda_matches(results.get("storico_oda", []), results_menu)
        found_count += self._add_extended_matches(results.get("extended", {}), results_menu)
        found_count += self._add_employees_matches(results.get("employees", []), results_menu)
        found_count += self._add_attivita_matches(results.get("attivita_programmate", []), results_menu)
        found_count += self._add_pdl_matches(results.get("pdl", []), results_menu)
        found_count += self._add_audit_matches(results.get("audit", []), results_menu)

        if found_count == 0:
            self._add_disabled_action(results_menu, "Nessun risultato trovato")

        # Posizionamento sotto la barra di ricerca
        if hasattr(self.mw, "global_search"):
            pos = self.mw.global_search.mapToGlobal(QPoint(0, self.mw.global_search.height()))
            results_menu.exec(pos)

    def _add_disabled_action(self, menu: QMenu, text: str) -> None:
        """Aggiunge un'azione disabilitata (header o placeholder)."""
        action = menu.addAction(text)
        if action:
            action.setEnabled(False)

    def _add_oda_matches(self, matches: list[dict[str, Any]], menu: QMenu) -> int:
        if not matches:
            return 0
        self._add_disabled_action(menu, "CONTABILIT  STRUMENTALE (OdA):")
        for oda in matches:
            text = f"OdA {oda['codice_oda']} - {oda['descrizione'][:50]}..."
            action = menu.addAction(text)
            if action:
                action.triggered.connect(lambda _, o=oda["codice_oda"]: self.mw._navigate_to_oda(o))
        menu.addSeparator()
        return len(matches)

    def _add_storico_oda_matches(self, matches: list[dict[str, Any]], menu: QMenu) -> int:
        if not matches:
            return 0
        self._add_disabled_action(menu, "STORICO OdA:")
        for m in matches:
            desc = m.get("descrizione", "")
            desc_short = (desc[:50] + "...") if len(desc) > 50 else desc
            text = f"OdA {m['oda']}/{m['pos_oda']} - {desc_short}"
            action = menu.addAction(text)
            if action:
                action.triggered.connect(lambda _, o=m["oda"]: self.mw._navigate_to(10))
        menu.addSeparator()
        return len(matches)

    def _add_extended_matches(self, ext_results: dict[str, Any], menu: QMenu) -> int:
        count = 0
        for cat, label, _nav_idx in (
            ("GIORNALIERE", "GIORNALIERE:", 1),
            ("CANTIERE", "CANTIERE (Scarico Ore):", None),
            ("CERTIFICATI", "CERTIFICATI:", 3),
        ):
            matches = ext_results.get(cat, [])
            if matches:
                self._add_disabled_action(menu, label)
                for m in matches[:10]:
                    if cat == "GIORNALIERE":
                        text = f"{m['data']} - {m['personale']} - {m['descrizione'][:40]}..."
                        action = menu.addAction(text)
                        if action:
                            action.triggered.connect(
                                lambda _, q=self._last_query: self.mw._navigate_to_extended(1, q)
                            )
                    elif cat == "CANTIERE":
                        text = f"{m['data']} - {m['personale']} - {m['commessa']}"
                        action = menu.addAction(text)
                        if action:
                            action.triggered.connect(
                                lambda _, q=self._last_query: self.mw._navigate_to_dataease(q)
                            )
                    elif cat == "CERTIFICATI":
                        text = f"{m['matricola']} - {m['modello']} ({m['costruttore']})"
                        action = menu.addAction(text)
                        if action:
                            action.triggered.connect(
                                lambda _, q=self._last_query: self.mw._navigate_to_extended(3, q)
                            )
                menu.addSeparator()
                count += len(matches)
        return count

    def _add_employees_matches(self, matches: list[dict[str, Any]], menu: QMenu) -> int:
        if not matches:
            return 0
        self._add_disabled_action(menu, "DIPENDENTI:")
        for emp in matches:
            text = f"{emp['cognome']} {emp['nome']}"
            action = menu.addAction(text)
            if action:
                action.triggered.connect(lambda _, q=text: self.mw._navigate_to_timbrature(q))
        menu.addSeparator()
        return len(matches)

    def _add_attivita_matches(self, matches: list[dict[str, Any]], menu: QMenu) -> int:
        if not matches:
            return 0
        self._add_disabled_action(menu, "AttivitàPROGRAMMATE:")
        for m in matches:
            desc = m.get("descrizione_attivita", "")
            desc_short = (desc[:40] + "...") if len(desc) > 40 else desc
            text = f"{m['area']} - {m['pdl']}: {desc_short}"
            action = menu.addAction(text)
            if action:
                action.triggered.connect(lambda: self.mw._navigate_to(3))
        menu.addSeparator()
        return len(matches)

    def _add_pdl_matches(self, matches: list[dict[str, Any]], menu: QMenu) -> int:
        if not matches:
            return 0
        self._add_disabled_action(menu, "PDL SAFEWORK:")
        for m in matches:
            desc = m.get("descrizione", "")
            desc_short = (desc[:40] + "...") if len(desc) > 40 else desc
            text = f"ODL {m['odl']} - {m['unita_tecnica']}: {desc_short}"
            action = menu.addAction(text)
            if action:
                action.triggered.connect(lambda: self.mw.navigate_to_panel("scarico_pdl"))
        menu.addSeparator()
        return len(matches)

    def _add_audit_matches(self, matches: list[dict[str, Any]], menu: QMenu) -> int:
        if not matches:
            return 0
        self._add_disabled_action(menu, "AUDIT LOG:")
        for log in matches[:3]:
            action = menu.addAction(f"{log['action']} - {log['entity']}")
            if action:
                action.triggered.connect(lambda: self.mw._navigate_to(6))
        return len(matches)
