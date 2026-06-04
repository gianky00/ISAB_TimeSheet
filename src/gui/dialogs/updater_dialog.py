"""SyncroJob - Updater Dialog.

UI components for update notifications and progress.
Moved from core/updater/gui.py to follow SRP.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from collections.abc import Callable


from src.application.services import version
from src.application.services.updater.engine import (
    DownloadWorker,
    run_installer_and_exit,
    set_pending_installer,
)
from src.gui.widgets.wave_progress import WaveProgressBar
from src.gui.workers.update_worker import UpdateCheckWorker

logger = logging.getLogger(__name__)

# Store active workers to prevent garbage collection
_active_update_worker: DownloadWorker | None = None
_active_check_worker: UpdateCheckWorker | None = None
_active_update_dialog: UpdateProgressDialog | None = None


class UpdateProgressDialog(QDialog):
    """Progress dialog for update downloads or network transfers.

    Inizializza il dialog di progresso.

    Args:
      url_or_path: URL o percorso locale del file da scaricare/trasferire.
      parent: Widget genitore.

    Attributes:
        current_value: Segnale o attributo della classe.
    """

    def __init__(self, url_or_path: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Aggiornamento SyncroJob")
        self.setFixedSize(450, 200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)

        self.lbl_status = QLabel("Avvio download...")
        self.pb = WaveProgressBar()
        # Nota: le impostazioni standard sono ora gestite internamente da WaveProgressBar

        self.lbl_details = QLabel("Preparazione...")
        self.lbl_retry = QLabel("")

        # Inizializza animazione per fluidit  estrema della barra
        self.animation = QPropertyAnimation(self, b"current_value")
        self.animation.setDuration(350)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._val_proxy = 0

        self.setup_ui()
        self.worker = DownloadWorker(url_or_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished_download.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.retrying.connect(self.on_retrying)

        if not url_or_path.startswith("http"):
            self.lbl_status.setText("Avvio trasferimento rete...")

    def setup_ui(self) -> None:
        """Configura gli elementi grafici del dialog."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        self.lbl_status.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.lbl_status)

        # La barra WaveProgressBar gestisce internamente stile e dimensioni
        layout.addWidget(self.pb)

        self.lbl_details.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.lbl_details)

        self.lbl_retry.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.lbl_retry.setStyleSheet("color: #DC3545;")
        layout.addWidget(self.lbl_retry)

    def start(self) -> None:
        """Mostra il dialog e avvia il worker di download."""
        self.show()
        self.worker.start()

    @Slot(int, int, float, float)
    def update_progress(self, downloaded: int, total: int, speed: float, eta: float) -> None:
        """Aggiorna la barra di progresso con animazione e le label informative."""
        self.lbl_retry.setText("")
        if total <= 0:
            self.pb.setMaximum(0)
            self.lbl_status.setText("Operazione in corso...")
            return

        self.pb.setMaximum(100)
        percentage = int((downloaded / total) * 100)

        # Avvia l'animazione verso il nuovo valore %
        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.stop()

        self.animation.setStartValue(self.pb.value())
        self.animation.setEndValue(percentage)
        self.animation.start()

        # Formattazione dettagli
        speed_mb = speed / (1024 * 1024)
        mb_down = downloaded / (1024 * 1024)
        mb_total = total / (1024 * 1024)

        eta_str = f"{int(eta // 60)}m {int(eta % 60)}s" if eta >= 60 else f"{int(eta)}s"
        action = "Scaricamento" if self.worker.url_or_path.startswith("http") else "Trasferimento"

        self.lbl_status.setText(f"[AVVIO] {action} in corso...")
        self.lbl_details.setText(
            f"   <b>{mb_down:.1f} / {mb_total:.1f} MB</b>      <b>{speed_mb:.2f} MB/s</b>    [ATTESA] <b>{eta_str}</b>"
        )

    def get_current_value(self) -> int:
        """Getter per QPropertyAnimation."""
        return self.pb.value()

    def set_current_value(self, val: int) -> None:
        """Setter per QPropertyAnimation."""
        self.pb.setValue(val)

    # Propriet  Qt per l'animazione
    current_value = Property(int, fget=get_current_value, fset=set_current_value)

    @Slot(int)
    def on_retrying(self, retry_count: int) -> None:
        """Mostra un avviso in caso di tentativi di riconnessione."""
        self.lbl_retry.setText(f"⚠️ Connessione instabile. Tentativo #{retry_count}...")

    @Slot(str)
    def on_finished(self, setup_path: str) -> None:
        """Gestisce il completamento del download chiudendo il dialog e proponendo l'installazione."""
        self.close()
        show_install_prompt(setup_path, cast("QWidget", self.parent()))

    @Slot(str)
    def on_error(self, err_msg: str) -> None:
        """Mostra un messaggio d'errore critico in caso di fallimento."""
        self.close()
        QMessageBox.critical(cast("QWidget", self.parent()), "Errore", f"Trasferimento interrotto: {err_msg}")


def show_install_prompt(setup_path: str, parent: QWidget | None = None) -> None:
    """Mostra un messaggio all'utente per decidere se installare subito o alla chiusura."""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle("[SYNC] Aggiornamento Pronto")
    msg_box.setText("L'aggiornamento  stato scaricato ed  pronto per l'installazione.\n\nCosa desideri fare?")
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setStyle(QApplication.style())

    btn_now = msg_box.addButton("Installa Ora", QMessageBox.ButtonRole.AcceptRole)
    btn_later = msg_box.addButton("Alla Chiusura", QMessageBox.ButtonRole.ActionRole)
    msg_box.addButton("Annulla", QMessageBox.ButtonRole.RejectRole)

    msg_box.setStyleSheet("""
    QMessageBox { background-color: white; }
    QLabel { color: black; font-size: 13px; }
    QPushButton { background-color: #f0f0f0; color: black; border: 1px solid #ccc; padding: 6px 15px; border-radius: 4px; font-weight: bold; }
    QPushButton:hover { background-color: #e0e0e0; }
  """)

    msg_box.exec()
    if msg_box.clickedButton() == btn_now:
        run_installer_and_exit(setup_path)
    elif msg_box.clickedButton() == btn_later:
        set_pending_installer(setup_path)
        QMessageBox.information(
            parent, "ℹ️ Info", "L'aggiornamento partir  automaticamente alla chiusura dell'app."
        )


def check_for_updates(
    parent: QWidget | None = None,
    silent: bool = True,
    callback: Callable[[dict[str, Any]], None] | None = None,
) -> None:
    """Controlla se sono disponibili aggiornamenti in background (Asincrono)."""
    global _active_check_worker  # noqa: PLW0603

    if _active_check_worker and _active_check_worker.isRunning():
        return

    _active_check_worker = UpdateCheckWorker(silent=silent)

    _active_check_worker.finished_signal.connect(lambda res: handle_update_result(res, parent, callback))
    _active_check_worker.no_update_signal.connect(
        lambda: not silent
        and QMessageBox.information(
            parent,
            "[OK] Aggiornamento",
            f"L'applicazione è aggiornata (v{version.__version__})",
        )
    )
    _active_check_worker.error_signal.connect(lambda msg: _on_update_error(msg, silent, parent))
    _active_check_worker.start()


def _on_update_error(msg: str, silent: bool, parent: QWidget | None) -> None:
    """Gestisce gli errori durante il controllo aggiornamenti."""
    if not silent:
        QMessageBox.warning(
            parent,
            "Errore Aggiornamento",
            f"Impossibile controllare gli aggiornamenti: {msg}",
        )
    logger.debug(f"Update check failed: {msg}")


def handle_update_result(
    latest_update: dict[str, Any],
    parent: QWidget | None = None,
    callback: Callable[[dict[str, Any]], None] | None = None,
) -> None:
    """Gestisce l'esito positivo del controllo aggiornamenti (Asincrono)."""
    if callback:
        callback(latest_update)
        return

    is_complete = latest_update.get("is_complete", False)
    setup_path = latest_update.get("setup_path", "")
    remote_ver_str = latest_update["version"]
    changelog = latest_update.get("changelog", "")
    download_url = latest_update.get("url", "")

    if is_complete:
        show_install_prompt(setup_path, parent)
    else:
        msg = f"Nuova versione {remote_ver_str} disponibile!\n"
        if changelog:
            msg += f"\nNovità:\n{changelog}\n"
        msg += "\nVuoi aggiornare ora?"
        reply = QMessageBox.question(
            parent,
            "[SYNC] Aggiornamento",
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            perform_auto_update(download_url, parent)


def perform_auto_update(download_url: str, parent: QWidget | None = None) -> None:
    """Avvia la procedura di download e installazione automatica dell'aggiornamento."""
    if parent is None:
        for widget in QApplication.topLevelWidgets():
            if widget.isWindow() and not widget.parent():
                parent = widget
                break

    global _active_update_worker  # noqa: PLW0603
    _active_update_worker = DownloadWorker(download_url)

    # Rilevamento banner robusto (MainWindow lo ha in tool_bar_component o come alias)
    banner = getattr(parent, "update_banner", None)
    if not banner and hasattr(parent, "tool_bar_component"):
        banner = getattr(cast("Any", parent).tool_bar_component, "update_banner", None)

    if banner:
        _active_update_worker.progress.connect(banner.update_progress)
        if hasattr(parent, "_on_update_downloaded"):
            _active_update_worker.finished_download.connect(cast("Any", parent)._on_update_downloaded)
        if hasattr(parent, "_on_update_error"):
            _active_update_worker.error.connect(cast("Any", parent)._on_update_error)
    else:
        global _active_update_dialog  # noqa: PLW0603
        _active_update_dialog = UpdateProgressDialog(download_url, parent)
        _active_update_dialog.start()
        return

    _active_update_worker.start()
