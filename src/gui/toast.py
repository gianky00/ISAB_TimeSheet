"""
Bot TS - Toast Notifications
Widget per notifiche non intrusive.
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint

class ToastOverlay(QWidget):
    """
    Overlay per mostrare notifiche temporanee (Toast).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Stile (Explicit colors for dark/light mode compatibility)
        # Forced black text on white background as requested
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                border-radius: 6px;
                border: 1px solid #ced4da;
            }
            QLabel {
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        # Effetto Opacità
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        # Animazione
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_toast)

        self.hide()

    def show_toast(self, message: str, duration: int = 3000):
        """Mostra il toast con il messaggio specificato."""
        self.label.setText(message)
        self.adjustSize()

        # Posiziona in basso al centro del genitore
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = parent_rect.height() - self.height() - 50
            self.move(x, y)
            self.raise_()

        self.show()
        self.opacity_effect.setOpacity(0)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

        self.timer.start(duration)

    def hide_toast(self):
        """Nasconde il toast con dissolvenza."""
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)
        self.anim.start()
        self.anim.finished.connect(self.hide)
