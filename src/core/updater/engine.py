"""
SyncroJob - Updater Engine
Business logic for checking and downloading updates.
"""

import contextlib
import json
import logging
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests
from PyQt6.QtCore import QThread, pyqtSignal

from .. import version

logger = logging.getLogger(__name__)

# Global state for pending updates
_pending_installer_path: str | None = None


def get_local_setup_path(url_or_path: str) -> str:
    """Determines the local path for the downloaded setup, handling both URL and Windows paths."""
    # Convert to forward slashes for unified parsing
    clean_path = url_or_path.replace("\\", "/")
    local_filename = clean_path.split("/")[-1]
    if not local_filename.endswith(".exe"):
        local_filename = "update_setup.exe"
    return os.path.join(tempfile.gettempdir(), local_filename)


class DownloadWorker(QThread):
    """Worker for resilient update downloading or network copying with progress support."""

    progress = pyqtSignal(int, int, float, float)
    finished_download = pyqtSignal(str)
    error = pyqtSignal(str)
    retrying = pyqtSignal(int)

    def __init__(self, url_or_path: str):
        super().__init__()
        self.url_or_path = url_or_path
        self._is_cancelled = False
        self.max_retries = 999
        self._ema_speed = 0.0

    def stop(self):
        """Richiede l'interruzione del download."""
        self._is_cancelled = True

    def run(self):
        """Esegue il download o la copia del file."""
        setup_path = get_local_setup_path(self.url_or_path)
        start_time = time.time()
        self._ema_speed = 0.0

        if Path(setup_path).exists() and time.time() - Path(setup_path).stat().st_mtime > 86400:
            with contextlib.suppress(Exception):
                Path(setup_path).unlink()

        if self.url_or_path.startswith("http"):
            self._run_http_download(setup_path)
        else:
            self._run_network_copy(setup_path, start_time)

    def _run_network_copy(self, setup_path, start_time):
        """Copies file from network path with progress feedback."""
        try:
            src_path = Path(self.url_or_path)
            if not src_path.exists():
                raise FileNotFoundError(f"Percorso di rete non trovato: {self.url_or_path}")

            total_size = src_path.stat().st_size
            downloaded = 0

            with open(self.url_or_path, "rb") as f_src, open(setup_path, "wb") as f_dst:
                while not self._is_cancelled:
                    chunk = f_src.read(1024 * 1024)  # 1MB chunks
                    if not chunk:
                        break

                    f_dst.write(chunk)
                    downloaded += len(chunk)

                    # Update EMA Speed
                    elapsed_total = time.time() - start_time
                    current_speed = downloaded / elapsed_total if elapsed_total > 0 else 0
                    self._ema_speed = current_speed

                    remaining_bytes = total_size - downloaded
                    eta = remaining_bytes / self._ema_speed if self._ema_speed > 0 else 0.0
                    self.progress.emit(downloaded, total_size, self._ema_speed, eta)

            if not self._is_cancelled:
                self.finished_download.emit(setup_path)
        except Exception as e:
            self.error.emit(str(e))

    def _run_http_download(self, setup_path):
        """Existing HTTP download logic with resume support."""
        downloaded = 0
        total_size = 0
        retries = 0

        while not self._is_cancelled:
            try:
                downloaded = Path(setup_path).stat().st_size if Path(setup_path).exists() else 0
                headers = {"Range": f"bytes={downloaded}-"} if downloaded > 0 else {}

                session = requests.Session()
                response = session.get(self.url_or_path, headers=headers, stream=True, timeout=(10, 30))

                if downloaded > 0 and response.status_code != 206:
                    downloaded = 0
                    with open(setup_path, "wb"):
                        pass

                if response.status_code not in (200, 206):
                    if response.status_code == 416 and total_size > 0 and downloaded >= total_size:
                        self.finished_download.emit(setup_path)
                        return
                    raise Exception(f"Server error: {response.status_code}")

                if downloaded == 0:
                    total_size = int(response.headers.get("content-length", 0))
                elif "Content-Range" in response.headers:
                    total_size = int(response.headers["Content-Range"].split("/")[-1])

                mode = "ab" if downloaded > 0 else "wb"
                with open(setup_path, mode) as f:
                    content_iterator = response.iter_content(chunk_size=131072)
                    last_time = time.time()

                    while not self._is_cancelled:
                        try:
                            chunk = next(content_iterator)
                            if not chunk:
                                break

                            current_time = time.time()
                            elapsed = current_time - last_time
                            last_time = current_time
                            chunk_size = len(chunk)
                            f.write(chunk)
                            downloaded += chunk_size

                            current_speed = chunk_size / elapsed if elapsed > 0 else 0
                            alpha = 0.1
                            if self._ema_speed == 0.0:
                                self._ema_speed = current_speed
                            else:
                                self._ema_speed = (alpha * current_speed) + ((1 - alpha) * self._ema_speed)

                            remaining_bytes = total_size - downloaded
                            eta = remaining_bytes / self._ema_speed if self._ema_speed > 0 else 0.0
                            self.progress.emit(downloaded, total_size, self._ema_speed, eta)
                            retries = 0
                        except StopIteration:
                            break

                if not self._is_cancelled and total_size > 0 and downloaded >= total_size:
                    self.finished_download.emit(setup_path)
                    return

                if not self._is_cancelled:
                    raise requests.exceptions.ConnectionError("Stream interrupted")

            except Exception:
                if self._is_cancelled:
                    return  # type: ignore[unreachable]
                retries += 1
                self.retrying.emit(retries)
                time.sleep(min(retries * 2, 10))


def run_installer_and_exit(setup_path: str):
    """Executes the installer and terminates the process (Fix B603)."""
    if Path(setup_path).exists():
        # Usa DETACHED_PROCESS su Windows per garantire che l'installer sopravviva alla chiusura dell'app
        flags = subprocess.DETACHED_PROCESS if os.name == "nt" else 0
        subprocess.Popen(
            [setup_path, "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"],
            creationflags=flags,
            close_fds=True,
        )
        sys.exit(0)


def run_pending_installer():
    """Executes the installer stored at app closure in a separate process."""
    global _pending_installer_path
    if _pending_installer_path and Path(_pending_installer_path).exists():
        # Usa DETACHED_PROCESS per slegarsi dal ciclo di vita dell'app corrente
        flags = subprocess.DETACHED_PROCESS if os.name == "nt" else 0
        # Avvio tramite cmd per il timeout, ma con quoting rinforzato
        args = [
            "cmd.exe",
            "/c",
            f'timeout /t 3 /nobreak > NUL && "{_pending_installer_path}" /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS',
        ]
        subprocess.Popen(args, shell=False, creationflags=flags, close_fds=True, stdin=subprocess.DEVNULL)


def set_pending_installer(path: str):
    """Sets the path for the installer to be run on closure."""
    global _pending_installer_path
    _pending_installer_path = path


def has_pending_update() -> bool:
    """Returns True if there is an update ready to be installed."""
    global _pending_installer_path
    return bool(_pending_installer_path and Path(_pending_installer_path).exists())


def get_web_update_info():
    """Fetches version info from Web."""
    if not getattr(version, "UPDATE_URL", None):
        return None

    try:
        response = requests.get(version.UPDATE_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.debug(f"Web update check failed: {e}")
    return None


def get_network_update_info():
    """Fetches version info from network share."""
    try:
        net_path = getattr(version, "NETWORK_UPDATE_PATH", None)
        if not net_path:
            return None

        json_path = Path(net_path) / "version.json"
        if json_path.exists():
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if (
                    data.get("url")
                    and not data["url"].startswith("http")
                    and not data["url"].startswith("\\\\")
                ):
                    data["url"] = str(Path(net_path) / data["url"])
                return data
    except Exception as e:
        logger.debug(f"Network update check failed: {e}")
    return None
