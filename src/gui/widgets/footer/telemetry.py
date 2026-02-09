import os
import platform
import socket
import time
from contextlib import suppress

import psutil
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QHideEvent, QShowEvent
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


class BootTelemetryWidget(QWidget):
    """Telemetria avanzata real-time (FASE 1: Boot)."""

    TEXT_COLOR = "#000000"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 2, 10, 2)
        layout.setSpacing(20)

        self.process = psutil.Process(os.getpid())
        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()
        self.session_id = f"{int(time.time()):x}".upper()
        self.font_style = f"font-family: 'Consolas', monospace; font-size: 13px; color: {self.TEXT_COLOR};"

        self.lbl_os = QLabel()
        self.lbl_os.setStyleSheet(self.font_style)
        self.lbl_arch = QLabel()
        self.lbl_arch.setStyleSheet(self.font_style)
        self.lbl_host = QLabel()
        self.lbl_host.setStyleSheet(self.font_style)
        self.lbl_ip = QLabel()
        self.lbl_ip.setStyleSheet(self.font_style)
        self.lbl_cpu = QLabel()
        self.lbl_cpu.setStyleSheet(self.font_style)
        self.lbl_ram = QLabel()
        self.lbl_ram.setStyleSheet(self.font_style)

        # Aggiunta semplificata per brevità
        layout.addWidget(self.lbl_os)
        layout.addWidget(self.lbl_host)
        layout.addWidget(self.lbl_cpu)
        layout.addWidget(self.lbl_ram)
        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)

    def showEvent(self, event: QShowEvent | None) -> None:
        if event is not None:
            super().showEvent(event)
        self.timer.start(1000)
        self._update_stats()

    def hideEvent(self, event: QHideEvent | None) -> None:
        if event is not None:
            super().hideEvent(event)
        self.timer.stop()

    def _update_stats(self) -> None:
        with suppress(Exception):
            self.lbl_os.setText(f"OS: {platform.system()}")
            self.lbl_host.setText(f"HOST: {socket.gethostname()}")
            self.lbl_cpu.setText(f"CPU: {psutil.cpu_percent()}%")
            self.lbl_ram.setText(f"RAM: {psutil.virtual_memory().percent}%")
