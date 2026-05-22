"""SyncroJob - Monitoring Controller.

Gestisce i controlli proattivi (abilitazioni, health) e i relativi timer.
"""

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, QTimer

from src.core.auth_monitor import check_expiring_isab_authorizations
from src.core.constants import Icons
from src.core.logging import get_logger
from src.gui.styles.constants import ANIMATION_TIMINGS
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

logger = get_logger(__name__)


class MonitoringController(QObject):
    """Controller per il monitoraggio dello stato del sistema e delle autorizzazioni."""

    def __init__(self, main_window: "MainWindow") -> None:
        """Inizializza la classe."""
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
            icon_size = 14
            if scaduti:
                msg += f"<img src='{red_dot}' width='{icon_size}' height='{icon_size}'> {len(scaduti)} Abilitazioni SCADUTE (>30 gg)<br/>"
            if in_scadenza:
                msg += f"<img src='{yellow_dot}' width='{icon_size}' height='{icon_size}'> {len(in_scadenza)} In scadenza (20-30 gg)<br/>"
            msg += "<br/><small>Controlla la tabella 'Dipendentì per i dettagli.</small>"

            toast_timeout_ms = 8000
            ToastManager.instance().show(
                msg, "warning" if in_scadenza or scaduti else "info", toast_timeout_ms, is_rich_text=True
            )
        except Exception:
            logger.exception("Errore monitoraggio autorizzazioni")
