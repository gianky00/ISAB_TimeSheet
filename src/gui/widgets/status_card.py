from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.design.colors import LIGHT
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class StatusCard(QFrame):
    """
    Card per la status bar che mostra lo stato di un servizio.
    Layout: [Icona] | [Titolo]     | [BADGE AUTOPILOT]
                    | [Stato]      |
    """

    clicked = pyqtSignal()

    def __init__(self, title: str, status: str = "In attesa", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # Cursore pointer per indicare cliccabilità
        self.setStyleSheet(
            f"""
            StatusCard {{
                background-color: {COLORS['bg_white']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 8px;
            }}
            StatusCard:hover {{
                background-color: {COLORS['bg_hover']};
                border-color: {COLORS['teal_accent']};
            }}
            """
        )

        self._palette = LIGHT
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)
        layout.setSpacing(12)

        # 1. Icona colorata (Barra verticale decorativa)
        self._icon_bar = QFrame()
        self._icon_bar.setFixedWidth(4)
        self._icon_bar.setStyleSheet(f"background-color: {self._palette.primary}; border-radius: 2px;")
        layout.addWidget(self._icon_bar)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(20, 20)
        icon_lbl.setScaledContents(True)
        icon_lbl.setPixmap(
            get_colored_icon(get_asset_path(Icons.CLOCK), self._palette.on_surface).pixmap(20, 20)
        )
        layout.addWidget(icon_lbl)

        # 2. Colonna Centrale: Titolo e Stato
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._title_label = QLabel(title)
        self._title_label.setStyleSheet(
            f"font-weight: 700; font-size: 13px; color: {self._palette.on_surface}; border: none; background: transparent;"
        )
        text_layout.addWidget(self._title_label)

        self._status = status
        self._status_label = QLabel(status)
        self._status_label.setStyleSheet(
            f"font-size: 11px; color: {self._palette.on_surface}; opacity: 0.8; border: none; background: transparent;"
        )
        text_layout.addWidget(self._status_label)

        layout.addLayout(text_layout)

        # 3. Spacer elastico (spinge il badge a destra)
        layout.addStretch()

        # 4. Badge Autopilot (Grande, a destra)
        self._meta_label = QLabel()
        self._meta_label.setVisible(False)
        self._meta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._meta_label)

    def setStatus(self, message: str, status_id: str | None = None) -> None:
        """Imposta il testo di stato e opzionalmente il colore dell'indicatore."""
        self._status_label.setText(message)
        if status_id:
            self._status = status_id
            self._icon_bar.setStyleSheet(
                f"background-color: {status_id if status_id.startswith('#') else self._palette.primary}; border-radius: 2px;"
            )

    def setAutopilot(self, active: bool, text: str = "") -> None:
        """
        Imposta l'indicatore dell'autopilot.
        Ora il badge è posizionato a destra e occupa visivamente più spazio verticale.
        """
        if active:
            self._meta_label.setText(text.upper() or "AUTO")
            self._meta_label.setVisible(True)
            # Stile "Big Badge": font 11px, grassetto, padding generoso
            self._meta_label.setStyleSheet(
                f"""
                font-size: 11px;
                font-weight: 800;
                color: {COLORS['success_material']};
                background-color: {COLORS['table_success_bg']};
                border-radius: 6px;
                padding: 6px 10px;
                border: 1px solid {COLORS['success_green']};
                """
            )
        else:
            self._meta_label.setVisible(False)

    def _update_status_display(self, message: str) -> None:
        """Aggiorna solo il testo dello stato (per compatibilità)."""
        self._status_label.setText(message)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """Emette il segnale clicked quando la card viene cliccata."""
        self.clicked.emit()
        super().mousePressEvent(event)
