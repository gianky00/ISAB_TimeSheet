"""
SyncroJob - Timeline Widgets
Widget per la visualizzazione cronologica dei log e dei report di missione.
"""

import re
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    QUrl,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QColor,
    QDesktopServices,
    QPainter,
    QPen,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.utils.helpers import get_asset_path
from src.utils.log_humanizer import SmartLogTranslator


class HorizontalLogItem(QWidget):
    """Widget per singolo elemento della timeline log orizzontale."""

    def __init__(self, human_msg, tech_msg, category, timestamp, parent=None):
        super().__init__(parent)
        self.setFixedSize(160, 90)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        self.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """
        )

        snapshot_path = None
        fixit_action = None

        if "[IMG:" in tech_msg:
            match = re.search(r"\[IMG:(.*?)\]", tech_msg)
            if match:
                snapshot_path = match.group(1)
                tech_msg = tech_msg.replace(match.group(0), "").strip()

        if "[FIXIT:" in tech_msg:
            match = re.search(r"\[FIXIT:(.*?)\]", tech_msg)
            if match:
                fixit_action = match.group(1)
                tech_msg = tech_msg.replace(match.group(0), "").strip()

        icons = {
            "start": "🚀",
            "login": "🔐",
            "search": "🔍",
            "download": "📥",
            "success": "✅",
            "error": "❌",
            "wait": "⏳",
            "info": "ℹ️",
        }
        colors = {
            "start": "#0d6efd",
            "login": "#6f42c1",
            "search": "#fd7e14",
            "download": "#0dcaf0",
            "success": "#198754",
            "error": "#dc3545",
            "wait": "#ffc107",
            "info": "#6c757d",
        }

        self.category_color = colors.get(category, "#6c757d")

        top_row = QHBoxLayout()
        top_row.setSpacing(5)

        lbl_icon = QLabel(icons.get(category, "•"))
        lbl_icon.setStyleSheet(f"font-size: 20px; color: {self.category_color};")
        top_row.addWidget(lbl_icon)

        lbl_time = QLabel(timestamp)
        lbl_time.setStyleSheet("color: #adb5bd; font-size: 11px; font-family: monospace;")
        top_row.addWidget(lbl_time)

        top_row.addStretch()
        layout.addLayout(top_row)

        self.lbl_human = QLabel(human_msg)
        self.lbl_human.setStyleSheet("font-weight: bold; font-size: 12px; color: #212529;")
        self.lbl_human.setWordWrap(True)
        self.lbl_human.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.lbl_human)

        layout.addStretch()

        action_layout = QHBoxLayout()
        action_layout.setSpacing(2)

        if snapshot_path:
            btn = QPushButton("📷")
            btn.setFixedSize(24, 20)
            btn.setToolTip("Apri Screenshot")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("background-color: #dc3545; color: white; border-radius: 3px; font-size: 10px;")
            btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(snapshot_path)))
            action_layout.addWidget(btn)

        if fixit_action == "ACCOUNT":
            btn = QPushButton("🔧")
            btn.setFixedSize(24, 20)
            btn.setToolTip("Configura Account")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("background-color: #ffc107; color: black; border-radius: 3px; font-size: 10px;")
            btn.clicked.connect(self._open_settings)
            action_layout.addWidget(btn)

        path_matches = re.findall(
            r'([a-zA-Z]:\[^ :<>|"\n]+|/(?:Users|home|tmp|var|usr|opt|app|data)/[^ :<>|"\n]+)',
            tech_msg,
        )
        seen = set()
        for path in path_matches:
            path = path.rstrip(".,';)]}").strip()
            if len(path) > 4 and "http" not in path and path not in seen:
                seen.add(path)
                btn = QPushButton("📂")
                btn.setFixedSize(24, 20)
                btn.setToolTip(f"Apri: {Path(path).name}")
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet("background-color: #17a2b8; color: white; border-radius: 3px; font-size: 10px;")
                btn.clicked.connect(lambda c, p=path: QDesktopServices.openUrl(QUrl.fromLocalFile(p)))
                action_layout.addWidget(btn)

        action_layout.addStretch()
        if action_layout.count() > 1:
            layout.addLayout(action_layout)

    def set_count(self, count):
        current_text = self.lbl_human.text()
        base = current_text.split(" (x")[0]
        self.lbl_human.setText(f"{base} (x{count})")

    def _open_settings(self):
        parent = self.window()
        if hasattr(parent, "show_settings"):
            parent.show_settings()


class HorizontalTimelineContainer(QWidget):
    """Container interno che disegna la linea di connessione."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 5, 10, 5)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setMinimumHeight(90)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        line_y = 20
        pen = QPen(QColor("#dee2e6"))
        pen.setWidth(2)
        painter.setPen(pen)

        if self.main_layout.count() > 0:
            first = self.main_layout.itemAt(0).widget()
            last = self.main_layout.itemAt(self.main_layout.count() - 1).widget()
            if first and last:
                start_x = first.geometry().center().x()
                end_x = last.geometry().center().x()
                painter.drawLine(start_x, line_y, end_x, line_y)


class HorizontalTimelineWidget(QScrollArea):
    """Widget Timeline Orizzontale con animazioni."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFixedHeight(110)
        self.setStyleSheet("border: none; background-color: transparent;")

        self.container = HorizontalTimelineContainer()
        self.setWidget(self.container)
        self.last_category = None
        self.consecutive_count = 0

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta != 0:
            scrollbar = self.horizontalScrollBar()
            scrollbar.setValue(scrollbar.value() - delta)
        else:
            super().wheelEvent(event)

    def add_widget(self, widget: QWidget):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        self.container.main_layout.addWidget(widget)

        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.start()

        QApplication.processEvents()
        self._smooth_scroll_to_end()
        self.container.update()

    def add_log(self, message: str):
        human, tech, cat = SmartLogTranslator.humanize(message)
        timestamp = datetime.now().strftime("%H:%M")

        if cat == self.last_category and cat in ["download", "search"]:
            self.consecutive_count += 1
            if self.container.main_layout.count() > 0:
                last_widget = self.container.main_layout.itemAt(
                    self.container.main_layout.count() - 1
                ).widget()
                if isinstance(last_widget, HorizontalLogItem):
                    last_widget.set_count(self.consecutive_count)
                    return
        else:
            self.consecutive_count = 1
            self.last_category = cat

        item = HorizontalLogItem(human, tech, cat, timestamp)
        self.add_widget(item)

    def _smooth_scroll_to_end(self):
        sb = self.horizontalScrollBar()
        start_val = sb.value()
        end_val = sb.maximum()

        self.scroll_anim = QPropertyAnimation(sb, b"value")
        self.scroll_anim.setDuration(400)
        self.scroll_anim.setStartValue(start_val)
        self.scroll_anim.setEndValue(end_val)
        self.scroll_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.scroll_anim.start()

    def clear(self):
        while self.container.main_layout.count():
            item = self.container.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.container.update()


class LogWidget(QWidget):
    """Widget per visualizzare i log (Horizontal Wrapper)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        header_layout = QHBoxLayout()
        label = QLabel("📋 Timeline Attività")
        label.setStyleSheet("font-weight: bold; font-size: 13px;")
        header_layout.addWidget(label)
        header_layout.addStretch()

        clear_btn = QPushButton("🧹 Pulisci Log")
        clear_btn.setMaximumWidth(120)
        clear_btn.setStyleSheet("QPushButton { background-color: #6c757d; color: white; border: none; border-radius: 4px; padding: 2px 8px; font-size: 11px; } QPushButton:hover { background-color: #5a6268; }")
        clear_btn.clicked.connect(self.clear)
        header_layout.addWidget(clear_btn)
        layout.addLayout(header_layout)

        self.timeline = HorizontalTimelineWidget()
        layout.addWidget(self.timeline)

    def append(self, message: str):
        self.timeline.add_log(message)

    def clear(self):
        self.timeline.clear()


class MissionReportCard(QFrame):
    """Card riepilogativa stile 'Mission Complete'."""

    def __init__(self, duration_str, status, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #e9ecef); border: 1px solid #dee2e6; border-radius: 8px; margin: 10px 5px; }")

        layout = QVBoxLayout(self)
        title_text = "🎉 Missione Compiuta!" if status else "⚠️ Missione Terminata"
        title_color = "#198754" if status else "#dc3545"
        lbl_title = QLabel(title_text)
        lbl_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {title_color};")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        stats_layout = QHBoxLayout()
        self._add_stat(stats_layout, "⏱️ Tempo", duration_str)
        self._add_stat(stats_layout, "📊 Esito", "Successo" if status else "Errore")
        layout.addLayout(stats_layout)

    def _add_stat(self, layout, label, value):
        container = QWidget()
        v_layout = QVBoxLayout(container)
        v_layout.setContentsMargins(0, 0, 0, 0)
        lbl_l = QLabel(label)
        lbl_l.setStyleSheet("font-size: 12px; color: #6c757d;")
        lbl_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_v = QLabel(value)
        lbl_v.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
        lbl_v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.addWidget(lbl_l)
        v_layout.addWidget(lbl_v)
        layout.addWidget(container)