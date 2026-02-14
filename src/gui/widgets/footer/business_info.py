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

from .components import ClickableLabel


class FooterLeftWidget(QWidget):
    """Parte sinistra del footer: Business Info."""

    portale_clicked = pyqtSignal()
    safework_clicked = pyqtSignal()
    TEXT_COLOR = "#000000"

    def __init__(self, parent: QWidget | None = None) -> None:
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
        self.client_item.setStyleSheet(f"color: {self.TEXT_COLOR}; font-size: 13px;")
        self.expiry_item = QLabel()
        self.expiry_item.setStyleSheet(f"color: {self.TEXT_COLOR}; font-size: 13px;")
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
        self.hw_id_item.setStyleSheet(f"color: {self.TEXT_COLOR}; font-size: 13px;")
        self.last_login_item = QLabel()
        self.last_login_item.setStyleSheet(f"color: {self.TEXT_COLOR}; font-size: 13px;")
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
        self.portale_item.setBaseStyle(f"color: {self.TEXT_COLOR}; font-size: 13px;")
        self.portale_item.clicked.connect(self.portale_clicked.emit)
        self.safe_item = ClickableLabel()
        self.safe_item.setBaseStyle(f"color: {self.TEXT_COLOR}; font-size: 13px;")
        self.safe_item.clicked.connect(self.safework_clicked.emit)
        v3.addWidget(self.portale_item)
        v3.addWidget(self.safe_item)
        layout.addWidget(col3)

        layout.addStretch()
        self.refresh_accounts()

    def _add_separator(self, layout: QHBoxLayout) -> None:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFixedHeight(32)
        line.setFixedWidth(2)
        line.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 transparent, stop:0.3 #BDBDBD, stop:0.7 #BDBDBD, stop:1 transparent); border: none;"
        )
        layout.addWidget(line)

    def update_info(self, client: str, expiry: str, last_login: str = "", hw_id: str = "") -> None:
        self.client_item.setText(f"<b>Cliente:</b> {client}")
        self.expiry_item.setText(f"<b>Scadenza:</b> {expiry}")
        if hw_id:
            self.hw_id_item.setText(f"<b>HW ID:</b> {hw_id}")
        if last_login:
            self.last_login_item.setText(f"<b>Ultimo Accesso:</b> {last_login}")

    def refresh_accounts(self) -> None:
        config = config_manager.load_config()
        portale = self._get_def(config.get("accounts", []))
        safe = self._get_def(config.get("safework_accounts", []))
        self.portale_item.setText(f"<b>🌐 Portale:</b> {portale or 'N.C.'}")
        self.safe_item.setText(f"<b>🛡️ SafeWork:</b> {safe or 'N.C.'}")

    def _get_def(self, accounts: list[dict[str, Any]]) -> str | None:
        for a in accounts:
            if a.get("default"):
                return str(a.get("username"))
        return str(accounts[0].get("username")) if accounts else None

    def fade_in(self, duration: int = 400) -> None:
        """Animazione di comparsa graduale."""
        self.setVisible(True)
        self.anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self.anim.setDuration(duration)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.start()
