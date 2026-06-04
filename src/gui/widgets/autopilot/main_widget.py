"""SyncroJob - Autopilot Main Widget.

Widget coordinatore per la visualizzazione e configurazione dei bot programmati (Autopilot).
Gestisce la pianificazione delle attivitàautomatiche e la loro visualizzazione in tempo reale.
"""

from contextlib import suppress
from typing import Any

from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QSize,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.application.services import config_manager
from src.application.services.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    IconButton,
)
from src.infrastructure.utils.helpers import get_asset_path, get_colored_icon

from .config_cards import AutopilotConfigCard, AutopilotConfigCardWithInterval, BotVisualInfo
from .event_card import AutopilotEventCard, EventInfo


class AutopilotWidget(QWidget):
    """Widget che mostra e configura gli eventi programmati dei bot (Autopilot).

    Supporta una modalità di visualizzazione (Live) e una di configurazione.
    Utilizza animazioni per le transizioni e indicatori visivi per lo stato del sistema.

    Inizializza il widget Autopilot.

    Args:
      parent: Widget genitore.

    Attributes:
        bot_sync_requested: Segnale o attributo della classe.
    """

    bot_sync_requested = Signal(str)  # Segnale per richiedere il sync di un bot specifico

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._config_mode = False
        self.footer_left_widget: Any = None
        self.status_bar: Any = None
        self._animating = False
        self._gear_animation: QParallelAnimationGroup | None = None
        self._setup_ui()

        # Timer di refresh automatico degli eventi (ogni minuto)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_events)
        self.refresh_timer.start(60000)

    def set_footer_widget(self, footer_left_widget: Any) -> None:
        """Collega il widget del footer per aggiornamenti contestuali."""
        self.footer_left_widget = footer_left_widget

    def set_status_bar(self, status_bar: Any) -> None:
        """Collega la barra di stato per segnalare attivitàdell'autopilot."""
        self.status_bar = status_bar

    def _setup_ui(self) -> None:
        """Configura il layout, l'header LIVE e i container per le card."""
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(600)
        self.setMaximumWidth(600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self._setup_header(main_layout)
        self._setup_containers(main_layout)

        self.refresh_events()
        self._refresh_config()

    def _setup_header(self, layout: QVBoxLayout) -> None:
        """Configura l'header con titolo e indicatore live."""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        title = QLabel("Autopilot")
        title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['text_dark']};")
        header_layout.addWidget(title)

        self._setup_live_indicator(header_layout)
        self._setup_config_button(header_layout)

        header_layout.addStretch()
        layout.addLayout(header_layout)

    def _setup_live_indicator(self, layout: QHBoxLayout) -> None:
        """Crea e anima l'indicatore LIVE."""
        self.live_container = QWidget()
        live_layout = QHBoxLayout(self.live_container)
        live_layout.setContentsMargins(5, 0, 5, 0)
        live_layout.setSpacing(5)

        self.live_dot = QLabel()
        self.live_dot.setFixedSize(8, 8)
        self.live_dot.setStyleSheet(
            f"background-color: {COLORS['success_green']}; border-radius: 4px; border: 1px solid {COLORS['success_dark']};"
        )

        self.live_text = QLabel("LIVE")
        self.live_text.setStyleSheet(
            f"color: {COLORS['success_green']}; font-size: 10px; font-weight: 800; letter-spacing: 1px;"
        )

        live_layout.addWidget(self.live_dot)
        live_layout.addWidget(self.live_text)
        layout.addWidget(self.live_container)

        self._start_live_animation()

    def _start_live_animation(self) -> None:
        """Avvia l'animazione di pulsazione dell'indicatore LIVE."""
        self.dot_opacity = QGraphicsOpacityEffect(self.live_container)
        self.live_container.setGraphicsEffect(self.dot_opacity)
        self.dot_anim = QPropertyAnimation(self.dot_opacity, b"opacity")
        self.dot_anim.setDuration(1000)
        self.dot_anim.setStartValue(0.3)
        self.dot_anim.setEndValue(1.0)
        self.dot_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.dot_anim.setLoopCount(-1)
        self.dot_anim.start()

    def _setup_config_button(self, layout: QHBoxLayout) -> None:
        """Configura il pulsante di accesso alle impostazioni."""
        self.config_btn = IconButton()
        self.config_btn.setIcon(get_colored_icon(get_asset_path(Icons.SETTINGS), COLORS["text_muted"]))
        self.config_btn.setIconSize(QSize(20, 20))
        self.config_btn.setFixedSize(32, 32)
        self.config_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.config_btn.setStyleSheet(
            f"QPushButton {{ background-color: {COLORS['bg_light']}; border: 1px solid {COLORS['border_light']}; border-radius: 16px; }} "
            f"QPushButton:hover {{ background-color: {COLORS['bg_hover']}; border-color: {COLORS['border_medium']}; }} "
            f"QPushButton:pressed {{ background-color: {COLORS['bg_alt']}; }}"
        )
        self.config_btn.clicked.connect(self._toggle_mode)
        layout.addWidget(self.config_btn)

    def _setup_containers(self, layout: QVBoxLayout) -> None:
        """Crea i container per la vista live e quella di configurazione."""
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

        layout.addWidget(self.view_widget)
        layout.addWidget(self.config_widget)
        self.config_widget.setVisible(False)
        layout.addStretch()

    def _toggle_mode(self) -> None:
        """Passa dalla modalità visualizzazione alla modalità configurazione con animazione."""
        if self._animating:
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

    def _stop_all_card_animations(self, layout: QGridLayout) -> None:
        """Ferma preventivamente tutte le animazioni attive nelle card dei layout."""
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None and item.widget():
                w = item.widget()
                if w:
                    if hasattr(w, "pulse_anim") and w.pulse_anim:
                        with suppress(Exception):
                            w.pulse_anim.stop()
                    if hasattr(w, "timer") and w.timer:
                        with suppress(Exception):
                            w.timer.stop()

    def _animate_gear_button(self) -> None:
        """Esegue un'animazione di scuotimento e scala sull'icona delle impostazioni."""
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

    def _cleanup_gear_animations(self) -> None:
        """Ferma in modo sicuro l'animazione dell'ingranaggio."""
        if self._gear_animation:
            with suppress(RuntimeError):
                self._gear_animation.stop()

    def _animate_transition(self, from_widget: QWidget, to_widget: QWidget) -> None:
        """Gestisce il cross-fade tra i widget di vista e configurazione."""
        to_widget.setVisible(True)
        to_widget.hide()

        def do_transition() -> None:
            from_widget.hide()
            to_widget.show()

        QTimer.singleShot(150, do_transition)

    def _restart_live_animations(self) -> None:
        """Ripristina le animazioni dell'indicatore LIVE dopo una transizione."""
        if hasattr(self, "dot_anim") and self.dot_anim:
            with suppress(RuntimeError):
                self.dot_anim.start()
        self._animating = False

    def refresh_events(self) -> None:
        """Ricarica la lista degli eventi programmati leggendo la configurazione corrente."""
        self._clear_layout(self.view_layout)

        config = config_manager.load_config()
        events: list[EventInfo] = self._get_enabled_events(config)

        if not events:
            self._show_empty_message()
            return

        for idx, event in enumerate(events):
            card = AutopilotEventCard(event, self)
            card.sync_requested.connect(self.bot_sync_requested.emit)
            self.view_layout.addWidget(card, idx // 2, idx % 2)

    def _clear_layout(self, layout: QGridLayout) -> None:
        """Rimuove tutti i widget da un layout in modo sicuro."""
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item and (widget := item.widget()):
                if hasattr(widget, "cleanup"):
                    widget.cleanup()
                widget.deleteLater()

    def _get_enabled_events(self, config: dict[str, Any]) -> list[EventInfo]:
        """Ritorna la lista degli eventi abilitati dalla configurazione."""
        events: list[EventInfo] = []
        if config.get("timbrature_autopilot_enabled", False):
            events.append(
                {
                    "id": "timbrature",
                    "module_id": "timbrature",
                    "name": "Timbrature Automatiche",
                    "time": config.get("timbrature_autopilot_time", "09:00"),
                    "icon": Icons.CLOCK,
                    "color": COLORS["warning_orange"],
                }
            )
        if config.get("scarico_oda_generale_autopilot_enabled", False):
            events.append(
                {
                    "id": "scarico_oda_generale",
                    "module_id": "oda",
                    "name": "Scarico OdA Generale",
                    "time": config.get("scarico_oda_generale_autopilot_time", "09:00"),
                    "icon": Icons.DOWNLOAD,
                    "color": COLORS["primary_dark"],
                }
            )
        if config.get("ricerca_pdl_autopilot_enabled", False):
            events.append(
                {
                    "id": "ricerca_pdl",
                    "module_id": "pdl",
                    "name": "Ricerca PDL",
                    "time": config.get("ricerca_pdl_autopilot_time", "09:00"),
                    "icon": Icons.SEARCH,
                    "color": COLORS["success_dark"],
                }
            )
        if config.get("report_email_autopilot_enabled", False):
            events.append(
                {
                    "id": "report_email",
                    "module_id": "none",
                    "name": f"Report Email (ogni {config.get('report_email_autopilot_interval_days', 7)}gg)",
                    "time": config.get("report_email_autopilot_time", "08:00"),
                    "icon": Icons.SEND,
                    "color": COLORS["purple"],
                }
            )
        if config.get("certificati_autopilot_enabled", False):
            events.append(
                {
                    "id": "certificati",
                    "module_id": "contabilita",
                    "name": f"Certificati Campione (ogni {config.get('certificati_autopilot_interval_days', 1)}gg)",
                    "time": config.get("certificati_autopilot_time", "08:30"),
                    "icon": Icons.FILE_TEXT,
                    "color": COLORS["teal_accent"],
                }
            )
        return events

    def _show_empty_message(self) -> None:
        """Mostra un messaggio quando non ci sono eventi programmati."""
        empty = QLabel("    Nessun bot programmato")
        empty.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 13px; font-style: italic; padding: 20px; "
            f"background-color: {COLORS['bg_light']}; border-radius: 8px; border: 1px dashed {COLORS['border_light']};"
        )
        empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.view_layout.addWidget(empty, 0, 0, 1, 2)

    def _refresh_config(self) -> None:
        """Ricarica i widget di configurazione per ogni bot supportato dall'autopilot."""
        self._clear_layout(self.config_layout)

        bots: list[BotVisualInfo] = [
            {
                "bot_id": "timbrature",
                "bot_name": "Timbrature Automatiche",
                "icon_path": Icons.CLOCK,
                "color": COLORS["warning_orange"],
            },
            {
                "bot_id": "scarico_oda_generale",
                "bot_name": "Scarico OdA Generale",
                "icon_path": Icons.DOWNLOAD,
                "color": COLORS["primary_dark"],
            },
            {
                "bot_id": "ricerca_pdl",
                "bot_name": "Ricerca PDL",
                "icon_path": Icons.SEARCH,
                "color": COLORS["success_dark"],
            },
        ]
        interval_tasks: list[BotVisualInfo] = [
            {
                "bot_id": "report_email",
                "bot_name": "Report Email ISAB",
                "icon_path": Icons.SEND,
                "color": COLORS["purple"],
            },
            {
                "bot_id": "certificati",
                "bot_name": "Certificati Campione",
                "icon_path": Icons.FILE_TEXT,
                "color": COLORS["teal_accent"],
            },
        ]

        idx = 0
        for bot in bots:
            card = AutopilotConfigCard(bot, parent=self)
            self.config_layout.addWidget(card, idx // 2, idx % 2)
            idx += 1
        for task in interval_tasks:
            card_with_interval = AutopilotConfigCardWithInterval(task, parent=self)
            self.config_layout.addWidget(card_with_interval, idx // 2, idx % 2)
            idx += 1
