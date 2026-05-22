"""SyncroJob - Update Controller.

Gestisce la logica di controllo aggiornamenti, download e prompt di installazione.
Aderisce al principio SRP separando la logica dell'updater dalla MainWindow.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from src.core.app_updater import (
    get_local_setup_path,
    get_pending_installer_path,
    has_pending_update,
    perform_auto_update,
    show_install_prompt,
)
from src.gui.widgets.toast import ToastManager

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger("UpdateController")


class UpdateController:
    """Controller per la gestione degli aggiornamenti dell'applicazione.

    Inizializza il controller degli aggiornamenti.

    Args:
        main_window: Riferimento alla finestra principale per l'aggiornamento dell'UI.
    """

    def __init__(self, main_window: MainWindow) -> None:
        self.mw = main_window

    def check_updates_startup(self) -> None:
        """Controlla se ci sono aggiornamenti pendenti o nuovi al boot."""
        if has_pending_update():
            path = get_pending_installer_path()
            if path:
                show_install_prompt(path, self.mw)

    def show_update_banner(self, version_info: dict[str, Any]) -> None:
        """Mostra il banner di aggiornamento nella toolbar."""
        if hasattr(self.mw, "tool_bar_component") and self.mw.tool_bar_component.update_banner:
            download_url = version_info.get("url", "")
            version_str = version_info.get("version", "")
            if download_url and version_str:
                self.mw.tool_bar_component.update_banner.show_update(version_str, download_url)

    def handle_download_update(self, download_url: str) -> None:
        """Avvia il processo di download dell'aggiornamento."""
        try:
            # Se il banner indica che è già completo, mostra direttamente la prompt di installazione
            banner = getattr(self.mw, "update_banner", None)
            if banner and getattr(banner, "_is_complete", False):
                setup_path = get_local_setup_path(download_url)
                show_install_prompt(setup_path, self.mw)
                return

            perform_auto_update(download_url, self.mw)
        except Exception as e:
            logger.exception("Inizializzazione download fallita")
            ToastManager.instance().show(f"Errore inizializzazione update: {e}", "error")

    def handle_update_error(self, message: str) -> None:
        """Gestisce errori durante lo scaricamento dell'aggiornamento."""
        if hasattr(self.mw, "update_banner") and self.mw.update_banner:
            self.mw.update_banner.show_error(message)
        ToastManager.instance().show(f"Errore download: {message}", "error")

    def handle_update_downloaded(self, setup_path: str) -> None:
        """Gestisce il completamento del download dell'aggiornamento."""
        if hasattr(self.mw, "update_banner") and self.mw.update_banner:
            banner = self.mw.update_banner
            banner._is_complete = True
            banner.update_label.setText("Aggiornamento Pronto!")
            banner.download_btn.setText("Installa Ora")
            banner.download_btn.setVisible(True)
            banner.progress_container.setVisible(False)

        show_install_prompt(setup_path, self.mw)
