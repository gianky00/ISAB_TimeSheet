"""
Widget Autopilot per visualizzare e configurare eventi programmati dei bot.
"""

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QSize,
    Qt,
    QTime,
    QTimer,
)
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTimeEdit,
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


class AutopilotConfigCard(QFrame):
    """
    Card per configurare un bot programmato.
    """

    def __init__(self, bot_id, bot_name, icon_path, color, parent=None):
        super().__init__(parent)
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.icon_path = icon_path
        self.color = color
        self.parent_widget = parent

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            f"""
            AutopilotConfigCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #ffffff);
                border-radius: 12px;
                border-left: 4px solid {color};
                border-top: 1px solid #e9ecef;
                border-right: 1px solid #e9ecef;
                border-bottom: 1px solid #e9ecef;
            }}
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Header con icona e nome
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setFixedSize(28, 28)
        icon_label.setPixmap(
            get_colored_icon(get_asset_path(icon_path), "#ffffff").pixmap(18, 18)
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                border-radius: 14px;
                border: none;
                padding: 5px;
            }}
        """
        )
        header_layout.addWidget(icon_label)

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
        header_layout.addWidget(name_lbl)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Checkbox abilitazione
        self.enable_check = QCheckBox("Abilita esecuzione automatica")
        self.enable_check.setStyleSheet(
            """
            QCheckBox {
                font-size: 13px;
                color: #495057;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #ced4da;
                background: #ffffff;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0d6efd, stop:1 #0a58ca);
                border-color: #0d6efd;
                image: url(assets/icons/check.svg);
            }
        """
        )
        self.enable_check.stateChanged.connect(self._on_config_changed)
        layout.addWidget(self.enable_check)

        # Time picker
        time_layout = QHBoxLayout()
        time_layout.setSpacing(10)

        time_label = QLabel("Orario esecuzione:")
        time_label.setStyleSheet(
            """
            QLabel {
                font-size: 13px;
                color: #495057;
            }
        """
        )
        time_layout.addWidget(time_label)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(9, 0))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setStyleSheet(
            """
            QTimeEdit {
                padding: 6px 10px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background: #ffffff;
                font-size: 13px;
                color: #212529;
            }
            QTimeEdit:focus {
                border-color: #0d6efd;
            }
        """
        )
        self.time_edit.timeChanged.connect(self._on_config_changed)
        time_layout.addWidget(self.time_edit)
        time_layout.addStretch()

        layout.addLayout(time_layout)

        # Carica configurazione salvata
        self._load_config()

    def _load_config(self):
        """Carica la configurazione salvata per questo bot."""
        config = config_manager.load_config()
        enabled_key = f"{self.bot_id}_autopilot_enabled"
        time_key = f"{self.bot_id}_autopilot_time"

        is_enabled = config.get(enabled_key, False)
        self.enable_check.setChecked(is_enabled)

        saved_time = config.get(time_key, "09:00")
        self.time_edit.setTime(QTime.fromString(saved_time, "HH:mm"))

    def _on_config_changed(self):
        """Salva la configurazione quando viene modificata."""
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_enabled", self.enable_check.isChecked()
        )
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_time", self.time_edit.time().toString("HH:mm")
        )

        # Notifica il parent widget per refresh
        if self.parent_widget and hasattr(self.parent_widget, "refresh_events"):
            # Usa un timer per evitare loop di refresh durante il cambio
            QTimer.singleShot(100, self.parent_widget.refresh_events)


class AutopilotWidget(QWidget):
    """
    Widget che mostra e configura gli eventi programmati dei bot (Autopilot).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config_mode = False  # False = visualizzazione, True = configurazione
        self._setup_ui()

        # Timer per aggiornare i bot programmati ogni minuto
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_events)
        self.refresh_timer.start(60000)  # 60 secondi

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        # Header con titolo e pulsante configurazione
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        title = QLabel("Autopilot")
        title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #495057; margin-bottom: 0px;"
        )
        header_layout.addWidget(title)

        # Pulsante configurazione con icona settings
        self.config_btn = QPushButton()
        self.config_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.SETTINGS), "#6c757d")
        )
        self.config_btn.setIconSize(QSize(20, 20))
        self.config_btn.setFixedSize(32, 32)
        self.config_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.config_btn.setToolTip("Configura pianificazioni automatiche")
        self.config_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #ced4da;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """
        )
        self.config_btn.clicked.connect(self._toggle_mode)
        header_layout.addWidget(self.config_btn)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Container per i due widget (view e config)
        self.view_widget = QWidget()
        self.view_layout = QVBoxLayout(self.view_widget)
        self.view_layout.setContentsMargins(0, 4, 0, 0)
        self.view_layout.setSpacing(8)

        self.config_widget = QWidget()
        self.config_layout = QVBoxLayout(self.config_widget)
        self.config_layout.setContentsMargins(0, 4, 0, 0)
        self.config_layout.setSpacing(8)

        # Inizialmente mostra solo view
        main_layout.addWidget(self.view_widget)
        main_layout.addWidget(self.config_widget)
        self.config_widget.setVisible(False)

        main_layout.addStretch()

        self.refresh_events()
        self._refresh_config()

    def _toggle_mode(self):
        """Toggle tra modalità visualizzazione e configurazione con animazione."""
        self._config_mode = not self._config_mode

        if self._config_mode:
            # Passaggio a config mode
            self._animate_transition(self.view_widget, self.config_widget)
        else:
            # Passaggio a view mode
            self._animate_transition(self.config_widget, self.view_widget)
            # Refresh events dopo aver configurato
            QTimer.singleShot(600, self.refresh_events)

    def _animate_transition(self, from_widget, to_widget):
        """
        Crea un'animazione spettacolare di transizione tra due widget.
        Effetto: fade out → fade in
        """
        # Crea nuovi effetti per questa animazione
        from_effect = QGraphicsOpacityEffect(from_widget)
        from_widget.setGraphicsEffect(from_effect)
        from_effect.setOpacity(1.0)

        to_effect = QGraphicsOpacityEffect(to_widget)
        to_widget.setGraphicsEffect(to_effect)
        to_effect.setOpacity(0.0)

        # Mostra il widget di destinazione (ma invisibile)
        to_widget.setVisible(True)

        # Animazione gruppo sequenziale
        sequence = QSequentialAnimationGroup(self)

        # FASE 1: Fade out del widget corrente
        fade_out = QPropertyAnimation(from_effect, b"opacity", self)
        fade_out.setDuration(300)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InCubic)

        sequence.addAnimation(fade_out)

        # Nascondi il widget di partenza al termine del fade out
        def hide_from():
            from_widget.setVisible(False)
            # Rimuovi l'effetto per liberare risorse
            from_widget.setGraphicsEffect(None)

        fade_out.finished.connect(hide_from)

        # FASE 2: Fade in del nuovo widget
        fade_in = QPropertyAnimation(to_effect, b"opacity", self)
        fade_in.setDuration(400)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Rimuovi l'effetto al termine per liberare risorse
        def cleanup_to():
            to_widget.setGraphicsEffect(None)

        fade_in.finished.connect(cleanup_to)

        sequence.addAnimation(fade_in)

        # Avvia l'animazione
        sequence.start()

        # Mantieni i riferimenti per evitare garbage collection
        self._current_animation = sequence
        self._from_effect = from_effect
        self._to_effect = to_effect

    def refresh_events(self):
        """Ricarica gli eventi programmati dai bot (modalità visualizzazione)."""
        # Pulisci eventi esistenti
        while self.view_layout.count() > 0:
            item = self.view_layout.takeAt(0)
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
            self.view_layout.addWidget(empty_lbl)
            return

        # Aggiungi event cards
        for event in events:
            card = AutopilotEventCard(
                event["name"], event["time"], event["icon"], event["color"], self
            )
            self.view_layout.addWidget(card)

    def _refresh_config(self):
        """Ricarica le configurazioni dei bot (modalità configurazione)."""
        # Pulisci config esistenti
        while self.config_layout.count() > 0:
            item = self.config_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Lista dei bot configurabili
        bots = [
            {
                "id": "timbrature",
                "name": "Timbrature Automatiche",
                "icon": Icons.CLOCK,
                "color": "#fd7e14",
            },
            # Aggiungi altri bot qui in futuro
        ]

        # Aggiungi config cards
        for bot in bots:
            card = AutopilotConfigCard(
                bot["id"], bot["name"], bot["icon"], bot["color"], self
            )
            self.config_layout.addWidget(card)
