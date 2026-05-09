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
from typing import Any, Final, cast

import requests
from PySide6.QtCore import QThread, Signal

from src.core import version

logger = logging.getLogger(__name__)

# Global state for pending updates
_pending_installer_path: str | None = None

# Constants for HTTP Status Codes
HTTP_OK: Final[int] = 200
HTTP_PARTIAL_CONTENT: Final[int] = 206
HTTP_RANGE_NOT_SATISFIABLE: Final[int] = 416

# Time constants
SECONDS_IN_DAY: Final[int] = 86400


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

    progress = Signal(int, int, float, float)
    finished_download = Signal(str)
    error = Signal(str)
    retrying = Signal(int)

    def __init__(self, url_or_path: str) -> None:
        super().__init__()
        self.url_or_path = url_or_path
        self._is_cancelled = False
        self.max_retries = 999
        self._ema_speed = 0.0
        self._last_progress_time = 0.0

    # Costanti per il controllo del flusso (Ottimizzazione GUI)
    PROGRESS_INTERVAL = 0.1  # 10 Hz (100ms)
    EMA_ALPHA = 0.1  # Coefficiente di smoothing per la velocit

    def stop(self) -> None:
        """Richiede l'interruzione del download."""
        self._is_cancelled = True

    def run(self) -> None:
        """Esegue le operazioni di aggiornamento nel thread dedicato."""
        setup_path = get_local_setup_path(self.url_or_path)
        self._ema_speed = 0.0

        if Path(setup_path).exists() and time.time() - Path(setup_path).stat().st_mtime > SECONDS_IN_DAY:
            with contextlib.suppress(Exception):
                Path(setup_path).unlink()

        if self.url_or_path.startswith("http"):
            self._run_http_download(setup_path)
        else:
            self._run_network_copy(setup_path)

    def _run_network_copy(self, setup_path: str) -> None:
        """Copies file from network path with progress feedback."""
        try:
            src_path = Path(self.url_or_path)
            if not src_path.exists():
                self._raise_network_path_not_found()

            total_size = src_path.stat().st_size
            downloaded = 0
            # Granularit  a 128KB (molto fluida anche su connessioni lente ~0.6MB/s)
            chunk_size = 128 * 1024

            with open(self.url_or_path, "rb") as f_src, open(setup_path, "wb") as f_dst:
                last_time = time.time()
                while not self._is_cancelled:
                    chunk = f_src.read(chunk_size)
                    if not chunk:
                        break

                    current_time = time.time()
                    elapsed = current_time - last_time
                    last_time = current_time

                    real_chunk_size = len(chunk)
                    f_dst.write(chunk)
                    downloaded += real_chunk_size

                    # Calcolo Velocità Dinamico (EMA)
                    current_speed = real_chunk_size / elapsed if elapsed > 0 else 0
                    if self._ema_speed == 0.0:
                        self._ema_speed = current_speed
                    else:
                        self._ema_speed = (self.EMA_ALPHA * current_speed) + (
                            (1 - self.EMA_ALPHA) * self._ema_speed
                        )

                    remaining_bytes = total_size - downloaded
                    eta = remaining_bytes / self._ema_speed if self._ema_speed > 0 else 0.0

                    # Throttling emissione segnali progress (max 10 Hz)
                    now = time.time()
                    if now - self._last_progress_time >= self.PROGRESS_INTERVAL or downloaded >= total_size:
                        self.progress.emit(downloaded, total_size, self._ema_speed, eta)
                        self._last_progress_time = now

            if not self._is_cancelled:
                self.finished_download.emit(setup_path)
        except Exception as e:
            self.error.emit(str(e))

    def _raise_network_path_not_found(self) -> None:
        err_msg = f"Percorso di rete non trovato: {self.url_or_path}"
        raise FileNotFoundError(err_msg)

    def _run_http_download(self, setup_path: str) -> None:
        """Existing HTTP download logic with resume support."""
        total_size = 0
        retries = 0
        max_retry_wait = 10

        while not self._is_cancelled:
            try:
                download_info = self._get_http_response(setup_path)
                if download_info is None:
                    return

                response, downloaded, total_size = download_info

                self._stream_download(response, setup_path, downloaded, total_size)

                if not self._is_cancelled and total_size > 0 and downloaded >= total_size:
                    self.finished_download.emit(setup_path)
                    return

                if not self._is_cancelled:
                    self._handle_interruption()

            except Exception:
                if self._is_cancelled:
                    return  # type: ignore[unreachable]
                retries += 1
                self.retrying.emit(retries)
                time.sleep(min(retries * 2, max_retry_wait))

    def _get_http_response(self, setup_path: str) -> tuple[requests.Response, int, int] | None:
        downloaded = Path(setup_path).stat().st_size if Path(setup_path).exists() else 0
        headers = {"Range": f"bytes={downloaded}-"} if downloaded > 0 else {}

        response = requests.get(self.url_or_path, headers=headers, stream=True, timeout=(10, 30))

        if downloaded > 0 and response.status_code != HTTP_PARTIAL_CONTENT:
            downloaded = 0
            with open(setup_path, "wb"):
                pass

        if response.status_code not in (HTTP_OK, HTTP_PARTIAL_CONTENT):
            if response.status_code == HTTP_RANGE_NOT_SATISFIABLE:
                self.finished_download.emit(setup_path)
                return None
            self._raise_server_error(response.status_code)

        total_size = 0
        if downloaded == 0:
            total_size = int(response.headers.get("content-length", 0))
        elif "Content-Range" in response.headers:
            total_size = int(response.headers["Content-Range"].split("/")[-1])

        return response, downloaded, total_size

    def _raise_server_error(self, status_code: int) -> None:
        err_msg = f"Server error: {status_code}"
        raise RuntimeError(err_msg)

    def _stream_download(
        self, response: requests.Response, setup_path: str, downloaded: int, total_size: int
    ) -> None:
        mode = "ab" if downloaded > 0 else "wb"
        # Buffer scrittura OS di 2MB per HTTP
        with open(setup_path, mode, buffering=2 * 1024 * 1024) as f:
            content_iterator = response.iter_content(chunk_size=1024 * 1024)
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
                    if self._ema_speed == 0.0:
                        self._ema_speed = current_speed
                    else:
                        self._ema_speed = (self.EMA_ALPHA * current_speed) + (
                            (1 - self.EMA_ALPHA) * self._ema_speed
                        )

                    remaining_bytes = total_size - downloaded
                    eta = remaining_bytes / self._ema_speed if self._ema_speed > 0 else 0.0

                    # Throttling emissione segnali progress (max 10 Hz)
                    now = time.time()
                    if now - self._last_progress_time >= self.PROGRESS_INTERVAL or downloaded >= total_size:
                        self.progress.emit(downloaded, total_size, self._ema_speed, eta)
                        self._last_progress_time = now
                except StopIteration:
                    break

    def _handle_interruption(self) -> None:
        """Helper to raise interruption error."""
        raise requests.exceptions.ConnectionError("Stream interrupted")  # noqa: TRY003


def run_installer_and_exit(setup_path: str) -> None:
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


def run_pending_installer() -> None:
    """Executes the installer stored at app closure in a separate process."""
    global _pending_installer_path  # noqa: PLW0602
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


def set_pending_installer(path: str) -> None:
    """Sets the path for the installer to be run on closure."""
    global _pending_installer_path  # noqa: PLW0603
    _pending_installer_path = path


def get_pending_installer_path() -> str | None:
    """Returns the path of the pending installer."""
    global _pending_installer_path  # noqa: PLW0602
    return _pending_installer_path


def has_pending_update() -> bool:
    """Returns True if there is an update ready to be installed."""
    global _pending_installer_path  # noqa: PLW0602
    return bool(_pending_installer_path and Path(_pending_installer_path).exists())


def get_web_update_info() -> dict[str, Any] | None:
    """Fetches version info from Web."""
    update_url = getattr(version, "UPDATE_URL", None)
    if not update_url:
        return None

    try:
        response = requests.get(update_url, timeout=5)
        if response.status_code == HTTP_OK:
            return cast("dict[str, Any]", response.json())
    except Exception as e:
        logger.debug("Web update check failed: %s", e)
    return None


def get_network_update_info() -> dict[str, Any] | None:
    """Fetches version info from network share."""
    try:
        net_path = getattr(version, "NETWORK_UPDATE_PATH", None)
        if not net_path:
            return None

        json_path = Path(net_path) / "version.json"
        if json_path.exists():
            with json_path.open("r", encoding="utf-8") as f:
                data = cast("dict[str, Any]", json.load(f))
                url = data.get("url")
                if url and not url.startswith("http") and not url.startswith("\\\\"):
                    data["url"] = str(Path(net_path) / url)
                return data
    except Exception as e:
        logger.debug("Network update check failed: %s", e)
    return None
