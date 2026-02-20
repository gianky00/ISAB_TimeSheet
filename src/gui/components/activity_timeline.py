"""
Timeline Widget Professionale - Standard Cyber-Stepper V5 (Cyber-Rail Ultra).
Design d'élite con trasparenze reali, bordi neon e ombre portate.
"""

import time
from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtProperty, QPropertyAnimation, QEasingCurve, pyqtSlot, QRectF, QPointF, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QRadialGradient, QPainterPath, QLinearGradient

from src.bots.base.base_bot import StepStatus

class TimelineNode:
    def __init__(self, name: str):
        self.name = name
        self.status = StepStatus.PENDING
        self.start_time = 0.0
        self.duration_str = ""

class ActivityTimelineWidget(QWidget):
    def __init__(self, parent=None):
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
        
        # Palette Cyber-Rail
        self.COLORS = {
            "bg": QColor(10, 12, 18, 240),      # Sfondo scuro semi-trasparente
            "grid": QColor(0, 229, 255, 15),   # Griglia tattica
            "border": QColor("#00E5FF"),       # Bordo Neon
            StepStatus.PENDING: QColor("#263238"),
            StepStatus.RUNNING: QColor("#00E5FF"),
            StepStatus.COMPLETED: QColor("#00E676"),
            StepStatus.ERROR: QColor("#FF1744"),
            "line_dim": QColor(30, 33, 50, 100),
            "text_active": QColor("#FFFFFF"),
            "text_dim": QColor("#78909C"),
            "dash": QColor("#FFFFFF")
        }
        
        # Effetto Ombra per profondità
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
        self.setMinimumWidth(280)
        self.setMinimumHeight(400)

    def _setup_animations(self):
        self._pulse_anim.setDuration(1000)
        self._pulse_anim.setStartValue(0.4)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._pulse_anim.setLoopCount(-1)

    def _tick(self):
        self._rotation_angle = (self._rotation_angle + 3) % 360
        self._grid_offset = (self._grid_offset + 0.3) % 25.0
        self._dash_offset = (self._dash_offset + 0.01) % 1.0
        self.update()

    def get_pulse_value(self) -> float: return self._pulse_value
    def set_pulse_value(self, value: float):
        self._pulse_value = value
        self.update()

    pulse_value = pyqtProperty(float, fget=get_pulse_value, fset=set_pulse_value) # type: ignore

    def set_steps(self, steps: list[tuple[str, str]]):
        self.nodes = [TimelineNode(name) for _, name in steps]
        self.update()

    @pyqtSlot(int, str, object)
    def on_step_changed(self, index: int, name: str, status):
        # Supporta sia l'oggetto Enum che l'indice dell'Enum
        if isinstance(status, int):
            # Mapping inverso se arriva come int (PyQt signal compat)
            status = list(StepStatus)[status-1] if status > 0 else StepStatus.PENDING

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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 1. DISEGNO SFONDO ARROTONDATO (Cyber-Frame)
        rect = QRectF(10, 10, self.width()-20, self.height()-20)
        path = QPainterPath()
        path.addRoundedRect(rect, 15, 15)
        
        painter.save()
        painter.setClipPath(path)
        painter.fillRect(rect, self.COLORS["bg"])
        self._draw_grid(painter, rect)
        painter.restore()
        
        # Bordo Neon soft
        painter.setPen(QPen(self.COLORS["border"], 1.2))
        painter.drawPath(path)
        
        if not self.nodes:
            self._draw_empty(painter)
            return

        x_axis = 55
        y_start = 60
        spacing = 70

        # 2. DISEGNO CONNETTORI
        for i in range(len(self.nodes) - 1):
            self._draw_connector_v5(painter, x_axis, y_start + i*spacing, y_start + (i+1)*spacing, self.nodes[i], self.nodes[i+1])

        # 3. DISEGNO NODI
        for i, node in enumerate(self.nodes):
            self._draw_node_v5(painter, x_axis, y_start + i*spacing, node)

    def _draw_grid(self, painter, rect):
        painter.setPen(QPen(self.COLORS["grid"], 0.5))
        step = 25
        for x in range(int(rect.left()), int(rect.right() + step), step):
            painter.drawLine(int(x + self._grid_offset), int(rect.top()), int(x + self._grid_offset), int(rect.bottom()))
        for y in range(int(rect.top()), int(rect.bottom() + step), step):
            painter.drawLine(int(rect.left()), int(y + self._grid_offset), int(rect.right()), int(y + self._grid_offset))

    def _draw_connector_v5(self, painter, x, y1, y2, n1, n2):
        is_done = n1.status == StepStatus.COMPLETED and n2.status != StepStatus.PENDING
        color = self.COLORS[StepStatus.COMPLETED] if is_done else self.COLORS["line_dim"]
        
        painter.setPen(QPen(color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(int(x), int(y1), int(x), int(y2))
        
        if n1.status == StepStatus.RUNNING or (n1.status == StepStatus.COMPLETED and n2.status == StepStatus.PENDING):
            # Energy Dash
            dy = y1 + (y2-y1) * self._dash_offset
            painter.setBrush(self.COLORS["dash"])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(x-2, dy-2, 4, 4))

    def _draw_node_v5(self, painter, x, y, node):
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
            grad = QRadialGradient(QPointF(x, y), g+5)
            grad.setColorAt(0, QColor(color.red(), color.green(), color.blue(), 120))
            grad.setColorAt(1, Qt.GlobalColor.transparent)
            painter.setBrush(grad)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(x-g-5, y-g-5, (g+5)*2, (g+5)*2))
            
        # Core
        painter.setBrush(color)
        painter.setPen(QPen(Qt.GlobalColor.white, 1.5))
        r = 8 if node.status != StepStatus.PENDING else 5
        painter.drawEllipse(QRectF(x-r, y-r, r*2, r*2))
        
        # Testo
        is_active = node.status == StepStatus.RUNNING
        painter.setPen(self.COLORS["text_active"] if node.status != StepStatus.PENDING else self.COLORS["text_dim"])
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold if is_active else QFont.Weight.Normal))
        painter.drawText(int(x+30), int(y+5), node.name.upper())
        
        if is_active or node.duration_str:
            painter.setFont(QFont("Consolas", 8))
            msg = "> ACTIVE" if is_active else f"> {node.duration_str}"
            painter.drawText(int(x+30), int(y+18), msg)

    def _draw_empty(self, painter):
        painter.setPen(self.COLORS["text_dim"])
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "[ LINK OFFLINE ]")
