"""
SyncroJob - Workflow Controller
Gestisce i flussi di lavoro complessi e le interazioni Command Palette -> Bot.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QDate, QObject, QTimer

from src.gui.main_window.page_index import PageIndex
from src.gui.widgets.toast import ToastManager

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow


class WorkflowController(QObject):
    """
    Controller per il coordinamento dei flussi di lavoro (workflow) dell'applicazione.
    Gestisce l'input proveniente dalla Command Palette e lo trasforma in azioni sui Bot.
    """

    def __init__(self, main_window: MainWindow) -> None:
        super().__init__(main_window)
        self.mw = main_window

    def run_timbrature_bot(self, mode: str) -> None:
        """Avvia il bot delle timbrature in una modalita' specifica."""
        # Assicurati che il pannello sia inizializzato
        if not hasattr(self.mw, "timbrature_bot_panel"):
            self.mw.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)

        panel: Any = getattr(self.mw, "timbrature_bot_panel", None)
        if panel:
            if not getattr(panel, "_mw_signals_connected", False):
                panel.status_changed.connect(
                    lambda color, msg: self.mw.status_bar_component.status_portale.setStatus(msg, color)
                )
                panel._mw_signals_connected = True

            data_da = QDate.currentDate().toString("dd.MM.yyyy")
            data_a = QDate.currentDate().toString("dd.MM.yyyy")
            if mode == "ieri":
                data_da = QDate.currentDate().addDays(-1).toString("dd.MM.yyyy")
                data_a = QDate.currentDate().addDays(-1).toString("dd.MM.yyyy")
            elif mode == "mese":
                data_da = QDate.currentDate().toString("01.MM.yyyy")

            ToastManager.instance().show(f"[AVVIO] Avvio Timbrature ({mode})...", "info")
            panel.run_externally({"data_da": data_da, "data_a": data_a})

    def handle_scarico_ts_input(self, args: list[Any]) -> None:
        """Gestisce l'input della Command Palette per lo scarico TS."""
        if not args or not args[0]:
            return
        self.mw.navigation_controller.navigate_to_panel("scarico_ts")
        panel: Any = getattr(self.mw, "scarico_panel", None)
        if panel:
            QTimer.singleShot(
                200,
                lambda: panel.run_externally({"single_item": {"numero_oda": args[0], "posizione_oda": ""}}),
            )

    def handle_dettagli_oda_input(self, args: list[Any]) -> None:
        """Gestisce l'input della Command Palette per i dettagli OdA."""
        if not args or not args[0]:
            return
        self.mw.navigation_controller.navigate_to_panel("dettagli_oda")
        panel: Any = getattr(self.mw, "dettagli_panel", None)
        if panel:
            QTimer.singleShot(
                200,
                lambda: panel.run_externally({"single_item": {"Numero OdA": args[0], "numero_oda": args[0]}}),
            )

    def handle_pdl_input(self, args: list[Any]) -> None:
        """Gestisce l'input della Command Palette per lo scarico PDL."""
        if not args or not args[0]:
            return
        self.mw.navigation_controller.navigate_to_panel("scarico_pdl")
        panel: Any = getattr(self.mw, "pdl_panel", None)
        if panel:
            QTimer.singleShot(
                200,
                lambda: panel.run_externally({"single_item": {"numero_pdl": args[0]}}),
            )

    def handle_prenota_bp_input(self, args: list[Any]) -> None:
        """Gestisce l'input della Command Palette per la prenotazione BP."""
        if not args or not args[0]:
            return
        self.mw.navigation_controller.navigate_to_panel("prenota_bp")
        panel: Any = getattr(self.mw, "prenota_panel", None)
        if panel:
            QTimer.singleShot(
                200,
                lambda: panel.run_externally({"single_item": {"numero_bp": args[0]}}),
            )

    def run_carico_ts(self) -> None:
        """Avvia la navigazione e l'automazione Carico TS."""
        self.mw.navigation_controller.navigate_to_panel("carico_ts")
        panel: Any = getattr(self.mw, "carico_panel", None)
        if panel:
            QTimer.singleShot(200, lambda: panel.run_externally({}))

    def run_sync_dataease(self) -> None:
        """Avvia la sincronizzazione DataEase."""
        self.mw.navigation_controller.navigate_to(PageIndex.DATAEASE)
        panel: Any = getattr(self.mw, "scarico_ore_panel", None)
        if panel and hasattr(panel, "_start_update"):
            QTimer.singleShot(200, panel._start_update)

    def run_sync_strumentale(self) -> None:
        """Avvia la sincronizzazione contabilit  strumentale."""
        self.mw.navigation_controller.navigate_to(PageIndex.STRUMENTALE)
        panel: Any = getattr(self.mw, "contabilita_panel", None)
        if panel and hasattr(panel, "refresh_tabs"):
            QTimer.singleShot(200, panel.refresh_tabs)

    def run_dettagli_oda_update(self) -> None:
        """Avvia l'aggiornamento massivo dello Storico OdA tramite il bot Dettagli OdA."""
        # 1. Recupera il pannello Automazioni (Lazy Loading) senza navigare
        automazioni_widget = self.mw.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)

        # Import lazy per evitare dipendenza circolare
        from src.gui.widgets.automazioni_widget import AutomazioniWidget  # noqa: PLC0415

        if isinstance(automazioni_widget, AutomazioniWidget):
            # 2. Imposta i tab corretti internamente
            automazioni_widget.set_active_tab(0, 0)

            # 3. Recupera il pannello bot registrato
            panel: Any = getattr(self.mw, "dettagli_panel", None)
            if panel:
                # Feedback visivo nello Storico OdA
                ToastManager.instance().show(
                    "[AVVIO] Sincronizzazione database OdA avviata in background...", "info"
                )

                # Calcola la data odierna nel formato richiesto: GG.MM.AAAA
                data_attuale = QDate.currentDate().toString("dd.MM.yyyy")

                # Avvio bot bypassando le righe (triggera Lista Generale)
                # Passiamo data_a come data attuale (override del widget UI)
                QTimer.singleShot(100, lambda: panel.run_externally({"rows": [], "data_a": data_attuale}))
