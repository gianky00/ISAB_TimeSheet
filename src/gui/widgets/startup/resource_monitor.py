"""
SyncroJob - Resource Monitor
HUD per il monitoraggio in tempo reale di RAM e CPU durante l'avvio.
"""

import ctypes
import os
import time
from contextlib import suppress
from ctypes import byref

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.utils.system_telemetry import FILETIME, get_current_process_ram_mb


class ResourceMonitor(QWidget):
    """HUD Monitor per Risorse (RAM/CPU Activity)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(140, 38)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Stats Layout (Vertical)
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(0)
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # RAM Indicator
        self.ram_lbl = QLabel("RAM: 0MB")
        self.ram_lbl.setStyleSheet(
            f"color: {hex_to_rgba(COLORS['primary_blue'], 0.9)}; font-size: 10px; font-weight: 700; font-family: 'Consolas';"
        )

        # CPU Indicator
        self.cpu_lbl = QLabel("CPU: 0%")
        self.cpu_lbl.setStyleSheet(
            f"color: {hex_to_rgba(COLORS['success_green'], 0.9)}; font-size: 10px; font-weight: 700; font-family: 'Consolas';"
        )

        stats_layout.addWidget(self.ram_lbl)
        stats_layout.addWidget(self.cpu_lbl)

        # Activity Indicator (Fake IO visualization)
        self.activity_bar = QFrame()
        self.activity_bar.setFixedSize(6, 28)
        self.activity_bar.setStyleSheet(
            f"background: {hex_to_rgba(COLORS['bg_white'], 0.1)}; border-radius: 3px;"
        )

        layout.addStretch()
        layout.addLayout(stats_layout)
        layout.addWidget(self.activity_bar)

        # CPU tracking state
        self.last_proc_time: int = 0
        self.last_time: float = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(500)  # 2Hz refresh

        self._activity_level = 0
        self._bar_fill: QLabel | None = None

    def _get_cpu_time(self) -> int:
        """Get total kernel + user time for this process in 100ns units."""
        with suppress(Exception):
            creation, exit, kernel, user = (
                FILETIME(),
                FILETIME(),
                FILETIME(),
                FILETIME(),
            )
            if ctypes.windll.kernel32.GetProcessTimes(
                ctypes.windll.kernel32.GetCurrentProcess(),
                byref(creation),
                byref(exit),
                byref(kernel),
                byref(user),
            ):

                def ft_to_int(ft: FILETIME) -> int:
                    return int((ft.dwHighDateTime << 32) + ft.dwLowDateTime)

                return ft_to_int(kernel) + ft_to_int(user)
        return 0

    def _update_stats(self) -> None:
        if not self.isVisible():
            return

        # Update RAM
        with suppress(Exception):
            mb = get_current_process_ram_mb()
            self.ram_lbl.setText(f"RAM: {int(mb)}MB")

        # Update CPU
        try:
            current_proc = self._get_cpu_time()
            current_time = time.time()

            if self.last_time > 0:
                delta_proc = current_proc - self.last_proc_time
                delta_time = current_time - self.last_time

                if delta_time > 0:
                    cpu_count = os.cpu_count() or 1
                    cpu_percent = (delta_proc / (delta_time * 10_000_000 * cpu_count)) * 100
                    self.cpu_lbl.setText(f"CPU: {cpu_percent:.1f}%")

            self.last_proc_time = current_proc
            self.last_time = current_time
        except Exception:
            self.cpu_lbl.setText("CPU: N/A")

        # Decay activity
        with suppress(Exception):
            self._activity_level = max(0, self._activity_level - 10)
            self._draw_activity()

    def trigger_activity(self) -> None:
        """Chiamato quando c'è un log event per simulare carico CPU/IO."""
        self._activity_level = min(100, self._activity_level + 30)
        self._draw_activity()

    def _draw_activity(self) -> None:
        h = int((self._activity_level / 100.0) * 28)
        if self._bar_fill is None:
            self._bar_fill = QLabel(self.activity_bar)
            self._bar_fill.setFixedWidth(6)
            self._bar_fill.move(0, 28)

        if self._activity_level > 80:
            col = COLORS["error_red"]
        elif self._activity_level > 40:
            col = COLORS["warning_yellow"]
        else:
            col = COLORS["success_green"]

        self._bar_fill.setFixedHeight(max(0, h))
        self._bar_fill.move(0, 28 - h)
        self._bar_fill.setStyleSheet(f"background: {col}; border-radius: 3px;")
