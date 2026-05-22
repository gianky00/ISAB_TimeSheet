"""SyncroJob - Footer Business Info.

Widget per la visualizzazione delle informazioni aziendali e degli account attivi nel footer.
"""

from typing import Any

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.gui.styles import COLORS

from .components import ClickableLabel


class FooterLeftWidget(QWidget):
    """Parte sinistra del footer: Business Info.

    Visualizza il nome del cliente, la scadenza della licenza, l'ID hardware e gli account dei portali.
    """

    portale_clicked = Signal()
    safework_clicked = Signal()
    engine_clicked = Signal()
    headless_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il widget del footer sinistro.

        Args:
          parent: Widget genitore.
        """
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 2, 0, 2)
        layout.setSpacing(20)

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)

        # Configurazione Colonne
        self._setup_client_col(layout)
        self._add_separator(layout)
        self._setup_hw_col(layout)
        self._add_separator(layout)
        self._setup_portals_col(layout)
        self._add_separator(layout)
        self._setup_engine_col(layout)

        layout.addStretch()
        self.refresh_accounts()

    def _setup_client_col(self, layout: QHBoxLayout) -> None:
        """Configura la colonna Cliente / Scadenza."""
        col = QWidget()
        v = QVBoxLayout(col)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(2)
        self.client_item = QLabel()
        self.client_item.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.expiry_item = QLabel()
        self.expiry_item.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        v.addWidget(self.client_item)
        v.addWidget(self.expiry_item)
        layout.addWidget(col)

    def _setup_hw_col(self, layout: QHBoxLayout) -> None:
        """Configura la colonna HW ID / Login."""
        col = QWidget()
        v = QVBoxLayout(col)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(2)
        self.hw_id_item = QLabel()
        self.hw_id_item.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.last_login_item = QLabel()
        self.last_login_item.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        v.addWidget(self.hw_id_item)
        v.addWidget(self.last_login_item)
        layout.addWidget(col)

    def _setup_portals_col(self, layout: QHBoxLayout) -> None:
        """Configura la colonna Portali."""
        col = QWidget()
        v = QVBoxLayout(col)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(2)
        self.portale_item = ClickableLabel()
        self.portale_item.setBaseStyle(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.portale_item.clicked.connect(self.portale_clicked.emit)
        self.safe_item = ClickableLabel()
        self.safe_item.setBaseStyle(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.safe_item.clicked.connect(self.safework_clicked.emit)
        v.addWidget(self.portale_item)
        v.addWidget(self.safe_item)
        layout.addWidget(col)

    def _setup_engine_col(self, layout: QHBoxLayout) -> None:
        """Configura la colonna Motore Automazione."""
        col = QWidget()
        v = QVBoxLayout(col)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(2)
        self.engine_item = ClickableLabel()
        self.engine_item.setBaseStyle(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.engine_item.clicked.connect(self.engine_clicked.emit)
        v.addWidget(self.engine_item)
        self.headless_item = ClickableLabel()
        self.headless_item.setBaseStyle(f"color: {COLORS['text_muted']}; font-size: 12px;")
        self.headless_item.clicked.connect(self.headless_clicked.emit)
        v.addWidget(self.headless_item)
        layout.addWidget(col)

    def _add_separator(self, layout: QHBoxLayout) -> None:
        """Aggiunge una linea verticale di separazione al layout."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFixedHeight(32)
        line.setFixedWidth(2)
        line.setStyleSheet(
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 transparent, stop:0.3 {COLORS['border_dark']}, stop:0.7 {COLORS['border_dark']}, stop:1 transparent); border: none;"
        )
        layout.addWidget(line)

    def update_info(self, client: str, expiry: str, last_login: str = "", hw_id: str = "") -> None:
        """Aggiorna le informazioni testuali del footer.

        Args:
          client: Nome del cliente licenziatario.
          expiry: Data di scadenza licenza.
          last_login: Data e ora dell'ultimo accesso riuscito.
          hw_id: Identificativo hardware della macchina corrente.
        """
        self.client_item.setText(f"<b>Cliente:</b> {client}")
        self.expiry_item.setText(f"<b>Scadenza:</b> {expiry}")
        if hw_id:
            self.hw_id_item.setText(f"<b>HW ID:</b> {hw_id}")
        if last_login:
            self.last_login_item.setText(f"<b>Ultimo Accesso:</b> {last_login}")

    def refresh_accounts(self) -> None:
        """Ricarica i nomi utente degli account, il motore e la modalità dai file di configurazione."""
        config = config_manager.load_config()
        portale = self._get_def(config.get("accounts", []))
        safe = self._get_def(config.get("safework_accounts", []))
        engine = config.get("automation_engine", "selenium").capitalize()

        self.portale_item.setText(f"<b>   Portale:</b> {portale or 'N.C.'}")
        self.safe_item.setText(f"<b>    SafeWork:</b> {safe or 'N.C.'}")
        self.engine_item.setText(f"<b>    Motore:</b> {engine}")

        is_headless = config.get("browser_headless", False)
        mode_text = "Nascosto" if is_headless else "Visibile"
        mode_icon = "         " if is_headless else "    "
        self.headless_item.setText(f"{mode_icon} Browser: {mode_text}")

    def _get_def(self, accounts: list[dict[str, Any]]) -> str | None:
        """Helper per estrarre l'username dell'account predefinito."""
        for a in accounts:
            if a.get("default"):
                return str(a.get("username"))
        return str(accounts[0].get("username")) if accounts else None

    def fade_in(self, duration: int = 400) -> None:
        """Esegue un'animazione di comparsa graduale (dissolvenza) del widget.

        Args:
          duration: Durata dell'animazione in ms.
        """
        self.setVisible(True)
        self.anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self.anim.setDuration(duration)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.start()
