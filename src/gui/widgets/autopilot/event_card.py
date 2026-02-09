from contextlib import suppress

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTime, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.utils.helpers import get_asset_path, get_colored_icon


class AutopilotEventCard(QFrame):
    """
    Card per visualizzare un singolo evento programmato del bot.
    """

    def __init__(
        self, bot_name: str, target_time_str: str, icon_path: str, color: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.bot_name = bot_name
        self.target_time_str = target_time_str
        self.icon_path = icon_path
        self.color = color

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            f"""
            AutopilotEventCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #ffffff);
                border-radius: 12px;
                border-left: 4px solid {color};
                border-top: 1px solid #e9ecef;
                border-right: 1px solid #e9ecef;
                border-bottom: 1px solid #e9ecef;
            }}
            AutopilotEventCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e9ecef, stop:1 #f8f9fa);
                border-left: 4px solid {color};
                border-top: 1px solid #ced4da;
                border-right: 1px solid #ced4da;
                border-bottom: 1px solid #ced4da;
            }}
        """
        )
        self.setFixedHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        self.icon_label.setPixmap(get_colored_icon(get_asset_path(icon_path), "#ffffff").pixmap(20, 20))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                border-radius: 16px;
                border: none;
                padding: 6px;
            }}
        """
        )
        layout.addWidget(self.icon_label)

        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        # Bot name
        name_lbl = QLabel(bot_name)
        name_lbl.setStyleSheet(
            """
            QLabel {
                font-weight: 600;
                font-size: 14px;
                color: #212529;
                border: none;
                background: transparent;
            }
        """
        )
        text_layout.addWidget(name_lbl)

        # Countdown label
        self.countdown_lbl = QLabel()
        self.countdown_lbl.setStyleSheet(
            """
            QLabel {
                font-size: 12px;
                color: #868e96;
                border: none;
                background: transparent;
                font-weight: 500;
            }
        """
        )
        text_layout.addWidget(self.countdown_lbl)

        layout.addLayout(text_layout)
        layout.addStretch()

        # --- ANIMAZIONE "VIVO" (Pulse Effect sull'icona) ---
        self.icon_opacity = QGraphicsOpacityEffect(self.icon_label)
        self.icon_label.setGraphicsEffect(self.icon_opacity)

        self.pulse_anim = QPropertyAnimation(self.icon_opacity, b"opacity")
        self.pulse_anim.setDuration(2000)
        self.pulse_anim.setStartValue(0.6)
        self.pulse_anim.setEndValue(1.0)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_anim.setLoopCount(-1)  # Infinito
        self.pulse_anim.start()

        # Timer per aggiornare il countdown ogni minuto
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_countdown)
        self.timer.start(60000)  # 60 secondi

        # Aggiorna countdown iniziale
        self._update_countdown()

    def cleanup(self) -> None:
        """Clean up animations and effects before deletion."""
        with suppress(RuntimeError, AttributeError):
            # Stop animations
            if hasattr(self, "pulse_anim") and self.pulse_anim:
                self.pulse_anim.stop()
                self.pulse_anim.deleteLater()

            if hasattr(self, "timer") and self.timer:
                self.timer.stop()

            # Remove graphics effect
            if hasattr(self, "icon_label") and self.icon_label:
                self.icon_label.setGraphicsEffect(None)

            # Delete effect (may not exist if animation was disabled)
            if hasattr(self, "icon_opacity") and self.icon_opacity:
                self.icon_opacity.deleteLater()

    def _update_countdown(self) -> None:
        """Aggiorna il countdown per il prossimo evento."""
        # Calcolo tempo residuo
        secs_to = QTime.currentTime().secsTo(QTime.fromString(self.target_time_str, "HH:mm"))
        if secs_to < 0:
            # Se l'orario è già passato, calcola per domani
            secs_to += 24 * 3600

        hours = secs_to // 3600
        mins = (secs_to % 3600) // 60

        if hours > 0:
            countdown = f"⏱️ Prossima esecuzione tra {hours}h {mins}m"
        else:
            countdown = f"⏱️ Prossima esecuzione tra {mins}m"

        self.countdown_lbl.setText(countdown)
