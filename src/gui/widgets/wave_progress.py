"""
SyncroJob - Wave Progress Bar
Custom widget for spectacular wave animation.
"""

import math
from typing import Any

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPainterPath
from PyQt6.QtWidgets import QProgressBar, QWidget


class WaveProgressBar(QProgressBar):
    """
    Barra di progresso custom con animazione ad onda spettacolare.
    Utilizza QPainter per il disegno sinusoidale a 60fps.
    """

    # Costanti estetiche per l'animazione
    ANIMATION_FPS = 16  # ms per frame (~60fps)
    DEFAULT_HEIGHT = 34
    WAVE_THRESHOLD_LIGHT = 0.55  # Soglia colore testo (nero/bianco)
    HEIGHT_THRESHOLD_MINI = 20  # Soglia per font ridotto (9px)
    HEIGHT_THRESHOLD_TEXT = 12  # Altezza minima per disegnare testo
    HEIGHT_THRESHOLD_WAVE = 15  # Soglia per ampiezza onda ridotta

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(self.DEFAULT_HEIGHT)
        self.setRange(0, 100)
        self.setValue(0)
        self.setTextVisible(False)  # Gestito nel paintEvent
        self._phase = 0.0
        self._phase2 = 0.0

        # Timer per l'animazione dell'onda
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_wave)
        self.timer.start(self.ANIMATION_FPS)

    def _update_wave(self) -> None:
        """Aggiorna le fasi delle onde per l'effetto di movimento."""
        if self.value() >= self.maximum() and self.maximum() > 0:
            # Mantieni l'animazione anche al 100% per fluidità se desiderato,
            # o fermala per risparmiare risorse.
            # Qui la fermiamo se completata.
            self.timer.stop()
            self.update()
            return

        self._phase += 0.08
        self._phase2 += 0.05
        self.update()

    def paintEvent(self, event: Any) -> None:
        """Disegno personalizzato dell'onda e del testo."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        width = rect.width()
        height = rect.height()
        radius = rect.height() // 4 if rect.height() < self.HEIGHT_THRESHOLD_MINI else 8

        # Clip per angoli arrotondati
        clip_path = QPainterPath()
        clip_path.addRoundedRect(0, 0, width, height, float(radius), float(radius))
        painter.setClipPath(clip_path)

        # 1. Sfondo
        painter.fillRect(rect, QColor("#F8F9FA"))
        painter.setPen(QColor("#E0E0E0"))
        painter.drawRoundedRect(0, 0, width - 1, height - 1, float(radius), float(radius))

        # Calcolo livello acqua (percentuale) con clamp di sicurezza [0, 1]
        raw_progress = self.value() / self.maximum() if self.maximum() > 0 else 0
        progress = max(0.0, min(1.0, raw_progress))
        water_level = height * (1 - progress)

        # 2. Onda Secondaria (Background wave)
        wave2_path = QPainterPath()
        wave2_path.moveTo(0.0, float(height))
        amplitude2 = height / 10 if height > self.HEIGHT_THRESHOLD_WAVE else 2.0
        wavelength2 = width / 6
        for x in range(0, width + 1, 2):
            y = water_level + amplitude2 * math.sin(x / wavelength2 + self._phase2)
            wave2_path.lineTo(float(x), float(y))
        wave2_path.lineTo(float(width), float(height))
        wave2_path.closeSubpath()

        wave2_color = QColor("#00B4DB")
        wave2_color.setAlpha(80)
        painter.fillPath(wave2_path, QBrush(wave2_color))

        # 3. Onda Primaria (Foreground wave)
        wave_path = QPainterPath()
        wave_path.moveTo(0.0, float(height))
        amplitude = height / 7 if height > self.HEIGHT_THRESHOLD_WAVE else 3.0
        wavelength = width / 5
        for x in range(0, width + 1, 2):
            y = water_level + amplitude * math.sin(x / wavelength + self._phase)
            wave_path.lineTo(float(x), float(y))
        wave_path.lineTo(float(width), float(height))
        wave_path.closeSubpath()

        gradient = QLinearGradient(0.0, water_level - amplitude, 0.0, float(height))
        gradient.setColorAt(0.0, QColor("#00B4DB"))  # Azure
        gradient.setColorAt(1.0, QColor("#0D6EFD"))  # Royal Blue
        painter.fillPath(wave_path, QBrush(gradient))

        # 4. Testo Percentuale (visibile solo se altezza sufficiente o sempre al centro)
        if height > self.HEIGHT_THRESHOLD_TEXT:
            percent_str = f"{int(progress * 100)}%"
            # Cambio colore dinamico basato sul livello dell'onda rispetto al centro
            color = "#212529" if progress < self.WAVE_THRESHOLD_LIGHT else "#FFFFFF"
            painter.setPen(QColor(color))

            font_size = 9 if height < self.HEIGHT_THRESHOLD_MINI else 10
            painter.setFont(QFont("Segoe UI Variable Display", font_size, QFont.Weight.Bold))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, percent_str)
