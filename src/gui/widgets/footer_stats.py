"""
SyncroJob - Footer Stats & Telemetry PRO
Widget avanzati per il monitoraggio risorse, stato bot e identità sessione.
Implementa logica a due fasi: FASE 1 (Boot) e FASE 2 (Operativo).
"""

import os
import time
from typing import Optional

import psutil
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager


class FooterItemWidget(QWidget):
    """Elemento informativo con tag e valore."""

    def __init__(
        self, label: str, value: str = "", color: str = "#607D8B", parent=None
    ):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        self.lbl_tag = QLabel(label)
        self.lbl_tag.setStyleSheet(
            f"color: {color}; font-weight: bold; font-size: 11px; background: transparent;"
        )
        layout.addWidget(self.lbl_tag)

        self.lbl_val = QLabel(value)
        self.lbl_val.setStyleSheet(
            "color: #212529; font-size: 11px; background: transparent;"
        )
        layout.addWidget(self.lbl_val)

    def set_text(self, text: str):
        self.lbl_val.setText(text)


class StartupConsole(QLabel):
    """Console per log di sistema nel footer (FASE 1: Boot)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Sistema Operativo Pronto")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            """
            QLabel {
                color: #546E7A;
                font-family: 'Segoe UI Semibold';
                font-size: 10px;
                padding: 0 15px;
                background: transparent;
            }
        """
        )
        self._log_queue = []

    def log(self, message: str, is_error: bool = False):
        """Registra un messaggio nel log della console."""
        color = "#cc0000" if is_error else "#000000"
        self.setText(message)
        self.setStyleSheet(
            f"color: {color}; font-family: 'Consolas', monospace; font-size: 13px; padding: 0 10px;"
        )
        self._log_queue.append((message, is_error))
        # Mantieni solo gli ultimi 100 messaggi
        if len(self._log_queue) > 100:
            self._log_queue.pop(0)

    def get_history(self):
        """Ritorna la storia dei log."""
        return self._log_queue

    def set_log(self, message: str, current: int = 0, total: int = 0):
        """Compatibilità con main_window.py - mostra il messaggio."""
        self.log(message)


class ClickableLabel(QLabel):
    """Label con hover effect per dati interattivi."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._base_style = ""
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def setBaseStyle(self, style: str):
        self._base_style = style
        self.setStyleSheet(style)

    def enterEvent(self, event):
        # Hover: sfondo leggero e sottolineatura
        self.setStyleSheet(
            self._base_style
            + " background: rgba(0,0,0,0.05); border-radius: 3px; padding: 2px 4px;"
        )
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self._base_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        # Nota: ClickableLabel non ha signal - solo visual feedback
        super().mousePressEvent(event)


class FooterLeftWidget(QWidget):
    """
    Parte sinistra del footer: Business Info con layout verticale ottimizzato.
    Colonna 1: Cliente/Scadenza | Colonna 2: Ultimo Accesso | Colonna 3: Portale/SafeWork
    """

    # Signal emessi quando si clicca sui label
    portale_clicked = pyqtSignal()
    safework_clicked = pyqtSignal()

    # Colore unificato nero
    TEXT_COLOR = "#000000"

    _fade_anim: Optional[QPropertyAnimation]

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 2, 0, 2)
        layout.setSpacing(20)

        # Opacity effect per fade-in
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)

        # Colonna 1: Cliente / Scadenza (verticale)
        col1 = QWidget()
        col1_layout = QVBoxLayout(col1)
        col1_layout.setContentsMargins(0, 0, 0, 0)
        col1_layout.setSpacing(2)

        self.client_item = QLabel()
        self.client_item.setStyleSheet(
            f"color: {self.TEXT_COLOR}; font-size: 13px; background: transparent;"
        )
        col1_layout.addWidget(self.client_item)

        self.expiry_item = QLabel()
        self.expiry_item.setStyleSheet(
            f"color: {self.TEXT_COLOR}; font-size: 13px; background: transparent;"
        )
        col1_layout.addWidget(self.expiry_item)
        layout.addWidget(col1)

        self._add_separator(layout)

        # Colonna 2: HW ID / Ultimo Accesso (verticale)
        col2 = QWidget()
        col2_layout = QVBoxLayout(col2)
        col2_layout.setContentsMargins(0, 0, 0, 0)
        col2_layout.setSpacing(2)

        self.hw_id_item = QLabel()
        self.hw_id_item.setStyleSheet(
            f"color: {self.TEXT_COLOR}; font-size: 13px; background: transparent;"
        )
        col2_layout.addWidget(self.hw_id_item)

        self.last_login_item = QLabel()
        self.last_login_item.setStyleSheet(
            f"color: {self.TEXT_COLOR}; font-size: 13px; background: transparent;"
        )
        col2_layout.addWidget(self.last_login_item)
        layout.addWidget(col2)

        self._add_separator(layout)

        # Colonna 3: Portale Fornitori / SafeWork (verticale) - con hover
        col3 = QWidget()
        col3_layout = QVBoxLayout(col3)
        col3_layout.setContentsMargins(0, 0, 0, 0)
        col3_layout.setSpacing(2)

        self.portale_item = ClickableLabel()
        self.portale_item.setBaseStyle(
            f"color: {self.TEXT_COLOR}; font-size: 13px; background: transparent;"
        )
        self.portale_item.mousePressEvent = lambda e: self.portale_clicked.emit()
        col3_layout.addWidget(self.portale_item)

        self.safe_item = ClickableLabel()
        self.safe_item.setBaseStyle(
            f"color: {self.TEXT_COLOR}; font-size: 13px; background: transparent;"
        )
        self.safe_item.mousePressEvent = lambda e: self.safework_clicked.emit()
        col3_layout.addWidget(self.safe_item)
        layout.addWidget(col3)

        layout.addStretch()
        self.refresh_accounts()

    def _add_separator(self, layout):
        """Separatore elegante con gradiente verticale."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFixedHeight(32)
        line.setFixedWidth(2)
        line.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 transparent,
                    stop:0.3 #BDBDBD,
                    stop:0.7 #BDBDBD,
                    stop:1 transparent
                );
                border: none;
            }
        """
        )
        layout.addWidget(line)

    def fade_in(self, duration: int = 400):
        """Animazione fade-in per transizione FASE 1 → FASE 2."""
        # Stop existing animation if any
        if hasattr(self, "_fade_anim") and self._fade_anim is not None:
            self._fade_anim.stop()
            self._fade_anim.deleteLater()

        self._opacity_effect.setOpacity(0.0)
        self.setVisible(True)
        self._fade_anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_anim.setDuration(duration)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade_anim.start()

    def update_info(
        self, client: str, expiry: str, last_login: str = "", hw_id: str = ""
    ):
        """Aggiorna le info di business (FASE 2)."""
        self.client_item.setText(f"<b>Cliente:</b> {client}")
        self.expiry_item.setText(f"<b>Scadenza:</b> {expiry}")
        if hw_id:
            self.hw_id_item.setText(f"<b>HW ID:</b> {hw_id}")
        if last_login:
            self.last_login_item.setText(f"<b>Ultimo Accesso:</b> {last_login}")

    def refresh_accounts(self):
        """Aggiorna lo stato dei bot account."""
        config = config_manager.load_config()
        accounts = config.get("accounts", [])
        safework = config.get("safework_accounts", [])

        portale_user = self._get_default_account(accounts)
        safe_user = self._get_default_account(safework)

        self.portale_item.setText(
            f"<b>🌐 Portale Fornitori:</b> {portale_user or 'N.C.'}"
        )
        self.safe_item.setText(f"<b>🛡️ SafeWork:</b> {safe_user or 'N.C.'}")

    @staticmethod
    def _get_default_account(accounts: list) -> Optional[str]:
        """Estrae l'account predefinito dalla lista."""
        if not accounts:
            return None
        # Cerca l'account marcato come default
        for account in accounts:
            if account.get("default"):
                return account.get("username")
        # Fallback: primo account
        return accounts[0].get("username") if accounts else None

    def _get_def(self, accounts: list) -> Optional[str]:
        """Compatibilità con codice legacy."""
        return self._get_default_account(accounts)


class BootTelemetryWidget(QWidget):
    """
    Telemetria avanzata real-time (FASE 1: Boot).
    Layout verticale con dati di sistema professionali.
    """

    # Colore unificato nero
    TEXT_COLOR = "#000000"

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 2, 10, 2)
        layout.setSpacing(20)

        self.process = psutil.Process(os.getpid())
        self.last_net = psutil.net_io_counters()
        self.last_ctx = psutil.cpu_stats().ctx_switches
        self.last_time = time.time()
        self.session_id = hex(int(time.time()))[2:].upper()

        self.font_style = f"font-family: 'Consolas', monospace; font-size: 13px; color: {self.TEXT_COLOR}; background: transparent;"

        # Colonna 1: OS / ARCH (Sistema)
        col1 = QWidget()
        col1_layout = QVBoxLayout(col1)
        col1_layout.setContentsMargins(0, 0, 0, 0)
        col1_layout.setSpacing(2)

        self.lbl_os = QLabel()
        self.lbl_os.setStyleSheet(self.font_style)
        col1_layout.addWidget(self.lbl_os)

        self.lbl_arch = QLabel()
        self.lbl_arch.setStyleSheet(self.font_style)
        col1_layout.addWidget(self.lbl_arch)
        layout.addWidget(col1)

        self._add_separator(layout)

        # Colonna 2: HOST / IP (Rete)
        col2 = QWidget()
        col2_layout = QVBoxLayout(col2)
        col2_layout.setContentsMargins(0, 0, 0, 0)
        col2_layout.setSpacing(2)

        self.lbl_host = QLabel()
        self.lbl_host.setStyleSheet(self.font_style)
        col2_layout.addWidget(self.lbl_host)

        self.lbl_ip = QLabel()
        self.lbl_ip.setStyleSheet(self.font_style)
        col2_layout.addWidget(self.lbl_ip)
        layout.addWidget(col2)

        self._add_separator(layout)

        # Colonna 3: CORE / FREQ (CPU Info)
        col3 = QWidget()
        col3_layout = QVBoxLayout(col3)
        col3_layout.setContentsMargins(0, 0, 0, 0)
        col3_layout.setSpacing(2)

        self.lbl_core = QLabel()
        self.lbl_core.setStyleSheet(self.font_style)
        col3_layout.addWidget(self.lbl_core)

        self.lbl_freq = QLabel()
        self.lbl_freq.setStyleSheet(self.font_style)
        col3_layout.addWidget(self.lbl_freq)
        layout.addWidget(col3)

        self._add_separator(layout)

        # Colonna 4: CPU / UPTIME (Performance)
        col4 = QWidget()
        col4_layout = QVBoxLayout(col4)
        col4_layout.setContentsMargins(0, 0, 0, 0)
        col4_layout.setSpacing(2)

        self.lbl_cpu = QLabel()
        self.lbl_cpu.setStyleSheet(self.font_style)
        col4_layout.addWidget(self.lbl_cpu)

        self.lbl_uptime = QLabel()
        self.lbl_uptime.setStyleSheet(self.font_style)
        col4_layout.addWidget(self.lbl_uptime)
        layout.addWidget(col4)

        self._add_separator(layout)

        # Colonna 5: RAM / NET (Risorse)
        col5 = QWidget()
        col5_layout = QVBoxLayout(col5)
        col5_layout.setContentsMargins(0, 0, 0, 0)
        col5_layout.setSpacing(2)

        self.lbl_ram = QLabel()
        self.lbl_ram.setStyleSheet(self.font_style)
        col5_layout.addWidget(self.lbl_ram)

        self.lbl_net = QLabel()
        self.lbl_net.setStyleSheet(self.font_style)
        col5_layout.addWidget(self.lbl_net)
        layout.addWidget(col5)

        self._add_separator(layout)

        # Colonna 6: THR / PID (Processo)
        col6 = QWidget()
        col6_layout = QVBoxLayout(col6)
        col6_layout.setContentsMargins(0, 0, 0, 0)
        col6_layout.setSpacing(2)

        self.lbl_threads = QLabel()
        self.lbl_threads.setStyleSheet(self.font_style)
        col6_layout.addWidget(self.lbl_threads)

        self.lbl_pid = QLabel()
        self.lbl_pid.setStyleSheet(self.font_style)
        col6_layout.addWidget(self.lbl_pid)
        layout.addWidget(col6)

        self._add_separator(layout)

        # Colonna 7: SID / I/O (Sessione)
        col7 = QWidget()
        col7_layout = QVBoxLayout(col7)
        col7_layout.setContentsMargins(0, 0, 0, 0)
        col7_layout.setSpacing(2)

        self.lbl_session = QLabel()
        self.lbl_session.setStyleSheet(self.font_style)
        col7_layout.addWidget(self.lbl_session)

        self.lbl_io = QLabel()
        self.lbl_io.setStyleSheet(self.font_style)
        col7_layout.addWidget(self.lbl_io)
        layout.addWidget(col7)

        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)

    def _add_separator(self, layout):
        """Separatore elegante con gradiente verticale."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFixedHeight(32)
        line.setFixedWidth(2)
        line.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 transparent,
                    stop:0.3 #9E9E9E,
                    stop:0.7 #9E9E9E,
                    stop:1 transparent
                );
                border: none;
            }
        """
        )
        layout.addWidget(line)

    def showEvent(self, event):
        super().showEvent(event)
        self.timer.start(1000)
        self._update_stats()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.timer.stop()

    def _update_stats(self):
        """Aggiorna le statistiche di sistema in real-time."""
        try:
            import platform
            import socket

            now = time.time()
            dt = now - self.last_time
            if dt <= 0:
                return

            # Col 1: OS / ARCH
            os_info = platform.system()
            os_release = platform.release()
            self.lbl_os.setText(f"OS: {os_info} {os_release}")
            self.lbl_arch.setText(f"ARCH: {platform.machine()}")

            # Col 2: HOST / IP
            hostname = socket.gethostname()
            self.lbl_host.setText(f"HOST: {hostname}")
            try:
                ip_addr = socket.gethostbyname(hostname)
            except Exception:
                ip_addr = "127.0.0.1"
            self.lbl_ip.setText(f"IP: {ip_addr}")

            # Col 3: CORE / FREQ
            cpu_count = psutil.cpu_count(logical=True)
            self.lbl_core.setText(f"CORE: {cpu_count}")
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                freq_ghz = cpu_freq.current / 1000
                self.lbl_freq.setText(f"FREQ: {freq_ghz:.2f} GHz")
            else:
                self.lbl_freq.setText("FREQ: N/A")

            # Col 4: CPU / UPTIME
            cpu_pct = psutil.cpu_percent(interval=0.1)
            self.lbl_cpu.setText(f"CPU: {cpu_pct:.1f}%")
            # Uptime del sistema
            try:
                boot_time = psutil.boot_time()
                uptime_seconds = now - boot_time
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                if hours >= 24:
                    days = hours // 24
                    hours = hours % 24
                    self.lbl_uptime.setText(f"UPTIME: {days}d {hours}h")
                else:
                    self.lbl_uptime.setText(f"UPTIME: {hours}h {minutes}m")
            except Exception:
                self.lbl_uptime.setText("UPTIME: N/A")

            # Col 5: RAM / NET
            ram = psutil.virtual_memory()
            ram_used = ram.used / (1024**3)
            self.lbl_ram.setText(f"RAM: {ram.percent:.1f}% ({ram_used:.1f}GB)")
            net_stats = psutil.net_if_stats()
            net_connected = any(stats.isup for stats in net_stats.values())
            # Badge colorato: verde = Online, rosso = Offline
            if net_connected:
                self.lbl_net.setText("NET: <span style='color:#4CAF50'>●</span> Online")
            else:
                self.lbl_net.setText(
                    "NET: <span style='color:#F44336'>●</span> Offline"
                )

            # Col 6: THR / PID
            self.lbl_threads.setText(f"THR: {self.process.num_threads()}")
            self.lbl_pid.setText(f"PID: {os.getpid()}")

            # Col 7: SID / I/O
            self.lbl_session.setText(f"SID: {self.session_id}")
            net = psutil.net_io_counters()
            io_rate = (
                (
                    net.bytes_recv
                    - self.last_net.bytes_recv
                    + net.bytes_sent
                    - self.last_net.bytes_sent
                )
                / dt
                / 1024
            )
            self.last_net = net
            self.lbl_io.setText(f"I/O: {io_rate:.1f} KB/s")

            self.last_time = now
        except Exception:
            pass


class AnimatedProgressBar(QWidget):
    """
    Progress bar animata con striature, shimmer e bordo pulsante.
    Effetto hacker-style professionale.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 18)

        self._value = 0
        self._stripe_offset = 0
        self._shimmer_pos = -50
        self._border_alpha = 255
        self._border_direction = -5  # Direzione pulsazione

        # Timer per animazioni (leggero, 30 FPS)
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._animate)
        self._anim_timer.setInterval(33)  # ~30 FPS

    def setValue(self, value: int):
        self._value = max(0, min(value, 100))
        self.update()

    def value(self) -> int:
        return self._value

    def showEvent(self, event):
        super().showEvent(event)
        self._anim_timer.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._anim_timer.stop()

    def _animate(self):
        """Aggiorna le animazioni."""
        # Striature che scorrono
        self._stripe_offset = (self._stripe_offset + 2) % 20

        # Shimmer che attraversa
        self._shimmer_pos += 4
        if self._shimmer_pos > self.width() + 50:
            self._shimmer_pos = -50

        # Bordo pulsante
        self._border_alpha += self._border_direction
        if self._border_alpha <= 100:
            self._border_direction = 5
        elif self._border_alpha >= 255:
            self._border_direction = -5

        self.update()

    def paintEvent(self, event):
        from PyQt6.QtCore import QRectF
        from PyQt6.QtGui import QColor, QLinearGradient, QPainter, QPen

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        radius = 4

        # 1. Sfondo
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(224, 224, 224))  # #E0E0E0
        painter.drawRoundedRect(QRectF(0, 0, w, h), radius, radius)

        # 2. Chunk (parte riempita)
        chunk_width = int((self._value / 100) * (w - 4))
        if chunk_width > 0:
            chunk_rect = QRectF(2, 2, chunk_width, h - 4)

            # Gradiente base nero
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRoundedRect(chunk_rect, radius - 1, radius - 1)

            # 3. Striature diagonali animate
            painter.setClipRect(chunk_rect)
            stripe_color = QColor(60, 60, 60)  # Grigio scuro per contrasto
            painter.setBrush(stripe_color)
            painter.setPen(Qt.PenStyle.NoPen)

            stripe_width = 10
            for x in range(-20 + self._stripe_offset, int(chunk_width) + 20, 20):
                points = [
                    (x, h),
                    (x + stripe_width, h),
                    (x + stripe_width + 15, 0),
                    (x + 15, 0),
                ]
                from PyQt6.QtCore import QPointF
                from PyQt6.QtGui import QPolygonF

                polygon = QPolygonF([QPointF(p[0] + 2, p[1]) for p in points])
                painter.drawPolygon(polygon)

            # 4. Shimmer (riflesso luminoso)
            painter.setClipRect(chunk_rect)
            shimmer_gradient = QLinearGradient(
                self._shimmer_pos, 0, self._shimmer_pos + 50, 0
            )
            shimmer_gradient.setColorAt(0.0, QColor(255, 255, 255, 0))
            shimmer_gradient.setColorAt(0.5, QColor(255, 255, 255, 80))
            shimmer_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
            painter.setBrush(shimmer_gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(chunk_rect, radius - 1, radius - 1)

            painter.setClipping(False)

        # 5. Bordo pulsante
        border_color = QColor(0, 0, 0, self._border_alpha)
        pen = QPen(border_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), radius, radius)

        painter.end()


class FooterRightWidget(QWidget):
    """
    Parte destra del footer: contiene Progress Bar (FASE 1) e Status Cards Bot (FASE 2).
    """

    def __init__(self, status_portale, status_safework, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 15, 0)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Progress Bar Animata (FASE 1: Loading)
        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Progress Label
        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet(
            "color: #000000; font-family: 'Consolas', monospace; font-weight: bold; font-size: 13px; background: transparent; min-width: 45px;"
        )
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        # Status Cards (FASE 2: Operational)
        self.status_portale = status_portale
        self.status_safework = status_safework
        layout.addWidget(status_portale)
        layout.addWidget(status_safework)

    def set_global_progress(self, value: int):
        """Aggiorna la progress bar (FASE 1) con percentuale."""
        value = max(0, min(value, 100))
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")

    def show_loading(self):
        """Mostra la progress bar (FASE 1: Boot)."""
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.status_portale.setVisible(False)
        self.status_safework.setVisible(False)
        # Ensure progress bar is properly displayed
        self.progress_bar.raise_()
        self.progress_label.raise_()

    def show_operational(self):
        """Mostra i status cards (FASE 2: Operativo) e nasconde la progress bar."""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.status_portale.setVisible(True)
        self.status_safework.setVisible(True)


class FooterStatsManager(QWidget):
    """
    Manager centrale per il footer: gestisce la transizione tra FASE 1 e FASE 2.
    Coordina la visibilità dei widget e il cambio di stato.
    """

    def __init__(
        self,
        left_widget: FooterLeftWidget,
        center_console: StartupConsole,
        right_widget: FooterRightWidget,
        parent=None,
    ):
        super().__init__(parent)
        self.left_widget = left_widget
        self.center_console = center_console
        self.right_widget = right_widget
        self.phase = "boot"  # 'boot' o 'operational'

    def transition_to_operational(
        self, client_name: str = "", expiry: str = "", last_login: str = ""
    ):
        """
        Transizione da FASE 1 (Boot) a FASE 2 (Operativo).
        Nasconde telemetria e progress, mostra business info e status cards.
        """
        self.phase = "operational"
        self.center_console.setText(
            "✓ Sistema SyncroJob pronto. Infrastruttura operativa completamente caricata e sincronizzata."
        )
        self.center_console.setStyleSheet(
            """color: #000000; font-family: 'Segoe UI Semibold'; font-size: 13px; padding: 0 10px; font-weight: 600;"""
        )
        self.right_widget.show_operational()
        if client_name or expiry or last_login:
            self.left_widget.update_info(client_name, expiry, last_login)

    def get_phase(self) -> str:
        """Ritorna la fase attuale ('boot' o 'operational')."""
        return self.phase

    def log_boot_message(self, message: str, is_error: bool = False):
        """Registra un messaggio durante la FASE 1 (Boot)."""
        if self.phase == "boot":
            self.center_console.log(message, is_error)
