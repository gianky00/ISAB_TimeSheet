"""
SyncroJob - Footer Business Info
Widget per la visualizzazione delle informazioni aziendali e degli account attivi nel footer.
"""

from typing import Any

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, pyqtSignal
from PyQt6.QtWidgets import (
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
    """
    Parte sinistra del footer: Business Info.
    Visualizza il nome del cliente, la scadenza della licenza, l'ID hardware e gli account dei portali.
    """

    portale_clicked = pyqtSignal()
    safework_clicked = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il widget del footer sinistro.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 2, 0, 2)
        layout.setSpacing(20)

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)

        # Colonna 1: Cliente / Scadenza
        col1 = QWidget()
        v1 = QVBoxLayout(col1)
        v1.setContentsMargins(0, 0, 0, 0)
        v1.setSpacing(2)
        self.client_item = QLabel()
        self.client_item.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.expiry_item = QLabel()
        self.expiry_item.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        v1.addWidget(self.client_item)
        v1.addWidget(self.expiry_item)
        layout.addWidget(col1)

        self._add_separator(layout)

        # Colonna 2: HW ID / Login
        col2 = QWidget()
        v2 = QVBoxLayout(col2)
        v2.setContentsMargins(0, 0, 0, 0)
        v2.setSpacing(2)
        self.hw_id_item = QLabel()
        self.hw_id_item.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.last_login_item = QLabel()
        self.last_login_item.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        v2.addWidget(self.hw_id_item)
        v2.addWidget(self.last_login_item)
        layout.addWidget(col2)

        self._add_separator(layout)

        # Colonna 3: Portali
        col3 = QWidget()
        v3 = QVBoxLayout(col3)
        v3.setContentsMargins(0, 0, 0, 0)
        v3.setSpacing(2)
        self.portale_item = ClickableLabel()
        self.portale_item.setBaseStyle(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.portale_item.clicked.connect(self.portale_clicked.emit)
        self.safe_item = ClickableLabel()
        self.safe_item.setBaseStyle(f"color: {COLORS['text_dark']}; font-size: 13px;")
        self.safe_item.clicked.connect(self.safework_clicked.emit)
        v3.addWidget(self.portale_item)
        v3.addWidget(self.safe_item)
        layout.addWidget(col3)

        layout.addStretch()
        self.refresh_accounts()

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
        """
        Aggiorna le informazioni testuali del footer.

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
        """Ricarica i nomi utente degli account di default dai file di configurazione."""
        config = config_manager.load_config()
        portale = self._get_def(config.get("accounts", []))
        safe = self._get_def(config.get("safework_accounts", []))
        self.portale_item.setText(f"<b>🌐 Portale:</b> {portale or 'N.C.'}")
        self.safe_item.setText(f"<b>🛡️ SafeWork:</b> {safe or 'N.C.'}")

    def _get_def(self, accounts: list[dict[str, Any]]) -> str | None:
        """Helper per estrarre l'username dell'account predefinito."""
        for a in accounts:
            if a.get("default"):
                return str(a.get("username"))
        return str(accounts[0].get("username")) if accounts else None

    def fade_in(self, duration: int = 400) -> None:
        """
        Esegue un'animazione di comparsa graduale (dissolvenza) del widget.

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
