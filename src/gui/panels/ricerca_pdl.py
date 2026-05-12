"""
SyncroJob - Ricerca PDL Panel
Pannello per il bot Ricerca PDL (SafeWork).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.gui.controllers.bot_worker import BotWorker
from src.gui.panels.base import BaseBotPanel
from src.gui.styles import COLORS, STATUS_COLORS
from src.gui.widgets.core_widgets import (
    FilterComboBox,
    StandardCheckBox,
)
from src.gui.widgets.toast import ToastManager

if TYPE_CHECKING:
    from src.bots.base.base_bot import BaseBot


class RicercaPDLPanel(BaseBotPanel):
    """
    Pannello per la ricerca ed esportazione massiva dei PDL da SafeWork.
    """

    data_updated = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello Ricerca PDL.

        Args:
          parent: Widget genitore.
        """
        super().__init__(
            bot_id="ricerca_pdl",
            bot_name="Ricerca PDL",
            bot_description="Ricerca ed esporta i PDL da SafeWork nel database locale.",
            parent=parent,
        )
        self.sync_module_id = "pdl"

        self.exclude_closed_check: StandardCheckBox
        self.site_combo: FilterComboBox

        self._setup_content()
        self._data_loaded = False
        # Il caricamento dati viene differito a showEvent

    def showEvent(self, event: Any) -> None:
        """Esegue il primo caricamento dati solo quando il pannello diventa visibile."""
        super().showEvent(event)
        if not self._data_loaded:
            self._data_loaded = True
            QTimer.singleShot(10, self._load_saved_data)

    def get_bot_class(self) -> type[BaseBot]:
        """Restituisce la classe SafeWorkPDLSearchBot associata."""
        from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot

        return SafeWorkPDLSearchBot

    def _setup_content(self) -> None:
        """Inizializza e posiziona i componenti UI di filtraggio e ricerca con design Modern Card."""
        # Sezione Parametri (Design Modern Card Uniformato)
        params_container = QFrame()
        params_container.setObjectName("filterBar")
        params_container.setStyleSheet(f"""
      QFrame#filterBar {{
        background-color: {COLORS["bg_white"]};
        border: 1px solid {COLORS["border_light"]};
        border-radius: 12px;
      }}
    """)

        params_layout = QHBoxLayout(params_container)
        params_layout.setContentsMargins(15, 10, 15, 10)
        params_layout.setSpacing(20)

        from src.gui.styles import COMBOBOX_STYLE, LABEL_MUTED

        # 1. Flag Escludi Chiusi
        vbox_check = QVBoxLayout()
        vbox_check.setSpacing(4)
        lbl_status = QLabel("STATO PERMESSI")
        lbl_status.setStyleSheet(LABEL_MUTED)
        vbox_check.addWidget(lbl_status)

        self.exclude_closed_check = StandardCheckBox("Escludi chiusi/scaduti")
        self.exclude_closed_check.setChecked(True)
        self.exclude_closed_check.setStyleSheet(f"color: {COLORS['text_dark']}; font-weight: 500;")
        self.exclude_closed_check.stateChanged.connect(self._save_data)
        vbox_check.addWidget(self.exclude_closed_check)
        params_layout.addLayout(vbox_check)

        # Vertical Divider
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        params_layout.addWidget(v_line)

        # 2. Selezione Sito
        vbox_site = QVBoxLayout()
        vbox_site.setSpacing(4)
        lbl_site = QLabel("SITO DI RIFERIMENTO")
        lbl_site.setStyleSheet(LABEL_MUTED)
        vbox_site.addWidget(lbl_site)

        self.site_combo = FilterComboBox()
        self.site_combo.addItems(["Seleziona tutto", "IGCC", "ISAB Nord", "ISAB Sud"])
        self.site_combo.setMinimumWidth(200)
        self.site_combo.setStyleSheet(COMBOBOX_STYLE)
        self.site_combo.currentTextChanged.connect(self._save_data)
        vbox_site.addWidget(self.site_combo)
        params_layout.addLayout(vbox_site)

        params_layout.addStretch()

        # Aggiunta al layout principale
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(10, 10, 10, 15)
        wrapper_layout.addWidget(params_container)
        self.content_layout.addWidget(wrapper)
        self.content_layout.addStretch()

    def _load_saved_data(self) -> None:
        """Carica le ultime impostazioni di ricerca salvate."""
        self._is_loading = True
        try:
            config = config_manager.load_config()
            self.exclude_closed_check.setChecked(config.get("pdl_search_exclude_closed", True))
            saved_site = config.get("pdl_search_site", "Seleziona tutto")
            self.site_combo.setCurrentText(saved_site)
        finally:
            self._is_loading = False

    def _save_data(self) -> None:
        """Salva i filtri di ricerca correnti nella configurazione."""
        if getattr(self, "_is_loading", False):
            return
        config_manager.set_config_value("pdl_search_exclude_closed", self.exclude_closed_check.isChecked())
        config_manager.set_config_value("pdl_search_site", self.site_combo.currentText())

    def _validate_and_switch_account(
        self, username: str, password: str, account_type: str
    ) -> tuple[str, str, str, bool]:
        """Verifica se l'account  di tipo ISAB e propone lo switch a Esecutore."""
        if account_type != "ISAB":
            return username, password, account_type, True

        sw_accounts = config_manager.load_config().get("safework_accounts", [])
        esecutore_acc = next((a for a in sw_accounts if a.get("type") == "Esecutore"), None)

        if esecutore_acc:
            msg = (
                "L'account SafeWork attualmente selezionato  di tipo <b>ISAB</b>.<br><br>"
                "La Ricerca PDL massiva richiede solitamente un account <b>Esecutore</b> per funzionare correttamente.<br><br>"
                f"Vuoi passare all'account Esecutore <b>{esecutore_acc.get('username')}</b> e proseguire?"
            )
            from src.gui.dialogs.confirmation_dialog import ConfirmationDialog

            if ConfirmationDialog.confirm(self, "Tipo Account Incompatibile", msg, is_rich_text=True):
                if config_manager.set_default_account("safework", esecutore_acc.get("username", "")):
                    from src.gui.main_window.main import MainWindow

                    main_win = self.window()
                    if isinstance(main_win, MainWindow):
                        main_win.status_bar_component.footer_left.refresh_accounts()
                    return (
                        esecutore_acc.get("username", ""),
                        esecutore_acc.get("password", ""),
                        "Esecutore",
                        True,
                    )
                ToastManager.instance().show("Errore durante lo switch dell'account.", "error")
        else:
            from src.gui.dialogs.confirmation_dialog import ConfirmationDialog

            ConfirmationDialog.show_warning(
                self,
                "Account non idoneo",
                "Questo bot richiede un account <b>Esecutore</b> e non sono stati trovati account alternativi.",
                is_rich_text=True,
            )
        return username, password, account_type, False

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """Avvia l'esecuzione del bot Ricerca PDL configurando worker e segnali."""
        super()._on_start(params_override)
        user, pwd, acc_type = self.get_safework_credentials()

        user, pwd, acc_type, ok = self._validate_and_switch_account(user, pwd, acc_type)
        if not ok:
            self._update_status(STATUS_COLORS["stopped"], "Pronto")
            self._reset_buttons()
            return

        if not user or not pwd:
            ToastManager.instance().show("Configura le credenziali SafeWork.", "warning")
            self._update_status(STATUS_COLORS["error"], "Credenziali mancanti")
            self._reset_buttons()
            return

        self._start_bot_worker(user, pwd, acc_type)

    def _reset_buttons(self) -> None:
        """Ripristina lo stato dei pulsanti Start/Stop."""
        if self.start_btn:
            self.start_btn.setEnabled(True)
        if self.stop_btn:
            self.stop_btn.setEnabled(False)

    def _start_bot_worker(self, user: str, pwd: str, acc_type: str) -> None:
        """Inizializza e avvia il worker per il bot."""
        bot_data = {
            "exclude_closed": self.exclude_closed_check.isChecked(),
            "site_selection": self.site_combo.currentText(),
        }
        cfg = config_manager.load_config()

        bot_params = {
            "username": user,
            "password": pwd,
            "account_type": acc_type,
            "headless": cfg.get("browser_headless", False),
            "timeout": cfg.get("browser_timeout", 30),
            "download_path": config_manager.get_download_path(),
        }

        main_win: Any = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        worker = BotWorker(
            bot_id="ricerca_pdl", bot_params=bot_params, data=[bot_data], telegram_service=tg_service
        )
        self.worker = worker
        self._setup_worker_connections(worker)

        if self.start_btn:
            self.start_btn.setEnabled(False)
        if self.stop_btn:
            self.stop_btn.setEnabled(True)
        if self.log_widget:
            self.log_widget.clear()
            self.log_widget.append("Avvio Ricerca PDL SafeWork...")
        worker.start()
        self.bot_started.emit()

    def get_safework_credentials(self) -> tuple[str, str, str]:
        """Recupera le credenziali SafeWork configurate. Ritorna (user, pass, tipo)."""
        # Prende il default da safework_accounts
        accounts = config_manager.load_config().get("safework_accounts", [])
        if not accounts:
            return "", "", "Esecutore"

        # Cerca il default
        default_acc = next((a for a in accounts if a.get("default")), accounts[0])
        return (
            default_acc.get("username", ""),
            default_acc.get("password", ""),
            default_acc.get("type", "Esecutore"),
        )

    def _on_worker_finished(self, success: bool) -> None:
        """Emette il segnale data_updated al termine dell'operazione."""
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()
