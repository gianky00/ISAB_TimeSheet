"""
SyncroJob - Info Widgets
Dialoghi e card informative.
"""

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class DetailedInfoDialog(QDialog):
    """Dialogo modale per spiegazioni dettagliate KPI."""

    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dettaglio KPI")
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setFixedWidth(400)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #ffffff;
                border: 2px solid #0d6efd;
                border-radius: 8px;
            }
            QLabel {
                color: #212529;
                font-size: 14px;
            }
        """
        )

        layout = QVBoxLayout(self)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #0d6efd; margin-bottom: 10px;")
        layout.addWidget(lbl_title)

        lbl_content = QLabel(content)
        lbl_content.setWordWrap(True)
        lbl_content.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(lbl_content)

        lbl_close = QLabel("\n(Clicca per chiudere)")
        lbl_close.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_close.setStyleSheet("color: #adb5bd; font-size: 11px;")
        layout.addWidget(lbl_close)

    def mousePressEvent(self, event):
        self.accept()


class InfoLabel(QPushButton):
    """Bottone informativo accessibile (icona ⓘ)."""

    def __init__(self, title, get_text_callback, parent=None):
        super().__init__("ⓘ", parent)
        self.title = title
        self.get_text_callback = get_text_callback
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.clicked.connect(self._show_info)
        self.setStyleSheet("QPushButton { color: #6c757d; font-weight: bold; font-size: 16px; background: transparent; border: none; padding: 0px 5px; } QPushButton:hover { color: #0d6efd; }")

    def _show_info(self):
        content = self.get_text_callback() if callable(self.get_text_callback) else str(self.get_text_callback)
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
    """Card per mostrare un KPI numerico principale."""

    def __init__(self, title, value, color="#0d6efd", parent=None, subtitle=None):
        super().__init__(parent)
        self.info_content_callback = lambda: "Nessuna informazione disponibile."
        self.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: 1px solid #e9ecef; }")
        self.setMinimumWidth(200)
        self.setMinimumHeight(120)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)

        header_layout = QHBoxLayout()
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #6c757d; font-size: 13px; font-weight: bold; border: none; background: transparent;")
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        self.info_icon = InfoLabel(title, self._get_info_content)
        header_layout.addWidget(self.info_icon)
        layout.addLayout(header_layout)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: 800; border: none; background: transparent;")
        self.lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_value)

        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setStyleSheet("color: #adb5bd; font-size: 11px; border: none; background: transparent;")
            lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_sub)

    def set_info_callback(self, callback):
        self.info_content_callback = callback

    def _get_info_content(self):
        return self.info_content_callback()
