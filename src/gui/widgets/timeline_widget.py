"""
SyncroJob - Cyber Log Console (V5 Edition)
Visualizzatore di log testuali verticali con estetica Cyber-Rail Ultra.
Combina la leggibilità della console classica con il design d'élite HUD.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from PyQt6.QtCore import (
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
    QFont,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
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
    """
    Singola riga di log testuale con timestamp e supporto per link ai file.
    Mantiene il nome originale per compatibilità con gli import globali.
    """
    def __init__(self, human_msg: str, tech_msg: str, category: str, timestamp: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(10)

        # Colori categoria (Neon) coordinati con ActivityTimeline
        colors = {
            "start": "#00E5FF",      # Cyan
            "login": "#CF94FF",      # Purple
            "search": "#FFAB40",     # Orange
            "download": "#40C4FF",   # Info
            "success": "#00E676",    # Green
            "error": "#FF1744",      # Red
            "wait": "#FFD600",       # Yellow
            "info": "#90A4AE"        # Gray
        }
        color = colors.get(category, "#B0BEC5")

        # Timestamp [HH:MM:SS]
        self.lbl_time = QLabel(f"[{timestamp}]")
        self.lbl_time.setStyleSheet("color: rgba(255, 255, 255, 0.3); font-family: 'Consolas'; font-size: 10px;")
        layout.addWidget(self.lbl_time)

        # Messaggio
        self.lbl_msg = QLabel(human_msg)
        self.lbl_msg.setWordWrap(True)
        self.lbl_msg.setStyleSheet(f"color: {color}; font-family: 'Segoe UI'; font-weight: 500; font-size: 11px;")
        layout.addWidget(self.lbl_msg, stretch=1)

        # Rilevamento percorsi per azione rapida
        self._add_actions(layout, tech_msg)

    def _add_actions(self, layout: QHBoxLayout, tech_msg: str):
        """Aggiunge pulsanti di apertura file se vengono rilevati percorsi nel log tecnico."""
        matches = re.findall(r'([a-zA-Z]:\\[^ :<>|"\n]+|/(?:Users|home|tmp|var|usr|opt|app|data)/[^ :<>|"\n]+)', tech_msg)
        for p in set(matches):
            p = p.rstrip(".,';)]}").strip()
            if len(p) > 4 and "http" not in p:
                btn = QPushButton()
                btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#00E5FF"))
                btn.setFixedSize(20, 20)
                btn.setToolTip(f"Apri: {Path(p).name}")
                btn.setStyleSheet("QPushButton { background: rgba(0, 229, 255, 0.1); border: none; border-radius: 3px; } QPushButton:hover { background: rgba(0, 229, 255, 0.3); }")
                btn.clicked.connect(lambda c, path=p: QDesktopServices.openUrl(QUrl.fromLocalFile(path)))
                layout.addWidget(btn)


class CyberTimelineFrame(QFrame):
    """
    Guscio estetico Cyber-Rail Ultra V5 per la console log.
    Disegna bordo neon, griglia e ombra.
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._pulse_value = 1.0
        self._grid_offset = 0.0
        
        # Ombra HUD pesante per profondità
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 220))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna lo sfondo, la griglia tattica e il bordo neon pulsante."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Rettangolo corretto per lasciare spazio all'ombra
        rect = QRectF(self.rect()).adjusted(10, 10, -10, -10)
        path = QPainterPath()
        path.addRoundedRect(rect, 15, 15)

        # 1. SFONDO DARK (Coordinato con ActivityTimeline)
        painter.fillPath(path, QColor(10, 12, 18, 245))

        # 2. GRIGLIA TATTICA ANIMATA
        painter.save()
        painter.setClipPath(path)
        painter.setPen(QPen(QColor(0, 229, 255, 12), 0.5))
        step = 25
        for x in range(int(rect.left()), int(rect.right() + step), step):
            painter.drawLine(int(x + self._grid_offset), int(rect.top()), int(x + self._grid_offset), int(rect.bottom()))
        for y in range(int(rect.top()), int(rect.bottom() + step), step):
            painter.drawLine(int(rect.left()), int(y + self._grid_offset), int(rect.right()), int(y + self._grid_offset))
        painter.restore()

        # 3. BORDO NEON PULSANTE (Cyan Elite)
        alpha = int(100 + (self._pulse_value * 155))
        painter.setPen(QPen(QColor(0, 229, 255, alpha), 1.5))
        painter.drawPath(path)


class HorizontalTimelineContainer(QWidget):
    """
    Contenitore trasparente per i log testuali.
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        self.log_layout = QVBoxLayout(self)
        self.log_layout.setContentsMargins(15, 10, 15, 10)
        self.log_layout.setSpacing(4)
        self.log_layout.addStretch()


class HorizontalTimelineWidget(QScrollArea):
    """
    Console di log a scorrimento verticale interna al frame Cyber.
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.viewport().setStyleSheet("background: transparent;")

        self.container = HorizontalTimelineContainer()
        self.setWidget(self.container)

    def add_log(self, message: str):
        """Aggiunge una riga di log in verticale con autoscroll."""
        human, tech, cat = SmartLogTranslator.humanize(message)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        item = HorizontalLogItem(human, tech, cat, timestamp)
        # Inserisci sopra lo stretch finale
        self.container.log_layout.insertWidget(self.container.log_layout.count() - 1, item)
        self._scroll_to_end()

    def _scroll_to_end(self):
        """Esegue lo scroll fluido verso il basso."""
        sb = self.verticalScrollBar()
        if sb:
            sb.setValue(sb.maximum())

    def clear(self):
        """Rimuove tutti i log dalla console."""
        while self.container.log_layout.count() > 1:
            item = self.container.log_layout.takeAt(0)
            if item and (w := item.widget()):
                w.deleteLater()

    def set_mood(self, mood: str):
        """Proxy per il mood del parent."""
        if hasattr(self.parent(), "set_mood"):
            self.parent().set_mood(mood)


class TimelineWidget(QWidget):
    """
    Widget Log Attività principale (Versione Orrizzontale HUD).
    Implementa l'estetica Cyber-Rail Ultra V5 con log testuali verticali.
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(220)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Header HUD
        header = QHBoxLayout()
        header.setContentsMargins(15, 0, 15, 0)
        lbl = QLabel("MISSION LOG STREAM")
        lbl.setStyleSheet("font-weight: 900; color: #607D8B; letter-spacing: 2px; font-size: 9px;")
        header.addWidget(lbl)
        header.addStretch()
        
        btn = ModernButton("PURGE", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL, icon=get_asset_path(Icons.TRASH))
        btn.clicked.connect(self.clear)
        header.addWidget(btn)
        layout.addLayout(header)

        # Cyber Frame (Il guscio estetico)
        self.frame = CyberTimelineFrame()
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(12, 12, 12, 12)

        # La console reale
        self.timeline = HorizontalTimelineWidget(self)
        self.frame_layout.addWidget(self.timeline)
        layout.addWidget(self.frame)

        # Timer Animazioni (Griglia e Battito)
        self._pulse_val = 1.0
        self._grid_off = 0.0
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._update_anim)
        self.anim_timer.start(16) # 60 FPS

        self.pulse_anim = QPropertyAnimation(self, b"pulse_value")
        self.pulse_anim.setDuration(1500)
        self.pulse_anim.setStartValue(0.4)
        self.pulse_anim.setEndValue(1.0)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_anim.start()

    @pyqtProperty(float)
    def pulse_value(self) -> float: 
        """Restituisce il valore di pulsazione neon."""
        return self._pulse_val
        
    @pulse_value.setter  # type: ignore
    def pulse_value(self, v: float):
        """Aggiorna il bordo neon."""
        self._pulse_val = v
        self.frame._pulse_value = v
        self.frame.update()

    def _update_anim(self):
        """Muove la griglia tattica."""
        self._grid_off = (self._grid_off + 0.3) % 25.0
        self.frame._grid_offset = self._grid_off
        self.frame.update()

    def append(self, msg: str, level: str = "INFO"): 
        """Aggiunge un messaggio al feed log."""
        self.timeline.add_log(msg)
        
    def clear(self): 
        """Pulisce la console."""
        self.timeline.clear()
        
    def set_mood(self, mood: str):
        """Regola l'intensità in base allo stato del bot."""
        if mood == "running": 
            self.pulse_anim.setDuration(800)
        else: 
            self.pulse_anim.setDuration(1500)

class MissionReportCard(QFrame):
    """Placeholder per compatibilità (non mostrata nel flusso testuale)."""
    def __init__(self, dur: str, status: bool, parent=None):
        super().__init__(parent)
        self.hide()
