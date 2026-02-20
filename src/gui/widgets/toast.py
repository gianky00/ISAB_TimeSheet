"""
SyncroJob - Toast Notifications
Widget per la visualizzazione di notifiche a scomparsa stile Android/Material.
"""

from PyQt6.QtCore import QPropertyAnimation, QRectF, Qt, QTimer, pyqtProperty
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class Toast(QWidget):
    """
    Singola notifica toast animata.
    Supporta diversi livelli di severità (info, success, warning, error).
    """

    def __init__(self, message: str, level: str = "info", parent: QWidget | None = None) -> None:
        """
        Inizializza la notifica toast.

        Args:
            message: Messaggio da visualizzare.
            level: Livello di severità ('info', 'success', 'warning', 'error').
            parent: Widget genitore (solitamente la MainWindow).
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.message = message
        self.level = level
        self._opacity_val = 0.0

        # Palette Colori Toast
        self.COLORS = {
            "info": QColor("#2196F3"),
            "success": QColor("#4CAF50"),
            "warning": QColor("#FF9800"),
            "error": QColor("#F44336"),
            "bg": QColor(33, 33, 33, 230),
            "text": QColor("#FFFFFF")
        }

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        self.label = QLabel(message)
        self.label.setStyleSheet("color: white; border: none; background: transparent;")
        self.label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.label)

        self.adjustSize()

    @pyqtProperty(float)  # type: ignore
    def opacity(self) -> float:
        """Restituisce l'opacità corrente del toast."""
        return self._opacity_val

    @opacity.setter  # type: ignore
    def opacity(self, val: float):
        """Imposta l'opacità e aggiorna il widget."""
        self._opacity_val = val
        self.setWindowOpacity(val)

    def paintEvent(self, event):
        """Disegna il background arrotondato del toast."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        rect = QRectF(self.rect().adjusted(1, 1, -1, -1))
        path.addRoundedRect(rect, 8, 8)

        color = self.COLORS.get(self.level, self.COLORS["info"])
        painter.fillPath(path, self.COLORS["bg"])

        # Bordo colorato a sinistra
        painter.setClipRect(0, 0, 5, self.height())
        painter.fillPath(path, color)


class ToastManager:
    """
    Gestore globale per le notifiche toast.
    Permette di mostrare messaggi da qualsiasi punto dell'app.
    """
    _instance = None

    def __init__(self):
        """Inizializza il manager dei toast."""
        self.active_toasts = []

    @classmethod
    def instance(cls):
        """Restituisce l'istanza singleton del manager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show(self, message: str, level: str = "info"):
        """
        Visualizza un nuovo toast.

        Args:
            message: Testo del messaggio.
            level: Livello di severità.
        """
        # Trova la main window come parent
        parent = None
        for widget in QApplication.topLevelWidgets():
            if widget.isWindow() and not widget.parent():
                parent = widget
                break

        toast = Toast(message, level, parent)
        self._position_toast(toast)
        self._animate_toast(toast)

    def _position_toast(self, toast):
        """Posiziona il toast in basso al centro rispetto alla finestra principale."""
        if toast.parentWidget():
            p_rect = toast.parentWidget().geometry()
            x = p_rect.x() + (p_rect.width() - toast.width()) // 2
            y = p_rect.y() + p_rect.height() - toast.height() - 50
            toast.move(x, y)
        toast.show()

    def _animate_toast(self, toast):
        """Gestisce l'animazione di comparsa, attesa e scomparsa del toast."""
        anim = QPropertyAnimation(toast, b"opacity")
        anim.setDuration(300)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.start()

        # Scomparsa automatica dopo 3 secondi
        QTimer.singleShot(3000, lambda: self._fade_out(toast))

    def _fade_out(self, toast):
        """Avvia l'animazione di dissolvenza in uscita."""
        anim = QPropertyAnimation(toast, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.finished.connect(toast.deleteLater)
        anim.start()
