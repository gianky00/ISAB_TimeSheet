"""
Widget Autopilot per visualizzare e configurare eventi programmati dei bot.
"""

from PyQt6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
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
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
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

        # --- ANIMAZIONE "VIVO" (Pulse Effect sull'icona) ---
        self.icon_opacity = QGraphicsOpacityEffect(icon_label)
        icon_label.setGraphicsEffect(self.icon_opacity)

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

        # Aggiorna anche il footer
        if (
            self.parent_widget
            and hasattr(self.parent_widget, "footer_left_widget")
            and self.parent_widget.footer_left_widget
        ):
            QTimer.singleShot(
                100, self.parent_widget.footer_left_widget.refresh_accounts
            )


class AutopilotConfigCardWithInterval(QFrame):
    """
    Card per configurare un task programmato con intervallo in giorni.
    Usato per report email e altri task non giornalieri.
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
            AutopilotConfigCardWithInterval {{
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
        layout.setSpacing(8)

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
        self.enable_check = QCheckBox("Abilita invio automatico")
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

        # Riga: Orario + Intervallo giorni
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(15)

        # Time picker
        time_label = QLabel("Ore:")
        time_label.setStyleSheet("font-size: 12px; color: #495057;")
        settings_layout.addWidget(time_label)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(8, 0))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setFixedWidth(70)
        self.time_edit.setStyleSheet(
            """
            QTimeEdit {
                padding: 4px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background: #ffffff;
                font-size: 12px;
                color: #212529;
            }
            QTimeEdit:focus {
                border-color: #0d6efd;
            }
        """
        )
        self.time_edit.timeChanged.connect(self._on_config_changed)
        settings_layout.addWidget(self.time_edit)

        # Intervallo giorni
        interval_label = QLabel("Ogni:")
        interval_label.setStyleSheet("font-size: 12px; color: #495057;")
        settings_layout.addWidget(interval_label)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 30)
        self.interval_spin.setValue(7)
        self.interval_spin.setSuffix(" gg")
        self.interval_spin.setFixedWidth(70)
        self.interval_spin.setStyleSheet(
            """
            QSpinBox {
                padding: 4px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background: #ffffff;
                font-size: 12px;
                color: #212529;
            }
            QSpinBox:focus {
                border-color: #0d6efd;
            }
        """
        )
        self.interval_spin.valueChanged.connect(self._on_config_changed)
        settings_layout.addWidget(self.interval_spin)
        settings_layout.addStretch()

        layout.addLayout(settings_layout)

        # Carica configurazione salvata
        self._load_config()

    def _load_config(self):
        """Carica la configurazione salvata per questo task."""
        config = config_manager.load_config()

        is_enabled = config.get(f"{self.bot_id}_autopilot_enabled", False)
        self.enable_check.setChecked(is_enabled)

        saved_time = config.get(f"{self.bot_id}_autopilot_time", "08:00")
        self.time_edit.setTime(QTime.fromString(saved_time, "HH:mm"))

        interval_days = config.get(f"{self.bot_id}_autopilot_interval_days", 7)
        self.interval_spin.setValue(interval_days)

    def _on_config_changed(self):
        """Salva la configurazione quando viene modificata."""
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_enabled", self.enable_check.isChecked()
        )
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_time", self.time_edit.time().toString("HH:mm")
        )
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_interval_days", self.interval_spin.value()
        )

        # Notifica il parent widget per refresh
        if self.parent_widget and hasattr(self.parent_widget, "refresh_events"):
            QTimer.singleShot(100, self.parent_widget.refresh_events)


class AutopilotWidget(QWidget):
    """
    Widget che mostra e configura gli eventi programmati dei bot (Autopilot).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config_mode = False  # False = visualizzazione, True = configurazione
        self.footer_left_widget = None  # Riferimento al footer per aggiornamenti
        self._setup_ui()

        # Timer per aggiornare i bot programmati ogni minuto
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_events)
        self.refresh_timer.start(60000)  # 60 secondi

    def set_footer_widget(self, footer_left_widget):
        """Imposta il riferimento al footer widget per gli aggiornamenti."""
        self.footer_left_widget = footer_left_widget

    def _setup_ui(self):
        # Imposta size policy per non influenzare altri widget nella stessa riga
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(600)  # Larghezza fissa per 2 colonne
        self.setMaximumWidth(600)

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

        # --- LIVE INDICATOR (Neon Dot) ---
        self.live_container = QWidget()
        live_layout = QHBoxLayout(self.live_container)
        live_layout.setContentsMargins(5, 0, 5, 0)
        live_layout.setSpacing(5)

        self.live_dot = QLabel()
        self.live_dot.setFixedSize(8, 8)
        self.live_dot.setStyleSheet(
            "background-color: #22c55e; border-radius: 4px; border: 1px solid #16a34a;"
        )

        self.live_text = QLabel("LIVE")
        self.live_text.setStyleSheet(
            "color: #22c55e; font-size: 10px; font-weight: 800; letter-spacing: 1px;"
        )

        live_layout.addWidget(self.live_dot)
        live_layout.addWidget(self.live_text)
        header_layout.addWidget(self.live_container)

        # Animazione Pulsante per il pallino LIVE
        self.dot_opacity = QGraphicsOpacityEffect(self.live_container)
        self.live_container.setGraphicsEffect(self.dot_opacity)

        self.dot_anim = QPropertyAnimation(self.dot_opacity, b"opacity")
        self.dot_anim.setDuration(1000)
        self.dot_anim.setStartValue(0.3)
        self.dot_anim.setEndValue(1.0)
        self.dot_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.dot_anim.setLoopCount(-1)
        self.dot_anim.start()

        # Pulsante configurazione con icona settings
        self.config_btn = QPushButton()
        self.config_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.SETTINGS), "#6c757d")
        )
        self.config_btn.setIconSize(QSize(20, 20))
        self.config_btn.setFixedSize(32, 32)
        self.config_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # Rimuovi tooltip per evitare sfondo nero
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
            QToolTip {
                background-color: #ffffff;
                color: #212529;
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                padding: 5px;
            }
        """
        )
        self.config_btn.clicked.connect(self._toggle_mode)
        header_layout.addWidget(self.config_btn)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Container per i due widget (view e config) - LAYOUT A 2 COLONNE
        self.view_widget = QWidget()
        self.view_layout = QGridLayout(self.view_widget)
        self.view_layout.setContentsMargins(0, 4, 0, 0)
        self.view_layout.setSpacing(8)
        self.view_layout.setColumnStretch(0, 1)  # Colonna 1 stretch
        self.view_layout.setColumnStretch(1, 1)  # Colonna 2 stretch

        self.config_widget = QWidget()
        self.config_layout = QGridLayout(self.config_widget)
        self.config_layout.setContentsMargins(0, 4, 0, 0)
        self.config_layout.setSpacing(8)
        self.config_layout.setColumnStretch(0, 1)  # Colonna 1 stretch
        self.config_layout.setColumnStretch(1, 1)  # Colonna 2 stretch

        # Inizialmente mostra solo view
        main_layout.addWidget(self.view_widget)
        main_layout.addWidget(self.config_widget)
        self.config_widget.setVisible(False)

        main_layout.addStretch()

        self.refresh_events()
        self._refresh_config()

    def _toggle_mode(self):
        """Toggle tra modalità visualizzazione e configurazione con animazione spettacolare."""
        self._config_mode = not self._config_mode

        # Animazione spettacolare del pulsante ingranaggio
        self._animate_gear_button()

        if self._config_mode:
            # Passaggio a config mode
            self._animate_transition(self.view_widget, self.config_widget)
        else:
            # Passaggio a view mode
            self._animate_transition(self.config_widget, self.view_widget)
            # Refresh events dopo aver configurato
            QTimer.singleShot(600, self.refresh_events)

    def _animate_gear_button(self):
        """
        Crea un'animazione SPETTACOLARE per il pulsante ingranaggio.
        # Combina: Scale bounce drammatico, Shake orizzontale, Pulsazione colore multi-fase.
        """
        # Salva posizione originale
        original_pos = self.config_btn.pos()
        original_style = self.config_btn.styleSheet()

        # === ANIMAZIONE PARALLELA (tutto insieme) ===
        parallel_group = QParallelAnimationGroup(self)

        # 1. SHAKE EFFECT (movimento orizzontale rapido)
        shake_anim = QPropertyAnimation(self.config_btn, b"pos", self)
        shake_anim.setDuration(500)
        shake_anim.setKeyValueAt(0.0, original_pos)
        shake_anim.setKeyValueAt(
            0.1, QPoint(original_pos.x() + 3, original_pos.y())
        )  # Destra
        shake_anim.setKeyValueAt(
            0.2, QPoint(original_pos.x() - 3, original_pos.y())
        )  # Sinistra
        shake_anim.setKeyValueAt(
            0.3, QPoint(original_pos.x() + 2, original_pos.y())
        )  # Destra
        shake_anim.setKeyValueAt(
            0.4, QPoint(original_pos.x() - 2, original_pos.y())
        )  # Sinistra
        shake_anim.setKeyValueAt(
            0.5, QPoint(original_pos.x() + 1, original_pos.y())
        )  # Destra
        shake_anim.setKeyValueAt(1.0, original_pos)  # Torna normale
        shake_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        parallel_group.addAnimation(shake_anim)

        # 2. PULSAZIONE DRAMMATICA con scala (zoom in/out/bounce)
        # Sequenza: 1.0 -> 1.5 (GRANDE) -> 0.8 -> 1.0 (bounce)
        scale_sequence = QSequentialAnimationGroup(self)

        # Scale UP DRAMMATICO (zoom in molto grande)
        scale_up = QPropertyAnimation(self.config_btn, b"iconSize", self)
        scale_up.setDuration(200)
        scale_up.setStartValue(QSize(20, 20))
        scale_up.setEndValue(QSize(30, 30))  # +50% size!
        scale_up.setEasingCurve(QEasingCurve.Type.OutCubic)
        scale_sequence.addAnimation(scale_up)

        # Scale DOWN (zoom out piccolo)
        scale_down = QPropertyAnimation(self.config_btn, b"iconSize", self)
        scale_down.setDuration(150)
        scale_down.setStartValue(QSize(30, 30))
        scale_down.setEndValue(QSize(16, 16))  # -20% size
        scale_down.setEasingCurve(QEasingCurve.Type.InCubic)
        scale_sequence.addAnimation(scale_down)

        # Scale NORMALIZE con BOUNCE ELASTICO (ritorno drammatico)
        scale_normal = QPropertyAnimation(self.config_btn, b"iconSize", self)
        scale_normal.setDuration(400)
        scale_normal.setStartValue(QSize(16, 16))
        scale_normal.setEndValue(QSize(20, 20))
        scale_normal.setEasingCurve(
            QEasingCurve.Type.OutElastic
        )  # ELASTIC = Super bounce!
        scale_sequence.addAnimation(scale_normal)

        parallel_group.addAnimation(scale_sequence)

        # 3. CAMBIO COLORE MULTI-FASE (effetto arcobaleno)
        # Sequenza: grigio -> blu -> viola -> verde -> grigio
        def set_blue():
            self.config_btn.setStyleSheet(
                """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #0d6efd, stop:1 #0a58ca);
                    border: 3px solid #0d6efd;
                    border-radius: 16px;
                }
            """
            )

        def set_purple():
            self.config_btn.setStyleSheet(
                """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #8b5cf6, stop:1 #7c3aed);
                    border: 3px solid #8b5cf6;
                    border-radius: 16px;
                }
            """
            )

        def set_green():
            self.config_btn.setStyleSheet(
                """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #10b981, stop:1 #059669);
                    border: 3px solid #10b981;
                    border-radius: 16px;
                }
            """
            )

        def restore_color():
            self.config_btn.setStyleSheet(original_style)

        # Timer per cambio colore rapido (caleidoscopio)
        QTimer.singleShot(0, set_blue)  # Blu immediato
        QTimer.singleShot(200, set_purple)  # Viola a 200ms
        QTimer.singleShot(400, set_green)  # Verde a 400ms
        QTimer.singleShot(750, restore_color)  # Ritorno normale a 750ms

        # === AVVIA ANIMAZIONE ===
        parallel_group.start()

        # Mantieni riferimenti per evitare garbage collection
        self._gear_animation = parallel_group
        self._gear_shake_anim = shake_anim

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
        """Ricarica gli eventi programmati dai bot (modalità visualizzazione) con layout a 2 colonne."""
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
                    "site": "portale_fornitori",
                }
            )

        # Bot Scarico OdA Generale (Portale Fornitori)
        if config.get("scarico_oda_generale_autopilot_enabled", False):
            target_time = config.get("scarico_oda_generale_autopilot_time", "09:00")
            events.append(
                {
                    "name": "Scarico OdA Generale",
                    "time": target_time,
                    "icon": Icons.DOWNLOAD,
                    "color": "#0d6efd",
                    "site": "portale_fornitori",
                }
            )

        # Bot Ricerca PDL (SafeWork)
        if config.get("ricerca_pdl_autopilot_enabled", False):
            target_time = config.get("ricerca_pdl_autopilot_time", "09:00")
            events.append(
                {
                    "name": "Ricerca PDL",
                    "time": target_time,
                    "icon": Icons.SEARCH,
                    "color": "#198754",
                    "site": "safework",
                }
            )

        # Report Email ISAB (con intervallo giorni)
        if config.get("report_email_autopilot_enabled", False):
            target_time = config.get("report_email_autopilot_time", "08:00")
            interval_days = config.get("report_email_autopilot_interval_days", 7)
            events.append(
                {
                    "name": f"Report Email (ogni {interval_days}gg)",
                    "time": target_time,
                    "icon": Icons.SEND,
                    "color": "#6f42c1",
                    "site": "internal",
                }
            )

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
            # Span su 2 colonne
            self.view_layout.addWidget(empty_lbl, 0, 0, 1, 2)
            return

        # Aggiungi event cards in griglia 2 colonne
        for idx, event in enumerate(events):
            card = AutopilotEventCard(
                event["name"], event["time"], event["icon"], event["color"], self
            )
            row = idx // 2  # Riga
            col = idx % 2  # Colonna (0 o 1)
            self.view_layout.addWidget(card, row, col)

    def _refresh_config(self):
        """Ricarica le configurazioni dei bot (modalità configurazione) con layout a 2 colonne."""
        # Pulisci config esistenti
        while self.config_layout.count() > 0:
            item = self.config_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Lista dei bot configurabili (giornalieri)
        bots = [
            {
                "id": "timbrature",
                "name": "Timbrature Automatiche",
                "icon": Icons.CLOCK,
                "color": "#fd7e14",
                "site": "portale_fornitori",
            },
            {
                "id": "scarico_oda_generale",
                "name": "Scarico OdA Generale",
                "icon": Icons.DOWNLOAD,
                "color": "#0d6efd",
                "site": "portale_fornitori",
            },
            {
                "id": "ricerca_pdl",
                "name": "Ricerca PDL",
                "icon": Icons.SEARCH,
                "color": "#198754",
                "site": "safework",
            },
        ]

        # Task con intervallo giorni configurabile
        interval_tasks = [
            {
                "id": "report_email",
                "name": "Report Email ISAB",
                "icon": Icons.SEND,
                "color": "#6f42c1",
            },
        ]

        # Aggiungi config cards per bot giornalieri
        idx = 0
        for bot in bots:
            card = AutopilotConfigCard(
                bot["id"], bot["name"], bot["icon"], bot["color"], self
            )
            row = idx // 2  # Riga
            col = idx % 2  # Colonna (0 o 1)
            self.config_layout.addWidget(card, row, col)
            idx += 1

        # Aggiungi config cards per task con intervallo
        for task in interval_tasks:
            card = AutopilotConfigCardWithInterval(
                task["id"], task["name"], task["icon"], task["color"], self
            )
            row = idx // 2
            col = idx % 2
            self.config_layout.addWidget(card, row, col)
            idx += 1
