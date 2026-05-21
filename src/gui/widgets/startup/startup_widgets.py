"""
SyncroJob - Startup Widgets
Collezione di widget animati utilizzati nella Splash Screen.
"""

import math

from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QRect, Qt, QTimer
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
)
from PySide6.QtWidgets import (
    QFrame,
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
            # Questo assicura che nulla venga disegnato fuori dagli angoli smussati
            clip_path = QPainterPath()
            clip_path.addRoundedRect(0.0, 0.0, float(w), float(h), float(r), float(r))
            painter.setClipPath(clip_path)

            # 2. GLOW INTERNO (Invece di esterno che veniva tagliato)
            for offset in (2, 4, 6):
                glow_path = QPainterPath()
                # Disegniamo leggermente all'interno per evitare artefatti di clipping
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

            # 3. MAIN CONIC BORDER (Posizionato esattamente sul bordo)
            cx, cy = w / 2.0, h / 2.0
            conic = QConicalGradient(cx, cy, -math.degrees(self.phase))
            conic.setColorAt(0.0, QColor(52, 152, 219, int(255 * intensity)))
            conic.setColorAt(0.2, QColor(155, 89, 182, int(120 * intensity)))
            conic.setColorAt(0.5, QColor(100, 60, 140, int(60 * intensity)))
            conic.setColorAt(0.8, QColor(100, 180, 235, int(120 * intensity)))
            conic.setColorAt(1.0, QColor(52, 152, 219, int(255 * intensity)))

            border_path = QPainterPath()
            # Un leggero inset di 1px assicura che l'antialiasing del bordo non venga tagliato
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
    """Progress bar con glow e shimmer."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la barra di progresso luminosa."""
        super().__init__(parent)
        self._value = 0
        self._display_value = 0.0
        self._shimmer = -100.0
        self._phase = 0.0
        self.setFixedHeight(6)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def _tick(self) -> None:
        """Aggiorna il progresso e l'effetto shimmer."""
        diff = self._value - self._display_value
        self._display_value += diff * 0.15
        self._shimmer += 4.0
        if self._shimmer > self.width() + 100:
            self._shimmer = -100.0
        self._phase += 0.08
        self.update()

    def setValue(self, val: int) -> None:
        """
        Imposta il valore del progresso (0-100).

        Args:
            val: Valore intero del progresso.
        """
        self._value = max(0, min(100, val))

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna la barra di progresso con effetto gradiente, shimmer e glow dinamico."""
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            w, h = self.width(), self.height()

            # 1. TRACK SFONDO
            track = QPainterPath()
            track.addRoundedRect(0.0, 0.0, float(w), float(h), 3.0, 3.0)
            painter.fillPath(track, QColor(15, 15, 25))

            if self._display_value > 0:
                pw = int((self._display_value / 100.0) * w)

                # 2. GLOW DINAMICO (Bagliore sotto la barra)
                glow_grad = QRadialGradient(pw, h / 2.0, 80.0)
                glow_grad.setColorAt(0, QColor(52, 152, 219, 40))
                glow_grad.setColorAt(1, QColor(52, 152, 219, 0))
                painter.save()
                painter.setBrush(QBrush(glow_grad))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPoint(int(pw), int(h / 2)), 60, 15)
                painter.restore()

                # 3. BARRA DI PROGRESSO
                grad = QLinearGradient(0.0, 0.0, float(pw), 0.0)
                grad.setColorAt(0, QColor(52, 152, 219))
                grad.setColorAt(1, QColor(155, 89, 182))

                progress = QPainterPath()
                progress.addRoundedRect(0.0, 0.0, float(pw), float(h), 3.0, 3.0)
                painter.fillPath(progress, grad)

                # 4. EFFETTO SHIMMER (Riflesso che scorre)
                if 0 < self._shimmer < pw:
                    painter.save()
                    shimmer = QLinearGradient(self._shimmer - 40.0, 0.0, self._shimmer + 40.0, 0.0)
                    shimmer.setColorAt(0, QColor(255, 255, 255, 0))
                    shimmer.setColorAt(0.5, QColor(255, 255, 255, 120))
                    shimmer.setColorAt(1, QColor(255, 255, 255, 0))
                    painter.setClipPath(progress)
                    painter.fillRect(int(self._shimmer - 40), 0, 80, h, shimmer)
                    painter.restore()
        finally:
            painter.end()


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
        """Inizializza la label typewriter."""
        super().__init__(parent)
        self._target, self._current, self._index = "", "", 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._type)

    def set_text_animated(self, text: str, speed: int = 20) -> None:
        """
        Imposta il testo con un'animazione di digitazione.

        Args:
            text: Testo da visualizzare.
            speed: Velocità di digitazione in ms.
        """
        self._target, self._current, self._index = text, "", 0
        self._timer.start(speed)

    def set_text_instant(self, text: str) -> None:
        """
        Imposta il testo istantaneamente senza animazione.

        Args:
            text: Testo da visualizzare.
        """
        self._timer.stop()
        self._target = self._current = text
        self._index = len(text)
        self.setText(text)

    def _type(self) -> None:
        """Slot del timer che aggiunge un carattere alla volta."""
        if self._index < len(self._target):
            self._index += 1
            self._current = self._target[: self._index]
            self.setText(self._current)
        else:
            self._timer.stop()


class ConsoleOverlay(QWidget):
    """Overlay per la console con effetto scanline e griglia CRT."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza l'overlay della console."""
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

        # Importazione pigra dei colori
        from src.gui.styles import COLORS

        self.COLORS = COLORS

        # Layout principale: aggiunge un margine per il contenitore
        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(10, 8, 10, 8)

        # Frame olografico interno
        self.frame = QFrame()
        c = QColor(COLORS["primary_blue"])
        self.frame.setStyleSheet(
            f"background: rgba(0, 0, 0, 0.5); "
            f"border: 1px solid rgba({c.red()}, {c.green()}, {c.blue()}, 0.25); "
            f"border-radius: 12px;"
        )
        self.container_layout.addWidget(self.frame)

        # Layout interno per le righe
        self.main_layout = QVBoxLayout(self.frame)
        self.main_layout.setContentsMargins(15, 8, 15, 8)
        self.main_layout.setSpacing(6)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.labels: list[QLabel] = []
        self.opacity_effects: list[QGraphicsOpacityEffect] = []
        self.animations: list[QPropertyAnimation] = []

        # Creazione delle righe
        for _ in range(self.num_rows):
            lbl = QLabel()
            lbl.setStyleSheet(
                "font-size: 11px; "
                "font-family: 'Consolas', 'Fira Code', monospace; "
                "color: white; "
                "background: transparent;"
            )
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            lbl.setFixedWidth(710)
            lbl.setFixedHeight(22)

            opacity = QGraphicsOpacityEffect(lbl)
            lbl.setGraphicsEffect(opacity)
            anim = QPropertyAnimation(opacity, b"opacity")
            anim.setEasingCurve(QEasingCurve.Type.InOutSine)
            anim.setDuration(600)

            self.main_layout.addWidget(lbl)
            self.labels.append(lbl)
            self.opacity_effects.append(opacity)
            self.animations.append(anim)

        self.setFixedWidth(750)
        self.setFixedHeight(120)  # Spazio per 3 righe + frame + margins

        # Timer per il ciclo di aggiornamento
        self.cycle_timer = QTimer(self)
        self.cycle_timer.timeout.connect(self.next_batch)

    def set_notes(self, notes: list[str]) -> None:
        """Configura le note e avvia il primo batch."""
        self.notes = [n for n in notes if n.strip()]
        if not self.notes:
            self.notes = ["VERSIONE OTTIMIZZATA - PRONTA ALL'USO"]

        self.current_idx = 0
        self._show_batch()

    def _format_note(self, note: str) -> str:
        """Formatta la nota con tag neon e stile premium."""
        clean = note.strip()
        lower = clean.lower()

        c_feat = self.COLORS.get("success_green", "#2ecc71")
        c_fix = self.COLORS.get("error_red", "#e74c3c")
        c_mod = self.COLORS.get("primary_blue", "#3498db")

        if lower.startswith("feat"):
            label, color = "FEAT", c_feat
            msg = clean.split(":", 1)[1].strip() if ":" in clean else clean[4:].strip()
        elif lower.startswith("fix"):
            label, color = "FIX", c_fix
            msg = clean.split(":", 1)[1].strip() if ":" in clean else clean[3:].strip()
        else:
            label, color = "UPD", c_mod
            msg = clean

        # Tronca se troppo lungo per la riga (Aumentato per nuova larghezza)
        max_chars = 90
        if len(msg) > max_chars:
            msg = msg[:max_chars] + "..."

        # Tag con effetto neon (tramite bold e colori saturi)
        return (
            f'<span style="color:{color}; font-weight:900; letter-spacing:1px;">[{label}]</span> '
            f'<span style="color:rgba(255,255,255,0.9); font-weight:500;">{msg.upper()}</span>'
        )

    def _show_batch(self) -> None:
        """Mostra un gruppo di note con animazione di fade-in."""
        for i in range(self.num_rows):
            note_idx = (self.current_idx + i) % len(self.notes)
            if i > 0 and note_idx == self.current_idx:
                self.labels[i].setText("")
                continue

            self.labels[i].setText(self._format_note(self.notes[note_idx]))

            self.animations[i].stop()
            self.animations[i].setStartValue(0.0)
            self.animations[i].setEndValue(1.0)
            QTimer.singleShot(i * 120, self.animations[i].start)

        self.cycle_timer.start(6000)

    def next_batch(self) -> None:
        """Passa al prossimo set di note con fade-out coordinato."""
        self.cycle_timer.stop()

        for i in range(self.num_rows):
            self.animations[i].stop()
            self.animations[i].setStartValue(self.opacity_effects[i].opacity())
            self.animations[i].setEndValue(0.0)
            if i == self.num_rows - 1:
                self.animations[i].finished.connect(self._on_fade_out_finished)
            self.animations[i].start()

    def _on_fade_out_finished(self) -> None:
        """Cambia indice e mostra il nuovo batch."""
        import contextlib

        with contextlib.suppress(Exception):
            self.animations[self.num_rows - 1].finished.disconnect(self._on_fade_out_finished)

        self.current_idx = (self.current_idx + self.num_rows) % len(self.notes)
        self._show_batch()
