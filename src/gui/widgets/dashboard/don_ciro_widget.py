"""SyncroJob - # ruff: noqa: PLR0913, PLR0915, C901.

Don Ciro - Widget Dashboard
Interfaccia Premium per la mascotte Don Ciro.
Refactored V9.1: Separazione completa tra Logica (Widget/Engine) e Rendering (DonCiroRenderer).
Integrazione con WeatherService per reattività climatica reale.
"""

from __future__ import annotations

import logging
from typing import Any

import shiboken6
from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPropertyAnimation,
    QTimer,
    Signal,
    Slot,
)
from PySide6.QtGui import (
    QPainter,
)
from PySide6.QtWidgets import QWidget

from src.core.mascot.don_ciro_engine import DonCiroEngine, DonState, WeatherCond
from src.core.weather_service import WeatherService
from src.gui.widgets.dashboard.don_ciro_renderer import DonCiroRenderer

logger = logging.getLogger(__name__)


class DonCiroWidget(QWidget):
    """Il Don Ciro: Visualizzazione 3D isometrica della mascotte aziendale.

    Inizializza la classe.
    """

    walk_phase_changed = Signal(float)
    action_phase_changed = Signal(float)
    yaw_angle_changed = Signal(float)
    blink_changed = Signal(float)
    label_phase_changed = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        fixed_width = 280
        fixed_height = 180
        self.setFixedWidth(fixed_width)
        self.setFixedHeight(fixed_height)

        # --- Componenti (SRP) ---
        self.engine = DonCiroEngine(self)
        self.renderer = DonCiroRenderer()
        self.weather_service = WeatherService.instance()

        # UI State (Solo visuale)
        self._walk_phase = 0.0
        self._action_phase = 0.0
        self._yaw_angle = 0.0
        self._blink = 1.0
        self._label_phase = 0.0

        self._init_animations()
        self._connect_signals()

    # ── Proprietà Animate (Qt) ──────────────────────────────────────────

    def get_walk_phase(self) -> float:
        """Ritorna la fase della camminata."""
        return self._walk_phase

    def set_walk_phase(self, v: float) -> None:
        """Imposta la fase della camminata."""
        if self._walk_phase != v:
            self._walk_phase = v
            # Sincronizza motore per la fisica
            self.engine._walk_phase = v
            self.walk_phase_changed.emit(v)
            self.update()

    walk_phase = Property(float, fget=get_walk_phase, fset=set_walk_phase, notify=walk_phase_changed)

    def get_action_phase(self) -> float:
        """Ritorna la fase dell'azione."""
        return self._action_phase

    def set_action_phase(self, v: float) -> None:
        """Imposta la fase dell'azione."""
        if self._action_phase != v:
            self._action_phase = v
            self.engine._action_phase = v
            self.action_phase_changed.emit(v)
            self.update()

    action_phase = Property(float, fget=get_action_phase, fset=set_action_phase, notify=action_phase_changed)

    def get_yaw_angle(self) -> float:
        """Ritorna l'angolo di imbardata."""
        return self._yaw_angle

    def set_yaw_angle(self, v: float) -> None:
        """Imposta l'angolo di imbardata."""
        if self._yaw_angle != v:
            self._yaw_angle = v
            self.engine._yaw_angle = v
            self.yaw_angle_changed.emit(v)
            self.update()

    yaw_angle = Property(float, fget=get_yaw_angle, fset=set_yaw_angle, notify=yaw_angle_changed)

    def get_blink(self) -> float:
        """Ritorna lo stato del battito ciglia."""
        return self._blink

    def set_blink(self, v: float) -> None:
        """Imposta lo stato del battito ciglia."""
        if self._blink != v:
            self._blink = v
            self.blink_changed.emit(v)
            self.update()

    blink = Property(float, fget=get_blink, fset=set_blink, notify=blink_changed)

    def get_label_phase(self) -> float:
        """Ritorna la fase del testo."""
        return self._label_phase

    def set_label_phase(self, v: float) -> None:
        """Imposta la fase del testo."""
        if self._label_phase != v:
            self._label_phase = v
            self.label_phase_changed.emit(v)
            self.update()

    label_phase = Property(float, fget=get_label_phase, fset=set_label_phase, notify=label_phase_changed)

    # ── Inizializzazione ────────────────────────────────────────────────

    def _init_animations(self) -> None:
        # Loop Camminata
        self.walk_anim = QPropertyAnimation(self, b"walk_phase")
        walk_duration = 1300
        self.walk_anim.setDuration(walk_duration)
        self.walk_anim.setStartValue(0.0)
        self.walk_anim.setEndValue(1.0)
        self.walk_anim.setLoopCount(-1)
        self.walk_anim.start()

        # Loop Testo Chrome
        self.label_anim = QPropertyAnimation(self, b"label_phase")
        label_duration = 4000
        self.label_anim.setDuration(label_duration)
        self.label_anim.setStartValue(0.0)
        self.label_anim.setEndValue(1.0)
        self.label_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.label_anim.setLoopCount(-1)
        self.label_anim.start()

        # Timer Battito Ciglia
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self._do_blink)
        blink_interval = 3500
        self.blink_timer.start(blink_interval)

    def _connect_signals(self) -> None:
        """Collega motore e servizi esterni."""
        self.engine.state_changed.connect(self._on_engine_state_changed)
        self.engine.physics_updated.connect(self.update)

        # Integrazione meteo reale
        self.weather_service.weather_data_ready.connect(self._on_real_weather_received)

    @Slot(object)
    def _on_engine_state_changed(self, state: DonState) -> None:
        """Gestisce i cambi di stato notificati dall'engine."""
        if not shiboken6.isValid(self):
            return
        if state == DonState.TURNING:
            self._trigger_ui_turn()
        elif state in (DonState.ACTION_WATCH, DonState.ACTION_TIE):
            self._trigger_ui_action()
        elif state == DonState.IDLE:
            self.walk_anim.pause()
        elif state == DonState.WALKING and self.walk_anim.state() == QPropertyAnimation.State.Paused:
            self.walk_anim.resume()

    @Slot(dict, dict)
    def _on_real_weather_received(self, weather: dict[str, Any], aqi: dict[str, Any]) -> None:
        """Adatta il comportamento di Don Ciro al meteo reale."""
        if not shiboken6.isValid(self):
            return
        curr = weather.get("current", {})
        code = curr.get("weather_code", 0)
        wind = curr.get("wind_gusts_10m", 0.0)

        # Soglie meteo
        code_rain_min = 51
        wind_threshold = 30

        if code >= code_rain_min:
            self.engine.weather = WeatherCond.RAINY
        elif wind > wind_threshold:
            self.engine.weather = WeatherCond.WINDY
        elif code <= 1:
            self.engine.weather = WeatherCond.SUNNY
        else:
            self.engine.weather = WeatherCond.NORMAL

    # ── Animazioni UI ───────────────────────────────────────────────────

    def _trigger_ui_turn(self) -> None:
        """Avvia l'animazione di rotazione nello Stack UI."""
        target = 180.0 if self.engine.look_dir > 0 else 0.0
        self.ta = QPropertyAnimation(self, b"yaw_angle")
        turn_duration = 800
        self.ta.setDuration(turn_duration)
        self.ta.setStartValue(self._yaw_angle)
        self.ta.setEndValue(target)
        self.ta.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.ta.finished.connect(
            lambda: self.engine.set_yaw_complete(target) if shiboken6.isValid(self) else None
        )
        self.ta.start()

    def _trigger_ui_action(self) -> None:
        """Avvia l'animazione di un'azione specifica."""
        self.act = QPropertyAnimation(self, b"action_phase")
        action_duration = 1500
        self.act.setDuration(action_duration)
        self.act.setStartValue(0.0)
        self.act.setEndValue(1.0)
        self.act.start()

    @Slot()
    def _do_blink(self) -> None:
        """Avvia il battito di ciglia."""
        if not shiboken6.isValid(self):
            return
        self.ba = QPropertyAnimation(self, b"blink")
        blink_duration = 120
        self.ba.setDuration(blink_duration)
        self.ba.setStartValue(1.0)
        self.ba.setKeyValueAt(0.5, 0.0)
        self.ba.setEndValue(1.0)
        self.ba.start()

    # ── Rendering ───────────────────────────────────────────────────────

    def paintEvent(self, event: Any) -> None:
        """Delega il rendering al DonCiroRenderer (SRP)."""
        p = QPainter(self)
        try:
            self.renderer.render(p, self, self.engine)
        finally:
            p.end()
