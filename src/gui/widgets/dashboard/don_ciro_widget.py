"""
SyncroJob - Don Ciro 8.2 (Zero-Warning Edition)
- Fix Artifact Anatomici: Eliminato l'effetto "pisello" della giacca e rifinito il collo.
- Spalle Squadrate: Busto a "V" per un look Enterprise solido.
- Animazione Testo Pro: Effetto Cromo metallico, Glow pulsante e Shimmer di particelle.
- Fisica della Giacca: Flap realistici 3D.
- Qualità Codice: 0 segnalazioni Ruff, Mypy e Refurb.
"""

import logging
import math
import random
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any

from PyQt6.QtCore import (  # type: ignore[attr-defined]
    QEasingCurve,
    QPointF,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
    pyqtProperty,
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class DonState(Enum):
    """Stati della macchina a stati di Don Ciro."""

    WALKING = 1
    TURNING = 2
    IDLE = 3
    ACTION_WATCH = 4
    ACTION_TIE = 5


class WeatherCond(Enum):
    """Condizioni meteorologiche simulate."""

    NORMAL = 1
    SUNNY = 2
    RAINY = 3
    WINDY = 4


@dataclass
class RenderItem:
    """Elemento della coda di rendering 3D con ordinamento Z."""

    z_depth: float
    draw_func: Callable[..., None]
    args: tuple[Any, ...]


class DonCiroWidget(QWidget):
    """Il Don Ciro v8.2: Anatomia corretta e Interfaccia Premium."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setFixedHeight(180)

        # Stato AI
        self._state = DonState.WALKING
        self._weather = WeatherCond.NORMAL
        self._walk_phase = 0.0
        self._action_phase = 0.0
        self._walk_x = 60.0
        self._yaw_angle = 0.0
        self._look_dir = 1.0
        self._idle_time = 0

        # Fisica Secondaria
        self._tie_angle = 0.0
        self._tie_vel = 0.0
        self._jacket_flap = 0.0
        self._jacket_vel = 0.0

        # UI & Perspective
        self._blink = 1.0
        self._label_phase = 0.0
        self._scale = 0.72
        self.THIGH_LEN = 30 * self._scale
        self.CALF_LEN = 30 * self._scale

        # Palette Cinematic
        self.C_SKIN = QColor("#FFDAB9")
        self.C_SUIT = QColor("#223344")
        self.C_SHIRT = QColor("#FFFFFF")
        self.C_TIE = QColor("#C0392B")
        self.C_HAIR = QColor("#1A1A1A")
        self.C_SHOE = QColor("#0A0A0A")

        self._init_engine()

    @pyqtProperty(float)
    def walk_phase(self) -> float:
        """Fase della camminata (0.0 - 1.0)."""
        return self._walk_phase

    @walk_phase.setter  # type: ignore[no-redef]
    def walk_phase(self, v: float) -> None:
        self._walk_phase = v
        self.update()

    @pyqtProperty(float)
    def action_phase(self) -> float:
        """Fase dell'azione idle (0.0 - 1.0)."""
        return self._action_phase

    @action_phase.setter  # type: ignore[no-redef]
    def action_phase(self, v: float) -> None:
        self._action_phase = v
        self.update()

    @pyqtProperty(float)
    def yaw_angle(self) -> float:
        """Angolo di rotazione 3D (0 - 180)."""
        return self._yaw_angle

    @yaw_angle.setter  # type: ignore[no-redef]
    def yaw_angle(self, v: float) -> None:
        self._yaw_angle = v
        self.update()

    @pyqtProperty(float)
    def blink(self) -> float:
        """Stato di chiusura occhi (0.0 - 1.0)."""
        return self._blink

    @blink.setter  # type: ignore[no-redef]
    def blink(self, v: float) -> None:
        self._blink = v
        self.update()

    @pyqtProperty(float)
    def label_phase(self) -> float:
        """Fase animazione etichetta testo."""
        return self._label_phase

    @label_phase.setter  # type: ignore[no-redef]
    def label_phase(self, v: float) -> None:
        self._label_phase = v
        self.update()

    def _init_engine(self) -> None:
        # Camminata
        self.walk_anim = QPropertyAnimation(self, b"walk_phase")
        self.walk_anim.setDuration(1300)
        self.walk_anim.setStartValue(0.0)
        self.walk_anim.setEndValue(1.0)
        self.walk_anim.setLoopCount(-1)
        self.walk_anim.start()

        # Testo
        self.label_anim = QPropertyAnimation(self, b"label_phase")
        self.label_anim.setDuration(4000)
        self.label_anim.setStartValue(0.0)
        self.label_anim.setEndValue(1.0)
        self.label_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.label_anim.setLoopCount(-1)
        self.label_anim.start()

        self.logic_timer = QTimer(self)
        self.logic_timer.timeout.connect(self._update_logic)
        self.logic_timer.start(16)

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self._do_blink)
        self.blink_timer.start(3500)

        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self._random_weather)
        self.weather_timer.start(20000)

    def _random_weather(self) -> None:
        """Cambia casualmente le condizioni climatiche simulate."""
        self._weather = random.choice(list(WeatherCond))  # noqa: S311

    def _update_logic(self) -> None:
        """Aggiorna fisica e logica comportamentale."""
        dt = 0.016
        cos_y = math.cos(math.radians(self._yaw_angle))

        # Fisica Cravatta (Molla)
        target_t = (
            math.sin(self._walk_phase * 2 * math.pi) * 12 * cos_y if self._state == DonState.WALKING else 0.0
        )
        if self._weather == WeatherCond.WINDY:
            target_t += 20 * self._look_dir
        self._tie_vel += (target_t - self._tie_angle) * 60.0 * dt - self._tie_vel * 8.0 * dt
        self._tie_angle += self._tie_vel * dt

        # Fisica Giacca (Flap posteriore)
        target_j = (
            -abs(math.sin(self._walk_phase * 2 * math.pi)) * 6 * cos_y
            if self._state == DonState.WALKING
            else 0.0
        )
        if self._weather == WeatherCond.WINDY:
            target_j -= 10 * self._look_dir
        self._jacket_vel += (target_j - self._jacket_flap) * 40.0 * dt - self._jacket_vel * 6.0 * dt
        self._jacket_flap += self._jacket_vel * dt

        if self._state == DonState.WALKING:
            speed = 0.65 * self._scale
            if self._weather == WeatherCond.RAINY:
                speed *= 1.2
            self._walk_x += speed * self._look_dir
            if 130 < self._walk_x < 150 and random.random() < 0.008:  # noqa: PLR2004, S311
                self._start_idle()
            elif self._look_dir > 0 and self._walk_x >= 210:  # noqa: PLR2004
                self._turn(180.0)
            elif self._look_dir < 0 and self._walk_x <= 70:  # noqa: PLR2004
                self._turn(0.0)
        elif self._state == DonState.IDLE:
            self._idle_time -= 16
            if self._idle_time <= 0:
                r = random.random()  # noqa: S311
                if r < 0.4:  # noqa: PLR2004
                    self._start_action(DonState.ACTION_WATCH)
                elif r < 0.8:  # noqa: PLR2004
                    self._start_action(DonState.ACTION_TIE)
                else:
                    self._resume_walk()
        self.update()

    def _turn(self, t: float) -> None:
        """Inizia la rotazione del personaggio."""
        self._state = DonState.TURNING
        self.ta = QPropertyAnimation(self, b"yaw_angle")
        self.ta.setDuration(800)
        self.ta.setStartValue(self._yaw_angle)
        self.ta.setEndValue(t)
        self.ta.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.ta.finished.connect(self._end_turn)
        self.ta.start()

    def _end_turn(self) -> None:
        """Conclude la rotazione e riprende la marcia."""
        self._look_dir = 1.0 if self._yaw_angle < 90 else -1.0  # noqa: PLR2004
        self._state = DonState.WALKING

    def _start_idle(self) -> None:
        """Entra in stato di attesa casuale."""
        self._state = DonState.IDLE
        self.walk_anim.pause()
        self._idle_time = random.randint(1500, 2500)  # noqa: S311

    def _resume_walk(self) -> None:
        """Riprende la camminata."""
        self._state = DonState.WALKING
        self.walk_anim.resume()

    def _start_action(self, a: DonState) -> None:
        """Inizia un'azione di disturbo idle (orologio o cravatta)."""
        self._state = a
        self.act = QPropertyAnimation(self, b"action_phase")
        self.act.setDuration(1500)
        self.act.setStartValue(0.0)
        self.act.setEndValue(1.0)
        self.act.finished.connect(self._resume_walk)
        self.act.start()

    def _do_blink(self) -> None:
        """Esegue il battito di ciglia."""
        self.ba = QPropertyAnimation(self, b"blink")
        self.ba.setDuration(120)
        self.ba.setStartValue(1.0)
        self.ba.setKeyValueAt(0.5, 0.0)
        self.ba.setEndValue(1.0)
        self.ba.start()

    def paintEvent(self, event: Any) -> None:  # noqa: ANN401, N802
        """Metodo di disegno principale."""
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.save()
        p.translate(self._walk_x, 150)
        self._draw_dynamic_shadow(p)
        self._render_ciro_3d(p)
        p.restore()
        self._draw_label(p)
        self._draw_weather_fx(p)

    def _draw_weather_fx(self, p: QPainter) -> None:
        """Effetti grafici del meteo a schermo intero."""
        if self._weather == WeatherCond.RAINY:
            p.setPen(QPen(QColor(255, 255, 255, 40), 1))
            for i in range(15):
                rx, ry = (self._walk_phase * 500 + i * 30) % 280, (self._walk_phase * 800 + i * 40) % 180
                p.drawLine(QPointF(rx, ry), QPointF(rx - 5, ry + 15))

    def _draw_dynamic_shadow(self, p: QPainter) -> None:
        """Ombra proiettata al suolo che reagisce al rimbalzo."""
        bob = abs(math.sin(self._walk_phase * 2 * math.pi)) if self._state == DonState.WALKING else 0.0
        s = (42 - bob * 4) * self._scale
        g = QRadialGradient(0, 0, s)
        g.setColorAt(0, QColor(0, 0, 0, int(80 - bob * 20)))
        g.setColorAt(1, Qt.GlobalColor.transparent)
        p.setBrush(QBrush(g))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(0, 0), s, 8 * self._scale)

    def _render_ciro_3d(self, p: QPainter) -> None:
        """Motore di proiezione 3D isometrica."""
        f = self._walk_phase * 2 * math.pi
        rad = math.radians(self._yaw_angle)
        cos_y, sin_y = math.cos(rad), math.sin(rad)
        sq = 1.0 - 0.03 * max(0.0, math.sin(f * 2)) if self._state == DonState.WALKING else 1.0
        by = (-68 - (abs(math.sin(f * 2)) * 6 if self._state == DonState.WALKING else 0)) * self._scale
        ln = (0.08 if self._state == DonState.WALKING else 0.0) * cos_y
        if self._weather == WeatherCond.WINDY:
            ln += 0.1 * self._look_dir

        hp_c = QPointF(0, by)
        sy = by - 42 * self._scale * sq
        sc = QPointF(ln * 12 * self._scale, sy)
        hd_p = QPointF(sc.x() + ln * 8 * self._scale, sy - 16 * self._scale * sq)

        if self._state == DonState.WALKING:
            sl, sh = 22 * self._scale * abs(cos_y), 12 * self._scale
            pr, pl = math.sin(f), math.sin(f + math.pi)
            frx, fry = pr * sl, (-abs(pr * sh) if pr > 0 else 0.0)
            flx, fly = pl * sl, (-abs(pl * sh) if pl > 0 else 0.0)
        else:
            frx, fry, flx, fly = 5 * self._scale, 0.0, -5 * self._scale, 0.0

        wo = 11 * self._scale
        r_hp, l_hp = QPointF(-wo * sin_y, by), QPointF(wo * sin_y, by)
        r_sh, l_sh = QPointF(sc.x() - wo * sin_y, sy), QPointF(sc.x() + wo * sin_y, sy)
        kn_r = self._solve_ik(r_hp, QPointF(r_hp.x() + frx, fry))
        kn_l = self._solve_ik(l_hp, QPointF(l_hp.x() + flx, fly))

        ar_p = QPointF(r_sh.x(), sy + 24 * self._scale)
        al_p = QPointF(l_sh.x(), sy + 24 * self._scale)
        if self._state == DonState.WALKING:
            asw = math.sin(f) * 18 * self._scale * cos_y
            ar_p.setX(ar_p.x() - asw)
            al_p.setX(al_p.x() + asw)
        elif self._state == DonState.ACTION_WATCH:
            ap = math.sin(self._action_phase * math.pi)
            al_p = QPointF(l_sh.x() + 10 * self._scale * cos_y, sy + 10 * self._scale - 10 * self._scale * ap)
            hd_p.setX(hd_p.x() + 5 * self._scale * ap * cos_y)
            hd_p.setY(hd_p.y() + 5 * self._scale * ap)
        elif self._state == DonState.ACTION_TIE:
            ap = math.sin(self._action_phase * math.pi)
            ar_p = QPointF(r_sh.x() - 5 * self._scale * cos_y, sy + 15 * self._scale - 12 * self._scale * ap)

        rq: list[RenderItem] = []
        rz, lz = wo * cos_y, -wo * cos_y
        rq.extend(
            (
                RenderItem(-rz, self._draw_leg, (r_hp, kn_r, QPointF(r_hp.x() + frx, fry), rz, cos_y)),
                RenderItem(-lz, self._draw_leg, (l_hp, kn_l, QPointF(l_hp.x() + flx, fly), lz, cos_y)),
                RenderItem(-rz, self._draw_arm, (r_sh, ar_p, rz, True)),
                RenderItem(-lz, self._draw_arm, (l_sh, al_p, lz, False)),
                RenderItem(0.0, self._draw_torso, (hp_c, sc, cos_y, sin_y)),
                RenderItem(0.5, self._draw_head, (hd_p, cos_y, sin_y)),
            )
        )
        rq.sort(key=lambda x: x.z_depth, reverse=True)
        p.save()
        p.scale(1.0, sq)
        for i in rq:
            i.draw_func(p, *i.args)
        p.restore()

    def _solve_ik(self, h: QPointF, f: QPointF) -> QPointF:
        """Risolve la cinematica inversa per le gambe."""
        dx, dy = f.x() - h.x(), f.y() - h.y()
        dist = math.sqrt(dx * dx + dy * dy)
        max_d = (self.THIGH_LEN + self.CALF_LEN) * 0.96
        dist = min(dist, max_d)
        a, b, c = self.THIGH_LEN, self.CALF_LEN, dist
        try:
            co = (a * a + c * c - b * b) / (2 * a * c)
            al = math.acos(max(-1.0, min(1.0, co)))
        except (ValueError, ZeroDivisionError):
            al = 0.1
        cy = math.cos(math.radians(self._yaw_angle))
        ba = math.atan2(dy, dx)
        ka = ba + (-al if cy >= 0 else al)
        return QPointF(h.x() + math.cos(ka) * a, h.y() + math.sin(ka) * a)

    def _draw_leg(self, p: QPainter, h: QPointF, k: QPointF, f: QPointF, z: float, cy: float) -> None:  # noqa: PLR0913
        """Disegna una gamba 3D."""
        op = 0.8 if z < 0 else 1.0
        p.setOpacity(op)
        c = self.C_SUIT.darker(110 if z < 0 else 100)
        path = QPainterPath()
        path.moveTo(h)
        path.lineTo(k)
        path.lineTo(f)
        p.setPen(QPen(c, 11 * self._scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawPath(path)
        self._draw_shoe(p, QPointF(f.x(), f.y() + 3 * self._scale), cy, z)
        p.setOpacity(1.0)

    def _draw_shoe(self, p: QPainter, f: QPointF, cy: float, z: float) -> None:
        """Disegna la scarpa Boutique con riflessi."""
        p.save()
        p.translate(f)
        p.scale(1.0 if cy >= 0 else -1.0, 1.0)
        s = self._scale
        if f.y() > -1:
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(QColor(0, 0, 0, 120)))
            p.drawEllipse(QRectF(-8 * s, -2 * s, 26 * s, 5 * s))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(self.C_SHOE))
        path = QPainterPath()
        path.moveTo(-8 * s, 0)
        path.lineTo(18 * s, 0)
        path.lineTo(18 * s, -4 * s)
        path.quadTo(15 * s, -10 * s, 5 * s, -11 * s)
        path.lineTo(-8 * s, -11 * s)
        path.closeSubpath()
        p.drawPath(path)
        p.setBrush(QBrush(QColor("#111111")))
        p.drawRect(QRectF(-8 * s, -3 * s, 8 * s, 3 * s))
        p.setBrush(QBrush(QColor(255, 255, 255, 100 if self._weather == WeatherCond.SUNNY else 40)))
        p.drawEllipse(QRectF(8 * s, -10 * s, 6 * s, 2 * s))
        p.restore()

    def _draw_arm(self, p: QPainter, sh: QPointF, hand: QPointF, z: float, is_right: bool) -> None:
        """Disegna un braccio con eventuale ombrello."""
        op = 0.8 if z < 0 else 1.0
        p.setOpacity(op)
        p.setPen(
            QPen(
                self.C_SUIT.darker(105 if z < 0 else 100),
                7 * self._scale,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            )
        )
        p.drawLine(sh, hand)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(self.C_SKIN.darker(105 if z < 0 else 100)))
        p.drawEllipse(hand, 5 * self._scale, 5 * self._scale)
        if self._weather == WeatherCond.RAINY and is_right and z >= 0:
            p.save()
            p.translate(hand)
            p.setPen(QPen(QColor(50, 50, 50), 2 * self._scale))
            p.drawLine(QPointF(0, 0), QPointF(0, -35 * self._scale))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(QColor("#111111")))
            p.drawChord(
                QRectF(-20 * self._scale, -45 * self._scale, 40 * self._scale, 20 * self._scale), 0, 180 * 16
            )
            p.restore()
        p.setOpacity(1.0)

    def _draw_torso(self, p: QPainter, hp: QPointF, sh: QPointF, cy: float, sy: float) -> None:  # noqa: PLR0915
        """Disegna il busto enterprise a V con collo e colletto."""
        s = self._scale
        w = 22 * s * (0.5 + 0.5 * abs(sy))
        ch = 5 * s * cy

        # FIX SILHOUETTE: Collo & Colletto
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(self.C_SKIN.darker(115)))
        p.drawRect(QRectF(sh.x() + ch - 4 * s, sh.y() - 5 * s, 8 * s, 8 * s))
        p.setBrush(QBrush(self.C_SHIRT))
        coll = QPainterPath()
        coll.moveTo(sh.x() + ch - 9 * s, sh.y())
        coll.lineTo(sh.x() + ch + 9 * s, sh.y())
        coll.lineTo(sh.x() + ch, sh.y() + 6 * s)
        coll.closeSubpath()
        p.drawPath(coll)

        # Flap Giacca
        if self._jacket_flap != 0 and sy < 0.3:  # noqa: PLR2004
            p.setBrush(QBrush(self.C_SUIT.darker(135)))
            j_path = QPainterPath()
            j_path.moveTo(hp.x() + ch, hp.y())
            j_path.lineTo(hp.x() + ch - (15 * s + self._jacket_flap) * cy, hp.y() + 8 * s)
            j_path.lineTo(hp.x() + ch, hp.y() + 5 * s)
            p.drawPath(j_path)

        # Busto a V
        path = QPainterPath()
        path.moveTo(sh.x() - w + ch, sh.y())
        path.lineTo(sh.x() + w + ch, sh.y())
        path.lineTo(hp.x() + w * 0.6 + ch, hp.y())
        path.lineTo(hp.x() - w * 0.6 + ch, hp.y())
        path.closeSubpath()
        grad = QLinearGradient(sh, hp)
        grad.setColorAt(0, self.C_SUIT.lighter(110))
        grad.setColorAt(1, self.C_SUIT.darker(120))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(self.C_SUIT.darker(145), 1.2 * s))
        p.drawPath(path)

        if sy > 0:
            p.setBrush(QBrush(self.C_SHIRT))
            p.setPen(Qt.PenStyle.NoPen)
            shirt = QPainterPath()
            shirt.moveTo(sh.x() + ch - 7 * s, sh.y() + 2 * s)
            shirt.lineTo(sh.x() + ch + 7 * s, sh.y() + 2 * s)
            shirt.lineTo(sh.x() + ch, sh.y() + 18 * s)
            p.drawPath(shirt)
            p.save()
            p.translate(sh.x() + ch, sh.y() + 2 * s)
            p.rotate(self._tie_angle)
            p.setBrush(QBrush(self.C_TIE))
            tie = QPainterPath()
            tie.moveTo(0, 0)
            tie.lineTo(-3.5 * s, 5 * s)
            tie.lineTo(0, 32 * s)
            tie.lineTo(3.5 * s, 5 * s)
            p.drawPath(tie)
            p.restore()

    def _draw_head(self, p: QPainter, pos: QPointF, cy: float, sy: float) -> None:  # noqa: PLR0915
        """Disegna la testa 3D con prospettiva capelli e occhi."""
        s = self._scale
        ev = max(0.0, min(1.0, abs(sy) * 2.5))
        # Orecchio Lontano
        ecb = self.C_SKIN.darker(140)
        p.setOpacity(ev)
        p.setBrush(QBrush(ecb))
        p.setPen(QPen(ecb.darker(120), 0.6 * s))
        if cy > 0:
            p.drawEllipse(QRectF(pos.x() + 10 * s * cy + 8 * s, pos.y() - 4 * s, 5 * s, 9 * s))
        else:
            p.drawEllipse(QRectF(pos.x() + 10 * s * cy - 13 * s, pos.y() - 4 * s, 5 * s, 9 * s))
        # Viso
        p.setOpacity(1.0)
        p.setPen(Qt.PenStyle.NoPen)
        grad = QRadialGradient(pos, 20 * s)
        grad.setColorAt(0, self.C_SKIN.lighter(105))
        grad.setColorAt(1, self.C_SKIN.darker(115))
        p.setBrush(QBrush(grad))
        p.drawEllipse(pos, 16 * s, 18 * s)
        # Orecchio Vicino
        ecf = self.C_SKIN.darker(120)
        p.setBrush(QBrush(ecf))
        p.setPen(QPen(ecf.darker(120), 0.6 * s))
        if cy > 0:
            p.drawEllipse(QRectF(pos.x() + 10 * s * cy - 13 * s, pos.y() - 4 * s, 5 * s, 9 * s))
        else:
            p.drawEllipse(QRectF(pos.x() + 10 * s * cy + 8 * s, pos.y() - 4 * s, 5 * s, 9 * s))
        # Capelli
        p.setBrush(QBrush(self.C_HAIR))
        p.setPen(Qt.PenStyle.NoPen)
        h_path = QPainterPath()
        ho = 7 * s * cy
        h_path.moveTo(pos.x() - 17 * s, pos.y() + 3 * s)
        h_path.cubicTo(
            pos.x() - 22 * s + ho,
            pos.y() - 35 * s,
            pos.x() + 22 * s + ho,
            pos.y() - 35 * s,
            pos.x() + 17 * s,
            pos.y() + 3 * s,
        )
        h_path.lineTo(pos.x() + 14 * s, pos.y() - 2 * s)
        h_path.lineTo(pos.x() + 12 * s * cy, pos.y() - 15 * s)
        h_path.lineTo(pos.x() - 14 * s, pos.y() - 2 * s)
        p.drawPath(h_path)
        # Occhi
        if sy > -0.2:  # noqa: PLR2004
            nx = pos.x() + 10 * s * cy
            gap = 5.5 * s * abs(sy)
            eh = 6 * s * self._blink
            p.setBrush(QBrush(Qt.GlobalColor.white))
            if self._weather == WeatherCond.SUNNY:
                p.setBrush(QBrush(QColor("#111111")))
                p.setPen(QPen(QColor(50, 50, 50), 1))
                p.drawRect(QRectF(nx + gap - 4 * s, pos.y(), 8 * s, 6 * s))
                if abs(sy) > 0.35:  # noqa: PLR2004
                    p.drawRect(QRectF(nx - gap - 4 * s, pos.y(), 8 * s, 6 * s))
                p.drawLine(
                    QPointF(nx - gap + 4 * s, pos.y() + 2 * s),
                    QPointF(nx + gap - 4 * s, pos.y() + 2 * s),
                )
            else:
                p.drawEllipse(QRectF(nx + gap - 2.5 * s, pos.y() + 1 * s, 5 * s, eh))
                if abs(sy) > 0.35:  # noqa: PLR2004
                    p.drawEllipse(QRectF(nx - gap - 2.5 * s, pos.y() + 1 * s, 5 * s, eh))
                if self._blink > 0.3:  # noqa: PLR2004
                    p.setBrush(QBrush(Qt.GlobalColor.black))
                    poff = 1.5 * s * cy
                    p.drawEllipse(QRectF(nx + gap - 1.2 * s + poff, pos.y() + 2 * s, 2.5 * s, 2.5 * s))
                    if abs(sy) > 0.35:  # noqa: PLR2004
                        p.drawEllipse(QRectF(nx - gap - 1.2 * s + poff, pos.y() + 2 * s, 2.5 * s, 2.5 * s))

    def _draw_label(self, p: QPainter) -> None:
        """Disegna l'etichetta animata spettacolare con effetto Chrome."""
        p.save()
        f = self._label_phase * 2 * math.pi
        # Glow Pulsante
        ga = int(25 + abs(math.sin(f)) * 35)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(QColor(255, 255, 255, ga)))
        p.drawEllipse(QRectF(self.rect().center().x() - 75, 8, 150, 32))
        # Chrome Text
        yo, sp = math.sin(f) * 4, 220 + math.sin(f) * 35
        p.translate(0, yo)
        font = QFont("Segoe UI", 10, QFont.Weight.Black)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, int(sp))
        p.setFont(font)
        # Drop Shadow
        p.setPen(QColor(0, 0, 0, 80))
        p.drawText(
            self.rect().adjusted(2, 12, 2, 12),
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
            "DON CIRO",
        )
        # Gradient Chrome Animato
        grad = QLinearGradient(0, 10, 0, 35)
        shift = math.sin(f) * 5
        grad.setColorAt(0, QColor("#D4AF37"))
        grad.setColorAt(max(0.0, min(1.0, 0.4 + (shift / 100))), QColor("#FFFFFF"))
        grad.setColorAt(0.5, QColor("#BDB76B"))
        grad.setColorAt(max(0.0, min(1.0, 0.6 + (shift / 100))), QColor("#FFFFFF"))
        grad.setColorAt(1, QColor("#223344"))
        p.setPen(QPen(grad, 0.5))
        p.setBrush(QBrush(grad))
        p.drawText(
            self.rect().adjusted(0, 10, 0, 10),
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
            "DON CIRO",
        )
        # Shimmer particles
        p.setPen(QPen(Qt.GlobalColor.white, 1.8))
        for i in range(6):
            px, py = self.width() / 2 - 65 + ((f * 90 + i * 35) % 130), 15 + math.sin(f * 4 + i) * 6
            p.setOpacity(0.3 + abs(math.sin(f * 5 + i)) * 0.7)
            p.drawPoint(QPointF(px, py))
        p.restore()
