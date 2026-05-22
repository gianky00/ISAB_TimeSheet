"""SyncroJob - Search Results Menu.

Componente grafico dedicato alla visualizzazione e navigazione dei risultati
della ricerca universale asincrona.
"""

import logging
from typing import Any

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu

logger = logging.getLogger(__name__)


class SearchResultsMenu(QMenu):
    """Menu a discesa per i risultati di ricerca.

    Gestisce la costruzione grafica, lo styling e le azioni di navigazione.
    """

    def __init__(self, main_window: Any, query: str, parent: Any = None) -> None:
        """Inizializza il menu dei risultati.

        Args:
            main_window: Finestra principale (MainWindow) per le navigazioni.
            query: La stringa cercata dall'utente.
            parent: Widget genitore opzionale.
        """
        # Inizializziamo QMenu con None per evitare che costruttori C++ ricevano MagicMock nei test
        super().__init__()
        if parent and type(parent).__name__ != "MagicMock":
            self.setParent(parent)

        self.mw = main_window
        self.query = query

        # Applica uno stile CSS moderno ed elegante coerente con la GUI
        self.setStyleSheet(
            """
            QMenu {
                background-color: white;
                border: 1px solid #dee2e6;
                padding: 5px;
                min-width: 450px;
            }
            QMenu::item {
                padding: 8px 25px;
                font-size: 13px;
            }
            QMenu::item:selected {
                background-color: #0d6efd;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background: #e9ecef;
                margin: 5px 0;
            }
            """
        )

    def build_and_exec(self, results: dict[str, Any], global_search_widget: Any) -> None:
        """Costruisce le voci del menu e lo esegue sotto il widget di ricerca.

        Args:
            results: Dizionario contenente le corrispondenze trovate.
            global_search_widget: Widget di input della barra di ricerca.
        """
        found_count = 0
        found_count += self._add_oda_matches(results.get("oda", []))
        found_count += self._add_storico_oda_matches(results.get("storico_oda", []))
        found_count += self._add_extended_matches(results.get("extended", {}))
        found_count += self._add_employees_matches(results.get("employees", []))
        found_count += self._add_attivita_matches(results.get("attivita_programmate", []))
        found_count += self._add_pdl_matches(results.get("pdl", []))
        found_count += self._add_audit_matches(results.get("audit", []))

        if found_count == 0:
            self._add_disabled_action("Nessun risultato trovato")

        # Calcola il posizionamento esatto sotto la barra di ricerca
        pos = global_search_widget.mapToGlobal(QPoint(0, global_search_widget.height()))
        self.exec(pos)

    def _add_disabled_action(self, text: str) -> None:
        """Aggiunge un'azione disabilitata che funge da intestazione di sezione."""
        action = self.addAction(text)
        if action:
            action.setEnabled(False)

    def _add_oda_matches(self, matches: list[dict[str, Any]]) -> int:
        """Aggiunge le corrispondenze della contabilità strumentale (OdA)."""
        if not matches:
            return 0
        self._add_disabled_action("CONTABILITÀ STRUMENTALE (OdA):")
        for oda in matches:
            text = f"OdA {oda['codice_oda']} - {oda['descrizione'][:50]}..."
            action = self.addAction(text)
            if action:
                # Conserviamo la lambda e usiamo i parametri di default per catturare l'identificatore oda esatto
                action.triggered.connect(lambda _, o=oda["codice_oda"]: self.mw._navigate_to_oda(o))
        self.addSeparator()
        return len(matches)

    def _add_storico_oda_matches(self, matches: list[dict[str, Any]]) -> int:
        """Aggiunge le corrispondenze dello storico OdA."""
        if not matches:
            return 0
        self._add_disabled_action("STORICO OdA:")
        for m in matches:
            desc = m.get("descrizione", "")
            desc_short = (desc[:50] + "...") if len(desc) > 50 else desc
            text = f"OdA {m['oda']}/{m['pos_oda']} - {desc_short}"
            action = self.addAction(text)
            if action:
                action.triggered.connect(lambda _, o=m["oda"]: self.mw._navigate_to(10))
        self.addSeparator()
        return len(matches)

    def _add_extended_matches(self, ext_results: dict[str, Any]) -> int:
        """Aggiunge corrispondenze estese (Giornaliere, Cantiere, Certificati)."""
        count = 0
        categories = [
            ("GIORNALIERE", "GIORNALIERE:", 1),
            ("CANTIERE", "CANTIERE (Scarico Ore):", None),
            ("CERTIFICATI", "CERTIFICATI:", 3),
        ]

        for cat, label, _ in categories:
            matches = ext_results.get(cat, [])
            if matches:
                self._add_disabled_action(label)
                for m in matches[:10]:
                    if cat == "GIORNALIERE":
                        text = f"{m['data']} - {m['personale']} - {m['descrizione'][:40]}..."
                        action = self.addAction(text)
                        if action:
                            action.triggered.connect(
                                lambda _, q=self.query: self.mw._navigate_to_extended(1, q)
                            )
                    elif cat == "CANTIERE":
                        text = f"{m['data']} - {m['personale']} - {m['commessa']}"
                        action = self.addAction(text)
                        if action:
                            action.triggered.connect(lambda _, q=self.query: self.mw._navigate_to_dataease(q))
                    elif cat == "CERTIFICATI":
                        text = f"{m['matricola']} - {m['modello']} ({m['costruttore']})"
                        action = self.addAction(text)
                        if action:
                            action.triggered.connect(
                                lambda _, q=self.query: self.mw._navigate_to_extended(3, q)
                            )
                self.addSeparator()
                count += len(matches)
        return count

    def _add_employees_matches(self, matches: list[dict[str, Any]]) -> int:
        """Aggiunge corrispondenze relative ai dipendenti."""
        if not matches:
            return 0
        self._add_disabled_action("DIPENDENTI:")
        for emp in matches:
            text = f"{emp['cognome']} {emp['nome']}"
            action = self.addAction(text)
            if action:
                action.triggered.connect(lambda _, q=text: self.mw._navigate_to_timbrature(q))
        self.addSeparator()
        return len(matches)

    def _add_attivita_matches(self, matches: list[dict[str, Any]]) -> int:
        """Aggiunge corrispondenze relative alle attività programmate."""
        if not matches:
            return 0
        self._add_disabled_action("Attività PROGRAMMATE:")
        for m in matches:
            desc = m.get("descrizione_attivita", "")
            desc_short = (desc[:40] + "...") if len(desc) > 40 else desc
            text = f"{m['area']} - {m['pdl']}: {desc_short}"
            action = self.addAction(text)
            if action:
                # Nessun argomento passato a _navigate_to, usiamo lambda senza argomenti
                action.triggered.connect(lambda: self.mw._navigate_to(3))
        self.addSeparator()
        return len(matches)

    def _add_pdl_matches(self, matches: list[dict[str, Any]]) -> int:
        """Aggiunge corrispondenze relative alle PDL Safework."""
        if not matches:
            return 0
        self._add_disabled_action("PDL SAFEWORK:")
        for m in matches:
            desc = m.get("descrizione", "")
            desc_short = (desc[:40] + "...") if len(desc) > 40 else desc
            text = f"ODL {m['odl']} - {m['unita_tecnica']}: {desc_short}"
            action = self.addAction(text)
            if action:
                action.triggered.connect(lambda: self.mw.navigate_to_panel("scarico_pdl"))
        self.addSeparator()
        return len(matches)

    def _add_audit_matches(self, matches: list[dict[str, Any]]) -> int:
        """Aggiunge corrispondenze relative all'Audit Log."""
        if not matches:
            return 0
        self._add_disabled_action("AUDIT LOG:")
        for log in matches[:3]:
            action = self.addAction(f"{log['action']} - {log['entity']}")
            if action:
                action.triggered.connect(lambda: self.mw._navigate_to(6))
        return len(matches)
