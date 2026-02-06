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

from src.utils.system_telemetry import FILETIME, get_current_process_ram_mb


class ResourceMonitor(QWidget):
    """HUD Monitor per Risorse (RAM/CPU Activity)."""

    def __init__(self, parent=None):
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
            "color: rgba(52, 152, 219, 0.9); font-size: 10px; font-weight: 700; font-family: 'Consolas';"
        )

        # CPU Indicator
        self.cpu_lbl = QLabel("CPU: 0%")
        self.cpu_lbl.setStyleSheet(
            "color: rgba(46, 204, 113, 0.9); font-size: 10px; font-weight: 700; font-family: 'Consolas';"
        )

        stats_layout.addWidget(self.ram_lbl)
        stats_layout.addWidget(self.cpu_lbl)

        # Activity Indicator (Fake IO visualization)
        self.activity_bar = QFrame()
        self.activity_bar.setFixedSize(6, 28)
        self.activity_bar.setStyleSheet(
            "background: rgba(255,255,255,0.1); border-radius: 3px;"
        )

        layout.addStretch()
        layout.addLayout(stats_layout)
        layout.addWidget(self.activity_bar)

        # CPU tracking state
        self.last_proc_time = 0
        self.last_time = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(500)  # 2Hz refresh

        self._activity_level = 0

    def _get_cpu_time(self):
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

                def ft_to_int(ft):
                    return (ft.dwHighDateTime << 32) + ft.dwLowDateTime

                return ft_to_int(kernel) + ft_to_int(user)
        return 0

    def _update_stats(self):
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
                    cpu_percent = (
                        delta_proc / (delta_time * 10_000_000 * cpu_count)
                    ) * 100
                    self.cpu_lbl.setText(f"CPU: {cpu_percent:.1f}%")

            self.last_proc_time = current_proc
            self.last_time = current_time
        except Exception:
            self.cpu_lbl.setText("CPU: N/A")

        # Decay activity
        with suppress(Exception):
            self._activity_level = max(0, self._activity_level - 10)
            self._draw_activity()

    def trigger_activity(self):
        """Chiamato quando c'è un log event per simulare carico CPU/IO."""
        self._activity_level = min(100, self._activity_level + 30)
        self._draw_activity()

    def _draw_activity(self):
        h = int((self._activity_level / 100) * 28)
        if not hasattr(self, "_bar_fill"):
            self._bar_fill = QLabel(self.activity_bar)
            self._bar_fill.setFixedWidth(6)
            self._bar_fill.move(0, 28)

        if self._activity_level > 80:
            col = "#e74c3c"
        elif self._activity_level > 40:
            col = "#f1c40f"
        else:
            col = "#2ecc71"

        self._bar_fill.setFixedHeight(max(0, h))
        self._bar_fill.move(0, 28 - h)
        self._bar_fill.setStyleSheet(f"background: {col}; border-radius: 3px;")
