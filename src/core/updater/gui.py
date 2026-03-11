"""
SyncroJob - Updater GUI
UI components for update notifications and progress.
"""

from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

import requests
from packaging import version as pkg_version
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QMessageBox, QProgressBar, QVBoxLayout, QWidget

from .. import version
from .engine import DownloadWorker, get_local_setup_path, run_installer_and_exit, set_pending_installer

# Store active worker to prevent garbage collection
_active_update_worker = None
_active_update_dialog = None


class UpdateProgressDialog(QDialog):
    """Fallback progress dialog for update downloads."""
    def __init__(self, url: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Aggiornamento Resiliente")
        self.setFixedSize(450, 200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.worker = DownloadWorker(url)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished_download.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.retrying.connect(self.on_retrying)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        self.lbl_status = QLabel("Avvio download...")
        self.lbl_status.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.lbl_status)
        self.pb = QProgressBar()
        self.pb.setFixedHeight(24)
        self.pb.setStyleSheet("QProgressBar { border: 1px solid #CCCCCC; border-radius: 6px; text-align: center; background-color: #F0F0F0; } QProgressBar::chunk { background-color: #0D6EFD; border-radius: 5px; }")
        layout.addWidget(self.pb)
        self.lbl_details = QLabel("Preparazione...")
        self.lbl_details.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.lbl_details)
        self.lbl_retry = QLabel("")
        self.lbl_retry.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.lbl_retry.setStyleSheet("color: #DC3545;")
        layout.addWidget(self.lbl_retry)

    def start(self):
        self.show()
        self.worker.start()

    @pyqtSlot(int, int, float, float)
    def update_progress(self, downloaded, total, speed, eta):
        self.lbl_retry.setText("")
        if total > 0:
            self.pb.setMaximum(total)
            self.pb.setValue(downloaded)
            percent = (downloaded / total) * 100
            mb_down = downloaded / (1024 * 1024)
            mb_total = total / (1024 * 1024)
            speed_mb = speed / (1024 * 1024)
            self.lbl_status.setText(f"Scaricamento: {int(percent)}% completato")
            self.lbl_details.setText(f"{mb_down:.1f} MB di {mb_total:.1f} MB ({speed_mb:.2f} MB/s) - ETA: {int(eta)}s")
        else:
            self.pb.setMaximum(0)
            self.lbl_status.setText("Scaricamento in corso...")

    @pyqtSlot(int)
    def on_retrying(self, retry_count):
        self.lbl_retry.setText(f"⚠️ Connessione persa. Tentativo di ripresa #{retry_count}...")

    @pyqtSlot(str)
    def on_finished(self, setup_path):
        self.close()
        show_install_prompt(setup_path, cast("QWidget", self.parent()))

    @pyqtSlot(str)
    def on_error(self, err_msg):
        self.close()
        QMessageBox.critical(cast("QWidget", self.parent()), "Errore", f"Download interrotto: {err_msg}")


def show_install_prompt(setup_path: str, parent: QWidget | None = None):
    """Shows choices for immediate or delayed installation."""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle("🔄 Aggiornamento Pronto")
    msg_box.setText("L'aggiornamento è stato scaricato ed è pronto per l'installazione.\n\nCosa desideri fare?")
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setStyle(QApplication.style())

    btn_now = msg_box.addButton("Installa Ora", QMessageBox.ButtonRole.AcceptRole)
    btn_later = msg_box.addButton("Alla Chiusura", QMessageBox.ButtonRole.ActionRole)
    msg_box.addButton("Annulla", QMessageBox.ButtonRole.RejectRole)

    msg_box.setStyleSheet("""
        QMessageBox { background-color: white; }
        QLabel { color: black; font-size: 13px; }
        QPushButton {
            background-color: #f0f0f0;
            color: black;
            border: 1px solid #ccc;
            padding: 6px 15px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #e0e0e0; }
    """)

    msg_box.exec()
    if msg_box.clickedButton() == btn_now:
        run_installer_and_exit(setup_path)
    elif msg_box.clickedButton() == btn_later:
        set_pending_installer(setup_path)
        QMessageBox.information(parent, "ℹ️ Info", "L'aggiornamento partirà automaticamente alla chiusura dell'app.")


def check_for_updates(
    parent: QWidget | None = None,
    silent: bool = True,
    callback: Callable[[str, str, str, bool, bool], Any] | None = None,
) -> None:
    """Checks for new version availability."""
    url = version.UPDATE_URL
    if not url or "example.com" in url:
        return

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            remote_ver_str = data.get("version")
            download_url = data.get("url")
            changelog = data.get("changelog", "")

            if not remote_ver_str or not download_url:
                return

            if pkg_version.parse(remote_ver_str) > pkg_version.parse(version.__version__):
                setup_path = get_local_setup_path(download_url)

                # HEAD request for remote size
                remote_size = 0
                try:
                    head_resp = requests.head(download_url, timeout=5)
                    remote_size = int(head_resp.headers.get("content-length", 0))
                except Exception:  # noqa: S110
                    pass

                local_size = Path(setup_path).stat().st_size if Path(setup_path).exists() else 0
                is_partial = 0 < local_size < remote_size
                is_complete = remote_size > 0 and local_size >= remote_size

                if callback:
                    callback(remote_ver_str, download_url, changelog, is_partial, is_complete)
                    return

                if is_complete:
                    show_install_prompt(setup_path, parent)
                else:
                    msg = _build_update_msg(remote_ver_str, changelog, is_partial, local_size, remote_size)
                    reply = QMessageBox.question(
                        parent, "🔄 Aggiornamento", msg,
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        perform_auto_update(download_url, parent)
            elif not silent:
                QMessageBox.information(parent, "✅ Aggiornamento", f"L'applicazione è aggiornata (v{version.__version__})")
    except Exception as e:
        if not silent:
            QMessageBox.warning(parent, "Errore Aggiornamento", str(e))


def _build_update_msg(ver, changelog, partial, local_s, remote_s) -> str:
    if partial:
        percent = (local_s / remote_s) * 100
        return f"Rilevato download parziale ({int(percent)}%) della versione {ver}.\n\nVuoi completare lo scaricamento ora?"

    msg = f"Nuova versione {ver} disponibile!\n"
    if changelog:
        msg += f"\nNovità:\n{changelog}\n"
    msg += "\nVuoi scaricarla ora?"
    return msg


def perform_auto_update(download_url: str, parent: QWidget | None = None):
    """Starts asynchronous download in background."""
    if parent is None:
        for widget in QApplication.topLevelWidgets():
            if widget.isWindow() and not widget.parent():
                parent = widget
                break

    global _active_update_worker
    _active_update_worker = DownloadWorker(download_url)

    if parent and hasattr(parent, "update_banner") and parent.update_banner:
        _active_update_worker.progress.connect(parent.update_banner.update_progress)
        if hasattr(parent, "_on_update_downloaded"):
            _active_update_worker.finished_download.connect(parent._on_update_downloaded)
    else:
        global _active_update_dialog
        _active_update_dialog = UpdateProgressDialog(download_url, parent)
        _active_update_dialog.start()
        return

    _active_update_worker.start()
