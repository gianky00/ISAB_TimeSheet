"""
SyncroJob - Cyber Log Console (V5 Edition)
Visualizzatore di log testuali verticali con estetica Cyber-Rail Ultra.
Combina la leggibilità della console classica con il design d'élite HUD.
"""

import re

from PyQt6.QtCore import (  # type: ignore[attr-defined]
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    QTimer,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
)
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS


class CyberTimelineFrame(QFrame):
    """
    Frame decorativo per la timeline dei log con griglia HUD e animazione pulse.
    Crea un'atmosfera tecnologica e professionale per lo stream dei log.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il frame cibernetico.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._pulse_value = 1.0
        self._grid_offset = 0.0

        # Animazione Pulse Bordo
        self.pulse_anim = QPropertyAnimation(self, b"pulse_value")
        self.pulse_anim.setDuration(1500)
        self.pulse_anim.setStartValue(0.6)
        self.pulse_anim.setEndValue(1.0)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_anim.start()

        # Timer per scorrimento griglia
        self.grid_timer = QTimer(self)
        self.grid_timer.timeout.connect(self._update_grid)
        self.grid_timer.start(50)

    def get_pulse_value(self) -> float:
        """Restituisce il valore corrente della pulsazione del bordo."""
        return self._pulse_value

    def set_pulse_value(self, v: float) -> None:
        """Imposta il valore della pulsazione e aggiorna il widget."""
        self._pulse_value = v
        self.update()

    # Proprietà per l'animazione QPropertyAnimation
    pulse_value = pyqtProperty(float, fget=get_pulse_value, fset=set_pulse_value)

    def _update_grid(self) -> None:
        """Sposta leggermente la griglia di sfondo per un effetto dinamico."""
        self._grid_offset = (self._grid_offset + 0.5) % 25
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """
        Disegna la card HUD con griglia animata e bordo pulsante.

        Args:
            event: Evento di pittura.
        """
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            rect = QRectF(self.rect()).adjusted(10, 10, -10, -10)
            path = QPainterPath()
            path.addRoundedRect(rect, 15, 15)
            painter.fillPath(path, QColor(COLORS["bg_white"]))

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
            c = QColor(COLORS["text_dark"])
            painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(), alpha), 1.5))
            painter.drawPath(path)
        finally:
            painter.end()


class LogEntryWidget(QWidget):
    """
    Singola riga di log formattata con timestamp e icone dinamiche.
    Utilizza regex per identificare e colorare i livelli di log.
    """

    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        """
        Crea un widget per una voce di log.

        Args:
            text: Testo grezzo del log.
            parent: Widget genitore.
        """
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)

        # Analisi Log (Regex per catturare Timestamp, Livello, Messaggio)
        pattern = r"\[(.*?)\]\s+(INFO|WARNING|ERROR|DEBUG|CRITICAL)\s+-\s+(.*?)\s+-\s+(.*)"
        match = re.search(pattern, text)

        color = COLORS["text_muted"]  # Default
        icon = "●"

        if match:
            level = match.group(2)
            msg = match.group(4)
            time_str = match.group(1).split()[-1]  # Solo l'ora

            if level == "INFO":
                color = COLORS["teal_accent"]
                icon = "ℹ"
            elif level == "WARNING":
                color = COLORS["warning_orange"]
                icon = "⚠"
            elif level in ("ERROR", "CRITICAL"):
                color = COLORS["error_red"]
                icon = "✖"
            elif level == "DEBUG":
                color = COLORS["purple"]
                icon = "⚙"

            self.lbl_time = QLabel(time_str)
            self.lbl_time.setStyleSheet(
                f"color: {COLORS['text_light']}; font-weight: bold; font-family: monospace;"
            )
            layout.addWidget(self.lbl_time)

            self.lbl_icon = QLabel(icon)
            self.lbl_icon.setStyleSheet(f"color: {color}; font-weight: 900; font-size: 14px;")
            layout.addWidget(self.lbl_icon)

            self.lbl_msg = QLabel(msg)
            self.lbl_msg.setWordWrap(True)
            self.lbl_msg.setStyleSheet(f"color: {COLORS['text_dark']}; font-weight: 500;")
            layout.addWidget(self.lbl_msg, 1)
        else:
            # Fallback per messaggi non standard
            self.lbl_msg = QLabel(text)
            self.lbl_msg.setWordWrap(True)
            self.lbl_msg.setStyleSheet(f"color: {COLORS['text_muted']}; font-family: monospace;")
            layout.addWidget(self.lbl_msg, 1)


class CyberLogConsole(QWidget):
    """
    Console di log avanzata con autoscroll e design Cyber-Rail.
    """

    log_added = pyqtSignal(str)
    """Segnale emesso quando un nuovo log viene aggiunto alla vista."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza la console di log.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura l'architettura della console con scroll area e frame Cyber."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame = CyberTimelineFrame()
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(25, 25, 25, 25)

        self.scroll_container = QScrollArea()
        self.scroll_container.setWidgetResizable(True)
        self.scroll_container.setStyleSheet("background: transparent; border: none;")

        self.content = QWidget()
        self.content.setStyleSheet("background: transparent;")
        self.log_layout = QVBoxLayout(self.content)
        self.log_layout.setContentsMargins(0, 0, 0, 0)
        self.log_layout.setSpacing(5)
        self.log_layout.addStretch()

        self.scroll_container.setWidget(self.content)
        self.frame_layout.addWidget(self.scroll_container)
        layout.addWidget(self.frame)

    def add_log(self, text: str) -> None:
        """
        Aggiunge una nuova voce di log alla console.

        Args:
            text: Il testo del log da visualizzare.
        """
        entry = LogEntryWidget(text)
        self.log_layout.insertWidget(self.log_layout.count() - 1, entry)

        # Autoscroll
        bar = self.scroll_container.verticalScrollBar()
        if bar:
            QTimer.singleShot(10, lambda: bar.setValue(bar.maximum()))
        self.log_added.emit(text)

    def append(self, text: str, status: str = "") -> None:
        """Metodo di compatibilità per il vecchio TimelineWidget."""
        self.add_log(text)

    def clear(self) -> None:
        """Svuota completamente la console dei log."""
        while self.log_layout.count() > 1:
            item = self.log_layout.takeAt(0)
            if item and (widget := item.widget()):
                widget.deleteLater()

    def set_mood(self, mood: str) -> None:
        """Imposta il mood visivo (es. running, idle)."""
        if mood == "running":
            self.frame.pulse_anim.setDuration(800)
        else:
            self.frame.pulse_anim.setDuration(1500)


class TimelineWidget(CyberLogConsole):
    """Alias per compatibilità con il vecchio sistema di logging."""


class MissionReportCard(QFrame):
    """Versione legacy mantenuta per compatibilità di export."""
    def __init__(self, dur: str, status: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.hide()


class HorizontalLogItem(QWidget):
    """Versione legacy mantenuta per compatibilità di export."""
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)


class HorizontalTimelineWidget(QWidget):
    """Versione legacy mantenuta per compatibilità di export."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)


class HorizontalTimelineContainer(QFrame):
    """Versione legacy mantenuta per compatibilità di export."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
