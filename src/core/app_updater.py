"""
SyncroJob - App Updater
Gestisce il controllo e la notifica di aggiornamenti dell'applicazione.
"""

import webbrowser

import requests
from packaging import version as pkg_version
from PyQt6.QtWidgets import QMessageBox

from . import version


def check_for_updates(parent=None, silent=True, callback=None):
    """Controlla se è disponibile una nuova versione dell'applicazione."""
    url = version.UPDATE_URL
    if not url:
        return

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return

        data = response.json()
        remote_ver_str = data.get("version")
        download_url = data.get("url")
        changelog = data.get("changelog", "")

        if not remote_ver_str:
            return

        if _is_newer_version(remote_ver_str):
            _handle_update_found(remote_ver_str, download_url, changelog, parent, callback)
        elif not silent:
            QMessageBox.information(
                parent,
                "✅ Aggiornamento",
                f"L'applicazione è aggiornata (v{version.__version__})",
            )

    except Exception as e:
        if not silent:
            print(f"[ERRORE] Aggiornamento: {e}")


def _is_newer_version(remote_ver_str: str) -> bool:
    """Compara la versione remota con quella locale."""
    try:
        current_ver = pkg_version.parse(version.__version__)
        remote_ver = pkg_version.parse(remote_ver_str)
        return remote_ver > current_ver
    except Exception:
        return False


def _handle_update_found(remote_ver, download_url, changelog, parent, callback):
    """Notifica l'utente o esegue il callback per l'aggiornamento trovato."""
    if callback:
        callback(remote_ver, download_url, changelog)
        return

    msg = (
        f"È disponibile una nuova versione!\n\n"
        f"Versione corrente: {version.__version__}\n"
        f"Nuova versione: {remote_ver}\n"
    )
    if changelog:
        msg += f"\nNovità:\n{changelog}\n"
    msg += "\nVuoi scaricarla ora?"

    res = QMessageBox.question(
        parent,
        "🔄 Aggiornamento Disponibile",
        msg,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )

    if res == QMessageBox.StandardButton.Yes and download_url:
        webbrowser.open(download_url)


if __name__ == "__main__":
    check_for_updates(silent=False)
