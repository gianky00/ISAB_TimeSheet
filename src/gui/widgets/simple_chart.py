from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS


class DonutChart(QWidget):
    """
    Grafico a ciambella leggero disegnato con QPainter.
    """

    def __init__(self, title: str = "Success Rate", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.title = title
        self.values = [0, 0]  # [Success, Error]
        self.colors = [QColor(COLORS["success_dark"]), QColor(COLORS["error_red"])]
        self.setMinimumSize(200, 200)

    def set_data(self, success_count: int, error_count: int) -> None:
        """
        Imposta i nuovi dati di successo/errore e aggiorna il grafico.

        Args:
          success_count: Numero di successi.
          error_count: Numero di errori.
        """
        self.values = [success_count, error_count]
        self.update()  # Trigger repaint

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna il grafico a ciambella basato sui dati correnti."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        width = rect.width()
        height = rect.height()

        # Center coordinates
        center_x = width / 2.0
        center_y = height / 2.0 + 10.0  # Offset for title

        size = min(width, height) * 0.7
        rect_f = QRectF(center_x - size / 2.0, center_y - size / 2.0, size, size)

        total = sum(self.values)
        if total == 0:
            # Draw empty grey circle
            pen = QPen(QColor(COLORS["bg_hover"]))
            pen.setWidth(15)
            painter.setPen(pen)
            painter.drawEllipse(rect_f)

            # Text 0%
            painter.setPen(QColor(COLORS["text_light"]))
            painter.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
            painter.drawText(rect_f, Qt.AlignmentFlag.AlignCenter, "N/A")
            painter.end()
            return

        start_angle = 90 * 16  # Start at 12 òclock, units in 1/16th of degree

        # Draw segments
        current_angle = float(start_angle)
        for i, val in enumerate(self.values):
            if val == 0:
                continue

            span_angle = -(val / total) * 360.0 * 16.0

            pen = QPen(self.colors[i])
            pen.setWidth(15)
            pen.setCapStyle(Qt.PenCapStyle.FlatCap)
            painter.setPen(pen)

            painter.drawArc(rect_f, int(current_angle), int(span_angle))
            current_angle += span_angle

        # Draw Center Text (Percentage)
        success_rate = int((self.values[0] / total) * 100)
        painter.setPen(QColor(COLORS["text_dark"]))
        painter.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        painter.drawText(rect_f, Qt.AlignmentFlag.AlignCenter, f"{success_rate}%")

        # Draw Subtext
        sub_rect = QRectF(rect_f)
        sub_rect.moveTop(rect_f.top() + 40.0)
        painter.setPen(QColor(COLORS["text_muted"]))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(sub_rect, Qt.AlignmentFlag.AlignCenter, "Successo")
        painter.end()

        # Draw Legend below
        # (Simplified: just relying on colors matching existing UI semantics)


class StatCard(QWidget):
    """Container per il grafico con titolo."""

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl = QLabel(title)
        lbl.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['text_dark']};")
        layout.addWidget(lbl)

        self.chart = DonutChart()
        layout.addWidget(self.chart)
