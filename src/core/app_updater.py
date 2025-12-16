"""
Bot TS - App Updater
Gestisce il controllo e la notifica di aggiornamenti dell'applicazione.
"""
import requests
import webbrowser
from packaging import version as pkg_version
from PyQt6.QtWidgets import QMessageBox
from . import version


def check_for_updates(parent=None, silent=True):
    """
    Controlla se è disponibile una nuova versione dell'applicazione.

    Interroga un endpoint JSON con formato:
    {
        "version": "2.0.0",
        "url": "https://example.com/download"
    }

    Args:
        parent: Widget parent per i dialog (opzionale)
        silent (bool): Se True, non mostra notifiche se non ci sono aggiornamenti
    """
    url = version.UPDATE_URL

    if not url:
        if not silent:
            print("[INFO] URL aggiornamenti non configurato")
        return

    try:
        print("[SISTEMA] Controllo aggiornamenti in corso...")
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            remote_ver_str = data.get("version")
            download_url = data.get("url")

            if remote_ver_str:
                current_ver = pkg_version.parse(version.__version__)
                remote_ver = pkg_version.parse(remote_ver_str)

                if remote_ver > current_ver:
                    msg = (
                        f"È disponibile una nuova versione!\n\n"
                        f"Versione corrente: {version.__version__}\n"
                        f"Nuova versione: {remote_ver_str}\n\n"
                        f"Vuoi scaricarla ora?"
                    )

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
                            QMessageBox.information(
                                parent,
                                "ℹ️ Info",
                                "Visita il sito per scaricare l'aggiornamento."
                            )
                else:
                    print("[SISTEMA] ✓ Applicazione aggiornata")
                    if not silent:
                        QMessageBox.information(
                            parent,
                            "✅ Aggiornamento",
                            f"L'applicazione è già aggiornata.\n"
                            f"Versione: {version.__version__}"
                        )
        else:
            if not silent:
                print(f"[AVVISO] Errore controllo aggiornamenti: HTTP {response.status_code}")

    except requests.Timeout:
        if not silent:
            print("[AVVISO] Timeout controllo aggiornamenti")
    except requests.RequestException as e:
        if not silent:
            print(f"[AVVISO] Errore connessione: {e}")
    except Exception as e:
        if not silent:
            print(f"[ERRORE] Controllo aggiornamenti: {e}")


if __name__ == "__main__":
    check_for_updates(silent=False)
