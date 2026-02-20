"""
SyncroJob - Ricerca PDL Panel
Pannello per il bot Ricerca PDL (SafeWork).
"""

from typing import Any

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QColor

from src.core import config_manager
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.widgets.toast import ToastManager


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

    def get_bot_class(self):
        """Restituisce la classe SafeWorkPDLSearchBot associata."""
        from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot
        return SafeWorkPDLSearchBot

    def _setup_content(self):
        """Inizializza e posiziona i componenti UI di filtraggio e ricerca con design Neon Card."""
        # Sezione Parametri (Design Neon Floating Card Standard)
        params_container = QFrame()
        params_container.setObjectName("paramsContainer")
        params_container.setStyleSheet("""
            QFrame#paramsContainer {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-bottom: 3px solid #00E5FF; /* Cyan Neon */
                border-radius: 12px;
            }
            QLabel {
                color: #424242;
                font-weight: bold;
                font-size: 13px;
                background: transparent;
            }
            QComboBox, QCheckBox {
                background: transparent;
            }
        """)
        
        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 40))
        params_container.setGraphicsEffect(shadow)

        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(15, 15, 15, 15)
        params_layout.setSpacing(15)

        # Riga unica per Flag e Sito
        top_row = QHBoxLayout()

        # 1. Flag Escludi Chiusi
        vbox_check = QVBoxLayout()
        vbox_check.addWidget(QLabel("Stato Permessi"))
        self.exclude_closed_check = QCheckBox("Escludi chiusi/scaduti")
        self.exclude_closed_check.setChecked(True)
        self.exclude_closed_check.stateChanged.connect(self._save_data)
        vbox_check.addWidget(self.exclude_closed_check)
        top_row.addLayout(vbox_check)

        top_row.addSpacing(20)

        # 2. Selezione Sito
        vbox_site = QVBoxLayout()
        vbox_site.addWidget(QLabel("Sito di Riferimento"))
        self.site_combo = QComboBox()
        self.site_combo.addItems(["Seleziona tutto", "IGCC", "ISAB Nord", "ISAB Sud"])
        self.site_combo.setMinimumWidth(180)
        self.site_combo.setMinimumHeight(38)
        self.site_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #cfd8dc;
                border-radius: 6px;
                padding: 5px 10px;
                background-color: #f8f9fa;
            }
            QComboBox:focus { border: 2px solid #00E5FF; background-color: #ffffff; }
        """)
        self.site_combo.currentTextChanged.connect(self._save_data)
        vbox_site.addWidget(self.site_combo)
        top_row.addLayout(vbox_site)

        top_row.addStretch()
        params_layout.addLayout(top_row)

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

    def get_bot_instance(self):
        """Crea e restituisce un'istanza configurata del bot Ricerca PDL."""
        from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot

        username, password = self.get_credentials()
        config = config_manager.load_config()

        return SafeWorkPDLSearchBot(
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
        )

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """Avvia l'esecuzione del bot Ricerca PDL configurando worker e segnali."""
        super()._on_start(params_override)
        username, password = self.get_credentials()

        # Ensure UI elements are available
        if self.start_btn is None:
            raise RuntimeError("Start button is None")
        if self.stop_btn is None:
            raise RuntimeError("Stop button is None")
        if self.log_widget is None:
            raise RuntimeError("Log widget is None")

        if not username or not password:
            ToastManager.instance().show("Configura le credenziali SafeWork nelle Impostazioni.", "warning")
            self._update_status("#C62828", "Credenziali mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        bot = self.get_bot_instance()
        if not bot:
            return

        bot_data = {
            "exclude_closed": self.exclude_closed_check.isChecked(),
            "site_selection": self.site_combo.currentText(),
        }

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        worker = BotWorker(bot, [bot_data], telegram_service=tg_service)
        self.worker = worker
        self._setup_worker_connections(worker)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio Ricerca PDL SafeWork...")
        worker.start()
        self.bot_started.emit()

    def get_credentials(self) -> tuple[str, str]:
        """Recupera le credenziali SafeWork configurate."""
        # Prende il default da safework_accounts
        accounts = config_manager.load_config().get("safework_accounts", [])
        if not accounts:
            return "", ""

        # Cerca il default
        default_acc = next((a for a in accounts if a.get("default")), accounts[0])
        return default_acc.get("username", ""), default_acc.get("password", "")

    def _on_worker_finished(self, success: bool):
        """Emette il segnale data_updated al termine dell'operazione."""
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()
