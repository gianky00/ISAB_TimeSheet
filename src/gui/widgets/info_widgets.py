"""SyncroJob - Info Widgets.

Dialoghi e card informative.
"""

from collections.abc import Callable

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.application.services.constants import Icons
from src.gui.styles import COLORS
from src.infrastructure.utils.helpers import get_asset_path, get_colored_icon


class DetailedInfoDialog(QDialog):
    """Dialogo modale per spiegazioni dettagliate KPI.

    Inizializza la classe.
    """

    def __init__(self, title: str, content: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Dettaglio KPI")
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setFixedWidth(400)
        self.setStyleSheet(
            f"""
      QDialog {{
        background-color: {COLORS["bg_white"]};
        border: 2px solid {COLORS["primary_dark"]};
        border-radius: 8px;
      }}
      QLabel {{
        color: {COLORS["text_dark"]};
        font-size: 14px;
      }}
    """
        )

        layout = QVBoxLayout(self)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(
            f"font-weight: bold; font-size: 16px; color: {COLORS['primary_dark']}; margin-bottom: 10px;"
        )
        layout.addWidget(lbl_title)

        lbl_content = QLabel(content)
        lbl_content.setWordWrap(True)
        lbl_content.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(lbl_content)

        lbl_close = QLabel("\n(Clicca per chiudere)")
        lbl_close.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_close.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px;")
        layout.addWidget(lbl_close)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """Chiude il dialogo al click del mouse."""
        self.accept()


class InfoLabel(QPushButton):
    """Bottone informativo accessibile (icona SVG).

    Inizializza la classe.
    """

    def __init__(
        self, title: str, get_text_callback: str | Callable[[], str], parent: QWidget | None = None
    ) -> None:
        super().__init__("", parent)
        self.setIcon(get_colored_icon(get_asset_path(Icons.HELP), COLORS["text_dark"]))
        self.setIconSize(QSize(18, 18))
        self.title = title
        self.get_text_callback = get_text_callback
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.clicked.connect(self._show_info)
        self.setStyleSheet(
            f"QPushButton {{ color: {COLORS['text_muted']}; font-weight: bold; font-size: 16px; background: transparent; border: none; padding: 0px 5px; }} QPushButton:hover {{ color: {COLORS['primary_dark']}; }}"
        )

    def _show_info(self) -> None:
        content = (
            self.get_text_callback() if callable(self.get_text_callback) else str(self.get_text_callback)
        )
        dlg = DetailedInfoDialog(self.title, content, self.window())
        cursor_pos = QCursor.pos()
        top_left = self.mapToGlobal(QPoint(0, 0))
        widget_rect = QRect(top_left, self.size())
        target_pos = cursor_pos if widget_rect.contains(cursor_pos) else widget_rect.center()
        screen = QApplication.screenAt(target_pos)
        if screen:
            dlg.adjustSize()
            x = target_pos.x()
            if x + dlg.width() > screen.availableGeometry().right():
                x -= dlg.width() + 10
            else:
                x += 10
            y = target_pos.y()
            if y + dlg.height() > screen.availableGeometry().bottom():
                y -= dlg.height() + 10
            else:
                y += 10
            dlg.move(x, y)
        else:
            dlg.move(target_pos)
        dlg.exec()


class KPIBigCard(QFrame):
    """Card per mostrare un KPiùnumerico principale.

    Inizializza la classe.
    """

    def __init__(
        self,
        title: str,
        value: str,
        color: str | None = None,
        parent: QWidget | None = None,
        subtitle: str | None = None,
    ) -> None:
        super().__init__(parent)
        accent = color or COLORS["primary_dark"]
        self.info_content_callback: Callable[[], str] = lambda: "Nessuna informazione disponibile."
        self.setStyleSheet(
            f"""
      QFrame {{
        background-color: {COLORS["bg_white"]};
        border-radius: 15px;
        border: 1px solid {COLORS["border_light"]};
        border-left: 5px solid {accent};
      }}
    """
        )
        self.setMinimumWidth(200)
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)

        header_layout = QHBoxLayout()
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 13px; font-weight: bold; border: none; background: transparent;"
        )
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        self.info_icon = InfoLabel(title, self._get_info_content)
        header_layout.addWidget(self.info_icon)
        layout.addLayout(header_layout)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(
            f"color: {accent}; font-size: 28px; font-weight: 800; border: none; background: transparent;"
        )
        self.lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_value)

        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setStyleSheet(
                f"color: {COLORS['text_light']}; font-size: 11px; border: none; background: transparent;"
            )
            lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_sub)

    def set_info_callback(self, callback: Callable[[], str]) -> None:
        """Imposta la funzione che restituisce il testo informativo del KPI."""
        self.info_content_callback = callback

    def _get_info_content(self) -> str:
        return self.info_content_callback()
