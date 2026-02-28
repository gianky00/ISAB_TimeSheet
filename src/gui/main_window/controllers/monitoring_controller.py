"""
SyncroJob - Monitoring Controller
Gestisce i controlli proattivi (abilitazioni, anomalie, health) e i relativi timer.
"""

from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, QTimer

from src.core.auth_monitor import check_expiring_isab_authorizations
from src.core.constants import Icons
from src.gui.styles.constants import ANIMATION_TIMINGS
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow


class MonitoringController(QObject):
    """
    Controller per il monitoraggio dello stato del sistema e delle autorizzazioni.
    """

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.mw = main_window
        self.auth_check_timer = QTimer(self)

    def start_monitoring(self) -> None:
        """Avvia i timer di monitoraggio."""
        self.check_isab_authorizations()
        self.auth_check_timer.timeout.connect(self.check_isab_authorizations)
        self.auth_check_timer.start(ANIMATION_TIMINGS["auth_check"])

    def check_isab_authorizations(self) -> None:
        """Esegue il controllo proattivo delle abilitazioni ISAB in scadenza."""
        try:
            expiring = check_expiring_isab_authorizations()

            # Aggiorna badge sidebar
            if hasattr(self.mw, "sidebar") and hasattr(self.mw.sidebar, "btn_dipendenti"):
                self.mw.sidebar.btn_dipendenti.set_badge(len(expiring))

            if not expiring:
                return

            scaduti = [d for d in expiring if d["stato"] == "SCADUTA"]
            in_scadenza = [d for d in expiring if d["stato"] == "IN SCADENZA"]

            red_dot = get_asset_path(Icons.STATUS_DOT_RED)
            yellow_dot = get_asset_path(Icons.STATUS_DOT_YELLOW)

            msg = "<b>Monitoraggio Abilitazioni ISAB</b><br/>"
            if scaduti:
                msg += f"<img src='{red_dot}' width='14' height='14'> {len(scaduti)} Abilitazioni SCADUTE (>30 gg)<br/>"
            if in_scadenza:
                msg += f"<img src='{yellow_dot}' width='14' height='14'> {len(in_scadenza)} In scadenza (20-30 gg)<br/>"
            msg += "<br/><small>Controlla la tabella 'Dipendenti' per i dettagli.</small>"

            ToastManager.instance().show(msg, "warning" if in_scadenza or scaduti else "info", 8000)
        except Exception as e:
            print(f"Errore monitoraggio autorizzazioni: {e}")

    def handle_anomalies_found(self, count: int) -> None:
        """Reagisce al rilevamento di anomalie nei dati."""
        if hasattr(self.mw, "sidebar"):
            self.mw.sidebar.btn_lyra.set_badge(count)
        if count > 0:
            alert_icon = get_asset_path(Icons.ALERT)
            ToastManager.instance().show(
                f"<img src='{alert_icon}' width='14' height='14'> Lyra ha rilevato {count} anomalie",
                "warning",
            )
