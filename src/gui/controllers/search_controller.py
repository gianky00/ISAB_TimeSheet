from typing import Optional

from PyQt6.QtCore import QObject, QPoint
from PyQt6.QtWidgets import QMenu

from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage


class SearchController(QObject):
    """Controller per la ricerca universale e la navigazione ai risultati."""

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window

    def perform_search(self, query: str):
        """Esegue la ricerca globale e mostra il menu dei risultati."""
        if not query or len(query) < 2:
            return

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
        found_count += self._search_oda(query, results_menu)
        found_count += self._search_storico_oda(query, results_menu)
        found_count += self._search_extended(query, results_menu)
        found_count += self._search_employees(query, results_menu)
        found_count += self._search_attivita_programmate(query, results_menu)
        found_count += self._search_pdl(query, results_menu)
        found_count += self._search_audit(query, results_menu)

        if found_count == 0:
            self._add_disabled_action(results_menu, "Nessun risultato trovato")

        pos = self.mw.global_search.mapToGlobal(QPoint(0, self.mw.global_search.height()))
        results_menu.exec(pos)

    def _add_disabled_action(self, menu: QMenu, text: str):
        """Helper sicuro per aggiungere un'azione disabilitata (header)."""
        action = menu.addAction(text)
        if action:
            action.setEnabled(False)

    def _search_oda(self, query: str, menu: QMenu) -> int:
        """Ricerca nella contabilità strumentale (OdA)."""
        try:
            from src.core.contabilita_manager import ContabilitaManager

            matches = ContabilitaManager.search_oda(query)
            if not matches:
                return 0

            self._add_disabled_action(menu, "CONTABILITÀ STRUMENTALE (OdA):")
            for oda in matches[:20]:
                text = f"OdA {oda['codice_oda']} - {oda['descrizione'][:50]}..."
                action = menu.addAction(text)
                if action:
                    action.triggered.connect(lambda _, o=oda["codice_oda"]: self.mw._navigate_to_oda(o))
            menu.addSeparator()
            return len(matches[:20])
        except Exception:
            return 0

    def _search_extended(self, query: str, menu: QMenu) -> int:
        """Ricerca nella contabilità estesa (Giornaliere, Cantiere, Certificati)."""
        try:
            from src.core.contabilita_manager import ContabilitaManager

            ext_matches = ContabilitaManager.search_extended(query)
            count = 0
            count += self._add_giornaliere_matches(query, menu, ext_matches.get("GIORNALIERE"))
            count += self._add_cantiere_matches(query, menu, ext_matches.get("CANTIERE"))
            count += self._add_certificati_matches(query, menu, ext_matches.get("CERTIFICATI"))
            return count
        except Exception:
            return 0

    def _add_giornaliere_matches(self, query: str, menu: QMenu, matches: Optional[list]) -> int:
        """Aggiunge i risultati delle Giornaliere al menu."""
        if not matches:
            return 0
        self._add_disabled_action(menu, "GIORNALIERE:")
        for g in matches[:20]:
            text = f"{g['data']} - {g['personale']} - {g['descrizione'][:40]}..."
            action = menu.addAction(text)
            if action:
                action.triggered.connect(lambda _, q=query: self.mw._navigate_to_extended(1, q))
        menu.addSeparator()
        return len(matches[:20])

    def _add_cantiere_matches(self, query: str, menu: QMenu, matches: Optional[list]) -> int:
        """Aggiunge i risultati del Cantiere al menu."""
        if not matches:
            return 0
        self._add_disabled_action(menu, "CANTIERE (Scarico Ore):")
        for c in matches[:20]:
            text = f"{c['data']} - {c['personale']} - {c['commessa']}"
            action = menu.addAction(text)
            if action:
                action.triggered.connect(lambda _, q=query: self.mw._navigate_to_dataease(q))
        menu.addSeparator()
        return len(matches[:20])

    def _add_certificati_matches(self, query: str, menu: QMenu, matches: Optional[list]) -> int:
        """Aggiunge i risultati dei Certificati al menu."""
        if not matches:
            return 0
        self._add_disabled_action(menu, "CERTIFICATI:")
        for c in matches[:20]:
            text = f"{c['matricola']} - {c['modello']} ({c['costruttore']})"
            action = menu.addAction(text)
            if action:
                action.triggered.connect(lambda _, q=query: self.mw._navigate_to_extended(3, q))
        menu.addSeparator()
        return len(matches[:20])

    def _search_employees(self, query: str, menu: QMenu) -> int:
        """Ricerca dei dipendenti."""
        try:
            matches = TimbratureStorage().search_employees(query)
            if not matches:
                return 0

            self._add_disabled_action(menu, "DIPENDENTI:")
            for emp in matches[:20]:
                text = f"{emp['cognome']} {emp['nome']}"
                action = menu.addAction(text)
                if action:
                    action.triggered.connect(lambda _, q=text: self.mw._navigate_to_timbrature(q))
            menu.addSeparator()
            return len(matches[:20])
        except Exception:
            return 0

    def _search_storico_oda(self, query: str, menu: QMenu) -> int:
        """Ricerca nello Storico OdA."""
        try:
            import sqlite3

            from src.core.config_manager import CONFIG_DIR

            db_path = CONFIG_DIR / "data" / "storico_oda.db"
            if not db_path.exists():
                return 0

            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Ricerca in tutte le colonne rilevanti
            search_pattern = f"%{query}%"
            cursor.execute(
                """
                SELECT oda, descrizione, pos_oda
                FROM storico_oda
                WHERE CAST(oda AS TEXT) LIKE ? OR
                      descrizione LIKE ? OR
                      testo_breve LIKE ? OR
                      CAST(contratto AS TEXT) LIKE ? OR
                      descrizione_fornitore LIKE ?
                LIMIT 10
                """,
                [search_pattern] * 5,
            )

            matches = cursor.fetchall()
            conn.close()

            if not matches:
                return 0

            self._add_disabled_action(menu, "STORICO OdA:")
            for oda, desc, pos in matches:
                desc_short = (desc[:50] + "...") if desc and len(desc) > 50 else desc
                text = f"OdA {oda}/{pos} - {desc_short}"
                action = menu.addAction(text)
                if action:
                    action.triggered.connect(lambda _, o=oda: self.mw._navigate_to(10))  # Storico OdA
            menu.addSeparator()
            return len(matches)
        except Exception:
            return 0

    def _search_attivita_programmate(self, query: str, menu: QMenu) -> int:
        """Ricerca nelle Attività Programmate."""
        try:
            import sqlite3

            from src.core.config_manager import CONFIG_DIR

            db_path = CONFIG_DIR / "data" / "contabilita.db"
            if not db_path.exists():
                return 0

            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            search_pattern = f"%{query}%"
            cursor.execute(
                """
                SELECT area, pdl, descrizione_attivita
                FROM attivita_programmate
                WHERE area LIKE ? OR
                      pdl LIKE ? OR
                      descrizione_attivita LIKE ? OR
                      stato_pdl LIKE ? OR
                      stato_attivita LIKE ?
                LIMIT 10
                """,
                [search_pattern] * 5,
            )

            matches = cursor.fetchall()
            conn.close()

            if not matches:
                return 0

            self._add_disabled_action(menu, "ATTIVITÀ PROGRAMMATE:")
            for area, pdl, desc in matches:
                desc_short = (desc[:40] + "...") if desc and len(desc) > 40 else desc
                text = f"{area} - {pdl}: {desc_short}"
                action = menu.addAction(text)
                if action:
                    action.triggered.connect(lambda: self.mw._navigate_to(3))  # Contabilità
            menu.addSeparator()
            return len(matches)
        except Exception:
            return 0

    def _search_pdl(self, query: str, menu: QMenu) -> int:
        """Ricerca nei PDL SafeWork."""
        try:
            import sqlite3

            from src.core.config_manager import CONFIG_DIR

            db_path = CONFIG_DIR / "data" / "pdl.db"
            if not db_path.exists():
                return 0

            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            search_pattern = f"%{query}%"
            cursor.execute(
                """
                SELECT odl, descrizione, unita_tecnica
                FROM pdl
                WHERE CAST(odl AS TEXT) LIKE ? OR
                      descrizione LIKE ? OR
                      unita_tecnica LIKE ? OR
                      stato LIKE ?
                LIMIT 10
                """,
                [search_pattern] * 4,
            )

            matches = cursor.fetchall()
            conn.close()

            if not matches:
                return 0

            self._add_disabled_action(menu, "PDL SAFEWORK:")
            for odl, desc, ut in matches:
                desc_short = (desc[:40] + "...") if desc and len(desc) > 40 else desc
                text = f"ODL {odl} - {ut}: {desc_short}"
                action = menu.addAction(text)
                if action:
                    action.triggered.connect(lambda: self.mw.navigate_to_panel("scarico_pdl"))
            menu.addSeparator()
            return len(matches)
        except Exception:
            return 0

    def _search_audit(self, query: str, menu: QMenu) -> int:
        """Ricerca negli Audit Log."""
        try:
            from src.core.audit_manager import AuditManager

            audit_logs = AuditManager.instance().get_logs(limit=100)
            matches = [
                log
                for log in audit_logs
                if query.lower() in str(log["action"]).lower() or query.lower() in str(log["entity"]).lower()
            ]
            if not matches:
                return 0

            self._add_disabled_action(menu, "AUDIT LOG:")
            for log in matches[:3]:
                action = menu.addAction(f"{log['action']} - {log['entity']}")
                if action:
                    action.triggered.connect(lambda: self.mw._navigate_to(6))
            return len(matches[:3])
        except Exception:
            return 0
