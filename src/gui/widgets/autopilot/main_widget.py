"""
SyncroJob - Autopilot Main Widget
Widget coordinatore per la visualizzazione e configurazione dei bot programmati.
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
    QTimer,
)
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon

from .config_cards import AutopilotConfigCard, AutopilotConfigCardWithInterval
from .event_card import AutopilotEventCard


class AutopilotWidget(QWidget):
    """
    Widget che mostra e configura gli eventi programmati dei bot (Autopilot).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config_mode = False
        self.footer_left_widget = None
        self.status_bar = None
        self._setup_ui()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_events)
        self.refresh_timer.start(60000)

    def set_footer_widget(self, footer_left_widget):
        self.footer_left_widget = footer_left_widget

    def set_status_bar(self, status_bar):
        self.status_bar = status_bar

    def _setup_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(600)
        self.setMaximumWidth(600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        title = QLabel("Autopilot")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #495057;")
        header_layout.addWidget(title)

        # --- LIVE INDICATOR ---
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

        self.dot_opacity = QGraphicsOpacityEffect(self.live_container)
        self.live_container.setGraphicsEffect(self.dot_opacity)
        self.dot_anim = QPropertyAnimation(self.dot_opacity, b"opacity")
        self.dot_anim.setDuration(1000)
        self.dot_anim.setStartValue(0.3)
        self.dot_anim.setEndValue(1.0)
        self.dot_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.dot_anim.setLoopCount(-1)
        self.dot_anim.start()

        # Pulsante configurazione
        self.config_btn = QPushButton()
        self.config_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.SETTINGS), "#6c757d")
        )
        self.config_btn.setIconSize(QSize(20, 20))
        self.config_btn.setFixedSize(32, 32)
        self.config_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.config_btn.setStyleSheet(
            """
            QPushButton { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 16px; }
            QPushButton:hover { background-color: #e9ecef; border-color: #ced4da; }
            QPushButton:pressed { background-color: #dee2e6; }
        """
        )
        self.config_btn.clicked.connect(self._toggle_mode)
        header_layout.addWidget(self.config_btn)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Container View e Config
        self.view_widget = QWidget()
        self.view_layout = QGridLayout(self.view_widget)
        self.view_layout.setContentsMargins(0, 4, 0, 0)
        self.view_layout.setSpacing(8)
        self.view_layout.setColumnStretch(0, 1)
        self.view_layout.setColumnStretch(1, 1)

        self.config_widget = QWidget()
        self.config_layout = QGridLayout(self.config_widget)
        self.config_layout.setContentsMargins(0, 4, 0, 0)
        self.config_layout.setSpacing(8)
        self.config_layout.setColumnStretch(0, 1)
        self.config_layout.setColumnStretch(1, 1)

        main_layout.addWidget(self.view_widget)
        main_layout.addWidget(self.config_widget)
        self.config_widget.setVisible(False)
        main_layout.addStretch()

        self.refresh_events()
        self._refresh_config()

    def _toggle_mode(self):
        if getattr(self, "_animating", False):
            return
        self._animating = True
        self._config_mode = not self._config_mode

        if hasattr(self, "dot_anim") and self.dot_anim:
            with suppress(RuntimeError):
                self.dot_anim.stop()

        self._stop_all_card_animations(self.view_layout)
        self._stop_all_card_animations(self.config_layout)
        self._animate_gear_button()

        if self._config_mode:
            self._animate_transition(self.view_widget, self.config_widget)
        else:
            self._animate_transition(self.config_widget, self.view_widget)
            QTimer.singleShot(600, self.refresh_events)

        QTimer.singleShot(800, self._restart_live_animations)

    def _stop_all_card_animations(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                w = item.widget()
                if hasattr(w, "pulse_anim") and w.pulse_anim:
                    with suppress(RuntimeError):
                        w.pulse_anim.stop()
                if hasattr(w, "timer") and w.timer:
                    with suppress(RuntimeError):
                        w.timer.stop()

    def _animate_gear_button(self):
        self._cleanup_gear_animations()
        original_pos = self.config_btn.pos()
        parallel_group = QParallelAnimationGroup(self)

        # Shake
        shake = QPropertyAnimation(self.config_btn, b"pos", self)
        shake.setDuration(500)
        shake.setKeyValueAt(0.0, original_pos)
        shake.setKeyValueAt(0.1, QPoint(original_pos.x() + 3, original_pos.y()))
        shake.setKeyValueAt(0.2, QPoint(original_pos.x() - 3, original_pos.y()))
        shake.setKeyValueAt(1.0, original_pos)
        parallel_group.addAnimation(shake)

        # Scale
        scale = QSequentialAnimationGroup(self)
        s1 = QPropertyAnimation(self.config_btn, b"iconSize", self)
        s1.setDuration(200)
        s1.setStartValue(QSize(20, 20))
        s1.setEndValue(QSize(30, 30))
        scale.addAnimation(s1)
        s2 = QPropertyAnimation(self.config_btn, b"iconSize", self)
        s2.setDuration(400)
        s2.setStartValue(QSize(30, 30))
        s2.setEndValue(QSize(20, 20))
        scale.addAnimation(s2)
        parallel_group.addAnimation(scale)

        parallel_group.start()
        self._gear_animation = parallel_group

    def _cleanup_gear_animations(self):
        if hasattr(self, "_gear_animation") and self._gear_animation:
            with suppress(RuntimeError):
                self._gear_animation.stop()

    def _animate_transition(self, from_widget, to_widget):
        to_widget.setVisible(True)
        to_widget.hide()

        def do_transition():
            from_widget.hide()
            to_widget.show()

        QTimer.singleShot(150, do_transition)

    def _restart_live_animations(self):
        if hasattr(self, "dot_anim") and self.dot_anim:
            with suppress(RuntimeError):
                self.dot_anim.start()
        self._animating = False

    def refresh_events(self):
        while self.view_layout.count() > 0:
            item = self.view_layout.takeAt(0)
            if item.widget():
                if hasattr(item.widget(), "cleanup"):
                    item.widget().cleanup()
                item.widget().deleteLater()
        QApplication.processEvents()

        config = config_manager.load_config()
        events = []
        if config.get("timbrature_autopilot_enabled", False):
            events.append(
                {
                    "name": "Timbrature Automatiche",
                    "time": config.get("timbrature_autopilot_time", "09:00"),
                    "icon": Icons.CLOCK,
                    "color": "#fd7e14",
                }
            )
        if config.get("scarico_oda_generale_autopilot_enabled", False):
            events.append(
                {
                    "name": "Scarico OdA Generale",
                    "time": config.get("scarico_oda_generale_autopilot_time", "09:00"),
                    "icon": Icons.DOWNLOAD,
                    "color": "#0d6efd",
                }
            )
        if config.get("ricerca_pdl_autopilot_enabled", False):
            events.append(
                {
                    "name": "Ricerca PDL",
                    "time": config.get("ricerca_pdl_autopilot_time", "09:00"),
                    "icon": Icons.SEARCH,
                    "color": "#198754",
                }
            )
        if config.get("report_email_autopilot_enabled", False):
            events.append(
                {
                    "name": f"Report Email (ogni {config.get('report_email_autopilot_interval_days', 7)}gg)",
                    "time": config.get("report_email_autopilot_time", "08:00"),
                    "icon": Icons.SEND,
                    "color": "#6f42c1",
                }
            )

        if not events:
            empty = QLabel("⏸️ Nessun bot programmato")
            empty.setStyleSheet(
                "color: #868e96; font-size: 13px; font-style: italic; padding: 20px; background-color: #f8f9fa; border-radius: 8px; border: 1px dashed #dee2e6;"
            )
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.view_layout.addWidget(empty, 0, 0, 1, 2)
            return

        for idx, event in enumerate(events):
            card = AutopilotEventCard(
                event["name"], event["time"], event["icon"], event["color"], self
            )
            self.view_layout.addWidget(card, idx // 2, idx % 2)

    def _refresh_config(self):
        while self.config_layout.count() > 0:
            item = self.config_layout.takeAt(0)
            if item.widget():
                if hasattr(item.widget(), "cleanup"):
                    item.widget().cleanup()
                item.widget().deleteLater()
        QApplication.processEvents()

        bots = [
            {
                "id": "timbrature",
                "name": "Timbrature Automatiche",
                "icon": Icons.CLOCK,
                "color": "#fd7e14",
            },
            {
                "id": "scarico_oda_generale",
                "name": "Scarico OdA Generale",
                "icon": Icons.DOWNLOAD,
                "color": "#0d6efd",
            },
            {
                "id": "ricerca_pdl",
                "name": "Ricerca PDL",
                "icon": Icons.SEARCH,
                "color": "#198754",
            },
        ]
        interval_tasks = [
            {
                "id": "report_email",
                "name": "Report Email ISAB",
                "icon": Icons.SEND,
                "color": "#6f42c1",
            },
        ]

        idx = 0
        for bot in bots:
            card = AutopilotConfigCard(
                bot["id"], bot["name"], bot["icon"], bot["color"], self
            )
            self.config_layout.addWidget(card, idx // 2, idx % 2)
            idx += 1
        for task in interval_tasks:
            card = AutopilotConfigCardWithInterval(
                task["id"], task["name"], task["icon"], task["color"], self
            )
            self.config_layout.addWidget(card, idx // 2, idx % 2)
            idx += 1
