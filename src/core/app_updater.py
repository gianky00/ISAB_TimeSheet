"""
Bot TS - App Updater
Gestisce il controllo e la notifica di aggiornamenti dell'applicazione.
"""
import requests
import webbrowser
from packaging import version as pkg_version
from PyQt6.QtWidgets import QMessageBox
from . import version
from src.core.audit_manager import AuditManager


def check_for_updates(parent=None, silent=True, callback=None):
    """
    Controlla se è disponibile una nuova versione dell'applicazione.

    Args:
        parent: Widget parent per i dialog
        silent (bool): Se True, non mostra notifiche se non ci sono aggiornamenti
        callback (callable): Se fornito, chiama questa funzione con (version, url) invece di mostrare il dialog
    """
    url = version.UPDATE_URL

    if not url:
        return

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            remote_ver_str = data.get("version")
            download_url = data.get("url")
            changelog = data.get("changelog", "")

            if remote_ver_str:
                current_ver = pkg_version.parse(version.__version__)
                remote_ver = pkg_version.parse(remote_ver_str)

                if remote_ver > current_ver:
                    if callback:
                        callback(remote_ver_str, download_url, changelog)
                        return

                    msg = (
                        f"È disponibile una nuova versione!\n\n"
                        f"Versione corrente: {version.__version__}\n"
                        f"Nuova versione: {remote_ver_str}\n"
                    )
                    if changelog:
                        msg += f"\nNovità:\n{changelog}\n"
                    
                    msg += "\nVuoi scaricarla ora?"

                    reply = QMessageBox.question(
                        parent,
                        "🔄 Aggiornamento Disponibile",
                        msg,
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )

                    if reply == QMessageBox.StandardButton.Yes:
                        if download_url:
                            webbrowser.open(download_url)
                else:
                    if not silent:
                        QMessageBox.information(parent, "✅ Aggiornamento", f"L'applicazione è aggiornata (v{version.__version__})")
    except Exception as e:
        if not silent:
            print(f"[ERRORE] Aggiornamento: {e}")


if __name__ == "__main__":
    check_for_updates(silent=False)
