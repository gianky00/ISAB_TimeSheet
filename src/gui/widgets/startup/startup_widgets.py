"""
SyncroJob - Startup Widgets
Collezione di widget animati utilizzati nella Splash Screen.
"""

import hashlib
import math

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRect,
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QPixmap,
    QRadialGradient,
    QShowEvent,
)
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class AnimatedBorder(QWidget):
    """Bordo con luce che scorre e ombre illuminate."""

    BORDER_RADIUS = 28

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il componente del bordo animato."""
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.phase = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def _tick(self) -> None:
        """Aggiorna la fase dell'animazione."""
        self.phase += 0.018
        if self.phase > math.pi * 2:
            self.phase -= math.pi * 2
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna il bordo con effetti glow e conici, rispettando rigorosamente gli angoli arrotondati."""
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            w, h = self.width(), self.height()
            r = self.BORDER_RADIUS
            intensity = 0.6 + 0.4 * math.sin(self.phase * 2)

            # 1. CLIP PATH PER EVITARE PUNTE NEGLI ANGOLI
            clip_path = QPainterPath()
            clip_path.addRoundedRect(0.0, 0.0, float(w), float(h), float(r), float(r))
            painter.setClipPath(clip_path)

            # 2. GLOW INTERNO
            for offset in (2, 4, 6):
                glow_path = QPainterPath()
                glow_path.addRoundedRect(
                    float(offset),
                    float(offset),
                    float(w - offset * 2),
                    float(h - offset * 2),
                    float(r - offset),
                    float(r - offset),
                )
                alpha = int((20 - offset * 2) * intensity)
                pen = QPen(QColor(52, 152, 219, alpha), float(offset * 2))
                pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setPen(pen)
                painter.drawPath(glow_path)

            # 3. MAIN CONIC BORDER
            cx, cy = w / 2.0, h / 2.0
            conic = QConicalGradient(cx, cy, -math.degrees(self.phase))
            conic.setColorAt(0.0, QColor(52, 152, 219, int(255 * intensity)))
            conic.setColorAt(0.2, QColor(155, 89, 182, int(120 * intensity)))
            conic.setColorAt(0.5, QColor(100, 60, 140, int(60 * intensity)))
            conic.setColorAt(0.8, QColor(100, 180, 235, int(120 * intensity)))
            conic.setColorAt(1.0, QColor(52, 152, 219, int(255 * intensity)))

            border_path = QPainterPath()
            border_path.addRoundedRect(1.0, 1.0, float(w - 2), float(h - 2), float(r - 1), float(r - 1))
            pen = QPen(QBrush(conic), 2.5)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.drawPath(border_path)

            self._draw_light_points(painter, w, h, r)
        finally:
            painter.end()

    def _draw_light_points(self, painter: QPainter, w: int, h: int, r: int) -> None:
        """Disegna i punti luce che scorrono sul bordo."""
        t = self.phase
        cx, cy = w / 2.0, h / 2.0
        a, b = (w / 2.0) - 6.0, (h / 2.0) - 6.0
        intensity = 0.5 + 0.5 * math.sin(self.phase * 3)

        for i in range(5):
            trail_t = t - i * 0.08
            trail_intensity = intensity * (1 - i * 0.2)
            px, py = cx + a * math.cos(trail_t), cy + b * math.sin(trail_t)
            if i == 0:
                glow = QRadialGradient(px, py, 50.0)
                glow.setColorAt(0, QColor(255, 255, 255, int(200 * trail_intensity)))
                glow.setColorAt(0.5, QColor(52, 152, 219, int(60 * trail_intensity)))
                glow.setColorAt(1, QColor(52, 152, 219, 0))
                painter.setBrush(QBrush(glow))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPoint(int(px), int(py)), 50, 50)
                painter.setBrush(QColor(255, 255, 255, int(255 * trail_intensity)))
                painter.drawEllipse(QPoint(int(px), int(py)), 4, 4)
            else:
                trail_size = 20 - i * 3
                painter.setBrush(QColor(52, 152, 219, int(80 * trail_intensity)))
                painter.drawEllipse(QPoint(int(px), int(py)), trail_size, trail_size)


class GlowingProgressBar(QWidget):
    """Progress bar premium con Laser Core, tracking dati e shimmer olografico."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la barra di progresso luminosa."""
        super().__init__(parent)
        self._value = 0
        self._display_value = 0.0
        self._shimmer = -100.0
        self._phase = 0.0
        # Altezza aumentata per ospitare il testo olografico
        self.setFixedHeight(28)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def _tick(self) -> None:
        """Aggiorna il progresso e l'effetto shimmer/laser."""
        diff = self._value - self._display_value
        # Smoothing del valore visualizzato
        self._display_value += diff * 0.12
        self._shimmer += 5.0
        if self._shimmer > self.width() + 150:
            self._shimmer = -150.0
        self._phase += 0.08
        self.update()

    def setValue(self, val: int) -> None:
        """Imposta il valore del progresso (0-100)."""
        self._value = max(0, min(100, val))

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna la barra Laser-Track con tracking dati olografico."""
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            w, h = self.width(), self.height()
            bar_h = 6
            bar_y = h - bar_h - 2

            self._draw_track(painter, w, bar_y, bar_h)

            if self._display_value > 1:
                pw = int((self._display_value / 100.0) * w)
                self._draw_progress_and_laser(painter, pw, bar_y, bar_h)
                self._draw_holographic_data(painter, pw, w, bar_y, bar_h)
                self._draw_shimmer(painter, pw, bar_y, bar_h)
        finally:
            painter.end()

    def _draw_track(self, painter: QPainter, w: int, bar_y: int, bar_h: int) -> None:
        """Disegna lo sfondo segmentato della barra."""
        track_path = QPainterPath()
        track_path.addRoundedRect(0.0, float(bar_y), float(w), float(bar_h), 2.0, 2.0)
        painter.fillPath(track_path, QColor(10, 10, 20, 180))

        painter.setPen(QColor(52, 152, 219, 30))
        for i in range(0, w, 20):
            painter.drawLine(i, bar_y, i, bar_y + bar_h)

    def _draw_progress_and_laser(self, painter: QPainter, pw: int, bar_y: int, bar_h: int) -> None:
        """Disegna il gradiente di progresso e il core laser."""
        glow_intensity = 0.6 + 0.4 * math.sin(self._phase)
        glow_grad = QRadialGradient(pw, bar_y + bar_h / 2.0, 100.0)
        glow_grad.setColorAt(0, QColor(52, 152, 219, int(60 * glow_intensity)))
        glow_grad.setColorAt(1, QColor(52, 152, 219, 0))

        painter.save()
        painter.setBrush(QBrush(glow_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(pw), int(bar_y + bar_h / 2)), 80, 25)
        painter.restore()

        grad = QLinearGradient(0.0, float(bar_y), float(pw), float(bar_y))
        grad.setColorAt(0, QColor(52, 152, 219))
        grad.setColorAt(1, QColor(155, 89, 182))

        progress_path = QPainterPath()
        progress_path.addRoundedRect(0.0, float(bar_y), float(pw), float(bar_h), 2.0, 2.0)
        painter.fillPath(progress_path, grad)

        laser_pen = QPen(QColor(255, 255, 255, int(180 * glow_intensity)), 1.5)
        painter.setPen(laser_pen)
        painter.drawLine(2, int(bar_y + bar_h / 2), pw - 2, int(bar_y + bar_h / 2))

    def _draw_holographic_data(self, painter: QPainter, pw: int, w: int, bar_y: int, bar_h: int) -> None:
        """Disegna la percentuale olografica che segue la barra."""
        from PySide6.QtGui import QFont

        painter.setPen(QColor(100, 200, 255, 220))
        font = QFont("Consolas", 10, QFont.Weight.Bold)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1)
        painter.setFont(font)

        perc_text = f"{int(self._display_value)}%"
        text_x = max(0, min(pw - 15, w - 40))

        painter.setPen(QColor(0, 0, 0, 150))
        painter.drawText(text_x + 1, bar_y - 6 + 1, perc_text)
        painter.setPen(QColor(100, 200, 255, 220))
        painter.drawText(text_x, bar_y - 6, perc_text)

        head_pen = QPen(QColor(255, 255, 255, 255), 2)
        painter.setPen(head_pen)
        painter.drawLine(pw, bar_y - 2, pw, bar_y + bar_h + 2)

    def _draw_shimmer(self, painter: QPainter, pw: int, bar_y: int, bar_h: int) -> None:
        """Disegna l'effetto shimmer in movimento."""
        if 0 < self._shimmer < pw:
            painter.save()
            shimmer = QLinearGradient(self._shimmer - 60.0, 0.0, self._shimmer + 60.0, 0.0)
            shimmer.setColorAt(0, QColor(255, 255, 255, 0))
            shimmer.setColorAt(0.5, QColor(255, 255, 255, 100))
            shimmer.setColorAt(1, QColor(255, 255, 255, 0))

            progress_path = QPainterPath()
            progress_path.addRoundedRect(0.0, float(bar_y), float(pw), float(bar_h), 2.0, 2.0)
            painter.setClipPath(progress_path)
            painter.fillRect(int(self._shimmer - 60), bar_y, 120, bar_h, shimmer)
            painter.restore()


class PulsingLogo(QWidget):
    """Logo statico con bagliore soffuso (Nessuna animazione)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il widget del logo in modalità statica."""
        super().__init__(parent)
        self.pixmap: QPixmap | None = None

    def set_pixmap(self, pm: QPixmap) -> None:
        """Imposta l'immagine del logo."""
        self.pixmap = pm
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna il logo e il bagliore in modo statico."""
        if not self.pixmap:
            return
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

            w, h = float(self.width()), float(self.height())
            cx, cy = w / 2.0, h / 2.0

            # 1. BAGLIORE STATICO
            glow = QRadialGradient(cx, cy, 65.0)
            glow.setColorAt(0, QColor(52, 152, 219, 70))
            glow.setColorAt(1, QColor(52, 152, 219, 0))

            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(int(cx), int(cy)), 70, 70)

            # 2. DISEGNO LOGO STATICO
            logo_size = 64
            target_rect = QRect(int(cx - logo_size / 2), int(cy - logo_size / 2), logo_size, logo_size)
            painter.drawPixmap(target_rect, self.pixmap)

        finally:
            painter.end()


class TechBlueprint(QWidget):
    """Overlay olografico tecnico con cerchi rotanti e griglie polari."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza l'overlay tecnico."""
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.phase = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def _tick(self) -> None:
        """Aggiorna la rotazione del blueprint."""
        self.phase += 0.01
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna i cerchi tecnici e la griglia polare."""
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            w, h = self.width(), self.height()
            cx, cy = w / 2.0, h / 2.0

            painter.setPen(QPen(QColor(52, 152, 219, 40), 1, Qt.PenStyle.DotLine))

            # 1. Cerchi rotanti concentrici
            for i in range(3):
                radius = 40 + i * 25
                speed = (i + 1) * 0.5
                angle = math.degrees(self.phase * speed)

                painter.save()
                painter.translate(cx, cy)
                painter.rotate(angle if i % 2 == 0 else -angle)

                # Arco parziale per effetto "blueprint"
                painter.drawArc(-radius, -radius, radius * 2, radius * 2, 0, 240 * 16)

                # Piccoli marcatori sui cerchi
                painter.setPen(QPen(QColor(52, 152, 219, 80), 2))
                painter.drawPoint(radius, 0)
                painter.restore()
            # 2. Griglia polare sottile
            painter.setPen(QColor(52, 152, 219, 20))
            for angle in range(0, 360, 45):
                rad = math.radians(angle + math.degrees(self.phase * 0.2))
                x2 = cx + 100 * math.cos(rad)
                y2 = cy + 100 * math.sin(rad)
                painter.drawLine(int(cx), int(cy), int(x2), int(y2))
        finally:
            painter.end()


class TypewriterLabel(QLabel):
    """Label con effetto typewriter fluido."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._full_text = ""
        self._current_text = ""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_text)

    def set_text_animated(self, text: str, speed: int = 25) -> None:
        """Inizia l'animazione di digitazione."""
        self._full_text = text
        self._current_text = ""
        self.setText("")
        self._timer.start(speed)

    def set_text_instant(self, text: str) -> None:
        """Imposta il testo istantaneamente senza animazione."""
        self._timer.stop()
        self._full_text = text
        self.setText(text)

    def _update_text(self) -> None:
        if len(self._current_text) < len(self._full_text):
            self._current_text += self._full_text[len(self._current_text)]
            self.setText(self._current_text)
        else:
            self._timer.stop()


class ConsoleOverlay(QWidget):
    """Overlay CRT per la console di diagnostica."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna scanline orizzontali e griglia di punti sottile."""
        painter = QPainter(self)
        try:
            w, h = self.width(), self.height()

            # 1. SCANLINES ORIZZONTALI
            painter.setPen(QColor(0, 0, 0, 45))
            for y in range(0, h, 2):
                painter.drawLine(0, y, w, y)

            # 2. GRIGLIA DI PUNTI SUBTLE
            painter.setPen(QColor(52, 152, 219, 15))
            grid_size = 10
            for x in range(0, w, grid_size):
                for y in range(0, h, grid_size):
                    painter.drawPoint(x, y)

            # 3. EFFETTO VIGNETTE INTERNO
            grad = QRadialGradient(w / 2.0, h / 2.0, max(w, h) * 0.6)
            grad.setColorAt(0, QColor(0, 0, 0, 0))
            grad.setColorAt(1, QColor(0, 0, 0, 40))
            painter.fillRect(0, 0, w, h, grad)
        finally:
            painter.end()


class ChangelogTicker(QWidget):
    """Widget premium multi-riga (3 righe) con contenitore olografico e tag neon."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.notes: list[str] = []
        self.current_idx = 0
        self.num_rows = 3
        self.target_positions: list[QPoint] = []
        self.positions_initialized = False

        from src.gui.styles import COLORS

        self.COLORS = COLORS
        self._setup_ui_structure()
        self._create_content_rows()

        self.setFixedWidth(800)
        self.setFixedHeight(150)
        self.cycle_timer = QTimer(self)
        self.cycle_timer.timeout.connect(self.next_batch)

    def _setup_ui_structure(self) -> None:
        """Inizializza la struttura base e l'header del ticker con effetti premium."""
        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(10, 8, 10, 8)
        self.container_layout.setSpacing(12)

        # Header con stile moderno e spaziatura generosa
        self.header_label = QLabel("NOVITÀ DELLA VERSIONE INSTALLATA")
        self.header_label.setStyleSheet(
            f"font-size: 11px; color: {self.COLORS['primary_blue']}; letter-spacing: 3px; font-weight: 900;"
        )
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Effetto Glow al titolo

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        c_blue = QColor(self.COLORS["primary_blue"])
        shadow.setColor(QColor(c_blue.red(), c_blue.green(), c_blue.blue(), 180))
        shadow.setOffset(0, 0)
        self.header_label.setGraphicsEffect(shadow)

        self.container_layout.addWidget(self.header_label)

        self.frame = QFrame()
        c = QColor(self.COLORS["primary_blue"])
        self.frame.setStyleSheet(
            f"background: rgba(0, 0, 0, 0.5); "
            f"border: 1px solid rgba({c.red()}, {c.green()}, {c.blue()}, 0.25); "
            f"border-radius: 12px;"
        )
        self.container_layout.addWidget(self.frame)

        self.main_layout = QVBoxLayout(self.frame)
        self.main_layout.setContentsMargins(15, 8, 15, 8)
        self.main_layout.setSpacing(6)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _create_content_rows(self) -> None:
        """Crea le righe di contenuto con i relativi effetti di animazione."""
        self.labels = []
        self.opacity_effects = []
        self.groups = []

        for _ in range(self.num_rows):
            lbl = QLabel()
            lbl.setStyleSheet(
                "font-size: 11px; font-family: 'Consolas', monospace; color: white; border: none; padding: 0px;"
            )
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            lbl.setFixedWidth(760)
            lbl.setFixedHeight(22)

            opacity = QGraphicsOpacityEffect(lbl)
            lbl.setGraphicsEffect(opacity)

            group = QParallelAnimationGroup(self)
            fade = QPropertyAnimation(opacity, b"opacity")
            fade.setDuration(700)
            fade.setEasingCurve(QEasingCurve.Type.OutCubic)

            slide = QPropertyAnimation(lbl, b"pos")
            slide.setDuration(700)
            slide.setEasingCurve(QEasingCurve.Type.OutBack)

            group.addAnimation(fade)
            group.addAnimation(slide)

            self.main_layout.addWidget(lbl)
            self.labels.append(lbl)
            self.opacity_effects.append(opacity)
            self.groups.append(group)

    def showEvent(self, event: QShowEvent) -> None:
        """Cattura le posizioni reali del layout prima della prima visualizzazione."""
        super().showEvent(event)
        if not self.positions_initialized:
            QTimer.singleShot(100, self._initialize_positions)

    def _initialize_positions(self) -> None:
        """Salva le coordinate statiche delle label per usarle come ancora delle animazioni."""
        self.target_positions = [lbl.pos() for lbl in self.labels]
        self.positions_initialized = True
        self._show_batch()

    def set_notes(self, notes: list[str]) -> None:
        """Configura le note. L'avvio effettivo avviene in showEvent."""
        self.notes = [n for n in notes if n.strip()]
        if not self.notes:
            self.notes = ["VERSIONE OTTIMIZZATA - PRONTA ALL'USO"]
        self.current_idx = 0

    def _format_note(self, note: str) -> str:
        """Formatta la nota con tag neon, commit SHA (DNA) e stile premium."""
        clean = note.strip()
        lower = clean.lower()

        # Generazione DNA deterministico basato sulla nota (Cyber-Trace)
        dna = hashlib.sha256(clean.encode()).hexdigest()[:7]

        c_feat = self.COLORS.get("success_green", "#2ecc71")
        c_fix = self.COLORS.get("error_red", "#e74c3c")
        c_mod = self.COLORS.get("primary_blue", "#3498db")

        if lower.startswith("feat"):
            label, color = "NEW", c_feat
            msg = clean.split(":", 1)[1].strip() if ":" in clean else clean[4:].strip()
        elif lower.startswith("fix"):
            label, color = "FIX", c_fix
            msg = clean.split(":", 1)[1].strip() if ":" in clean else clean[3:].strip()
        else:
            label, color = "UPDATE", c_mod
            msg = clean

        max_chars = 85
        if len(msg) > max_chars:
            msg = msg[:max_chars] + "..."

        return (
            f'<span style="color:{color}; font-weight:900; letter-spacing:1px;">[{label}]</span> '
            f"<span style=\"color:rgba(255,255,255,0.4); font-family:'Consolas';\">[{dna}]</span> "
            f'<span style="color:rgba(255,255,255,0.9); font-weight:500;">{msg.upper()}</span>'
        )

    def _show_batch(self) -> None:
        """Mostra un gruppo di note con animazione di slide-up e fade-in."""
        from typing import cast

        if not self.positions_initialized:
            return

        for i in range(self.num_rows):
            note_idx = (self.current_idx + i) % len(self.notes)
            if i > 0 and note_idx == self.current_idx:
                self.labels[i].setText("")
                continue

            self.labels[i].setText(self._format_note(self.notes[note_idx]))

            final_pos = self.target_positions[i]
            start_pos = QPoint(final_pos.x(), final_pos.y() + 15)

            fade_anim = cast("QPropertyAnimation", self.groups[i].animationAt(0))
            slide_anim = cast("QPropertyAnimation", self.groups[i].animationAt(1))

            self.groups[i].stop()
            fade_anim.setStartValue(0.0)
            fade_anim.setEndValue(1.0)

            slide_anim.setStartValue(start_pos)
            slide_anim.setEndValue(final_pos)

            QTimer.singleShot(i * 150, self.groups[i].start)

        self.cycle_timer.start(3500)

    def next_batch(self) -> None:
        """Passa al prossimo set di note con fade-out coordinato."""
        from typing import cast

        self.cycle_timer.stop()

        for i in range(self.num_rows):
            fade_anim = cast("QPropertyAnimation", self.groups[i].animationAt(0))
            self.groups[i].stop()
            fade_anim.setStartValue(self.opacity_effects[i].opacity())
            fade_anim.setEndValue(0.0)
            if i == self.num_rows - 1:
                fade_anim.finished.connect(self._on_fade_out_finished)
            fade_anim.start()

    def _on_fade_out_finished(self) -> None:
        """Cambia indice e mostra il nuovo batch."""
        import contextlib

        with contextlib.suppress(Exception):
            self.groups[self.num_rows - 1].animationAt(0).finished.disconnect(self._on_fade_out_finished)

        self.current_idx = (self.current_idx + self.num_rows) % len(self.notes)
        self._show_batch()


class PulseIndicator(QWidget):
    """Indicatore di caricamento premium con anello ad espansione olografico."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self._pulse_radius = 4.0
        self._pulse_opacity = 0.8

        # Importazione pigra colori
        from src.gui.styles import COLORS

        self.color = QColor(COLORS["primary_blue"])

        # Animazione del raggio e opacità
        self.anim_group = QParallelAnimationGroup(self)

        self.radius_anim = QPropertyAnimation(self, b"pulse_radius")
        self.radius_anim.setDuration(1500)
        self.radius_anim.setStartValue(4.0)
        self.radius_anim.setEndValue(14.0)
        self.radius_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.opacity_anim = QPropertyAnimation(self, b"pulse_opacity")
        self.opacity_anim.setDuration(1500)
        self.opacity_anim.setStartValue(0.8)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.setEasingCurve(QEasingCurve.Type.Linear)

        self.anim_group.addAnimation(self.radius_anim)
        self.anim_group.addAnimation(self.opacity_anim)
        self.anim_group.setLoopCount(-1)
        self.anim_group.start()

    @Property(float)
    def pulse_radius(self) -> float:
        return self._pulse_radius

    @pulse_radius.setter  # type: ignore
    def pulse_radius(self, val: float) -> None:
        self._pulse_radius = val
        self.update()

    @Property(float)
    def pulse_opacity(self) -> float:
        return self._pulse_opacity

    @pulse_opacity.setter  # type: ignore
    def pulse_opacity(self, val: float) -> None:
        self._pulse_opacity = val
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            cx, cy = self.width() / 2.0, self.height() / 2.0

            # 1. NUCLEO FISSO
            painter.setBrush(self.color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(int(cx), int(cy)), 4, 4)

            # 2. ANELLO PULSANTE
            if self._pulse_opacity > 0:
                alpha = int(self._pulse_opacity * 255)
                pen_color = QColor(self.color.red(), self.color.green(), self.color.blue(), alpha)
                painter.setPen(QPen(pen_color, 1.5))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawEllipse(
                    QPoint(int(cx), int(cy)), int(self._pulse_radius), int(self._pulse_radius)
                )
        finally:
            painter.end()
