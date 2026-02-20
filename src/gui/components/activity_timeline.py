"""
Timeline Widget Professionale - Standard Cyber-Stepper V2.
Design ultra-moderno con sfondi integrati, neon glow e animazioni fluide.
"""

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QRectF, Qt, pyqtProperty, pyqtSlot
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QRadialGradient
from PyQt6.QtWidgets import QWidget

from src.bots.base.base_bot import StepStatus


class TimelineNode:
    def __init__(self, name: str):
        self.name = name
        self.status = StepStatus.PENDING

class ActivityTimelineWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nodes: list[TimelineNode] = []
        self._pulse_value = 0.0
        self._pulse_anim = QPropertyAnimation(self, b"pulse_value")
        self._setup_animation()

        # Palette Cyber-Tech V2 (High Contrast)
        self.COLORS = {
            "bg": QColor("#0F111A"),           # Sfondo scuro profondo
            StepStatus.PENDING: QColor("#37474F"),    # Grigio bluastro
            StepStatus.RUNNING: QColor("#00E5FF"),    # Cyan Neon
            StepStatus.COMPLETED: QColor("#00E676"),  # Emerald Neon
            StepStatus.ERROR: QColor("#FF1744"),      # Rosso vivido
            "line": QColor("#1E2132"),         # Linea binario
            "text_active": QColor("#FFFFFF"),
            "text_dim": QColor("#90A4AE")
        }

        self.setMinimumWidth(260)
        self.setMinimumHeight(300)

    def _setup_animation(self):
        self._pulse_anim.setDuration(1000)
        self._pulse_anim.setStartValue(0.4)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._pulse_anim.setLoopCount(-1)

    def get_pulse_value(self) -> float: return self._pulse_value
    def set_pulse_value(self, value: float):
        self._pulse_value = value
        self.update()

    pulse_value = pyqtProperty(float, fget=get_pulse_value, fset=set_pulse_value) # type: ignore

    def set_steps(self, steps: list[tuple[str, str]]):
        """Popola la timeline con gli step del bot."""
        self.nodes = [TimelineNode(name) for _, name in steps]
        self.update()

    @pyqtSlot(int, str, object)
    def on_step_changed(self, index: int, name: str, status: StepStatus):
        if 0 <= index < len(self.nodes):
            self.nodes[index].status = status
            if any(n.status == StepStatus.RUNNING for n in self.nodes):
                if self._pulse_anim.state() != QPropertyAnimation.State.Running:
                    self._pulse_anim.start()
            else:
                self._pulse_anim.stop()
                self._pulse_value = 1.0
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 0. Sfondo del Widget (Cyber Panel)
        rect = QRectF(0, 0, self.width(), self.height())
        path = QPainterPath()
        path.addRoundedRect(rect, 8, 8)
        painter.fillPath(path, self.COLORS["bg"])

        if not self.nodes:
            self._draw_empty_state(painter)
            return

        x_axis = 45
        y_start = 50
        spacing = 60

        # 1. Disegna il Binario (Linea di collegamento)
        pen = QPen(self.COLORS["line"], 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(x_axis, y_start, x_axis, y_start + (len(self.nodes) - 1) * spacing)

        # 2. Disegna gli Step
        for i, node in enumerate(self.nodes):
            y = y_start + i * spacing
            self._draw_node(painter, x_axis, y, node)
            self._draw_text(painter, x_axis + 30, y, node)

    def _draw_node(self, painter, x, y, node):
        color = self.COLORS[node.status]

        if node.status == StepStatus.RUNNING:
            # Effetto GLOW pulsante
            glow_size = 15 * self._pulse_value
            grad = QRadialGradient(QPointF(x, y), glow_size)
            grad.setColorAt(0, QColor(color.red(), color.green(), color.blue(), int(180 * self._pulse_value)))
            grad.setColorAt(1, Qt.GlobalColor.transparent)
            painter.setBrush(grad)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(x - glow_size, y - glow_size, glow_size * 2, glow_size * 2))

            # Centro Neon
            painter.setBrush(color)
            painter.setPen(QPen(Qt.GlobalColor.white, 2))
            painter.drawEllipse(QRectF(x - 7, y - 7, 14, 14))

        elif node.status == StepStatus.COMPLETED:
            # Cerchio solido con spunta
            painter.setBrush(color)
            painter.setPen(QPen(Qt.GlobalColor.white, 1))
            painter.drawEllipse(QRectF(x - 10, y - 10, 20, 20))
            painter.setPen(QPen(Qt.GlobalColor.white, 2))
            painter.drawLine(int(x-4), int(y), int(x-1), int(y+4))
            painter.drawLine(int(x-1), int(y+4), int(x+5), int(y-3))

        elif node.status == StepStatus.ERROR:
            painter.setBrush(self.COLORS[StepStatus.ERROR])
            painter.setPen(QPen(Qt.GlobalColor.white, 2))
            painter.drawEllipse(QRectF(x - 10, y - 10, 20, 20))
            painter.drawText(QRectF(x-10, y-10, 20, 20), Qt.AlignmentFlag.AlignCenter, "!")

        else: # PENDING
            painter.setBrush(self.COLORS[StepStatus.PENDING])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(x - 6, y - 6, 12, 12))

    def _draw_text(self, painter, x, y, node):
        is_active = node.status in (StepStatus.RUNNING, StepStatus.COMPLETED)
        painter.setPen(self.COLORS["text_active"] if is_active else self.COLORS["text_dim"])

        font = QFont("Segoe UI", 10)
        font.setBold(is_active)
        painter.setFont(font)

        # Testo con leggera ombra se attivo
        if is_active:
            painter.setPen(QColor(0, 0, 0, 150))
            painter.drawText(int(x+1), int(y + 6), node.name)
            painter.setPen(self.COLORS["text_active"])

        painter.drawText(int(x), int(y + 5), node.name)

    def _draw_empty_state(self, painter):
        painter.setPen(self.COLORS["text_dim"])
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Light))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Timeline non inizializzata")
