"""
Widget Autopilot per visualizzare e configurare eventi programmati dei bot.
"""

from contextlib import suppress

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

    def cleanup(self):
        """Clean up animations and effects before deletion."""
        try:
            # Stop animations
            if hasattr(self, "pulse_anim") and self.pulse_anim is not None:
                self.pulse_anim.stop()
                self.pulse_anim.deleteLater()

            if hasattr(self, "timer") and self.timer is not None:
                self.timer.stop()

            # Remove graphics effect
            if hasattr(self, "icon_label") and self.icon_label:
                self.icon_label.setGraphicsEffect(None)

            # Delete effect (may not exist if animation was disabled)
            if hasattr(self, "icon_opacity") and self.icon_opacity:
                self.icon_opacity.deleteLater()
        except (RuntimeError, AttributeError):
            pass  # Widget already deleted or attribute missing

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
        icon_label.setPixmap(get_colored_icon(get_asset_path(icon_path), "#ffffff").pixmap(18, 18))
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
        config_manager.set_config_value(f"{self.bot_id}_autopilot_enabled", self.enable_check.isChecked())
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_time", self.time_edit.time().toString("HH:mm")
        )

        # Notifica il parent widget per refresh
        if self.parent_widget and hasattr(self.parent_widget, "refresh_events"):
            # Usa un timer per evitare loop di refresh durante il cambio
            QTimer.singleShot(100, self.parent_widget.refresh_events)

        # Aggiorna anche il footer (Account & Status Cards)
        if self.parent_widget:
            if hasattr(self.parent_widget, "footer_left_widget") and self.parent_widget.footer_left_widget:
                QTimer.singleShot(100, self.parent_widget.footer_left_widget.refresh_accounts)

            if hasattr(self.parent_widget, "status_bar") and self.parent_widget.status_bar:
                QTimer.singleShot(100, self.parent_widget.status_bar.update_autopilot_ui)


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
        icon_label.setPixmap(get_colored_icon(get_asset_path(icon_path), "#ffffff").pixmap(18, 18))
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
        config_manager.set_config_value(f"{self.bot_id}_autopilot_enabled", self.enable_check.isChecked())
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_time", self.time_edit.time().toString("HH:mm")
        )
        config_manager.set_config_value(f"{self.bot_id}_autopilot_interval_days", self.interval_spin.value())

        # Notifica il parent widget per refresh
        if self.parent_widget and hasattr(self.parent_widget, "refresh_events"):
            QTimer.singleShot(100, self.parent_widget.refresh_events)

        # Aggiorna anche il footer (Account & Status Cards)
        if self.parent_widget:
            if hasattr(self.parent_widget, "footer_left_widget") and self.parent_widget.footer_left_widget:
                QTimer.singleShot(100, self.parent_widget.footer_left_widget.refresh_accounts)

            if hasattr(self.parent_widget, "status_bar") and self.parent_widget.status_bar:
                QTimer.singleShot(100, self.parent_widget.status_bar.update_autopilot_ui)


class AutopilotWidget(QWidget):
    """
    Widget che mostra e configura gli eventi programmati dei bot (Autopilot).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config_mode = False  # False = visualizzazione, True = configurazione
        self.footer_left_widget = None  # Riferimento al footer per aggiornamenti
        self.status_bar = None  # Riferimento alla StatusBarComponent
        self._setup_ui()

        # Timer per aggiornare i bot programmati ogni minuto
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_events)
        self.refresh_timer.start(60000)  # 60 secondi

    def set_footer_widget(self, footer_left_widget):
        """Imposta il riferimento al footer widget per gli aggiornamenti."""
        self.footer_left_widget = footer_left_widget

    def set_status_bar(self, status_bar):
        """Imposta il riferimento alla barra di stato per aggiornamenti Autopilot."""
        self.status_bar = status_bar

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
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #495057; margin-bottom: 0px;")
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
        self.config_btn.setIcon(get_colored_icon(get_asset_path(Icons.SETTINGS), "#6c757d"))
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

    def _stop_all_card_animations(self, layout):
        """Ferma ricorsivamente tutte le animazioni delle card in un layout."""
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if not item or not item.widget():
                continue

            widget = item.widget()
            # Stop pulse animation
            if hasattr(widget, "pulse_anim") and widget.pulse_anim:
                with suppress(RuntimeError):
                    widget.pulse_anim.stop()

            # Stop timers
            if hasattr(widget, "timer") and widget.timer:
                with suppress(RuntimeError):
                    widget.timer.stop()

    def _toggle_mode(self):
        """Toggle tra modalità visualizzazione e configurazione con animazione spettacolare."""
        if getattr(self, "_animating", False):
            return

        self._animating = True
        self._config_mode = not self._config_mode

        # 1. Stop LIVE dot animation
        if hasattr(self, "dot_anim") and self.dot_anim:
            with suppress(RuntimeError):
                self.dot_anim.stop()

        # 2. Stop card animations in both layouts
        self._stop_all_card_animations(self.view_layout)
        self._stop_all_card_animations(self.config_layout)

        # 3. Effettua la transizione
        self._animate_gear_button()

        if self._config_mode:
            self._animate_transition(self.view_widget, self.config_widget)
        else:
            self._animate_transition(self.config_widget, self.view_widget)
            QTimer.singleShot(600, self.refresh_events)

        # 4. Restart animazioni dopo la transizione
        QTimer.singleShot(800, self._restart_live_animations)

    def _restart_live_animations(self):
        """Ripristina le animazioni globali dopo la transizione."""
        if hasattr(self, "dot_anim") and self.dot_anim:
            with suppress(RuntimeError):
                self.dot_anim.start()
        self._animating = False
        QTimer.singleShot(800, lambda: setattr(self, "_animating", False))

    def _cleanup_gear_animations(self):
        """Ferma e pulisce le animazioni del gear button se in esecuzione."""
        if hasattr(self, "_gear_animation") and self._gear_animation:
            try:
                if self._gear_animation.state() == QParallelAnimationGroup.State.Running:
                    self._gear_animation.stop()
                self._gear_animation.deleteLater()
            except RuntimeError:
                pass

        if hasattr(self, "_gear_shake_anim") and self._gear_shake_anim:
            try:
                if self._gear_shake_anim.state() == QPropertyAnimation.State.Running:
                    self._gear_shake_anim.stop()
            except RuntimeError:
                pass

        if hasattr(self, "_gear_scale_sequence") and self._gear_scale_sequence:
            try:
                if self._gear_scale_sequence.state() == QSequentialAnimationGroup.State.Running:
                    self._gear_scale_sequence.stop()
            except RuntimeError:
                pass

    def _create_shake_animation(self, original_pos):
        """Crea l'animazione di shake orizzontale per il gear button."""
        shake_anim = QPropertyAnimation(self.config_btn, b"pos", self)
        shake_anim.setDuration(500)
        shake_anim.setKeyValueAt(0.0, original_pos)
        shake_anim.setKeyValueAt(0.1, QPoint(original_pos.x() + 3, original_pos.y()))
        shake_anim.setKeyValueAt(0.2, QPoint(original_pos.x() - 3, original_pos.y()))
        shake_anim.setKeyValueAt(0.3, QPoint(original_pos.x() + 2, original_pos.y()))
        shake_anim.setKeyValueAt(0.4, QPoint(original_pos.x() - 2, original_pos.y()))
        shake_anim.setKeyValueAt(0.5, QPoint(original_pos.x() + 1, original_pos.y()))
        shake_anim.setKeyValueAt(1.0, original_pos)
        shake_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        return shake_anim

    def _create_scale_animation(self):
        """Crea l'animazione di scale bounce per il gear button."""
        scale_sequence = QSequentialAnimationGroup(self)

        # Scale UP (zoom in)
        scale_up = QPropertyAnimation(self.config_btn, b"iconSize", self)
        scale_up.setDuration(200)
        scale_up.setStartValue(QSize(20, 20))
        scale_up.setEndValue(QSize(30, 30))
        scale_up.setEasingCurve(QEasingCurve.Type.OutCubic)
        scale_sequence.addAnimation(scale_up)

        # Scale DOWN (zoom out)
        scale_down = QPropertyAnimation(self.config_btn, b"iconSize", self)
        scale_down.setDuration(150)
        scale_down.setStartValue(QSize(30, 30))
        scale_down.setEndValue(QSize(16, 16))
        scale_down.setEasingCurve(QEasingCurve.Type.InCubic)
        scale_sequence.addAnimation(scale_down)

        # Scale NORMALIZE con bounce elastico
        scale_normal = QPropertyAnimation(self.config_btn, b"iconSize", self)
        scale_normal.setDuration(400)
        scale_normal.setStartValue(QSize(16, 16))
        scale_normal.setEndValue(QSize(20, 20))
        scale_normal.setEasingCurve(QEasingCurve.Type.OutElastic)
        scale_sequence.addAnimation(scale_normal)

        return scale_sequence

    def _setup_color_transitions(self, original_style):
        """Configura le transizioni di colore a caleidoscopio per il gear button."""

        def set_color(gradient_start, gradient_end, border_color):
            try:
                self.config_btn.setStyleSheet(
                    f"""
                    QPushButton {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 {gradient_start}, stop:1 {gradient_end});
                        border: 3px solid {border_color};
                        border-radius: 16px;
                    }}
                """
                )
            except RuntimeError:
                pass

        def restore_color():
            try:
                self.config_btn.setStyleSheet(original_style)
            except RuntimeError:
                pass

        # Timer per cambio colore rapido (caleidoscopio)
        QTimer.singleShot(0, lambda: set_color("#0d6efd", "#0a58ca", "#0d6efd"))  # Blu
        QTimer.singleShot(200, lambda: set_color("#8b5cf6", "#7c3aed", "#8b5cf6"))  # Viola
        QTimer.singleShot(400, lambda: set_color("#10b981", "#059669", "#10b981"))  # Verde
        QTimer.singleShot(750, restore_color)

    def _animate_gear_button(self):
        """
        Crea un'animazione spettacolare per il pulsante ingranaggio.
        Combina: Scale bounce, Shake orizzontale, Pulsazione colore multi-fase.
        """
        # Cleanup animazioni precedenti
        self._cleanup_gear_animations()

        # Salva stato originale
        original_pos = self.config_btn.pos()
        original_style = self.config_btn.styleSheet()

        # Crea gruppo animazione parallela
        parallel_group = QParallelAnimationGroup(self)

        # 1. Shake effect
        shake_anim = self._create_shake_animation(original_pos)
        parallel_group.addAnimation(shake_anim)

        # 2. Scale bounce effect
        scale_sequence = self._create_scale_animation()
        parallel_group.addAnimation(scale_sequence)

        # 3. Color transitions
        self._setup_color_transitions(original_style)

        # Cleanup quando finisce
        parallel_group.finished.connect(lambda: parallel_group.deleteLater() if parallel_group else None)

        # Avvia e mantieni riferimenti
        parallel_group.start()
        self._gear_animation = parallel_group
        self._gear_shake_anim = shake_anim
        self._gear_scale_sequence = scale_sequence

    def _animate_transition(self, from_widget, to_widget):
        """
        Crea un'animazione spettacolare di transizione tra due widget.
        Effetto: fade out → fade in - SIMPLIFIED VERSION without QGraphicsOpacityEffect
        """
        # Stop any previous animation
        if hasattr(self, "_current_animation") and self._current_animation:
            try:
                if self._current_animation.state() == QSequentialAnimationGroup.State.Running:
                    self._current_animation.stop()
                self._current_animation.deleteLater()
            except RuntimeError:
                pass

        # Clean up any previous effects
        from_widget.setGraphicsEffect(None)
        to_widget.setGraphicsEffect(None)

        # Simple cross-fade without opacity effects
        # Just hide/show with a timer delay
        to_widget.setVisible(True)
        to_widget.hide()

        def do_transition():
            from_widget.hide()
            to_widget.show()

        # Delay transition slightly for smoother visual effect
        QTimer.singleShot(150, do_transition)

    def refresh_events(self):
        """Ricarica gli eventi programmati dai bot (modalità visualizzazione) con layout a 2 colonne."""
        from PyQt6.QtWidgets import QApplication

        # Pulisci eventi esistenti
        widgets_to_delete = []
        while self.view_layout.count() > 0:
            item = self.view_layout.takeAt(0)
            widget = item.widget()
            if widget:
                # Clean up animations before deleting
                if hasattr(widget, "cleanup"):
                    widget.cleanup()
                widgets_to_delete.append(widget)

        # Delete all widgets
        for widget in widgets_to_delete:
            widget.deleteLater()

        # CRITICAL: Force immediate processing of delete events
        QApplication.processEvents()

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
            card = AutopilotEventCard(event["name"], event["time"], event["icon"], event["color"], self)
            row = idx // 2  # Riga
            col = idx % 2  # Colonna (0 o 1)
            self.view_layout.addWidget(card, row, col)

    def _refresh_config(self):
        """Ricarica le configurazioni dei bot (modalità configurazione) con layout a 2 colonne."""
        from PyQt6.QtWidgets import QApplication

        # Pulisci config esistenti
        widgets_to_delete = []
        while self.config_layout.count() > 0:
            item = self.config_layout.takeAt(0)
            widget = item.widget()
            if widget:
                # Clean up any animations before deleting
                if hasattr(widget, "cleanup"):
                    widget.cleanup()
                widgets_to_delete.append(widget)

        # Delete all widgets
        for widget in widgets_to_delete:
            widget.deleteLater()

        # CRITICAL: Force immediate processing of delete events
        QApplication.processEvents()

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
            card = AutopilotConfigCard(bot["id"], bot["name"], bot["icon"], bot["color"], self)
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
