"""
Timeline Widget Professionale - Standard Cyber-Stepper V5 (Cyber-Rail Ultra).
Design d'élite con trasparenze reali, bordi neon e ombre portate.
"""

import time

from PyQt6.QtCore import (  # type: ignore[attr-defined]
    QEasingCurve,
    QPointF,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
    pyqtProperty,
    pyqtSlot,
)
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QRadialGradient
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QWidget

from src.bots.base.base_bot import StepStatus


class TimelineNode:
    """
    Rappresenta un singolo nodo all'interno della timeline delle attività.
    Mantiene lo stato, il tempo di inizio e la durata dell'operazione.
    """

    def __init__(self, name: str):
        """
        Inizializza un nuovo nodo.

        Args:
            name: Nome visualizzato dello step.
        """
        self.name = name
        self.status = StepStatus.PENDING
        self.start_time = 0.0
        self.duration_str = ""


class ActivityTimelineWidget(QWidget):
    """
    Widget grafico avanzato (Cyber-Stepper V5) per il monitoraggio dei bot.
    Visualizza una timeline verticale con animazioni neon, griglia tattica e flussi dati.
    """

    def __init__(self, parent=None):
        """
        Inizializza il widget e configura le animazioni e i colori.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.nodes: list[TimelineNode] = []

        # Abilita trasparenza per angoli smussati perfetti
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Animazioni
        self._pulse_value = 0.0
        self._rotation_angle = 0
        self._grid_offset = 0.0
        self._dash_offset = 0.0

        self._pulse_anim = QPropertyAnimation(self, b"pulse_value")
        self._setup_animations()

        # Timer per elementi dinamici
        self._ui_timer = QTimer(self)
        self._ui_timer.timeout.connect(self._tick)
        self._ui_timer.start(16)

        # Palette Cyber-Rail LIGHT MODE
        self.COLORS = {
            "bg": QColor(255, 255, 255, 250),  # Sfondo Bianco quasi opaco
            "grid": QColor(0, 0, 0, 10),  # Griglia scura molto soft
            "border": QColor("#212121"),  # Bordo Scuro Accent
            StepStatus.PENDING: QColor("#CFD8DC"),  # Grigio chiaro per attesa
            StepStatus.RUNNING: QColor("#212121"),  # Scuro per esecuzione
            StepStatus.COMPLETED: QColor("#00E676"),  # Green
            StepStatus.ERROR: QColor("#FF1744"),  # Red
            "line_dim": QColor(236, 239, 241),  # Linee di connessione chiare
            "text_active": QColor("#212121"),  # Testo scuro per contrasto
            "text_dim": QColor("#90A4AE"),  # Testo spento
            "dash": QColor("#212121"),  # Particelle scure
        }

        # Effetto Ombra più delicato per il tema light
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

        self.setMinimumWidth(280)
        self.setMinimumHeight(400)

    def _setup_animations(self):
        """Configura le animazioni di pulsazione per gli step attivi e per il bordo in hover."""
        self._pulse_anim.setDuration(1000)
        self._pulse_anim.setStartValue(0.4)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._pulse_anim.setLoopCount(-1)

        # Animazione specifica per il bordo (indipendente dagli step)
        self._border_pulse_val = 1.0
        self._border_pulse_anim = QPropertyAnimation(self, b"border_pulse")
        self._border_pulse_anim.setDuration(1500)
        self._border_pulse_anim.setStartValue(0.4)
        self._border_pulse_anim.setEndValue(1.0)
        self._border_pulse_anim.setLoopCount(-1)
        self._border_pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)

    def enterEvent(self, event):
        """
        Avvia la pulsazione del bordo al passaggio del mouse.

        Args:
            event: Evento di ingresso.
        """
        self._border_pulse_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        Ferma la pulsazione e ripristina il bordo solido.

        Args:
            event: Evento di uscita.
        """
        self._border_pulse_anim.stop()
        self.border_pulse = 1.0
        super().leaveEvent(event)

    def get_border_pulse(self) -> float:
        """Restituisce il valore corrente della pulsazione del bordo."""
        return self._border_pulse_val

    def set_border_pulse(self, value: float):
        """Imposta il valore della pulsazione del bordo e forza il ridisegno."""
        self._border_pulse_val = value
        self.update()

    border_pulse = pyqtProperty(float, fget=get_border_pulse, fset=set_border_pulse)

    def _tick(self):
        """Metodo di aggiornamento periodico per gli elementi dinamici (60 FPS)."""
        self._rotation_angle, self._grid_offset, self._dash_offset = (
            (self._rotation_angle + 3) % 360,
            (self._grid_offset + 0.3) % 25.0,
            (self._dash_offset + 0.01) % 1.0,
        )
        self.update()

    def get_pulse_value(self) -> float:
        """Restituisce il valore corrente della pulsazione neon."""
        return self._pulse_value

    def set_pulse_value(self, value: float):
        """Imposta il valore della pulsazione e forza il ridisegno."""
        self._pulse_value = value
        self.update()

    pulse_value = pyqtProperty(float, fget=get_pulse_value, fset=set_pulse_value)

    def set_steps(self, steps: list[tuple[str, str]]):
        """
        Inizializza la lista degli step da visualizzare.

        Args:
            steps: Lista di tuple (ID, Nome) degli step.
        """
        self.nodes = [TimelineNode(name) for _, name in steps]
        self.update()

    @pyqtSlot(int, str, object)
    def on_step_changed(self, index: int, name: str, status):
        """
        Slot chiamato quando lo stato di uno step del bot cambia.

        Args:
            index: Indice dello step.
            name: Nome dello step.
            status: Nuovo stato (StepStatus o int).
        """
        # Supporta sia l'oggetto Enum che l'indice dell'Enum
        if isinstance(status, int):
            # Mapping inverso se arriva come int (PyQt signal compat)
            status = list(StepStatus)[status - 1] if status > 0 else StepStatus.PENDING

        if 0 <= index < len(self.nodes):
            node = self.nodes[index]
            node.status = status

            if status == StepStatus.RUNNING:
                node.start_time = time.time()
                if self._pulse_anim.state() != QPropertyAnimation.State.Running:
                    self._pulse_anim.start()
            elif status in (StepStatus.COMPLETED, StepStatus.ERROR):
                if node.start_time > 0:
                    dur = time.time() - node.start_time
                    node.duration_str = f"{dur:.1f}s"

            if not any(n.status == StepStatus.RUNNING for n in self.nodes):
                self._pulse_anim.stop()
                self._pulse_value = 1.0
            self.update()

    def paintEvent(self, event):
        """
        Gestisce il disegno personalizzato del widget (Grid, Connectors, Nodes).

        Args:
            event: Evento di disegno.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. DISEGNO SFONDO ARROTONDATO (Cyber-Frame)
        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)
        path = QPainterPath()
        path.addRoundedRect(rect, 15, 15)

        painter.save()
        painter.setClipPath(path)
        painter.fillRect(rect, self.COLORS["bg"])
        self._draw_grid(painter, rect)
        painter.restore()

        # Bordo Neon soft (Con pulsazione in hover)
        alpha = int(100 + (self._border_pulse_val * 155))
        c = self.COLORS["border"]
        painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(), alpha), 1.2))
        painter.drawPath(path)

        if not self.nodes:
            self._draw_empty(painter)
            return

        # CALCOLO DINAMICO SPAZIATURA
        num_nodes = len(self.nodes)
        x_axis = 55

        # Margini interni alla card
        margin_y = 40
        available_h = rect.height() - (margin_y * 2)

        spacing = min(75, available_h / (num_nodes - 1)) if num_nodes > 1 else 0

        # Centra verticalmente se c'è spazio in eccesso
        total_timeline_h = (num_nodes - 1) * spacing
        y_start = rect.top() + (rect.height() - total_timeline_h) / 2

        # 2. DISEGNO CONNETTORI
        for i in range(len(self.nodes) - 1):
            self._draw_connector_v5(
                painter,
                x_axis,
                y_start + i * spacing,
                y_start + (i + 1) * spacing,
                self.nodes[i],
                self.nodes[i + 1],
            )

        # 3. DISEGNO NODI
        for i, node in enumerate(self.nodes):
            self._draw_node_v5(painter, x_axis, y_start + i * spacing, node, rect)

    def _draw_grid(self, painter, rect):
        """
        Disegna la griglia tattica animata sullo sfondo.

        Args:
            painter: Oggetto QPainter.
            rect: Rettangolo di disegno.
        """
        painter.setPen(QPen(self.COLORS["grid"], 0.5))
        step, left, top, right, bottom = (
            25,
            int(rect.left()),
            int(rect.top()),
            int(rect.right()),
            int(rect.bottom()),
        )

        for x in range(left, right + step, step):
            painter.drawLine(int(x + self._grid_offset), top, int(x + self._grid_offset), bottom)
        for y in range(top, bottom + step, step):
            painter.drawLine(left, int(y + self._grid_offset), right, int(y + self._grid_offset))

    def _draw_connector_v5(self, painter, x, y1, y2, n1, n2):
        """
        Disegna la linea di connessione tra due nodi con effetti di flusso dati.

        Args:
            painter: Oggetto QPainter.
            x: Coordinata X.
            y1: Coordinata Y di partenza.
            y2: Coordinata Y di arrivo.
            n1: Nodo di partenza.
            n2: Nodo di arrivo.
        """
        is_done = n1.status == StepStatus.COMPLETED and n2.status != StepStatus.PENDING
        color = self.COLORS[StepStatus.COMPLETED] if is_done else self.COLORS["line_dim"]

        painter.setPen(QPen(color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(int(x), int(y1), int(x), int(y2))

        if n1.status == StepStatus.RUNNING or (
            n1.status == StepStatus.COMPLETED and n2.status == StepStatus.PENDING
        ):
            # Energy Dash
            dy = y1 + (y2 - y1) * self._dash_offset
            painter.setBrush(self.COLORS["dash"])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(x - 2, dy - 2, 4, 4))

    def _draw_node_v5(self, painter, x, y, node, container_rect):
        """
        Disegna un singolo nodo della timeline con i relativi effetti di stato.

        Args:
            painter: Oggetto QPainter.
            x: Coordinata X del nodo.
            y: Coordinata Y del nodo.
            node: Oggetto TimelineNode da disegnare.
            container_rect: Rettangolo del contenitore per calcolare l'overflow del testo.
        """
        color = self.COLORS[node.status]

        if node.status == StepStatus.RUNNING:
            # Scanner Orbital
            painter.save()
            painter.translate(x, y)
            painter.rotate(self._rotation_angle)
            painter.setPen(QPen(color, 1.5, Qt.PenStyle.DashLine))
            painter.drawEllipse(QRectF(-16, -16, 32, 32))
            painter.restore()

            # Glow
            g = 12 * self._pulse_value
            grad = QRadialGradient(QPointF(x, y), g + 5)
            grad.setColorAt(0, QColor(color.red(), color.green(), color.blue(), 120))
            grad.setColorAt(1, Qt.GlobalColor.transparent)
            painter.setBrush(grad)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(x - g - 5, y - g - 5, (g + 5) * 2, (g + 5) * 2))

        # Core
        painter.setBrush(color)
        painter.setPen(QPen(Qt.GlobalColor.white, 1.5))
        r = 8 if node.status != StepStatus.PENDING else 5
        painter.drawEllipse(QRectF(x - r, y - r, r * 2, r * 2))

        # Testo
        is_active = node.status == StepStatus.RUNNING
        painter.setPen(
            self.COLORS["text_active"] if node.status != StepStatus.PENDING else self.COLORS["text_dim"]
        )

        font_main = QFont("Segoe UI", 9, QFont.Weight.DemiBold if is_active else QFont.Weight.Normal)
        painter.setFont(font_main)

        # Calcolo area testo per evitare overflow orizzontale
        text_x = int(x + 30)
        available_w = int(container_rect.right() - text_x - 10)

        from PyQt6.QtGui import QFontMetrics

        fm = QFontMetrics(font_main)
        display_name = fm.elidedText(node.name.upper(), Qt.TextElideMode.ElideRight, available_w)

        painter.drawText(text_x, int(y + 4), display_name)

        if is_active or node.duration_str:
            font_sub = QFont("Consolas", 8)
            painter.setFont(font_sub)
            msg = "> ACTIVE" if is_active else f"> {node.duration_str}"
            painter.drawText(text_x, int(y + 16), msg)

    def _draw_empty(self, painter):
        """
        Disegna lo stato vuoto del widget quando non ci sono step.

        Args:
            painter: Oggetto QPainter.
        """
        painter.setPen(self.COLORS["text_dim"])
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "[ LINK OFFLINE ]")
