"""
SyncroJob - Cyber Log Console (V5 Edition)
Visualizzatore di log testuali verticali con estetica Cyber-Rail Ultra.
Combina la leggibilità della console classica con il design d'élite HUD.
"""

import re
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import (  # type: ignore[attr-defined]
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
    QUrl,
    pyqtProperty,
)
from PyQt6.QtGui import (
    QColor,
    QDesktopServices,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
)
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.log_humanizer import SmartLogTranslator


class HorizontalLogItem(QWidget):
    """
    Singola riga di log testuale con timestamp e supporto per link ai file.
    """

    def __init__(self, human_msg: str, tech_msg: str, category: str, timestamp: str, parent=None):
        super().__init__(parent)
        self.human_msg = human_msg
        self.tech_msg = tech_msg
        self.timestamp = timestamp
        self.category = category
        self.braille_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.frame_idx = 0

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(10)

        # Colori categoria
        color = {
            "start": "#212121",
            "login": "#212121",
            "search": "#212121",
            "download": "#212121",
            "success": "#2E7D32",  # Verde più scuro per successo
            "error": "#C62828",
            "wait": "#EF6C00",
            "action": "#00796B",  # Teal per azioni
            "info": "#212121",
        }.get(category, "#212121")

        # Timestamp [HH:MM:SS]
        self.lbl_time = QLabel(f"[{timestamp}]")
        self.lbl_time.setStyleSheet("color: #90A4AE; font-family: 'Consolas'; font-size: 11px;")
        self.lbl_time.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.lbl_time)

        # Animazione Braille per attese
        if category == "wait":
            self.lbl_spinner = QLabel(self.braille_frames[0])
            self.lbl_spinner.setStyleSheet(
                f"color: {color}; font-family: 'Consolas'; font-weight: bold; font-size: 14px;"
            )
            layout.addWidget(self.lbl_spinner)

            self.timer = QTimer(self)
            self.timer.timeout.connect(self._update_spinner)
            self.timer.start(100)

        # Messaggio
        self.lbl_msg = QLabel(human_msg)
        self.lbl_msg.setWordWrap(True)
        self.lbl_msg.setStyleSheet(
            f"color: {color}; font-family: 'Segoe UI'; font-weight: 500; font-size: 13px;"
        )
        self.lbl_msg.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.lbl_msg, stretch=1)

        # Azioni rapide (cartelle)
        self._add_actions(layout, tech_msg)

    def _update_spinner(self):
        """Aggiorna il frame dell'animazione braille."""
        self.frame_idx = (self.frame_idx + 1) % len(self.braille_frames)
        self.lbl_spinner.setText(self.braille_frames[self.frame_idx])

    def stop_spinner(self):
        """Ferma l'animazione e nasconde lo spinner."""
        if hasattr(self, "timer") and self.timer.isActive():
            self.timer.stop()
        if hasattr(self, "lbl_spinner"):
            self.lbl_spinner.hide()

    def _add_actions(self, layout: QHBoxLayout, tech_msg: str):
        matches = re.findall(
            r'([a-zA-Z]:\\[^ :<>|"\n]+|/(?:Users|home|tmp|var|usr|opt|app|data)/[^ :<>|"\n]+)', tech_msg
        )
        for p in set(matches):
            p = p.rstrip(".,';)]}").strip()
            if len(p) > 4 and "http" not in p:
                btn = QPushButton()
                btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#212121"))
                btn.setFixedSize(22, 22)
                btn.setToolTip(f"Apri: {Path(p).name}")
                btn.setStyleSheet(
                    "QPushButton { background: rgba(33, 33, 33, 0.05); border: none; border-radius: 3px; } QPushButton:hover { background: rgba(33, 33, 33, 0.1); }"
                )
                btn.clicked.connect(lambda c, path=p: QDesktopServices.openUrl(QUrl.fromLocalFile(path)))
                layout.addWidget(btn)


class CyberTimelineFrame(QFrame):
    """Guscio estetico HUD."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._pulse_value = 1.0
        self._grid_offset = 0.0
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(10, 10, -10, -10)
        path = QPainterPath()
        path.addRoundedRect(rect, 15, 15)
        painter.fillPath(path, QColor(255, 255, 255, 250))
        painter.save()
        painter.setClipPath(path)
        painter.setPen(QPen(QColor(0, 0, 0, 10), 0.5))
        step = 25
        for x in range(int(rect.left()), int(rect.right() + step), step):
            painter.drawLine(
                int(x + self._grid_offset), int(rect.top()), int(x + self._grid_offset), int(rect.bottom())
            )
        for y in range(int(rect.top()), int(rect.bottom() + step), step):
            painter.drawLine(
                int(rect.left()), int(y + self._grid_offset), int(rect.right()), int(y + self._grid_offset)
            )
        painter.restore()
        alpha = int(100 + (self._pulse_value * 155))
        painter.setPen(QPen(QColor(33, 33, 33, alpha), 1.5))
        painter.drawPath(path)


class HorizontalTimelineContainer(QWidget):
    """Contenitore trasparente per i log testuali (per compatibilità)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        self.log_layout = QVBoxLayout(self)


class HorizontalTimelineWidget(QListWidget):
    """Console log multi-selezione."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setUniformItemSizes(False)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setStyleSheet("""
            QListWidget { background: transparent; border: none; outline: none; }
            QListWidget::item { border-bottom: 1px solid rgba(0,0,0,0.03); }
            QListWidget::item:selected { background: rgba(0, 150, 136, 0.1); border-left: 3px solid #009688; color: black; }
        """)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def add_log(self, message: str):
        # Ferma tutti gli spinner precedenti prima di aggiungere un nuovo log
        for i in range(self.count()):
            item = self.item(i)
            w = self.itemWidget(item)
            if isinstance(w, HorizontalLogItem):
                w.stop_spinner()

        human, tech, cat = SmartLogTranslator.humanize(message)
        timestamp = datetime.now().strftime("%H:%M:%S")
        list_item = QListWidgetItem(self)
        item_widget = HorizontalLogItem(human, tech, cat, timestamp)
        list_item.setSizeHint(item_widget.sizeHint())
        self.addItem(list_item)
        self.setItemWidget(list_item, item_widget)
        self.scrollToBottom()

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        # Forza sfondo bianco e testo nero per il menu
        menu.setStyleSheet("""
            QMenu {
                background-color: #FFFFFF;
                color: #212121;
                border: 1px solid #CCCCCC;
                font-family: 'Segoe UI';
                font-size: 13px;
            }
            QMenu::item {
                padding: 6px 25px 6px 20px;
            }
            QMenu::item:selected {
                background-color: #E0F2F1;
                color: #000000;
            }
        """)

        selected = self.selectedItems()
        if selected:
            action_copy = menu.addAction("Copia Selezione")
            if action_copy:
                action_copy.triggered.connect(self._copy_selection)

        action_select_all = menu.addAction("Seleziona Tutto")
        if action_select_all:
            action_select_all.triggered.connect(self.selectAll)

        action_copy_all = menu.addAction("Copia Tutto")
        if action_copy_all:
            action_copy_all.triggered.connect(self._copy_all)

        menu.exec(self.mapToGlobal(pos))

    def _copy_selection(self):
        """Copia le righe selezionate (quello che vede l'utente)."""
        lines = []
        # Ordiniamo per riga per mantenere la sequenza temporale corretta
        selected_rows = sorted([self.row(item) for item in self.selectedItems()])
        for row in selected_rows:
            w = self.itemWidget(self.item(row))
            if isinstance(w, HorizontalLogItem):
                lines.append(f"[{w.timestamp}] {w.human_msg}")
        if lines:
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText("\n".join(lines))

    def _copy_all(self):
        """Copia l'intero log (quello che vede l'utente)."""
        lines = []
        for i in range(self.count()):
            w = self.itemWidget(self.item(i))
            if isinstance(w, HorizontalLogItem):
                lines.append(f"[{w.timestamp}] {w.human_msg}")
        if lines:
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText("\n".join(lines))

    def _copy_text(self, text):
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(text)

    def keyPressEvent(self, event):
        """Gestisce scorciatoie Ctrl+C (copia) e Ctrl+A (seleziona tutto)."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_C:
                self._copy_selection()
                return
            if event.key() == Qt.Key.Key_A:
                self.selectAll()
                return
        super().keyPressEvent(event)


class TimelineWidget(QWidget):
    """Widget Log Principale."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(220)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        header = QHBoxLayout()
        header.setContentsMargins(15, 0, 15, 0)
        lbl = QLabel("MISSION LOG STREAM")
        lbl.setStyleSheet("font-weight: 900; color: #607D8B; letter-spacing: 2px; font-size: 9px;")
        header.addWidget(lbl)
        header.addStretch()
        btn = ModernButton(
            "PULISCI LOG",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
        )
        btn.clicked.connect(self.clear)
        header.addWidget(btn)
        layout.addLayout(header)
        self.frame = CyberTimelineFrame()
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(12, 12, 12, 12)
        self.timeline = HorizontalTimelineWidget(self)
        self.frame_layout.addWidget(self.timeline)
        layout.addWidget(self.frame)
        self._pulse_val = 1.0
        self._grid_off = 0.0
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._update_anim)
        self.anim_timer.start(16)
        self.pulse_anim = QPropertyAnimation(self, b"pulse_value")
        self.pulse_anim.setDuration(1500)
        self.pulse_anim.setStartValue(0.4)
        self.pulse_anim.setEndValue(1.0)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)

    def enterEvent(self, event):
        self.pulse_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.pulse_anim.stop()
        self._set_pulse_value(1.0)
        super().leaveEvent(event)

    def _get_pulse_value(self) -> float:
        return self._pulse_val

    def _set_pulse_value(self, v: float):
        self._pulse_val = v
        self.frame._pulse_value = v
        self.frame.update()

    pulse_value = pyqtProperty(float, _get_pulse_value, _set_pulse_value)

    def _update_anim(self):
        self._grid_off = (self._grid_off + 0.3) % 25.0
        self.frame._grid_offset = self._grid_off
        self.frame.update()

    def append(self, msg: str, level: str = "INFO"):
        self.timeline.add_log(msg)

    def clear(self):
        self.timeline.clear()

    def set_mood(self, mood: str):
        if mood == "running":
            self.pulse_anim.setDuration(800)
        else:
            self.pulse_anim.setDuration(1500)


class MissionReportCard(QFrame):
    def __init__(self, dur: str, status: bool, parent=None):
        super().__init__(parent)
        self.hide()
