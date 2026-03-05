"""
SyncroJob - Don Ciro 7.4 (Advanced Perspective & Animated UI)
- Orecchie Dinamiche: Solo una visibile in profilo, due in rotazione (Z-Alpha Sorting).
- Titolo Animato: Scritta "DON CIRO" con floating verticale, spaziatura variabile e pulsazione opacità.
- Fix Anatomici: Ginocchia, occhi e capelli coerenti con la rotazione 3D.
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
)
from PyQt6.QtWidgets import QWidget

from src.gui.styles import COLORS

logger = logging.getLogger(__name__)

@dataclass
class RenderItem:
    z_depth: float
    draw_func: Callable
    args: tuple

class DonCiroWidget(QWidget):
    """L'omino perfetto con interfaccia animata e prospettiva evoluta."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setFixedHeight(180)
        
        # Stato Animazione
        self._walk_phase = 0.0
        self._walk_x = 60.0
        self._yaw_angle = 0.0 
        self._look_dir = 1.0
        self._is_turning = False
        
        # Fisica e UI
        self._blink = 1.0
        self._label_phase = 0.0 # Per animazione scritta
        self._scale = 0.75 
        self.THIGH_LEN = 30 * self._scale
        self.CALF_LEN = 30 * self._scale
        
        # Palette Cinematic
        self.C_SKIN = QColor("#FFDAB9")
        self.C_SUIT = QColor("#2C3E50")
        self.C_SHIRT = QColor("#FFFFFF")
        self.C_TIE = QColor("#C0392B")
        self.C_HAIR = QColor("#1A1A1A")
        self.C_SHOE = QColor("#000000")
        
        self._init_engine()

    @pyqtProperty(float)
    def walk_phase(self) -> float: return self._walk_phase
    @walk_phase.setter
    def walk_phase(self, v: float) -> None:
        self._walk_phase = v
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

    def _init_engine(self) -> None:
        # Animazione Camminata
        self.walk_anim = QPropertyAnimation(self, b"walk_phase")
        self.walk_anim.setDuration(1250); self.walk_anim.setStartValue(0.0); self.walk_anim.setEndValue(1.0); self.walk_anim.setLoopCount(-1); self.walk_anim.start()
        
        # Animazione Scritta DON CIRO (Floating)
        self.label_anim = QPropertyAnimation(self, b"label_phase")
        self.label_anim.setDuration(3000); self.label_anim.setStartValue(0.0); self.label_anim.setEndValue(1.0); self.label_anim.setEasingCurve(QEasingCurve.Type.InOutQuad); self.label_anim.setLoopCount(-1); self.label_anim.start()

        self.logic_timer = QTimer(self); self.logic_timer.timeout.connect(self._update_ai); self.logic_timer.start(16)
        self.blink_timer = QTimer(self); self.blink_timer.timeout.connect(self._do_blink); self.blink_timer.start(3200)

    def _update_ai(self) -> None:
        if self._is_turning: return
        speed = 0.65 * self._scale
        if self._look_dir > 0:
            if self._walk_x < 210: self._walk_x += speed
            else: self._turn(180.0)
        else:
            if self._walk_x > 70: self._walk_x -= speed
            else: self._turn(0.0)
        self.update()

    def _turn(self, target: float) -> None:
        self._is_turning = True
        self.ta = QPropertyAnimation(self, b"yaw_angle")
        self.ta.setDuration(800); self.ta.setStartValue(self._yaw_angle); self.ta.setEndValue(target); self.ta.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.ta.finished.connect(self._end_turn); self.ta.start()

    def _end_turn(self) -> None:
        self._is_turning = False
        self._look_dir = 1.0 if self._yaw_angle < 90 else -1.0

    def _do_blink(self) -> None:
        if random.random() > 0.4:
            self.ba = QPropertyAnimation(self, b"blink")
            self.ba.setDuration(120); self.ba.setStartValue(1.0); self.ba.setKeyValueAt(0.5, 0.0); self.ba.setEndValue(1.0); self.ba.start()

    def paintEvent(self, event) -> None:
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.save(); painter.translate(self._walk_x, 150)
        self._draw_dynamic_shadow(painter)
        self._render_ciro_3d(painter)
        painter.restore(); self._draw_label(painter)

    def _draw_dynamic_shadow(self, painter: QPainter) -> None:
        f = self._walk_phase * 2 * math.pi; bob = abs(math.sin(f * 2))
        size = (42 - bob * 4) * self._scale; grad = QRadialGradient(0, 0, size)
        grad.setColorAt(0, QColor(0, 0, 0, 60)); grad.setColorAt(1, Qt.GlobalColor.transparent)
        painter.setBrush(QBrush(grad)); painter.setPen(Qt.PenStyle.NoPen); painter.drawEllipse(QPointF(0, 0), size, 8*self._scale)

    def _render_ciro_3d(self, painter: QPainter) -> None:
        f = self._walk_phase * 2 * math.pi; rad = math.radians(self._yaw_angle); cos_y, sin_y = math.cos(rad), math.sin(rad)
        bounce_y = (-68 - abs(math.sin(f * 2)) * 5) * self._scale; lean = (0.08 if not self._is_turning else 0.0) * cos_y
        hip_c = QPointF(0, bounce_y); sh_y = bounce_y - 42*self._scale; sh_c = QPointF(lean*12*self._scale, sh_y)
        head_p = QPointF(sh_c.x() + lean*8*self._scale, sh_y - 16*self._scale)
        step_len = 22 * self._scale * abs(cos_y); step_h = 12 * self._scale
        pos_r = math.sin(f); foot_r_x = pos_r * step_len; foot_r_y = -abs(pos_r * step_h) if pos_r > 0 else 0
        pos_l = math.sin(f + math.pi); foot_l_x = pos_l * step_len; foot_l_y = -abs(pos_l * step_h) if pos_l > 0 else 0
        w_off = 11 * self._scale; r_hip_3d = QPointF(-w_off * sin_y, bounce_y); l_hip_3d = QPointF(w_off * sin_y, bounce_y)
        r_sh_3d = QPointF(sh_c.x() - w_off * sin_y, sh_y); l_sh_3d = QPointF(sh_c.x() + w_off * sin_y, sh_y)
        knee_r = self._solve_ik(r_hip_3d, QPointF(r_hip_3d.x() + foot_r_x, foot_r_y)); knee_l = self._solve_ik(l_hip_3d, QPointF(l_hip_3d.x() + foot_l_x, foot_l_y))
        render_queue = []; r_z, l_z = w_off * cos_y, -w_off * cos_y
        render_queue.append(RenderItem(-r_z, self._draw_leg, (r_hip_3d, knee_r, QPointF(r_hip_3d.x()+foot_r_x, foot_r_y), r_z, cos_y)))
        render_queue.append(RenderItem(-l_z, self._draw_leg, (l_hip_3d, knee_l, QPointF(l_hip_3d.x()+foot_l_x, foot_l_y), l_z, cos_y)))
        asw = math.sin(f) * 18 * self._scale * cos_y
        render_queue.append(RenderItem(-r_z, self._draw_arm, (r_sh_3d, QPointF(r_sh_3d.x()-asw, sh_y+22*self._scale), r_z)))
        render_queue.append(RenderItem(-l_z, self._draw_arm, (l_sh_3d, QPointF(l_sh_3d.x()+asw, sh_y+22*self._scale), l_z)))
        render_queue.append(RenderItem(0.0, self._draw_torso, (hip_c, sh_c, cos_y, sin_y)))
        render_queue.append(RenderItem(0.5, self._draw_head, (head_p, cos_y, sin_y)))
        render_queue.sort(key=lambda x: x.z_depth, reverse=True)
        for item in render_queue: item.draw_func(painter, *item.args)

    def _solve_ik(self, hip: QPointF, foot: QPointF) -> QPointF:
        dx, dy = foot.x() - hip.x(), foot.y() - hip.y(); dist = math.sqrt(dx*dx + dy*dy); max_d = (self.THIGH_LEN + self.CALF_LEN) * 0.96
        if dist > max_d: dist = max_d
        a, b, c = self.THIGH_LEN, self.CALF_LEN, dist
        try: cos_alpha = (a*a + c*c - b*b) / (2*a*c); alpha = math.acos(max(-1, min(1, cos_alpha)))
        except: alpha = 0.1
        # FIX GINOCCHIA: Basato sulla rotazione reale (cos_y)
        cy = math.cos(math.radians(self._yaw_angle)); bang = math.atan2(dy, dx)
        knee_angle = bang + (-alpha if cy >= 0 else alpha)
        return QPointF(hip.x() + math.cos(knee_angle) * a, hip.y() + math.sin(knee_angle) * a)

    def _draw_leg(self, painter: QPainter, hip, knee, foot, z, cos_y) -> None:
        op = 0.6 if z < 0 else 1.0; painter.setOpacity(op); c = self.C_SUIT.darker(110 if z < 0 else 100); p = QPainterPath(); p.moveTo(hip); p.lineTo(knee); p.lineTo(foot)
        painter.setPen(QPen(c, 11*self._scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)); painter.drawPath(p)
        self._draw_shoe(painter, QPointF(foot.x(), foot.y() + 3*self._scale), cos_y, z); painter.setOpacity(1.0)

    def _draw_shoe(self, painter: QPainter, foot: QPointF, cos_y: float, z: float) -> None:
        painter.save(); painter.translate(foot); painter.scale(1.0 if cos_y >= 0 else -1.0, 1.0)
        s = self._scale; painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QBrush(self.C_SHOE))
        path = QPainterPath(); path.moveTo(-8*s, 0); path.lineTo(18*s, 0); path.lineTo(18*s, -4*s); path.quadTo(15*s, -10*s, 5*s, -11*s); path.lineTo(-8*s, -11*s); path.closeSubpath()
        painter.drawPath(path); painter.setBrush(QBrush(QColor("#222222"))); painter.drawRect(QRectF(-8*s, -3*s, 8*s, 3*s)); painter.setBrush(QBrush(QColor(255,255,255,40))); painter.drawEllipse(QRectF(8*s, -10*s, 6*s, 2*s)); painter.restore()

    def _draw_arm(self, painter: QPainter, sh, hand, z) -> None:
        op = 0.6 if z < 0 else 1.0; painter.setOpacity(op); painter.setPen(QPen(self.C_SUIT, 7*self._scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)); painter.drawLine(sh, hand)
        painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QBrush(self.C_SKIN)); painter.drawEllipse(hand, 5*self._scale, 5*self._scale); painter.setOpacity(1.0)

    def _draw_torso(self, painter: QPainter, hip, sh, cos_y, sin_y) -> None:
        s = self._scale; w = 22 * s * (0.5 + 0.5 * abs(sin_y)); ch_off = 5 * s * cos_y
        path = QPainterPath(); path.moveTo(sh.x()-w+ch_off, sh.y()); path.cubicTo(sh.x()-w, sh.y()+18*s, hip.x()-w*0.6, hip.y()-18*s, hip.x()-w*0.6+ch_off, hip.y())
        path.lineTo(hip.x()+w*0.6+ch_off, hip.y()); path.cubicTo(hip.x()+w*0.6, hip.y()-18*s, sh.x()+w, sh.y()+18*s, sh.x()+w+ch_off, sh.y()); path.closeSubpath()
        grad = QLinearGradient(sh, hip); grad.setColorAt(0, self.C_SUIT.lighter(110)); grad.setColorAt(1, self.C_SUIT.darker(120))
        painter.setBrush(QBrush(grad)); painter.setPen(QPen(self.C_SUIT.darker(140), 1)); painter.drawPath(path)
        if sin_y > 0:
            painter.setBrush(QBrush(self.C_SHIRT)); painter.setPen(Qt.PenStyle.NoPen)
            shirt = QPainterPath(); shirt.moveTo(sh.x()+ch_off-7*s, sh.y()); shirt.lineTo(sh.x()+ch_off+7*s, sh.y()); shirt.lineTo(sh.x()+ch_off, sh.y()+18*s); painter.drawPath(shirt)
            painter.setBrush(QBrush(self.C_TIE)); tie = QPainterPath(); tie.moveTo(sh.x()+ch_off, sh.y()); tie.lineTo(sh.x()+ch_off-3*s, sh.y()+5*s); tie.lineTo(sh.x()+ch_off, sh.y()+32*s); tie.lineTo(sh.x()+ch_off+3*s, sh.y()+5*s); painter.drawPath(tie)

    def _draw_head(self, painter: QPainter, pos, cos_y, sin_y) -> None:
        s = self._scale
        # Calcolo visibilità orecchie basato sulla rotazione (come gli occhi)
        # ear_vis: 0 in pieno profilo (sin_y=0), 1 frontale
        ear_vis = max(0.0, min(1.0, abs(sin_y) * 2.0))
        
        # 1. ORECCHIO LONTANO (Si vede solo se frontale)
        e_col_back = self.C_SKIN.darker(140)
        painter.setOpacity(ear_vis)
        painter.setBrush(QBrush(e_col_back)); painter.setPen(QPen(e_col_back.darker(120), 0.6 * s))
        if cos_y > 0: painter.drawEllipse(QRectF(pos.x() + 10*s*cos_y + 8*s, pos.y() - 4*s, 5*s, 9*s))
        else:         painter.drawEllipse(QRectF(pos.x() + 10*s*cos_y - 13*s, pos.y() - 4*s, 5*s, 9*s))
        painter.setOpacity(1.0)

        # 2. VISO
        painter.setPen(Qt.PenStyle.NoPen); grad = QRadialGradient(pos, 20*s); grad.setColorAt(0, self.C_SKIN.lighter(105)); grad.setColorAt(1, self.C_SKIN.darker(115))
        painter.setBrush(QBrush(grad)); painter.drawEllipse(pos, 16*s, 18*s)
        
        # 3. ORECCHIO VICINO (Sempre visibile di profilo)
        e_col_front = self.C_SKIN.darker(120); painter.setBrush(QBrush(e_col_front)); painter.setPen(QPen(e_col_front.darker(120), 0.6 * s))
        if cos_y > 0: painter.drawEllipse(QRectF(pos.x() + 10*s*cos_y - 13*s, pos.y() - 4*s, 5*s, 9*s))
        else:         painter.drawEllipse(QRectF(pos.x() + 10*s*cos_y + 8*s, pos.y() - 4*s, 5*s, 9*s))
        
        # 4. CAPELLI DINAMICI
        painter.setBrush(QBrush(self.C_HAIR)); painter.setPen(Qt.PenStyle.NoPen); h_path = QPainterPath(); h_off = 7 * s * cos_y
        h_path.moveTo(pos.x() - 17*s, pos.y() + 3*s); h_path.cubicTo(pos.x() - 22*s + h_off, pos.y() - 35*s, pos.x() + 22*s + h_off, pos.y() - 35*s, pos.x() + 17*s, pos.y() + 3*s)
        h_path.lineTo(pos.x() + 14*s, pos.y() - 2*s); h_path.lineTo(pos.x() + 12*s * cos_y, pos.y() - 15*s); h_path.lineTo(pos.x() - 14*s, pos.y() - 2*s); painter.drawPath(h_path)
        
        # 5. OCCHI (Solo uno laterale, due frontali)
        if sin_y > -0.2:
            nx = pos.x() + 10*s * cos_y; gap = 5.5*s * abs(sin_y); eh = 6*s * self._blink; painter.setBrush(QBrush(Qt.GlobalColor.white))
            painter.drawEllipse(QRectF(nx + gap - 2.5*s, pos.y() + 1*s, 5*s, eh))
            if abs(sin_y) > 0.35: painter.drawEllipse(QRectF(nx - gap - 2.5*s, pos.y() + 1*s, 5*s, eh))
            if self._blink > 0.3:
                painter.setBrush(QBrush(Qt.GlobalColor.black)); poff = 1.5*s*cos_y; painter.drawEllipse(QRectF(nx + gap - 1.2*s + poff, pos.y() + 2*s, 2.5*s, 2.5*s))
                if abs(sin_y) > 0.35: painter.drawEllipse(QRectF(nx - gap - 1.2*s + poff, pos.y() + 2*s, 2.5*s, 2.5*s))

    def _draw_label(self, painter: QPainter) -> None:
        painter.save()
        f = self._label_phase * 2 * math.pi
        y_off = math.sin(f) * 3
        spacing = 200 + math.sin(f) * 20
        painter.translate(0, y_off)
        painter.setPen(QColor(COLORS['text_muted']))
        font = QFont("Segoe UI", 9, QFont.Weight.Black)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, spacing)
        painter.setFont(font); painter.setOpacity(0.15 + abs(math.sin(f)) * 0.1)
        painter.drawText(self.rect().adjusted(0, 10, 0, 0), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter, "DON CIRO")
        painter.restore()
