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

        # --- 1. Contabilità Strumentale (OdA) ---
        try:
            from src.core.contabilita_manager import ContabilitaManager

            oda_matches = ContabilitaManager.search_oda(query)
            if oda_matches:
                results_menu.addAction("📊 CONTABILITÀ STRUMENTALE (OdA):").setEnabled(
                    False
                )
                for oda in oda_matches[:20]:
                    text = f"OdA {oda['codice_oda']} - {oda['descrizione'][:50]}..."
                    action = results_menu.addAction(text)
                    action.triggered.connect(
                        lambda _, o=oda["codice_oda"]: self.mw._navigate_to_oda(o)
                    )
                    found_count += 1
                results_menu.addSeparator()
        except Exception:
            pass

        # --- 2. Contabilità Estesa ---
        try:
            ext_matches = ContabilitaManager.search_extended(query)
            # Giornaliere
            if ext_matches.get("GIORNALIERE"):
                results_menu.addAction("📂 GIORNALIERE:").setEnabled(False)
                for g in ext_matches["GIORNALIERE"][:20]:
                    text = (
                        f"{g['data']} - {g['personale']} - {g['descrizione'][:40]}..."
                    )
                    action = results_menu.addAction(text)
                    action.triggered.connect(
                        lambda _, q=query: self.mw._navigate_to_extended(1, q)
                    )
                    found_count += 1
                results_menu.addSeparator()
            # Cantiere
            if ext_matches.get("CANTIERE"):
                results_menu.addAction("🏗️ CANTIERE (Scarico Ore):").setEnabled(False)
                for c in ext_matches["CANTIERE"][:20]:
                    text = f"{c['data']} - {c['personale']} - {c['commessa']}"
                    action = results_menu.addAction(text)
                    action.triggered.connect(
                        lambda _, q=query: self.mw._navigate_to_dataease(q)
                    )
                    found_count += 1
                results_menu.addSeparator()
            # Certificati
            if ext_matches.get("CERTIFICATI"):
                results_menu.addAction("📜 CERTIFICATI:").setEnabled(False)
                for c in ext_matches["CERTIFICATI"][:20]:
                    text = f"{c['matricola']} - {c['modello']} ({c['costruttore']})"
                    action = results_menu.addAction(text)
                    action.triggered.connect(
                        lambda _, q=query: self.mw._navigate_to_extended(3, q)
                    )
                    found_count += 1
                results_menu.addSeparator()
        except Exception:
            pass

        # --- 3. Dipendenti ---
        try:
            emp_matches = TimbratureStorage().search_employees(query)
            if emp_matches:
                results_menu.addAction("👥 DIPENDENTI:").setEnabled(False)
                for emp in emp_matches[:20]:
                    text = f"{emp['cognome']} {emp['nome']}"
                    action = results_menu.addAction(text)
                    action.triggered.connect(
                        lambda _, q=text: self.mw._navigate_to_timbrature(q)
                    )
                    found_count += 1
                results_menu.addSeparator()
        except Exception:
            pass

        # --- 4. Audit Log ---
        try:
            from src.core.audit_manager import AuditManager

            audit_logs = AuditManager().get_logs(limit=100)
            matches = [
                log
                for log in audit_logs
                if query.lower() in str(log["action"]).lower()
                or query.lower() in str(log["entity"]).lower()
            ]
            if matches:
                results_menu.addAction("🛡️ AUDIT LOG:").setEnabled(False)
                for log in matches[:3]:
                    action = results_menu.addAction(
                        f"{log['action']} - {log['entity']}"
                    )
                    action.triggered.connect(lambda: self.mw._navigate_to(6))
                    found_count += 1
        except Exception:
            pass

        if found_count == 0:
            results_menu.addAction("❌ Nessun risultato trovato").setEnabled(False)

        pos = self.mw.global_search.mapToGlobal(
            QPoint(0, self.mw.global_search.height())
        )
        results_menu.exec(pos)
