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
        found_count += self._search_extended(query, results_menu)
        found_count += self._search_employees(query, results_menu)
        found_count += self._search_audit(query, results_menu)

        if found_count == 0:
            self._add_disabled_action(results_menu, "❌ Nessun risultato trovato")

        pos = self.mw.global_search.mapToGlobal(
            QPoint(0, self.mw.global_search.height())
        )
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

            self._add_disabled_action(menu, "📊 CONTABILITÀ STRUMENTALE (OdA):")
            for oda in matches[:20]:
                text = f"OdA {oda['codice_oda']} - {oda['descrizione'][:50]}..."
                action = menu.addAction(text)
                if action:
                    action.triggered.connect(
                        lambda _, o=oda["codice_oda"]: self.mw._navigate_to_oda(o)
                    )
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

            # Giornaliere
            if ext_matches.get("GIORNALIERE"):
                self._add_disabled_action(menu, "📂 GIORNALIERE:")
                for g in ext_matches["GIORNALIERE"][:20]:
                    text = (
                        f"{g['data']} - {g['personale']} - {g['descrizione'][:40]}..."
                    )
                    action = menu.addAction(text)
                    if action:
                        action.triggered.connect(
                            lambda _, q=query: self.mw._navigate_to_extended(1, q)
                        )
                    count += 1
                menu.addSeparator()

            # Cantiere
            if ext_matches.get("CANTIERE"):
                self._add_disabled_action(menu, "🏗️ CANTIERE (Scarico Ore):")
                for c in ext_matches["CANTIERE"][:20]:
                    text = f"{c['data']} - {c['personale']} - {c['commessa']}"
                    action = menu.addAction(text)
                    if action:
                        action.triggered.connect(
                            lambda _, q=query: self.mw._navigate_to_dataease(q)
                        )
                    count += 1
                menu.addSeparator()

            # Certificati
            if ext_matches.get("CERTIFICATI"):
                self._add_disabled_action(menu, "📜 CERTIFICATI:")
                for c in ext_matches["CERTIFICATI"][:20]:
                    text = f"{c['matricola']} - {c['modello']} ({c['costruttore']})"
                    action = menu.addAction(text)
                    if action:
                        action.triggered.connect(
                            lambda _, q=query: self.mw._navigate_to_extended(3, q)
                        )
                    count += 1
                menu.addSeparator()

            return count
        except Exception:
            return 0

    def _search_employees(self, query: str, menu: QMenu) -> int:
        """Ricerca dei dipendenti."""
        try:
            matches = TimbratureStorage().search_employees(query)
            if not matches:
                return 0

            self._add_disabled_action(menu, "👥 DIPENDENTI:")
            for emp in matches[:20]:
                text = f"{emp['cognome']} {emp['nome']}"
                action = menu.addAction(text)
                if action:
                    action.triggered.connect(
                        lambda _, q=text: self.mw._navigate_to_timbrature(q)
                    )
            menu.addSeparator()
            return len(matches[:20])
        except Exception:
            return 0

    def _search_audit(self, query: str, menu: QMenu) -> int:
        """Ricerca negli Audit Log."""
        try:
            from src.core.audit_manager import AuditManager

            audit_logs = AuditManager().get_logs(limit=100)
            matches = [
                log
                for log in audit_logs
                if query.lower() in str(log["action"]).lower()
                or query.lower() in str(log["entity"]).lower()
            ]
            if not matches:
                return 0

            self._add_disabled_action(menu, "🛡️ AUDIT LOG:")
            for log in matches[:3]:
                action = menu.addAction(f"{log['action']} - {log['entity']}")
                if action:
                    action.triggered.connect(lambda: self.mw._navigate_to(6))
            return len(matches[:3])
        except Exception:
            return 0
