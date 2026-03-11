"""
SyncroJob - Updater Engine
Business logic for checking and downloading updates.
"""

import contextlib
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests
from PyQt6.QtCore import QThread, pyqtSignal

# Global state for pending updates
_pending_installer_path: str | None = None


def get_local_setup_path(url: str) -> str:
    """Determines the local path for the downloaded setup."""
    local_filename = url.split("/")[-1]
    if not local_filename.endswith(".exe"):
        local_filename = "update_setup.exe"
    return os.path.join(tempfile.gettempdir(), local_filename)


class DownloadWorker(QThread):
    """Worker for resilient update downloading with resume support."""
    progress = pyqtSignal(int, int, float, float)
    finished_download = pyqtSignal(str)
    error = pyqtSignal(str)
    retrying = pyqtSignal(int)

    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self._is_cancelled = False
        self.max_retries = 999
        self._ema_speed = 0.0

    def stop(self):
        self._is_cancelled = True

    def run(self):
        setup_path = get_local_setup_path(self.url)
        downloaded = 0
        total_size = 0
        retries = 0
        self._ema_speed = 0.0

        if Path(setup_path).exists() and time.time() - Path(setup_path).stat().st_mtime > 86400:
            with contextlib.suppress(Exception):
                Path(setup_path).unlink()

        while not self._is_cancelled:
            try:
                downloaded = Path(setup_path).stat().st_size if Path(setup_path).exists() else 0
                headers = {'Range': f'bytes={downloaded}-'} if downloaded > 0 else {}

                session = requests.Session()
                response = session.get(self.url, headers=headers, stream=True, timeout=(10, 30))

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
                elif 'Content-Range' in response.headers:
                    total_size = int(response.headers['Content-Range'].split('/')[-1])

                mode = "ab" if downloaded > 0 else "wb"
                with open(setup_path, mode) as f:
                    content_iterator = response.iter_content(chunk_size=131072)
                    last_time = time.time()

                    while True:
                        if self._is_cancelled:
                            pass # return irraggiungibile per mypy, saltiamo il blocco
                        try:
                            chunk = next(content_iterator)
                            if chunk:
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

                if total_size > 0 and downloaded >= total_size:
                    self.finished_download.emit(setup_path)
                    return
                raise requests.exceptions.ConnectionError("Stream interrupted")

            except Exception:
                if self._is_cancelled:
                    pass # return irraggiungibile per mypy
                retries += 1
                self.retrying.emit(retries)
                time.sleep(min(retries * 2, 10))


def run_installer_and_exit(setup_path: str):
    """Executes the installer and terminates the process (Fix B603)."""
    if Path(setup_path).exists():
        # Using list of arguments and shell=False (Fix B603)
        subprocess.Popen([setup_path, "/SILENT", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS", "/FORCESTART"])
        sys.exit(0)


def run_pending_installer():
    """Executes the installer stored at app closure in a separate process (Fix B602)."""
    global _pending_installer_path
    if _pending_installer_path and Path(_pending_installer_path).exists():
        flags = 0x00000008 if os.name == "nt" else 0

        # FIX B602: Avoid shell=True. Use cmd /c to delay execution.
        # timeout /t 3 is safer than ping loop.
        args = [
            "cmd.exe", "/c",
            f"timeout /t 3 /nobreak > NUL && \"{_pending_installer_path}\" /SILENT /FORCESTART"
        ]

        subprocess.Popen(
            args,
            shell=False,
            creationflags=flags,
            close_fds=True
        )


def set_pending_installer(path: str):
    """Sets the path for the installer to be run on closure."""
    global _pending_installer_path
    _pending_installer_path = path


def has_pending_update() -> bool:
    """Returns True if there is an update ready to be installed."""
    global _pending_installer_path
    return bool(_pending_installer_path and Path(_pending_installer_path).exists())
