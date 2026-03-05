"""
SyncroJob - Don Ciro 8.0 (The Living Entity Engine)
- AI State Machine (Walking, Idle, Check Watch, Adjust Tie).
- Secondary Physics (Pendulum Tie, Dynamic Jacket Tails).
- Squash & Stretch (Disney principles per impatto e spinta).
- Environmental Context (Ombrello per pioggia, Occhiali per sole).
- Contact Shadows & Ambient Occlusion.
"""

import logging
import math
import random
from enum import Enum
from dataclasses import dataclass
from typing import Callable

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    pyqtProperty,
    QPointF,
    QRectF,
    QTimer,
)
from PyQt6.QtGui import (
    QPainter,
    QPen,
    QColor,
    QBrush,
    QLinearGradient,
    QRadialGradient,
    QPainterPath,
    QFont,
    QTransform,
)
from PyQt6.QtWidgets import QWidget

from src.gui.styles import COLORS

logger = logging.getLogger(__name__)

class DonState(Enum):
    WALKING = 1
    TURNING = 2
    IDLE = 3
    ACTION_WATCH = 4
    ACTION_TIE = 5

class WeatherCond(Enum):
    NORMAL = 1
    SUNNY = 2
    RAINY = 3
    WINDY = 4

@dataclass
class RenderItem:
    z_depth: float
    draw_func: Callable
    args: tuple

class DonCiroWidget(QWidget):
    """Il Don Ciro 8.0: Intelligenza, Fisica e Contesto."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setFixedHeight(180)
        
        # AI & Stati
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
        
        # UI & Costanti
        self._blink = 1.0
        self._label_phase = 0.0
        self._scale = 0.72 
        self.THIGH_LEN = 30 * self._scale
        self.CALF_LEN = 30 * self._scale
        
        # Palette Cinematic
        self.C_SKIN = QColor("#FFDAB9")
        self.C_SUIT = QColor("#223344") # Charcoal Blue
        self.C_SHIRT = QColor("#FFFFFF")
        self.C_TIE = QColor("#C0392B")
        self.C_HAIR = QColor("#1A1A1A")
        self.C_SHOE = QColor("#0A0A0A")
        
        self._init_engine()

    # --- PROPERTIES ---
    @pyqtProperty(float)
    def walk_phase(self) -> float: return self._walk_phase
    @walk_phase.setter
    def walk_phase(self, v: float) -> None:
        self._walk_phase = v
        self.update()

    @pyqtProperty(float)
    def action_phase(self) -> float: return self._action_phase
    @action_phase.setter
    def action_phase(self, v: float) -> None:
        self._action_phase = v
        self.update()

    @pyqtProperty(float)
    def yaw_angle(self) -> float: return self._yaw_angle
    @yaw_angle.setter
    def yaw_angle(self, v: float) -> None:
        self._yaw_angle = v
        self.update()

    @pyqtProperty(float)
    def blink(self) -> float: return self._blink
    @blink.setter
    def blink(self, v: float) -> None:
        self._blink = v
        self.update()

    @pyqtProperty(float)
    def label_phase(self) -> float: return self._label_phase
    @label_phase.setter
    def label_phase(self, v: float) -> None:
        self._label_phase = v
        self.update()

    # --- ENGINE ---
    def _init_engine(self) -> None:
        self.walk_anim = QPropertyAnimation(self, b"walk_phase")
        self.walk_anim.setDuration(1300); self.walk_anim.setStartValue(0.0); self.walk_anim.setEndValue(1.0); self.walk_anim.setLoopCount(-1)
        self.walk_anim.start()
        
        self.label_anim = QPropertyAnimation(self, b"label_phase")
        self.label_anim.setDuration(3000); self.label_anim.setStartValue(0.0); self.label_anim.setEndValue(1.0); self.label_anim.setEasingCurve(QEasingCurve.Type.InOutQuad); self.label_anim.setLoopCount(-1)
        self.label_anim.start()

        self.logic_timer = QTimer(self); self.logic_timer.timeout.connect(self._update_physics_and_ai); self.logic_timer.start(16)
        self.blink_timer = QTimer(self); self.blink_timer.timeout.connect(self._do_blink); self.blink_timer.start(3500)
        
        # Simulatore clima casuale (ogni 15 secondi cambia)
        self.weather_timer = QTimer(self); self.weather_timer.timeout.connect(self._random_weather); self.weather_timer.start(15000)

    def _random_weather(self):
        self._weather = random.choice(list(WeatherCond))

    def _update_physics_and_ai(self) -> None:
        dt = 0.016
        cos_y = math.cos(math.radians(self._yaw_angle))
        
        # FISICA SECONDARIA (Molla-Smorzatore)
        # 1. Cravatta
        target_tie = 0.0
        if self._state == DonState.WALKING:
            target_tie = math.sin(self._walk_phase * 2 * math.pi) * 12 * cos_y
        if self._weather == WeatherCond.WINDY:
            target_tie += 25 * self._look_dir # Vento laterale
        
        force_t = (target_tie - self._tie_angle) * 60.0 - self._tie_vel * 8.0
        self._tie_vel += force_t * dt
        self._tie_angle += self._tie_vel * dt
        
        # 2. Giacca (Lembi)
        target_jacket = 0.0
        if self._state == DonState.WALKING:
            # La giacca si apre in base alla velocità
            target_jacket = -abs(math.sin(self._walk_phase * 2 * math.pi)) * 10 * cos_y
        if self._weather == WeatherCond.WINDY:
            target_jacket -= 20 * self._look_dir
            
        force_j = (target_jacket - self._jacket_flap) * 40.0 - self._jacket_vel * 6.0
        self._jacket_vel += force_j * dt
        self._jacket_flap += self._jacket_vel * dt

        # AI STATE MACHINE
        if self._state == DonState.WALKING:
            speed = 0.65 * self._scale
            # Il vento rallenta o accelera
            if self._weather == WeatherCond.WINDY: speed *= 0.8
            if self._weather == WeatherCond.RAINY: speed *= 1.2 # Fretta per la pioggia
            
            self._walk_x += speed * self._look_dir
            
            # Chance di fermarsi al centro (se non piove)
            if self._weather != WeatherCond.RAINY and 130 < self._walk_x < 150 and random.random() < 0.008:
                self._start_idle()
                return

            if self._look_dir > 0 and self._walk_x >= 210: self._turn(180.0)
            elif self._look_dir < 0 and self._walk_x <= 70: self._turn(0.0)
            
        elif self._state == DonState.IDLE:
            self._idle_time -= 16
            if self._idle_time <= 0:
                r = random.random()
                if r < 0.4: self._start_action(DonState.ACTION_WATCH)
                elif r < 0.8: self._start_action(DonState.ACTION_TIE)
                else: self._resume_walk()
                
        self.update()

    # --- TRANSIZIONI STATO ---
    def _turn(self, target: float) -> None:
        self._state = DonState.TURNING
        self.ta = QPropertyAnimation(self, b"yaw_angle")
        self.ta.setDuration(750); self.ta.setStartValue(self._yaw_angle); self.ta.setEndValue(target); self.ta.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.ta.finished.connect(self._end_turn); self.ta.start()

    def _end_turn(self) -> None:
        self._look_dir = 1.0 if self._yaw_angle < 90 else -1.0
        self._state = DonState.WALKING

    def _start_idle(self) -> None:
        self._state = DonState.IDLE
        self.walk_anim.pause()
        self._idle_time = random.randint(1000, 2000)

    def _resume_walk(self) -> None:
        self._state = DonState.WALKING
        self.walk_anim.resume()

    def _start_action(self, action: DonState) -> None:
        self._state = action
        self.act_anim = QPropertyAnimation(self, b"action_phase")
        self.act_anim.setDuration(1500)
        self.act_anim.setStartValue(0.0)
        self.act_anim.setEndValue(1.0)
        self.act_anim.finished.connect(self._end_action)
        self.act_anim.start()

    def _end_action(self) -> None:
        self._resume_walk()

    def _do_blink(self) -> None:
        if random.random() > 0.3:
            self.ba = QPropertyAnimation(self, b"blink")
            self.ba.setDuration(120); self.ba.setStartValue(1.0); self.ba.setKeyValueAt(0.5, 0.0); self.ba.setEndValue(1.0); self.ba.start()

    # --- RENDERING ---
    def paintEvent(self, event) -> None:
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.save(); painter.translate(self._walk_x, 150)
        
        self._draw_dynamic_shadow(painter)
        self._render_ciro_3d(painter)
        
        painter.restore()
        self._draw_label(painter)
        self._draw_weather_fx(painter)

    def _draw_weather_fx(self, painter: QPainter):
        # Disegna effetti atmosferici leggeri a schermo
        if self._weather == WeatherCond.RAINY:
            painter.setPen(QPen(QColor(255, 255, 255, 40), 1))
            for i in range(15):
                rx = (self._walk_phase * 500 + i * 30) % 280
                ry = (self._walk_phase * 800 + i * 40) % 180
                painter.drawLine(QPointF(rx, ry), QPointF(rx - 5, ry + 15))

    def _draw_dynamic_shadow(self, painter: QPainter) -> None:
        if self._state == DonState.WALKING: f = self._walk_phase * 2 * math.pi; bob = abs(math.sin(f * 2))
        else: bob = 0
        
        size = (42 - bob * 4) * self._scale
        grad = QRadialGradient(0, 0, size)
        grad.setColorAt(0, QColor(0, 0, 0, int(80 - bob*20))); grad.setColorAt(1, Qt.GlobalColor.transparent)
        painter.setBrush(QBrush(grad)); painter.setPen(Qt.PenStyle.NoPen); painter.drawEllipse(QPointF(0, 0), size, 8*self._scale)

    def _render_ciro_3d(self, painter: QPainter) -> None:
        f = self._walk_phase * 2 * math.pi
        rad = math.radians(self._yaw_angle); cos_y, sin_y = math.cos(rad), math.sin(rad)
        
        # SQUASH & STRETCH (Solo in Walking)
        squash = 1.0
        if self._state == DonState.WALKING:
            # Quando il piede tocca terra (sin(f*2) max), si schiaccia leggermente
            squash = 1.0 - 0.03 * max(0, math.sin(f * 2))
            bounce_y = (-68 - abs(math.sin(f * 2)) * 6) * self._scale
        else:
            bounce_y = -68 * self._scale
            
        lean = (0.08 if self._state == DonState.WALKING else 0.0) * cos_y
        
        # Se c'è vento, si inclina
        if self._weather == WeatherCond.WINDY: lean += 0.1 * self._look_dir
        
        hip_c = QPointF(0, bounce_y)
        sh_y = bounce_y - 42*self._scale*squash; sh_c = QPointF(lean*12*self._scale, sh_y)
        head_p = QPointF(sh_c.x() + lean*8*self._scale, sh_y - 16*self._scale*squash)
        
        # MOTORE IK GAMBE
        if self._state == DonState.WALKING:
            step_len = 22 * self._scale * abs(cos_y); step_h = 12 * self._scale
            pos_r = math.sin(f); foot_r_x = pos_r * step_len; foot_r_y = -abs(pos_r * step_h) if pos_r > 0 else 0
            pos_l = math.sin(f + math.pi); foot_l_x = pos_l * step_len; foot_l_y = -abs(pos_l * step_h) if pos_l > 0 else 0
        else:
            # Piedi pari in Idle
            foot_r_x, foot_r_y = 5*self._scale, 0
            foot_l_x, foot_l_y = -5*self._scale, 0

        w_off = 11 * self._scale
        r_hip_3d = QPointF(-w_off * sin_y, bounce_y); l_hip_3d = QPointF(w_off * sin_y, bounce_y)
        r_sh_3d = QPointF(sh_c.x() - w_off * sin_y, sh_y); l_sh_3d = QPointF(sh_c.x() + w_off * sin_y, sh_y)
        
        knee_r = self._solve_ik(r_hip_3d, QPointF(r_hip_3d.x() + foot_r_x, foot_r_y))
        knee_l = self._solve_ik(l_hip_3d, QPointF(l_hip_3d.x() + foot_l_x, foot_l_y))

        render_queue = []; r_z, l_z = w_off * cos_y, -w_off * cos_y
        render_queue.append(RenderItem(-r_z, self._draw_leg, (r_hip_3d, knee_r, QPointF(r_hip_3d.x()+foot_r_x, foot_r_y), r_z, cos_y)))
        render_queue.append(RenderItem(-l_z, self._draw_leg, (l_hip_3d, knee_l, QPointF(l_hip_3d.x()+foot_l_x, foot_l_y), l_z, cos_y)))
        
        # BRACCIA E AZIONI IDLE
        arm_r_p = QPointF(r_sh_3d.x(), sh_y+24*self._scale)
        arm_l_p = QPointF(l_sh_3d.x(), sh_y+24*self._scale)
        
        if self._state == DonState.WALKING:
            asw = math.sin(f) * 18 * self._scale * cos_y
            arm_r_p.setX(arm_r_p.x() - asw)
            arm_l_p.setX(arm_l_p.x() + asw)
        elif self._state == DonState.ACTION_WATCH:
            # Guarda l'orologio (Braccio sinistro si alza)
            a_p = math.sin(self._action_phase * math.pi)
            arm_l_p = QPointF(l_sh_3d.x() + 10*self._scale*cos_y, sh_y + 10*self._scale - 10*self._scale*a_p)
            head_p.setX(head_p.x() + 5*self._scale*a_p*cos_y)
            head_p.setY(head_p.y() + 5*self._scale*a_p) # Abbassa la testa
        elif self._state == DonState.ACTION_TIE:
            # Si sistema la cravatta (Braccio destro si alza al petto)
            a_p = math.sin(self._action_phase * math.pi)
            arm_r_p = QPointF(r_sh_3d.x() - 5*self._scale*cos_y, sh_y + 15*self._scale - 12*self._scale*a_p)
            
        render_queue.append(RenderItem(-r_z, self._draw_arm, (r_sh_3d, arm_r_p, r_z, squash, True)))
        render_queue.append(RenderItem(-l_z, self._draw_arm, (l_sh_3d, arm_l_p, l_z, squash, False)))
        
        render_queue.append(RenderItem(0.0, self._draw_torso, (hip_c, sh_c, cos_y, sin_y, squash)))
        render_queue.append(RenderItem(0.5, self._draw_head, (head_p, cos_y, sin_y, squash)))

        render_queue.sort(key=lambda x: x.z_depth, reverse=True)
        
        painter.save()
        # Applica lo Squash verticale al centro
        painter.scale(1.0, squash)
        for item in render_queue: item.draw_func(painter, *item.args)
        painter.restore()

    def _solve_ik(self, hip: QPointF, foot: QPointF) -> QPointF:
        dx, dy = foot.x() - hip.x(), foot.y() - hip.y(); dist = math.sqrt(dx*dx + dy*dy); max_d = (self.THIGH_LEN + self.CALF_LEN) * 0.96
        if dist > max_d: dist = max_d
        a, b, c = self.THIGH_LEN, self.CALF_LEN, dist
        try: cos_alpha = (a*a + c*c - b*b) / (2*a*c); alpha = math.acos(max(-1, min(1, cos_alpha)))
        except: alpha = 0.1
        cy = math.cos(math.radians(self._yaw_angle)); bang = math.atan2(dy, dx)
        knee_angle = bang + (-alpha if cy >= 0 else alpha)
        return QPointF(hip.x() + math.cos(knee_angle) * a, hip.y() + math.sin(knee_angle) * a)

    def _draw_leg(self, painter: QPainter, hip, knee, foot, z, cos_y) -> None:
        op = 0.8 if z < 0 else 1.0; painter.setOpacity(op); c = self.C_SUIT.darker(110 if z < 0 else 100); p = QPainterPath(); p.moveTo(hip); p.lineTo(knee); p.lineTo(foot)
        painter.setPen(QPen(c, 11*self._scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)); painter.drawPath(p)
        self._draw_shoe(painter, QPointF(foot.x(), foot.y() + 3*self._scale), cos_y, z)
        painter.setOpacity(1.0)

    def _draw_shoe(self, painter: QPainter, foot: QPointF, cos_y: float, z: float) -> None:
        painter.save(); painter.translate(foot); painter.scale(1.0 if cos_y >= 0 else -1.0, 1.0)
        s = self._scale
        
        # Contact Shadow (Ambient Occlusion a terra)
        if foot.y() > -1:
            painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QBrush(QColor(0,0,0, 120)))
            painter.drawEllipse(QRectF(-8*s, -2*s, 26*s, 5*s))

        painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QBrush(self.C_SHOE))
        path = QPainterPath(); path.moveTo(-8*s, 0); path.lineTo(18*s, 0); path.lineTo(18*s, -4*s); path.quadTo(15*s, -10*s, 5*s, -11*s); path.lineTo(-8*s, -11*s); path.closeSubpath()
        painter.drawPath(path); painter.setBrush(QBrush(QColor("#111111"))); painter.drawRect(QRectF(-8*s, -3*s, 8*s, 3*s))
        # Riflesso scarpa Boutique
        if self._weather == WeatherCond.SUNNY:
            painter.setBrush(QBrush(QColor(255,255,255,100))) # Più brillante al sole
        else:
            painter.setBrush(QBrush(QColor(255,255,255,40)))
        painter.drawEllipse(QRectF(8*s, -10*s, 6*s, 2*s)); painter.restore()

    def _draw_arm(self, painter: QPainter, sh, hand, z, squash, is_right) -> None:
        op = 0.8 if z < 0 else 1.0; painter.setOpacity(op); painter.setPen(QPen(self.C_SUIT.darker(105 if z < 0 else 100), 7*self._scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)); painter.drawLine(sh, hand)
        painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QBrush(self.C_SKIN.darker(105 if z<0 else 100))); painter.drawEllipse(hand, 5*self._scale, 5*self._scale)
        
        # Ombrello in caso di pioggia
        if self._weather == WeatherCond.RAINY and is_right and z >= 0:
            painter.save(); painter.translate(hand)
            painter.setPen(QPen(QColor(50,50,50), 2*self._scale)); painter.drawLine(QPointF(0,0), QPointF(0, -35*self._scale))
            painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QBrush(QColor("#111111")))
            painter.drawChord(QRectF(-20*self._scale, -45*self._scale, 40*self._scale, 20*self._scale), 0, 180 * 16)
            painter.restore()
            
        painter.setOpacity(1.0)

    def _draw_torso(self, painter: QPainter, hip, sh, cos_y, sin_y, squash) -> None:
        s = self._scale; w = 22 * s * (0.5 + 0.5 * abs(sin_y)); ch_off = 5 * s * cos_y
        
        # Lembo Giacca Posteriore (Secondary Motion)
        if self._jacket_flap != 0:
            painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QBrush(self.C_SUIT.darker(130)))
            j_path = QPainterPath(); j_path.moveTo(hip.x() - w*0.6 + ch_off, hip.y())
            j_path.lineTo(hip.x() - w*0.8 + ch_off - self._jacket_flap, hip.y() + 10*s)
            j_path.lineTo(hip.x() + ch_off, hip.y() + 8*s)
            j_path.closeSubpath(); painter.drawPath(j_path)

        path = QPainterPath(); path.moveTo(sh.x()-w+ch_off, sh.y()); path.cubicTo(sh.x()-w, sh.y()+18*s, hip.x()-w*0.6, hip.y()-18*s, hip.x()-w*0.6+ch_off, hip.y())
        path.lineTo(hip.x()+w*0.6+ch_off, hip.y()); path.cubicTo(hip.x()+w*0.6, hip.y()-18*s, sh.x()+w, sh.y()+18*s, sh.x()+w+ch_off, sh.y()); path.closeSubpath()
        grad = QLinearGradient(sh, hip); grad.setColorAt(0, self.C_SUIT.lighter(110)); grad.setColorAt(1, self.C_SUIT.darker(120))
        painter.setBrush(QBrush(grad)); painter.setPen(QPen(self.C_SUIT.darker(140), 1)); painter.drawPath(path)
        
        if sin_y > 0:
            painter.setBrush(QBrush(self.C_SHIRT)); painter.setPen(Qt.PenStyle.NoPen)
            shirt = QPainterPath(); shirt.moveTo(sh.x()+ch_off-7*s, sh.y()); shirt.lineTo(sh.x()+ch_off+7*s, sh.y()); shirt.lineTo(sh.x()+ch_off, sh.y()+18*s); painter.drawPath(shirt)
            
            # Cravatta Pendolo (Fisica Reale)
            painter.save()
            painter.translate(sh.x()+ch_off, sh.y())
            painter.rotate(self._tie_angle)
            painter.setBrush(QBrush(self.C_TIE)); tie = QPainterPath(); tie.moveTo(0, 0); tie.lineTo(-3*s, 5*s); tie.lineTo(0, 32*s); tie.lineTo(3*s, 5*s); painter.drawPath(tie)
            painter.restore()

    def _draw_head(self, painter: QPainter, pos, cos_y, sin_y, squash) -> None:
        s = self._scale
        ear_vis = max(0.0, min(1.0, abs(sin_y) * 2.0))
        e_col_back = self.C_SKIN.darker(140); painter.setOpacity(ear_vis); painter.setBrush(QBrush(e_col_back)); painter.setPen(QPen(e_col_back.darker(120), 0.6 * s))
        if cos_y > 0: painter.drawEllipse(QRectF(pos.x() + 10*s*cos_y + 8*s, pos.y() - 4*s, 5*s, 9*s))
        else:         painter.drawEllipse(QRectF(pos.x() + 10*s*cos_y - 13*s, pos.y() - 4*s, 5*s, 9*s))
        painter.setOpacity(1.0)

        painter.setPen(Qt.PenStyle.NoPen); grad = QRadialGradient(pos, 20*s); grad.setColorAt(0, self.C_SKIN.lighter(105)); grad.setColorAt(1, self.C_SKIN.darker(115))
        painter.setBrush(QBrush(grad)); painter.drawEllipse(pos, 16*s, 18*s)
        
        e_col_front = self.C_SKIN.darker(120); painter.setBrush(QBrush(e_col_front)); painter.setPen(QPen(e_col_front.darker(120), 0.6 * s))
        if cos_y > 0: painter.drawEllipse(QRectF(pos.x() + 10*s*cos_y - 13*s, pos.y() - 4*s, 5*s, 9*s))
        else:         painter.drawEllipse(QRectF(pos.x() + 10*s*cos_y + 8*s, pos.y() - 4*s, 5*s, 9*s))
        
        painter.setBrush(QBrush(self.C_HAIR)); painter.setPen(Qt.PenStyle.NoPen); h_path = QPainterPath(); h_off = 7 * s * cos_y
        h_path.moveTo(pos.x() - 17*s, pos.y() + 3*s); h_path.cubicTo(pos.x() - 22*s + h_off, pos.y() - 35*s, pos.x() + 22*s + h_off, pos.y() - 35*s, pos.x() + 17*s, pos.y() + 3*s)
        h_path.lineTo(pos.x() + 14*s, pos.y() - 2*s); h_path.lineTo(pos.x() + 12*s * cos_y, pos.y() - 15*s); h_path.lineTo(pos.x() - 14*s, pos.y() - 2*s); painter.drawPath(h_path)
        
        if sin_y > -0.2:
            nx = pos.x() + 10*s * cos_y; gap = 5.5*s * abs(sin_y); eh = 6*s * self._blink
            
            # Occhiali da sole se SUNNY
            if self._weather == WeatherCond.SUNNY:
                painter.setBrush(QBrush(QColor("#111111"))); painter.setPen(QPen(QColor(50,50,50), 1))
                painter.drawRect(QRectF(nx + gap - 4*s, pos.y(), 8*s, 6*s))
                if abs(sin_y) > 0.35: painter.drawRect(QRectF(nx - gap - 4*s, pos.y(), 8*s, 6*s))
                painter.drawLine(QPointF(nx - gap + 4*s, pos.y() + 2*s), QPointF(nx + gap - 4*s, pos.y() + 2*s)) # Ponte occhiali
            else:
                painter.setBrush(QBrush(Qt.GlobalColor.white))
                painter.drawEllipse(QRectF(nx + gap - 2.5*s, pos.y() + 1*s, 5*s, eh))
                if abs(sin_y) > 0.35: painter.drawEllipse(QRectF(nx - gap - 2.5*s, pos.y() + 1*s, 5*s, eh))
                if self._blink > 0.3:
                    painter.setBrush(QBrush(Qt.GlobalColor.black)); poff = 1.5*s*cos_y; painter.drawEllipse(QRectF(nx + gap - 1.2*s + poff, pos.y() + 2*s, 2.5*s, 2.5*s))
                    if abs(sin_y) > 0.35: painter.drawEllipse(QRectF(nx - gap - 1.2*s + poff, pos.y() + 2*s, 2.5*s, 2.5*s))

    def _draw_label(self, painter: QPainter) -> None:
        painter.save()
        f = self._label_phase * 2 * math.pi; y_off = math.sin(f) * 3; spacing = 200 + math.sin(f) * 20
        painter.translate(0, y_off); painter.setPen(QColor(COLORS['text_muted']))
        font = QFont("Segoe UI", 9, QFont.Weight.Black); font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, spacing)
        painter.setFont(font); painter.setOpacity(0.15 + abs(math.sin(f)) * 0.1)
        painter.drawText(self.rect().adjusted(0, 10, 0, 0), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter, "DON CIRO")
        painter.restore()
