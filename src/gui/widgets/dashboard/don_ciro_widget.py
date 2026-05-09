"""
SyncroJob - Don Ciro Widget
Interfaccia Premium per la mascotte Don Ciro.
Refactored V9.0: SRP Compliance - Logica delegata a DonCiroEngine.
Integrazione con WeatherService per reattività climatica reale.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPointF,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PySide6.QtWidgets import QWidget

from src.core.mascot.don_ciro_engine import DonCiroEngine, DonState, WeatherCond
from src.core.weather_service import WeatherService

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


@dataclass
class RenderItem:
    """Elemento della coda di rendering 3D con ordinamento Z."""

    z_depth: float
    draw_func: Callable[..., None]
    args: tuple[Any, ...]


class DonCiroWidget(QWidget):
    """Il Don Ciro: Visualizzazione 3D isometrica della mascotte aziendale."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setFixedHeight(180)

        # Inizializza il motore (SRP)
        self.engine = DonCiroEngine(self)
        self.weather_service = WeatherService.instance()

        # UI State (Solo visuale)
        self._walk_phase = 0.0
        self._action_phase = 0.0
        self._yaw_angle = 0.0
        self._blink = 1.0
        self._label_phase = 0.0

        # Palette Cinematic
        self.C_SKIN = QColor("#FFDAB9")
        self.C_SUIT = QColor("#223344")
        self.C_SHIRT = QColor("#FFFFFF")
        self.C_TIE = QColor("#C0392B")
        self.C_HAIR = QColor("#1A1A1A")
        self.C_SHOE = QColor("#0A0A0A")

        self._init_animations()
        self._connect_signals()

    # ── Proprietà Animate (Qt) ──────────────────────────────────────────

    @Property(float)
    def walk_phase(self) -> float:
        """Ritorna la fase della camminata."""
        return self._walk_phase

    @walk_phase.setter  # type: ignore[no-redef]
    def walk_phase(self, v: float) -> None:
        self._walk_phase = v
        # Sincronizza motore per la fisica
        self.engine._walk_phase = v
        self.update()

    @Property(float)
    def action_phase(self) -> float:
        """Ritorna la fase dell'azione."""
        return self._action_phase

    @action_phase.setter  # type: ignore[no-redef]
    def action_phase(self, v: float) -> None:
        self._action_phase = v
        self.engine._action_phase = v
        self.update()

    @Property(float)
    def yaw_angle(self) -> float:
        """Ritorna l'angolo di imbardata."""
        return self._yaw_angle

    @yaw_angle.setter  # type: ignore[no-redef]
    def yaw_angle(self, v: float) -> None:
        self._yaw_angle = v
        self.engine._yaw_angle = v
        self.update()

    @Property(float)
    def blink(self) -> float:
        """Ritorna lo stato del battito ciglia."""
        return self._blink

    @blink.setter  # type: ignore[no-redef]
    def blink(self, v: float) -> None:
        self._blink = v
        self.update()

    @Property(float)
    def label_phase(self) -> float:
        """Ritorna la fase del testo."""
        return self._label_phase

    @label_phase.setter  # type: ignore[no-redef]
    def label_phase(self, v: float) -> None:
        self._label_phase = v
        self.update()

    # ── Inizializzazione ────────────────────────────────────────────────

    def _init_animations(self) -> None:
        # Loop Camminata
        self.walk_anim = QPropertyAnimation(self, b"walk_phase")
        self.walk_anim.setDuration(1300)
        self.walk_anim.setStartValue(0.0)
        self.walk_anim.setEndValue(1.0)
        self.walk_anim.setLoopCount(-1)
        self.walk_anim.start()

        # Loop Testo Chrome
        self.label_anim = QPropertyAnimation(self, b"label_phase")
        self.label_anim.setDuration(4000)
        self.label_anim.setStartValue(0.0)
        self.label_anim.setEndValue(1.0)
        self.label_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.label_anim.setLoopCount(-1)
        self.label_anim.start()

        # Timer Battito Ciglia
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self._do_blink)
        self.blink_timer.start(3500)

    def _connect_signals(self) -> None:
        """Collega motore e servizi esterni."""
        self.engine.state_changed.connect(self._on_engine_state_changed)
        self.engine.physics_updated.connect(self.update)

        # Integrazione meteo reale
        self.weather_service.weather_data_ready.connect(self._on_real_weather_received)

    def _on_engine_state_changed(self, state: DonState) -> None:
        """Gestisce i cambi di stato notificati dall'engine."""
        if state == DonState.TURNING:
            self._trigger_ui_turn()
        elif state in (DonState.ACTION_WATCH, DonState.ACTION_TIE):
            self._trigger_ui_action()
        elif state == DonState.IDLE:
            self.walk_anim.pause()
        elif state == DonState.WALKING and self.walk_anim.state() == QPropertyAnimation.State.Paused:
            self.walk_anim.resume()

    def _on_real_weather_received(self, weather: dict[str, Any], aqi: dict[str, Any]) -> None:
        """Adatta il comportamento di Don Ciro al meteo reale."""
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
        self.ta.setDuration(800)
        self.ta.setStartValue(self._yaw_angle)
        self.ta.setEndValue(target)
        self.ta.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.ta.finished.connect(lambda: self.engine.set_yaw_complete(target))
        self.ta.start()

    def _trigger_ui_action(self) -> None:
        """Avvia l'animazione di un'azione specifica."""
        self.act = QPropertyAnimation(self, b"action_phase")
        self.act.setDuration(1500)
        self.act.setStartValue(0.0)
        self.act.setEndValue(1.0)
        self.act.start()

    def _do_blink(self) -> None:
        """Avvia il battito di ciglia."""
        self.ba = QPropertyAnimation(self, b"blink")
        self.ba.setDuration(120)
        self.ba.setStartValue(1.0)
        self.ba.setKeyValueAt(0.5, 0.0)
        self.ba.setEndValue(1.0)
        self.ba.start()

    # ── Rendering ───────────────────────────────────────────────────────

    def paintEvent(self, event: Any) -> None:
        """Disegna il widget."""
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.save()
        p.translate(self.engine.walk_x, 150)
        self._draw_dynamic_shadow(p)
        self._render_ciro_3d(p)
        p.restore()
        self._draw_label(p)
        self._draw_weather_fx(p)

    def _draw_weather_fx(self, p: QPainter) -> None:
        """Disegna gli effetti meteo."""
        if self.engine.weather == WeatherCond.RAINY:
            p.setPen(QPen(QColor(255, 255, 255, 40), 1))
            for i in range(15):
                rx = (self._walk_phase * 500 + i * 30) % 280
                ry = (self._walk_phase * 800 + i * 40) % 180
                p.drawLine(QPointF(rx, ry), QPointF(rx - 5, ry + 15))

    def _draw_dynamic_shadow(self, p: QPainter) -> None:
        """Disegna l'ombra al suolo."""
        bob = abs(math.sin(self._walk_phase * 2 * math.pi)) if self.engine.state == DonState.WALKING else 0.0
        s = (42 - bob * 4) * self.engine.scale
        g = QRadialGradient(0, 0, s)
        g.setColorAt(0, QColor(0, 0, 0, int(80 - bob * 20)))
        g.setColorAt(1, Qt.GlobalColor.transparent)
        p.setBrush(QBrush(g))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(0, 0), s, 8 * self.engine.scale)

    def _render_ciro_3d(self, p: QPainter) -> None:
        """Assembla e disegna le parti del corpo in ordine Z."""
        f = self._walk_phase * 2 * math.pi
        rad = math.radians(self._yaw_angle)
        cos_y, sin_y = math.cos(rad), math.sin(rad)
        sq = 1.0 - 0.03 * max(0.0, math.sin(f * 2)) if self.engine.state == DonState.WALKING else 1.0
        by = (
            -68 - (abs(math.sin(f * 2)) * 6 if self.engine.state == DonState.WALKING else 0)
        ) * self.engine.scale
        ln = (0.08 if self.engine.state == DonState.WALKING else 0.0) * cos_y

        hp_c = QPointF(0, by)
        sy = by - 42 * self.engine.scale * sq
        sc = QPointF(ln * 12 * self.engine.scale, sy)
        hd_p = QPointF(sc.x() + ln * 8 * self.engine.scale, sy - 16 * self.engine.scale * sq)

        if self.engine.state == DonState.WALKING:
            sl, sh = 22 * self.engine.scale * abs(cos_y), 12 * self.engine.scale
            pr, pl = math.sin(f), math.sin(f + math.pi)
            frx, fry = pr * sl, (-abs(pr * sh) if pr > 0 else 0.0)
            flx, fly = pl * sl, (-abs(pl * sh) if pl > 0 else 0.0)
        else:
            frx, fry, flx, fly = 5 * self.engine.scale, 0.0, -5 * self.engine.scale, 0.0

        wo = 11 * self.engine.scale
        r_hp, l_hp = QPointF(-wo * sin_y, by), QPointF(wo * sin_y, by)
        r_sh, l_sh = QPointF(sc.x() - wo * sin_y, sy), QPointF(sc.x() + wo * sin_y, sy)
        kn_r = self.engine.solve_ik(r_hp, QPointF(r_hp.x() + frx, fry))
        kn_l = self.engine.solve_ik(l_hp, QPointF(l_hp.x() + flx, fly))

        ar_p = QPointF(r_sh.x(), sy + 24 * self.engine.scale)
        al_p = QPointF(l_sh.x(), sy + 24 * self.engine.scale)

        if self.engine.state == DonState.WALKING:
            asw = math.sin(f) * 18 * self.engine.scale * cos_y
            ar_p.setX(ar_p.x() - asw)
            al_p.setX(al_p.x() + asw)
        elif self.engine.state == DonState.ACTION_WATCH:
            ap = math.sin(self._action_phase * math.pi)
            al_p = QPointF(
                l_sh.x() + 10 * self.engine.scale * cos_y,
                sy + 10 * self.engine.scale - 10 * self.engine.scale * ap,
            )
            hd_p.setX(hd_p.x() + 5 * self.engine.scale * ap * cos_y)
            hd_p.setY(hd_p.y() + 5 * self.engine.scale * ap)
        elif self.engine.state == DonState.ACTION_TIE:
            ap = math.sin(self._action_phase * math.pi)
            ar_p = QPointF(
                r_sh.x() - 5 * self.engine.scale * cos_y,
                sy + 15 * self.engine.scale - 12 * self.engine.scale * ap,
            )

        rq = [
            RenderItem(
                -wo * cos_y, self._draw_leg, (r_hp, kn_r, QPointF(r_hp.x() + frx, fry), wo * cos_y, cos_y)
            ),
            RenderItem(
                wo * cos_y, self._draw_leg, (l_hp, kn_l, QPointF(l_hp.x() + flx, fly), -wo * cos_y, cos_y)
            ),
            RenderItem(-wo * cos_y, self._draw_arm, (r_sh, ar_p, wo * cos_y, True)),
            RenderItem(wo * cos_y, self._draw_arm, (l_sh, al_p, -wo * cos_y, False)),
            RenderItem(0.0, self._draw_torso, (hp_c, sc, cos_y, sin_y)),
            RenderItem(0.5, self._draw_head, (hd_p, cos_y, sin_y)),
        ]
        rq.sort(key=lambda x: x.z_depth, reverse=True)
        p.save()
        p.scale(1.0, sq)
        for i in rq:
            i.draw_func(p, *i.args)
        p.restore()

    def _draw_leg(self, p: QPainter, h: QPointF, k: QPointF, f: QPointF, z: float, cy: float) -> None:  # noqa: PLR0913
        """Disegna una gamba."""
        p.setOpacity(0.8 if z < 0 else 1.0)
        c = self.C_SUIT.darker(110 if z < 0 else 100)
        path = QPainterPath()
        path.moveTo(h)
        path.lineTo(k)
        path.lineTo(f)
        p.setPen(QPen(c, 11 * self.engine.scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawPath(path)
        self._draw_shoe(p, QPointF(f.x(), f.y() + 3 * self.engine.scale), cy, z)
        p.setOpacity(1.0)

    def _draw_shoe(self, p: QPainter, f: QPointF, cy: float, z: float) -> None:
        """Disegna la scarpa."""
        p.save()
        p.translate(f)
        p.scale(1.0 if cy >= 0 else -1.0, 1.0)
        s = self.engine.scale
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
        p.restore()

    def _draw_arm(self, p: QPainter, sh: QPointF, hand: QPointF, z: float, is_right: bool) -> None:
        """Disegna un braccio."""
        p.setOpacity(0.8 if z < 0 else 1.0)
        p.setPen(
            QPen(
                self.C_SUIT.darker(105 if z < 0 else 100),
                7 * self.engine.scale,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            )
        )
        p.drawLine(sh, hand)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(self.C_SKIN.darker(105 if z < 0 else 100)))
        p.drawEllipse(hand, 5 * self.engine.scale, 5 * self.engine.scale)
        if self.engine.weather == WeatherCond.RAINY and is_right and z >= 0:
            p.save()
            p.translate(hand)
            p.setPen(QPen(QColor(50, 50, 50), 2 * self.engine.scale))
            p.drawLine(QPointF(0, 0), QPointF(0, -35 * self.engine.scale))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(QColor("#111111")))
            p.drawChord(
                QRectF(
                    -20 * self.engine.scale,
                    -45 * self.engine.scale,
                    40 * self.engine.scale,
                    20 * self.engine.scale,
                ),
                0,
                180 * 16,
            )
            p.restore()
        p.setOpacity(1.0)

    def _draw_torso(self, p: QPainter, hp: QPointF, sh: QPointF, cy: float, sy: float) -> None:  # noqa: PLR0915
        """Disegna il busto con colletto e cravatta."""
        s = self.engine.scale
        w = 22 * s * (0.5 + 0.5 * abs(sy))
        ch = 5 * s * cy

        # 1. Collo e Colletto
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

        # 2. Flap Giacca (Dietro)
        if self.engine.jacket_flap != 0 and sy < 0.3:  # noqa: PLR2004
            p.setBrush(QBrush(self.C_SUIT.darker(135)))
            j_path = QPainterPath()
            j_path.moveTo(hp.x() + ch, hp.y())
            j_path.lineTo(hp.x() + ch - (15 * s + self.engine.jacket_flap) * cy, hp.y() + 8 * s)
            j_path.lineTo(hp.x() + ch, hp.y() + 5 * s)
            p.drawPath(j_path)

        # 3. Busto Principale
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

        # 4. Camicia e Cravatta (Davanti)
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
            p.rotate(self.engine.tie_angle)
            p.setBrush(QBrush(self.C_TIE))
            tie = QPainterPath()
            tie.moveTo(0, 0)
            tie.lineTo(-3.5 * s, 5 * s)
            tie.lineTo(0, 32 * s)
            tie.lineTo(3.5 * s, 5 * s)
            p.drawPath(tie)
            p.restore()

    def _draw_head(self, p: QPainter, pos: QPointF, cy: float, sy: float) -> None:
        """Disegna la testa."""
        s = self.engine.scale
        ev = max(0.0, min(1.0, abs(sy) * 2.5))
        p.setOpacity(ev)
        p.setBrush(QBrush(self.C_SKIN.darker(140)))
        p.setPen(QPen(self.C_SKIN.darker(160), 0.6 * s))
        off = 8 * s if cy > 0 else -13 * s
        p.drawEllipse(QRectF(pos.x() + 10 * s * cy + off, pos.y() - 4 * s, 5 * s, 9 * s))
        p.setOpacity(1.0)
        p.setPen(Qt.PenStyle.NoPen)
        grad = QRadialGradient(pos, 20 * s)
        grad.setColorAt(0, self.C_SKIN.lighter(105))
        grad.setColorAt(1, self.C_SKIN.darker(115))
        p.setBrush(QBrush(grad))
        p.drawEllipse(pos, 16 * s, 18 * s)
        p.setBrush(QBrush(self.C_HAIR))
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
        if sy > -0.2:  # noqa: PLR2004
            nx = pos.x() + 10 * s * cy
            gap = 5.5 * s * abs(sy)
            eh = 6 * s * self._blink
            color = Qt.GlobalColor.white if self.engine.weather != WeatherCond.SUNNY else QColor("#111111")
            p.setBrush(QBrush(color))
            p.drawEllipse(QRectF(nx + gap - 2.5 * s, pos.y() + 1 * s, 5 * s, eh))
            if abs(sy) > 0.35:  # noqa: PLR2004
                p.drawEllipse(QRectF(nx - gap - 2.5 * s, pos.y() + 1 * s, 5 * s, eh))

    def _draw_label(self, p: QPainter) -> None:
        """Disegna l'etichetta."""
        p.save()
        f = self._label_phase * 2 * math.pi
        ga = int(25 + abs(math.sin(f)) * 35)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(QColor(255, 255, 255, ga)))
        p.drawEllipse(QRectF(self.rect().center().x() - 75, 8, 150, 32))
        yo, sp = math.sin(f) * 4, 220 + math.sin(f) * 35
        p.translate(0, yo)
        font = QFont("Segoe UI", 10, QFont.Weight.Black)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, int(sp))
        p.setFont(font)
        p.setPen(QColor(0, 0, 0, 80))
        p.drawText(
            self.rect().adjusted(2, 12, 2, 12),
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
            "DON CIRO",
        )
        grad = QLinearGradient(0, 10, 0, 35)
        grad.setColorAt(0, QColor("#D4AF37"))
        grad.setColorAt(0.5, QColor("#BDB76B"))
        grad.setColorAt(1, QColor("#223344"))
        p.setPen(QPen(grad, 0.5))
        p.setBrush(QBrush(grad))
        p.drawText(
            self.rect().adjusted(0, 10, 0, 10),
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
            "DON CIRO",
        )
        p.restore()
