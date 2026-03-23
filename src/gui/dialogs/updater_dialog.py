"""
SyncroJob - Updater Dialog
UI components for update notifications and progress.
Moved from core/updater/gui.py to follow SRP.
"""

import contextlib
import logging
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, cast

import requests
from packaging import version as pkg_version
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QMessageBox, QProgressBar, QVBoxLayout, QWidget

from src.core import version
from src.core.updater.engine import (
    DownloadWorker,
    get_local_setup_path,
    get_network_update_info,
    get_web_update_info,
    run_installer_and_exit,
    set_pending_installer,
)

logger = logging.getLogger(__name__)

# Store active worker to prevent garbage collection
_active_update_worker = None
_active_update_dialog = None


class UpdateProgressDialog(QDialog):
    """Progress dialog for update downloads or network transfers."""

    def __init__(self, url_or_path: str, parent: QWidget | None = None):  # noqa: ANN204
        super().__init__(parent)
        self.setWindowTitle("Aggiornamento SyncroJob")
        self.setFixedSize(450, 200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.worker = DownloadWorker(url_or_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished_download.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.retrying.connect(self.on_retrying)

        if not url_or_path.startswith("http"):
            self.lbl_status.setText("Avvio trasferimento rete...")

    def setup_ui(self):  # noqa: ANN201
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        self.lbl_status = QLabel("Avvio download...")
        self.lbl_status.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.lbl_status)
        self.pb = QProgressBar()
        self.pb.setFixedHeight(24)
        self.pb.setStyleSheet(
            "QProgressBar { border: 1px solid #CCCCCC; border-radius: 6px; text-align: center; background-color: #F0F0F0; } QProgressBar::chunk { background-color: #0D6EFD; border-radius: 5px; }"
        )
        layout.addWidget(self.pb)
        self.lbl_details = QLabel("Preparazione...")
        self.lbl_details.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.lbl_details)
        self.lbl_retry = QLabel("")
        self.lbl_retry.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.lbl_retry.setStyleSheet("color: #DC3545;")
        layout.addWidget(self.lbl_retry)

    def start(self):  # noqa: ANN201
        self.show()
        self.worker.start()

    @pyqtSlot(int, int, float, float)
    def update_progress(self, downloaded, total, speed, eta):  # noqa: ANN001, ANN201
        self.lbl_retry.setText("")
        if total > 0:
            self.pb.setMaximum(total)
            self.pb.setValue(downloaded)
            percent = (downloaded / total) * 100
            mb_down = downloaded / (1024 * 1024)
            mb_total = total / (1024 * 1024)
            speed_mb = speed / (1024 * 1024)
            action = "Scaricamento" if self.worker.url_or_path.startswith("http") else "Trasferimento"
            self.lbl_status.setText(f"{action}: {int(percent)}% completato")
            self.lbl_details.setText(
                f"{mb_down:.1f} MB di {mb_total:.1f} MB ({speed_mb:.2f} MB/s) - ETA: {int(eta)}s"
            )
        else:
            self.pb.setMaximum(0)
            self.lbl_status.setText("Operazione in corso...")

    @pyqtSlot(int)
    def on_retrying(self, retry_count):  # noqa: ANN001, ANN201
        self.lbl_retry.setText(f"⚠️ Connessione instabile. Tentativo #{retry_count}...")

    @pyqtSlot(str)
    def on_finished(self, setup_path):  # noqa: ANN001, ANN201
        self.close()
        show_install_prompt(setup_path, cast("QWidget", self.parent()))

    @pyqtSlot(str)
    def on_error(self, err_msg):  # noqa: ANN001, ANN201
        self.close()
        QMessageBox.critical(cast("QWidget", self.parent()), "Errore", f"Trasferimento interrotto: {err_msg}")


def show_install_prompt(setup_path: str, parent: QWidget | None = None):  # noqa: ANN201
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle("🔄 Aggiornamento Pronto")
    msg_box.setText(
        "L'aggiornamento è stato scaricato ed è pronto per l'installazione.\n\nCosa desideri fare?"
    )
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
            parent, "ℹ️ Info", "L'aggiornamento partirà automaticamente alla chiusura dell'app."
        )


def check_for_updates(  # noqa: PLR0912
    parent: QWidget | None = None,
    silent: bool = True,
    callback: Callable[[str, str, str, bool, bool], Any] | None = None,
) -> None:
    update_sources = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(get_web_update_info): "Web",
            executor.submit(get_network_update_info): "Network",
        }
        for future in as_completed(futures):
            info = future.result()
            if info and info.get("version"):
                update_sources.append(info)

    if not update_sources:
        if not silent:
            QMessageBox.information(
                parent, "✅ Aggiornamento", f"L'applicazione è aggiornata (v{version.__version__})"
            )
        return

    latest_update = max(update_sources, key=lambda x: pkg_version.parse(x["version"]))
    remote_ver_str = latest_update["version"]
    download_url = latest_update.get("url")
    changelog = latest_update.get("changelog", "")

    if not download_url:
        if not silent:
            QMessageBox.information(
                parent, "✅ Aggiornamento", f"L'applicazione è aggiornata (v{version.__version__})"
            )
        return

    if pkg_version.parse(remote_ver_str) > pkg_version.parse(version.__version__):
        setup_path = get_local_setup_path(download_url)
        remote_size = 0
        if download_url.startswith("http"):
            try:
                head_resp = requests.head(download_url, timeout=5)
                remote_size = int(head_resp.headers.get("content-length", 0))
            except Exception as e:
                logger.debug(f"Failed to get remote size: {e}")
        else:
            with contextlib.suppress(Exception):
                remote_size = Path(download_url).stat().st_size

        local_size = Path(setup_path).stat().st_size if Path(setup_path).exists() else 0
        is_partial = 0 < local_size < remote_size
        is_complete = remote_size > 0 and local_size >= remote_size

        if callback:
            callback(remote_ver_str, download_url, changelog, is_partial, is_complete)
            return

        if is_complete:
            show_install_prompt(setup_path, parent)
        else:
            msg = f"Nuova versione {remote_ver_str} disponibile!\n"
            if changelog:
                msg += f"\nNovità:\n{changelog}\n"
            msg += "\nVuoi aggiornare ora?"
            reply = QMessageBox.question(
                parent,
                "🔄 Aggiornamento",
                msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                perform_auto_update(download_url, parent)
    elif not silent:
        QMessageBox.information(
            parent, "✅ Aggiornamento", f"L'applicazione è aggiornata (v{version.__version__})"
        )


def perform_auto_update(download_url: str, parent: QWidget | None = None):  # noqa: ANN201
    if parent is None:
        for widget in QApplication.topLevelWidgets():
            if widget.isWindow() and not widget.parent():
                parent = widget
                break

    global _active_update_worker  # noqa: PLW0603
    _active_update_worker = DownloadWorker(download_url)

    if parent and hasattr(parent, "update_banner") and parent.update_banner:
        _active_update_worker.progress.connect(parent.update_banner.update_progress)
        if hasattr(parent, "_on_update_downloaded"):
            _active_update_worker.finished_download.connect(parent._on_update_downloaded)
    else:
        global _active_update_dialog  # noqa: PLW0603
        _active_update_dialog = UpdateProgressDialog(download_url, parent)
        _active_update_dialog.start()
        return

    _active_update_worker.start()
