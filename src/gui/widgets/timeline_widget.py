"""
SyncroJob - Timeline Widgets
Widget per la visualizzazione cronologica dei log e dei report di missione.
"""

import re
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import (
    QPropertyAnimation,
    Qt,
    QUrl,
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

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.log_humanizer import SmartLogTranslator


class HorizontalLogItem(QWidget):
    """Widget per singolo elemento della timeline log orizzontale."""

    def __init__(self, human_msg, tech_msg, category, timestamp, parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 150)
        self.setStyleSheet(
            "QWidget { background-color: white; border: 1px solid #dee2e6; border-radius: 8px; } QLabel { background-color: transparent; border: none; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # 1. Parse Metadata
        snap_path, fixit_act, tech_msg = self._parse_metadata(tech_msg)

        # 2. Header
        layout.addLayout(self._setup_header(category, timestamp))

        # 3. Content
        self.lbl_human = QLabel(human_msg)
        self.lbl_human.setStyleSheet("font-weight: bold; font-size: 13px; color: #212529;")
        self.lbl_human.setWordWrap(True)
        self.lbl_human.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.lbl_human)
        layout.addStretch()

        # 4. Actions
        self._setup_actions(layout, tech_msg, snap_path, fixit_act)

    def _parse_metadata(self, tech_msg: str) -> tuple[str | None, str | None, str]:
        snap, fixit = None, None
        if m := re.search(r"\[IMG:(.*?)\]", tech_msg):
            snap = m.group(1)
            tech_msg = tech_msg.replace(m.group(0), "").strip()
        if m := re.search(r"\[FIXIT:(.*?)\]", tech_msg):
            fixit = m.group(1)
            tech_msg = tech_msg.replace(m.group(0), "").strip()
        return snap, fixit, tech_msg

    def _setup_header(self, category: str, timestamp: str) -> QHBoxLayout:
        icons = {
            "start": Icons.ROCKET,
            "login": Icons.LOCK,
            "search": Icons.SEARCH,
            "download": Icons.DOWNLOAD,
            "success": Icons.CHECK_CIRCLE,
            "error": Icons.X_CIRCLE,
            "wait": Icons.CLOCK,
            "info": Icons.HELP,
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

        row = QHBoxLayout()
        row.setSpacing(5)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(
            get_colored_icon(get_asset_path(icons.get(category, Icons.HELP)), "#000000").pixmap(24, 24)
        )
        row.addWidget(icon_lbl)
        time_lbl = QLabel(timestamp)
        time_lbl.setStyleSheet("color: #adb5bd; font-size: 12px; font-family: monospace;")
        row.addWidget(time_lbl)
        row.addStretch()
        return row

    def _setup_actions(self, layout, tech_msg, snap_path, fixit_act):
        action_row = QHBoxLayout()
        action_row.setSpacing(5)
        if snap_path:
            btn = self._create_btn(Icons.EYE, "#dc3545", "Apri Screenshot")
            btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(snap_path)))
            action_row.addWidget(btn)
        if fixit_act == "ACCOUNT":
            btn = self._create_btn(Icons.SETTINGS, "#ffc107", "Configura Account", "black")
            btn.clicked.connect(self._open_settings)
            action_row.addWidget(btn)
        self._add_path_btns(action_row, tech_msg)
        action_row.addStretch()
        if action_row.count() > 1:
            layout.addLayout(action_row)

    def _create_btn(self, icon, bg, tip, fg="white"):
        btn = QPushButton()
        btn.setIcon(get_colored_icon(get_asset_path(icon), "#000000"))
        btn.setFixedSize(30, 24)
        btn.setToolTip(tip)
        btn.setStyleSheet(f"background-color: {bg}; color: {fg}; border-radius: 4px;")
        return btn

    def _add_path_btns(self, layout, msg):
        matches = re.findall(
            r'([a-zA-Z]:\[^ :<>|"\n]+|/(?:Users|home|tmp|var|usr|opt|app|data)/[^ :<>|"\n]+)',
            msg,
        )
        for p in set(matches):
            p = p.rstrip(".,';)]}").strip()
            if len(p) > 4 and "http" not in p:
                btn = self._create_btn(Icons.FOLDER_OPEN, "#17a2b8", f"Apri: {Path(p).name}")
                btn.clicked.connect(lambda c, path=p: QDesktopServices.openUrl(QUrl.fromLocalFile(path)))
                layout.addWidget(btn)

    def set_count(self, count):
        base = self.lbl_human.text().split(" (x")[0]
        self.lbl_human.setText(f"{base} (x{count})")

    def _open_settings(self):
        win = self.window()
        if hasattr(win, "show_settings"):
            win.show_settings()


class HorizontalTimelineContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 5, 10, 5)
        self.main_layout.setSpacing(10)
        self.main_layout.addStretch()
        self.setMinimumHeight(160)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor("#dee2e6"))
        pen.setWidth(2)
        painter.setPen(pen)
        widgets = [
            self.main_layout.itemAt(i).widget()
            for i in range(self.main_layout.count())
            if self.main_layout.itemAt(i).widget() and not self.main_layout.itemAt(i).widget().isHidden()
        ]
        if len(widgets) >= 2:
            start_x = widgets[0].geometry().center().x()
            end_x = widgets[-1].geometry().center().x()
            painter.drawLine(start_x, 30, end_x, 30)


class HorizontalTimelineWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFixedHeight(220)
        self.setStyleSheet("border: none; background-color: transparent;")
        self.container = HorizontalTimelineContainer()
        self.setWidget(self.container)
        self.last_category = None
        self.consecutive_count = 0

    def set_mood(self, _mood: str):
        """Imposta il mood della timeline (es. running, error, success)."""

    def add_widget(self, widget: QWidget):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        idx = self.container.main_layout.count() - 1
        self.container.main_layout.insertWidget(max(0, idx), widget)
        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
        QApplication.processEvents()
        self._scroll_to_end()

    def add_log(self, message: str):
        human, tech, cat = SmartLogTranslator.humanize(message)
        if cat == self.last_category and cat in ("download", "search"):
            self.consecutive_count += 1
            items = [
                self.container.main_layout.itemAt(i).widget()
                for i in range(self.container.main_layout.count())
                if isinstance(self.container.main_layout.itemAt(i).widget(), HorizontalLogItem)
            ]
            if items:
                items[-1].set_count(self.consecutive_count)
                return
        self.consecutive_count = 1
        self.last_category = cat
        self.add_widget(HorizontalLogItem(human, tech, cat, datetime.now().strftime("%H:%M")))

    def _scroll_to_end(self):
        sb = self.horizontalScrollBar()
        self.scroll_anim = QPropertyAnimation(sb, b"value")
        self.scroll_anim.setDuration(400)
        self.scroll_anim.setStartValue(sb.value())
        self.scroll_anim.setEndValue(sb.maximum())
        self.scroll_anim.start()

    def clear(self):
        while self.container.main_layout.count():
            item = self.container.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.container.main_layout.addStretch()


class TimelineWidget(QWidget):
    """
    Widget visualizing a vertical timeline of events.
    Each event supports title, description, timestamp, and metadata.
    """

    def __init__(self, parent=None):
        """Initialize the timeline widget."""
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        header = QHBoxLayout()
        header.addWidget(QLabel("<b>Timeline Attività</b>"))
        header.addStretch()
        btn = ModernButton(
            "Pulisci Log",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
        )
        btn.clicked.connect(self.clear)
        header.addWidget(btn)
        layout.addLayout(header)
        self.timeline = HorizontalTimelineWidget()
        layout.addWidget(self.timeline)

    def append(self, message: str):
        self.timeline.add_log(message)

    def clear(self):
        self.timeline.clear()


class MissionReportCard(QFrame):
    def __init__(self, duration_str, status, parent=None):
        super().__init__(parent)
        self.setFixedSize(260, 150)
        self.setStyleSheet(
            "QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #e9ecef); border: 1px solid #dee2e6; border-radius: 8px; margin: 10px 5px; }"
        )
        layout = QVBoxLayout(self)
        title = "Missione Compiuta!" if status else "Missione Terminata"
        lbl = QLabel(f"<b style='color:{'#198754' if status else '#dc3545'}; font-size:18px;'>{title}</b>")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
        stats = QHBoxLayout()
        for k, v in (
            ("Tempo", duration_str),
            ("Esito", "Successo" if status else "Errore"),
        ):
            cont = QWidget()
            vl = QVBoxLayout(cont)
            vl.addWidget(
                QLabel(
                    f"<span style='color:#6c757d;'>{k}</span>",
                    alignment=Qt.AlignmentFlag.AlignCenter,
                )
            )
            vl.addWidget(QLabel(f"<b>{v}</b>", alignment=Qt.AlignmentFlag.AlignCenter))
            stats.addWidget(cont)
        layout.addLayout(stats)
