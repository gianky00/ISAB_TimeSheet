"""
Widget Autopilot per visualizzare eventi programmati dei bot.
"""

from PyQt6.QtCore import Qt, QTime, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon


class AutopilotEventCard(QFrame):
    """
    Card per visualizzare un singolo evento programmato del bot.
    """

    def __init__(self, bot_name, target_time_str, icon_path, color, parent=None):
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
        icon_label = QLabel()
        icon_label.setFixedSize(32, 32)
        icon_label.setPixmap(
            get_colored_icon(get_asset_path(icon_path), "#ffffff").pixmap(20, 20)
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                border-radius: 16px;
                border: none;
                padding: 6px;
            }}
        """
        )
        layout.addWidget(icon_label)

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

        # Timer per aggiornare il countdown ogni minuto
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_countdown)
        self.timer.start(60000)  # 60 secondi

        # Aggiorna countdown iniziale
        self._update_countdown()

    def _update_countdown(self):
        """Aggiorna il countdown per il prossimo evento."""
        target_time = QTime.fromString(self.target_time_str, "HH:mm")
        now = QTime.currentTime()

        # Calcolo tempo residuo
        secs_to = now.secsTo(target_time)
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


class AutopilotWidget(QWidget):
    """
    Widget che mostra gli eventi programmati dei bot (Autopilot).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

        # Timer per aggiornare i bot programmati ogni minuto
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_events)
        self.refresh_timer.start(60000)  # 60 secondi

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Title
        title = QLabel("Autopilot")
        title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #495057; margin-bottom: 0px;"
        )
        layout.addWidget(title)

        # Container for event cards
        self.events_widget = QWidget()
        self.events_layout = QVBoxLayout(self.events_widget)
        self.events_layout.setContentsMargins(0, 4, 0, 0)
        self.events_layout.setSpacing(8)

        layout.addWidget(self.events_widget)
        layout.addStretch()

        self.refresh_events()

    def refresh_events(self):
        """Ricarica gli eventi programmati dai bot."""
        # Pulisci eventi esistenti
        while self.events_layout.count() > 0:
            item = self.events_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        config = config_manager.load_config()

        # Controlla se ci sono bot programmati
        events = []

        # Bot Timbrature (Portale Fornitori)
        if config.get("timbrature_autopilot_enabled", False):
            target_time = config.get("timbrature_autopilot_time", "09:00")
            events.append(
                {
                    "name": "Timbrature Automatiche",
                    "time": target_time,
                    "icon": Icons.CLOCK,
                    "color": "#fd7e14",
                }
            )

        # Qui puoi aggiungere altri bot quando saranno disponibili
        # if config.get("safework_autopilot_enabled", False):
        #     target_time = config.get("safework_autopilot_time", "10:00")
        #     events.append({
        #         "name": "SafeWork Bot",
        #         "time": target_time,
        #         "icon": Icons.SHIELD,
        #         "color": "#198754",
        #     })

        # Se non ci sono eventi, mostra messaggio
        if not events:
            empty_lbl = QLabel("⏸️ Nessun bot programmato")
            empty_lbl.setStyleSheet(
                """
                QLabel {
                    color: #868e96;
                    font-size: 13px;
                    font-weight: 500;
                    font-style: italic;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border: 1px dashed #dee2e6;
                }
            """
            )
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.events_layout.addWidget(empty_lbl)
            return

        # Aggiungi event cards
        for event in events:
            card = AutopilotEventCard(
                event["name"], event["time"], event["icon"], event["color"], self
            )
            self.events_layout.addWidget(card)
