"""
SyncroJob - Ricerca PDL Panel
Pannello per il bot Ricerca PDL (SafeWork).
"""

from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.gui.panels.base import BaseBotPanel, BotWorker
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

    data_updated = pyqtSignal()

    def __init__(self, parent=None):
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
        self._setup_content()
        QTimer.singleShot(10, self._load_saved_data)

    def get_bot_class(self) -> type["BaseBot"]:
        """Restituisce la classe SafeWorkPDLSearchBot associata."""
        from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot

        return SafeWorkPDLSearchBot

    def _setup_content(self):
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

    def _load_saved_data(self):
        """Carica le ultime impostazioni di ricerca salvate."""
        config = config_manager.load_config()
        self.exclude_closed_check.setChecked(config.get("pdl_search_exclude_closed", True))
        saved_site = config.get("pdl_search_site", "Seleziona tutto")
        self.site_combo.setCurrentText(saved_site)

    def _save_data(self):
        """Salva i filtri di ricerca correnti nella configurazione."""
        config_manager.set_config_value("pdl_search_exclude_closed", self.exclude_closed_check.isChecked())
        config_manager.set_config_value("pdl_search_site", self.site_combo.currentText())

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """Avvia l'esecuzione del bot Ricerca PDL configurando worker e segnali."""
        super()._on_start(params_override)
        username, password, account_type = self.get_safework_credentials()

        # Ensure UI elements are available
        if self.start_btn is None:
            raise RuntimeError("Start button is None")
        if self.stop_btn is None:
            raise RuntimeError("Stop button is None")
        if self.log_widget is None:
            raise RuntimeError("Log widget is None")

        if not username or not password:
            ToastManager.instance().show("Configura le credenziali SafeWork nelle Impostazioni.", "warning")
            self._update_status(STATUS_COLORS["error"], "Credenziali mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        bot_data = {
            "exclude_closed": self.exclude_closed_check.isChecked(),
            "site_selection": self.site_combo.currentText(),
        }

        from src.core.config_manager import load_config
        config = load_config()

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None


        # Configura i parametri per il BotWorker (verranno passati a create_bot nel thread secondario)
        bot_params = {
            "username": username,
            "password": password,
            "account_type": account_type,
            "headless": config.get("browser_headless", False),
            "timeout": config.get("browser_timeout", 30),
            "download_path": config_manager.get_download_path(),
        }

        # Inizializza il worker in modo asincrono
        worker = BotWorker(
            bot_id="ricerca_pdl",
            bot_params=bot_params,
            data=[bot_data],
            telegram_service=tg_service,
        )
        self.worker = worker
        self._setup_worker_connections(worker)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
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

    def _on_worker_finished(self, success: bool):
        """Emette il segnale data_updated al termine dell'operazione."""
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()
