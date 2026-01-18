"""
SyncroJob - Footer Stats & Telemetry PRO
Widget avanzati per il monitoraggio risorse, stato bot e identità sessione.
Implementa logica a due fasi: FASE 1 (Boot) e FASE 2 (Operativo).
"""

import os
import time
from typing import Optional

import psutil
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
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
                font-size: 11px;
                padding: 0 20px;
                background: transparent;
            }
        """
        )
        self._log_queue = []

    def log(self, message: str, is_error: bool = False):
        """Registra un messaggio nel log della console."""
        color = "#dc3545" if is_error else "#546E7A"
        self.setText(message)
        self.setStyleSheet(
            f"color: {color}; font-family: 'Segoe UI Semibold'; font-size: 11px; padding: 0 20px;"
        )
        self._log_queue.append((message, is_error))
        # Mantieni solo gli ultimi 100 messaggi
        if len(self._log_queue) > 100:
            self._log_queue.pop(0)

    def get_history(self):
        """Ritorna la storia dei log."""
        return self._log_queue

    def set_log(self, message: str, current: int = 0, total: int = 0):
        """Compatibilità con main_window.py - mostra il messaggio con barra di progresso."""
        self.log(message)
        if total > 0:
            # Potrebbe essere esteso per mostrare la barra di progresso nel testo
            pct = (current / total * 100) if total > 0 else 0
            self.setText(f"{message} ({pct:.0f}%)")


class FooterLeftWidget(QWidget):
    """
    Parte sinistra del footer: alterna tra FASE 1 (Telemetria) e FASE 2 (Business Info).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 0, 5)
        layout.setSpacing(15)

        # FASE 2: Business Info Items
        self.client_item = FooterItemWidget("CLIENTE:")
        layout.addWidget(self.client_item)

        self.expiry_item = FooterItemWidget("SCADENZA:")
        layout.addWidget(self.expiry_item)

        self._add_separator(layout)

        self.last_login_item = FooterItemWidget("ULTIMO ACCESSO:")
        layout.addWidget(self.last_login_item)

        self._add_separator(layout)

        # OS Info cluster (sempre visibile)
        import platform

        os_name = "Windows" if os.name == "nt" else platform.system()
        self.os_item = FooterItemWidget("OS:", value=os_name, color="#455A64")
        layout.addWidget(self.os_item)

        self._add_separator(layout)

        # Account Info (FASE 2)
        self.isab_item = FooterItemWidget("ISAB:", color="#1565C0")
        layout.addWidget(self.isab_item)

        self.safe_item = FooterItemWidget("SafeWork:", color="#D81B60")
        layout.addWidget(self.safe_item)

        layout.addStretch()

        self.refresh_accounts()

    def _add_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFixedHeight(18)
        line.setStyleSheet("color: #CFD8DC; border-left: 1px solid #CFD8DC;")
        layout.addWidget(line)

    def update_info(self, client: str, expiry: str, last_login: str = ""):
        """Aggiorna le info di business (FASE 2)."""
        self.client_item.set_text(client)
        self.expiry_item.set_text(expiry)
        if last_login:
            self.last_login_item.set_text(last_login)

    def refresh_accounts(self):
        """Aggiorna lo stato dei bot account."""
        config = config_manager.load_config()
        accounts = config.get("accounts", [])
        safework = config.get("safework_accounts", [])

        isab_user = self._get_default_account(accounts)
        safe_user = self._get_default_account(safework)

        self.isab_item.set_text(isab_user or "N.C.")
        self.safe_item.set_text(safe_user or "N.C.")

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
    Mostra: Host, IP, CPU, RAM, Lag.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(15)

        self.process = psutil.Process(os.getpid())
        self.last_net = psutil.net_io_counters()
        self.last_ctx = psutil.cpu_stats().ctx_switches
        self.last_time = time.time()
        self.session_id = hex(int(time.time()))[2:].upper()

        self.font_style = "font-family: 'Consolas', 'Monospace'; font-size: 10px; background: transparent;"

        # Host
        self.lbl_host = QLabel()
        layout.addWidget(self.lbl_host)

        # IP (simulato con localhost)
        self.lbl_ip = QLabel()
        layout.addWidget(self.lbl_ip)

        # CPU
        self.lbl_cpu = QLabel()
        layout.addWidget(self.lbl_cpu)

        # RAM
        self.lbl_ram = QLabel()
        layout.addWidget(self.lbl_ram)

        # Lag (Context Switches)
        self.lbl_lag = QLabel()
        layout.addWidget(self.lbl_lag)

        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)

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
            now = time.time()
            dt = now - self.last_time
            if dt <= 0:
                return

            # Host
            import socket

            hostname = socket.gethostname()
            self.lbl_host.setText(
                f"<span style='color:#607D8B'>HOST:</span> <span style='color:#1565C0'>{hostname}</span>"
            )
            self.lbl_host.setStyleSheet(self.font_style)

            # IP (Localhost)
            try:
                ip_addr = socket.gethostbyname(hostname)
            except Exception:
                ip_addr = "127.0.0.1"
            self.lbl_ip.setText(
                f"<span style='color:#607D8B'>IP:</span> <span style='color:#1565C0'>{ip_addr}</span>"
            )
            self.lbl_ip.setStyleSheet(self.font_style)

            # CPU %
            cpu_pct = psutil.cpu_percent(interval=0.1)
            cpu_color = (
                "#2E7D32" if cpu_pct < 50 else "#E65100" if cpu_pct < 80 else "#dc3545"
            )
            self.lbl_cpu.setText(
                f"<span style='color:#607D8B'>CPU:</span> <span style='color:{cpu_color}'>{cpu_pct:.1f}%</span>"
            )
            self.lbl_cpu.setStyleSheet(self.font_style)

            # RAM
            ram = psutil.virtual_memory()
            ram_pct = ram.percent
            ram_color = (
                "#2E7D32" if ram_pct < 50 else "#E65100" if ram_pct < 80 else "#dc3545"
            )
            self.lbl_ram.setText(
                f"<span style='color:#607D8B'>RAM:</span> <span style='color:{ram_color}'>{ram_pct:.1f}%</span>"
            )
            self.lbl_ram.setStyleSheet(self.font_style)

            # Lag (Context Switches per secondo)
            ctx = psutil.cpu_stats().ctx_switches
            ctx_s = int((ctx - self.last_ctx) / dt)
            self.last_ctx = ctx
            self.lbl_lag.setText(
                f"<span style='color:#607D8B'>LAG:</span> <span style='color:#E65100'>{ctx_s}/s</span>"
            )
            self.lbl_lag.setStyleSheet(self.font_style)

            self.last_time = now
        except Exception:
            pass


class FooterRightWidget(QWidget):
    """
    Parte destra del footer: contiene Progress Bar (FASE 1) e Status Cards Bot (FASE 2).
    """

    def __init__(self, status_portale, status_safework, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 10, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Progress Bar (FASE 1: Loading)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(True)  # Visibile in FASE 1
        self.progress_bar.setMaximumHeight(8)
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar { border: 1px solid #E0E0E0; border-radius: 4px; background: #F5F5F5; }
            QProgressBar::chunk { background-color: #0d6efd; border-radius: 3px; }
        """
        )
        layout.addWidget(self.progress_bar)

        # Status Cards (FASE 2: Operational)
        self.status_portale = status_portale
        self.status_safework = status_safework
        layout.addWidget(status_portale)
        layout.addWidget(status_safework)

    def set_global_progress(self, value: int):
        """Aggiorna la progress bar (FASE 1)."""
        if value < 0:
            self.progress_bar.setVisible(False)
        else:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(min(value, 100))

    def show_loading(self):
        """Mostra la progress bar (FASE 1: Boot)."""
        self.progress_bar.setVisible(True)
        self.status_portale.setVisible(False)
        self.status_safework.setVisible(False)

    def show_operational(self):
        """Mostra i status cards (FASE 2: Operativo)."""
        self.progress_bar.setVisible(False)
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
            "SyncroJob operativo. Tutti i moduli caricati correttamente."
        )
        self.center_console.setStyleSheet(
            """color: #2E7D32; font-family: 'Segoe UI Semibold'; font-size: 11px; padding: 0 20px;"""
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
