"""SyncroJob - Don Ciro Engine.

Motore logico e fisico per la mascotte Don Ciro.
Separa la simulazione del comportamento dalla visualizzazione UI.
"""

import math
import random  # nosec B311
from enum import Enum, auto

from PySide6.QtCore import QObject, QPointF, QTimer, Signal

# Costanti di Configurazione
FPS = 60
DT = 1.0 / FPS
MIN_WALK_X = 70.0
MAX_WALK_X = 210.0
IDLE_ZONE_MIN = 130.0
IDLE_ZONE_MAX = 150.0
IDLE_CHANCE = 0.008
TURN_THRESHOLD = 90.0
TURN_ANGLE_LEFT = 0.0
TURN_ANGLE_RIGHT = 180.0

# Soglie Probabilit
ACTION_WATCH_THRESHOLD = 0.4
ACTION_TIE_THRESHOLD = 0.8


class DonState(Enum):
    """Stati della macchina a stati di Don Ciro."""

    WALKING = auto()
    TURNING = auto()
    IDLE = auto()
    ACTION_WATCH = auto()
    ACTION_TIE = auto()


class WeatherCond(Enum):
    """Condizioni meteorologiche simulate/reali per la mascotte."""

    NORMAL = auto()
    SUNNY = auto()
    RAINY = auto()
    WINDY = auto()


class DonCiroEngine(QObject):
    """Motore di simulazione per Don Ciro.

    Gestisce fisica, cinematica inversa e stati comportamentali.

    Inizializza la classe.
    """

    state_changed = Signal(object)
    physics_updated = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        # Parametri di Scala
        self._scale = 0.72
        self.THIGH_LEN = 30 * self._scale
        self.CALF_LEN = 30 * self._scale

        # Generatore random sicuro
        self._rng = random.SystemRandom()

        # Stato Interno
        self._state = DonState.WALKING
        self._weather = WeatherCond.NORMAL
        self._walk_phase = 0.0
        self._action_phase = 0.0
        self._walk_x = 60.0
        self._yaw_angle = 0.0
        self._look_dir = 1.0
        self._idle_time = 0

        # Fisica Molle
        self._tie_angle = 0.0
        self._tie_vel = 0.0
        self._jacket_flap = 0.0
        self._jacket_vel = 0.0

        # Timer Logica
        self.logic_timer = QTimer(self)
        self.logic_timer.timeout.connect(self.update_physics)
        self.logic_timer.start(int(DT * 1000))

    @property
    def scale(self) -> float:
        """Restituisce il fattore di scala della mascotte."""
        return self._scale

    @property
    def walk_x(self) -> float:
        """Restituisce la coordinata X corrente di cammino."""
        return self._walk_x

    @property
    def yaw_angle(self) -> float:
        """Restituisce l'angolo di rotazione (imbardata) della mascotte."""
        return self._yaw_angle

    @property
    def look_dir(self) -> float:
        """Restituisce la direzione dello sguardo (-1 per sinistra, 1 per destra)."""
        return self._look_dir

    @property
    def state(self) -> DonState:
        """Restituisce lo stato comportamentale corrente della mascotte."""
        return self._state

    @property
    def weather(self) -> WeatherCond:
        """Restituisce le condizioni meteorologiche correnti."""
        return self._weather

    @weather.setter
    def weather(self, value: WeatherCond) -> None:
        self._weather = value

    @property
    def tie_angle(self) -> float:
        """Restituisce l'angolo corrente di oscillazione della cravatta."""
        return self._tie_angle

    @property
    def jacket_flap(self) -> float:
        """Restituisce l'oscillazione corrente della giacca."""
        return self._jacket_flap

    def _update_accessories_physics(self, cos_y: float) -> None:
        # 1. Fisica Cravatta (Molla)
        target_t = (
            math.sin(self._walk_phase * 2 * math.pi) * 12 * cos_y if self._state == DonState.WALKING else 0.0
        )
        if self._weather == WeatherCond.WINDY:
            target_t += 20 * self._look_dir

        self._tie_vel += (target_t - self._tie_angle) * 60.0 * DT - self._tie_vel * 8.0 * DT
        self._tie_angle += self._tie_vel * DT

        # 2. Fisica Giacca (Flap)
        target_j = (
            -abs(math.sin(self._walk_phase * 2 * math.pi)) * 6 * cos_y
            if self._state == DonState.WALKING
            else 0.0
        )
        if self._weather == WeatherCond.WINDY:
            target_j -= 10 * self._look_dir

        self._jacket_vel += (target_j - self._jacket_flap) * 40.0 * DT - self._jacket_vel * 6.0 * DT
        self._jacket_flap += self._jacket_vel * DT

    def _handle_walking_state(self) -> None:
        """Gestisce lo stato di camminata."""
        speed = 0.65 * self._scale
        if self._weather == WeatherCond.RAINY:
            speed *= 1.2
        self._walk_x += speed * self._look_dir

        # Check inversioni o idle
        if IDLE_ZONE_MIN < self._walk_x < IDLE_ZONE_MAX and self._rng.random() < IDLE_CHANCE:
            self._start_idle()
        elif self._look_dir > 0 and self._walk_x >= MAX_WALK_X:
            self.trigger_turn(TURN_ANGLE_RIGHT)
        elif self._look_dir < 0 and self._walk_x <= MIN_WALK_X:
            self.trigger_turn(TURN_ANGLE_LEFT)

    def _handle_idle_state(self) -> None:
        """Gestisce lo stato di inattività."""
        self._idle_time -= 16
        if self._idle_time <= 0:
            self._pick_random_action()

    def _update_state_machine(self) -> None:
        # 3. Comportamento (Macchina a Stati)
        if self._state == DonState.WALKING:
            self._handle_walking_state()
        elif self._state == DonState.IDLE:
            self._handle_idle_state()

    def update_physics(self) -> None:
        """Ciclo di aggiornamento della fisica (60 FPS)."""
        cos_y = math.cos(math.radians(self._yaw_angle))

        self._update_accessories_physics(cos_y)
        self._update_state_machine()

        self.physics_updated.emit()

    def trigger_turn(self, _target_angle: float) -> None:
        """Segnala la necessit  di ruotare."""
        self._state = DonState.TURNING
        self.state_changed.emit(self._state)

    def set_yaw_complete(self, angle: float) -> None:
        """Chiamato dalla UI quando la rotazione  finita."""
        self._yaw_angle = angle
        # 90 gradi  il punto di inversione visiva
        self._look_dir = 1.0 if self._yaw_angle < TURN_THRESHOLD else -1.0
        self._state = DonState.WALKING
        self.state_changed.emit(self._state)

    def _start_idle(self) -> None:
        self._state = DonState.IDLE
        self._idle_time = self._rng.randint(1500, 2500)
        self.state_changed.emit(self._state)

    def _pick_random_action(self) -> None:
        r = self._rng.random()
        if r < ACTION_WATCH_THRESHOLD:
            self._state = DonState.ACTION_WATCH
        elif r < ACTION_TIE_THRESHOLD:
            self._state = DonState.ACTION_TIE
        else:
            self._state = DonState.WALKING
        self.state_changed.emit(self._state)

    def solve_ik(self, hip: QPointF, foot: QPointF) -> QPointF:
        """Risolve la cinematica inversa per un arto."""
        dx, dy = foot.x() - hip.x(), foot.y() - hip.y()
        dist = math.sqrt(dx * dx + dy * dy)
        max_d = (self.THIGH_LEN + self.CALF_LEN) * 0.96
        dist = min(dist, max_d)

        a, b, c = self.THIGH_LEN, self.CALF_LEN, dist
        try:
            co = (a * a + c * c - b * b) / (2 * a * c)
            alpha = math.acos(max(-1.0, min(1.0, co)))
        except (ValueError, ZeroDivisionError):
            alpha = 0.1

        cy = math.cos(math.radians(self._yaw_angle))
        base_angle = math.atan2(dy, dx)
        knee_angle = base_angle + (-alpha if cy >= 0 else alpha)

        return QPointF(hip.x() + math.cos(knee_angle) * a, hip.y() + math.sin(knee_angle) * a)
