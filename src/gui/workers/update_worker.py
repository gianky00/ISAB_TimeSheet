"""SyncroJob - Update Check Worker.

Worker asincrono per il controllo degli aggiornamenti senza bloccare la GUI.
"""

import contextlib
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import requests
from packaging import version as pkg_version
from PySide6.QtCore import QThread, Signal

from src.core import version
from src.core.updater.engine import (
    get_local_setup_path,
    get_network_update_info,
    get_web_update_info,
)

logger = logging.getLogger(__name__)


class UpdateCheckWorker(QThread):
    """Worker che interroga i server di aggiornamento in background.

    Inizializza la classe.
    """

    finished_signal = Signal(dict)  # Risultato del controllo
    no_update_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, silent: bool = True) -> None:
        super().__init__()
        self.silent = silent

    def run(self) -> None:
        """Esegue il controllo su Web e Network."""
        try:
            update_sources = self._fetch_sources()

            if not update_sources:
                self.no_update_signal.emit()
                return

            latest_update = max(update_sources, key=lambda x: pkg_version.parse(x["version"]))
            remote_ver_str = latest_update["version"]
            download_url = latest_update.get("url")

            if not download_url or pkg_version.parse(remote_ver_str) <= pkg_version.parse(
                version.__version__
            ):
                self.no_update_signal.emit()
                return

            self._process_update_info(latest_update, download_url)

        except Exception as e:
            logger.exception("Errore durante il controllo aggiornamenti")
            self.error_signal.emit(str(e))

    def _fetch_sources(self) -> list[dict[str, Any]]:
        """Recupera le info da web e rete locale."""
        update_sources = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(get_web_update_info): "Web",
                executor.submit(get_network_update_info): "Network",
            }
            for future in as_completed(futures):
                with contextlib.suppress(Exception):
                    info = future.result()
                    if info and info.get("version"):
                        update_sources.append(info)
        return update_sources

    def _process_update_info(self, latest_update: dict[str, Any], download_url: str) -> None:
        """Calcola dimensioni e stato del download locale."""
        setup_path = get_local_setup_path(download_url)
        remote_size = 0

        if download_url.startswith("http"):
            with contextlib.suppress(Exception):
                head_resp = requests.head(download_url, timeout=5)
                remote_size = int(head_resp.headers.get("content-length", 0))
        else:
            with contextlib.suppress(Exception):
                remote_size = Path(download_url).stat().st_size

        local_size = Path(setup_path).stat().st_size if Path(setup_path).exists() else 0
        is_complete = remote_size > 0 and local_size >= remote_size

        latest_update["is_complete"] = is_complete
        latest_update["setup_path"] = setup_path

        self.finished_signal.emit(latest_update)
