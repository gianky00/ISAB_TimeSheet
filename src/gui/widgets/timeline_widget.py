"""
SyncroJob - Enterprise Log Console
Visualizzatore di log testuali pulito e professionale per SyncroJob.
Sostituisce l'estetica HUD con un design moderno coerente con il sistema.
"""

import re

from PySide6.QtCore import QRectF, Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS


class StandardTimelineFrame(QFrame):
    """Frame pulito ed elegante per i log in stile Enterprise."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {COLORS['bg_white']}; border-radius: 12px;")

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna un bordo sottile e professionale intorno alla console."""
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
            path = QPainterPath()
            path.addRoundedRect(rect, 12, 12)

            painter.setPen(QPen(QColor(COLORS["border_light"]), 1))
            painter.drawPath(path)
        finally:
            painter.end()


class LogEntryWidget(QWidget):
    """Riga di log con timestamp e feedback cromatico per livello."""

    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(12)

        pattern = r"\[(.*?)\]\s+(INFO|WARNING|ERROR|DEBUG|CRITICAL|SUCCESS)\s+-\s+(.*?)\s+-\s+(.*)"
        match = re.search(pattern, text)

        color = COLORS["text_dark"]
        icon = "  "

        if match:
            level = match.group(2)
            msg = match.group(4)
            time_str = match.group(1).split()[-1]

            if level == "INFO":
                color = COLORS["primary_blue"]
                icon = "  "
            elif level == "WARNING":
                color = COLORS["warning_orange"]
                icon = "  "
            elif level in ("ERROR", "CRITICAL"):
                color = COLORS["error_red"]
                icon = "  "
            elif level == "SUCCESS":
                color = COLORS["success_dark"]
                icon = "  "

            self.lbl_time = QLabel(time_str)
            self.lbl_time.setStyleSheet(
                f"color: {COLORS['text_muted']}; font-family: monospace; font-size: 11px;"
            )
            layout.addWidget(self.lbl_time)

            self.lbl_icon = QLabel(icon)
            self.lbl_icon.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
            layout.addWidget(self.lbl_icon)

            self.lbl_msg = QLabel(msg)
            self.lbl_msg.setWordWrap(True)
            self.lbl_msg.setStyleSheet(f"color: {COLORS['text_dark']}; font-weight: 500; font-size: 12px;")
            layout.addWidget(self.lbl_msg, 1)
        else:
            self.lbl_msg = QLabel(text)
            self.lbl_msg.setWordWrap(True)
            self.lbl_msg.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
            layout.addWidget(self.lbl_msg, 1)


class EnterpriseLogConsole(QWidget):
    """Console di log professionale con autoscroll e design coordinato."""

    log_added = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame = StandardTimelineFrame()
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(10, 10, 10, 10)

        self.scroll_container = QScrollArea()
        self.scroll_container.setWidgetResizable(True)
        self.scroll_container.setStyleSheet("background: transparent; border: none;")

        self.content = QWidget()
        self.content.setStyleSheet("background: transparent;")
        self.log_layout = QVBoxLayout(self.content)
        self.log_layout.setContentsMargins(0, 0, 0, 0)
        self.log_layout.setSpacing(2)
        self.log_layout.addStretch()

        self.scroll_container.setWidget(self.content)
        self.frame_layout.addWidget(self.scroll_container)
        layout.addWidget(self.frame)

    def add_log(self, text: str) -> None:
        """Aggiunge una riga di log alla console con autoscroll."""
        entry = LogEntryWidget(text)
        self.log_layout.insertWidget(self.log_layout.count() - 1, entry)

        bar = self.scroll_container.verticalScrollBar()
        if bar:
            # Fix: Ensure bar is not deleted when timer fires (prevents RuntimeError in tests)
            from shiboken6 import Shiboken

            def safe_scroll() -> None:
                """Esegue lo scroll in modo sicuro per evitare crash UI."""
                if Shiboken.isValid(bar):
                    bar.setValue(bar.maximum())

            QTimer.singleShot(20, safe_scroll)
        self.log_added.emit(text)

    def append(self, text: str, status: str = "") -> None:
        """Alias di compatibilit  per aggiungere log."""
        self.add_log(text)

    def clear(self) -> None:
        """Rimuove tutti i log visualizzati nella console."""
        while self.log_layout.count() > 1:
            item = self.log_layout.takeAt(0)
            if item and (widget := item.widget()):
                widget.deleteLater()

    def set_mood(self, mood: str) -> None:
        """Metodo mantenuto per compatibilit  API."""


class MissionReportCard(QFrame):
    """Card riassuntiva di fine missione in stile Enterprise."""

    def __init__(self, duration: str, success: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(f"""
      QFrame {{
        background-color: {COLORS["bg_light"]};
        border: 2px solid {COLORS["success_dark"] if success else COLORS["error_red"]};
        border-radius: 10px;
      }}
    """)
        layout = QVBoxLayout(self)
        title = QLabel("MISSION REPORT" if success else "MISSION FAILED")
        title.setStyleSheet(f"font-weight: bold; color: {COLORS['text_dark']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        info = QLabel(f"Durata: {duration}")
        info.setStyleSheet(f"color: {COLORS['text_muted']};")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)


# Alias di compatibilit  per il vecchio sistema
TimelineWidget = EnterpriseLogConsole
HorizontalTimelineWidget = EnterpriseLogConsole
HorizontalTimelineContainer = StandardTimelineFrame
HorizontalLogItem = LogEntryWidget
