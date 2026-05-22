from typing import Any

from PySide6.QtCore import Qt, QThreadPool, QTimer, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.core_widgets import PrimaryButton
from src.gui.workers.integrity_worker import IntegrityWorker
from src.utils.helpers import get_asset_path, get_colored_icon

# Stile forzato per i tooltip in Light Mode
TOOLTIP_CSS = """
QToolTip {
    background-color: #FFFFFF;
    color: #212121;
    border: 1px solid #BBBBBB;
    border-radius: 6px;
    padding: 8px 12px;
}
"""


class SecurityDashboard(QWidget):
    """
    Dashboard di sicurezza e audit log.
    Visualizza statistiche, grafici semplificati e log critici.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.audit_manager = AuditManager.instance()
        self.setStyleSheet(TOOLTIP_CSS)
        self._first_refresh_done = False

        # Widget members (Strict Typing - Option D)
        self.kpi_layout: QHBoxLayout
        self.chart_container: QHBoxLayout
        self.log_area: QScrollArea
        self.log_content: QWidget
        self.log_layout: QVBoxLayout

        self._setup_ui()

        # Auto-refresh ogni minuto
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        refresh_interval_ms = 60000
        self.timer.start(refresh_interval_ms)

        # Il refresh iniziale viene differito a showEvent per non bloccare lo startup

    def showEvent(self, event: Any) -> None:
        """Esegue il primo refresh solo quando il widget diventa visibile."""
        super().showEvent(event)
        if not self._first_refresh_done:
            self._first_refresh_done = True
            delay_ms = 100
            QTimer.singleShot(delay_ms, self.refresh)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        main_spacing = 20
        layout.setSpacing(main_spacing)
        main_margin = 20
        layout.setContentsMargins(main_margin, main_margin, main_margin, main_margin)

        # 1. Header & KPI
        header_layout = QHBoxLayout()
        title = QLabel("🛡️ Security Center")
        title_font_size = 24
        title.setStyleSheet(
            f"font-size: {title_font_size}px; font-weight: bold; color: {COLORS['text_dark']};"
        )
        header_layout.addWidget(title)
        header_layout.addStretch()

        integrity_btn = PrimaryButton("Verifica Integrità")
        integrity_btn.setIcon(get_colored_icon(get_asset_path(Icons.SHIELD), "white"))
        integrity_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS["success_dark"]}; color: white; border: none;
                padding: 8px 15px; border-radius: 5px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {COLORS["success_green"]}; }}
        """
        )
        integrity_btn.clicked.connect(self._run_integrity_check)
        header_layout.addWidget(integrity_btn)

        layout.addLayout(header_layout)

        # KPI Cards
        self.kpi_layout = QHBoxLayout()
        layout.addLayout(self.kpi_layout)

        # 2. Daily Stats Chart (Simplified CSS Bars)
        chart_frame = QFrame()
        chart_frame.setStyleSheet(
            f"background: {COLORS['bg_white']}; border-radius: 10px; border: 1px solid {COLORS['border_light']};"
        )
        chart_layout = QVBoxLayout(chart_frame)

        chart_title = QLabel("Ultimi 7 Giorni")
        chart_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        chart_layout.addWidget(chart_title)

        self.chart_container = QHBoxLayout()
        self.chart_container.setAlignment(Qt.AlignmentFlag.AlignBottom)
        chart_layout.addLayout(self.chart_container)

        layout.addWidget(chart_frame)

        # 3. Recent Critical Logs
        log_label = QLabel("Eventi Critici Recenti")
        log_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        layout.addWidget(log_label)

        self.log_area = QScrollArea()
        self.log_area.setWidgetResizable(True)
        self.log_content = QWidget()
        self.log_layout = QVBoxLayout(self.log_content)
        self.log_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.log_area.setWidget(self.log_content)

        self.log_area.setStyleSheet(
            f"""
            QScrollArea {{ border: 1px solid {COLORS["border_light"]}; border-radius: 8px; background: {COLORS["bg_white"]}; }}
            QWidget {{ background: {COLORS["bg_white"]}; }}
        """
        )
        layout.addWidget(self.log_area)

    def refresh(self) -> None:
        """Aggiorna tutti i componenti della dashboard (KPI, Grafico, Log)."""
        days_stats = 7
        stats = self.audit_manager.get_stats_by_day(days=days_stats)
        self._update_kpi(stats)
        self._update_chart(stats)
        self._update_logs()

    def _update_kpi(self, stats: dict[str, dict[str, int]]) -> None:
        # Calcola totali
        total_err = sum(d.get("error", 0) for d in stats.values())
        total_warn = sum(d.get("warning", 0) for d in stats.values())
        total_ok = sum(d.get("success", 0) for d in stats.values())
        total = total_err + total_warn + total_ok

        percent_100 = 100
        rate = (total_ok / total * percent_100) if total > 0 else percent_100

        # Clear layout
        while self.kpi_layout.count():
            item = self.kpi_layout.takeAt(0)
            if item:
                w = item.widget()
                if w is not None:
                    w.deleteLater()

        self.kpi_layout.addWidget(
            self._create_kpi_card("Success Rate", f"{rate:.1f}%", COLORS["success_dark"])
        )
        self.kpi_layout.addWidget(self._create_kpi_card("Errori (7gg)", str(total_err), COLORS["error_red"]))
        self.kpi_layout.addWidget(
            self._create_kpi_card("Warning (7gg)", str(total_warn), COLORS["warning_yellow"])
        )

    def _create_kpi_card(self, title: str, value: str, color: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            f"""
            background: {COLORS["bg_white"]}; border-radius: 8px;
            border: 1px solid {COLORS["border_light"]}; border-left: 5px solid {color};
        """
        )
        layout = QVBoxLayout(card)
        t = QLabel(title)
        t.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        v = QLabel(value)
        v.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        layout.addWidget(t)
        layout.addWidget(v)
        return card

    def _update_chart(self, stats: dict[str, dict[str, int]]) -> None:
        while self.chart_container.count():
            item = self.chart_container.takeAt(0)
            if item:
                w = item.widget()
                if w is not None:
                    w.deleteLater()

        max_val = 0
        for d in stats.values():
            tot = d.get("error", 0) + d.get("success", 0) + d.get("warning", 0)
            max_val = max(max_val, tot)

        if max_val == 0:
            max_val = 1

        for date_str, data in stats.items():
            err = data.get("error", 0)
            ok = data.get("success", 0)
            warn = data.get("warning", 0)
            total = err + ok + warn

            # Bar Container
            bar_cont = QVBoxLayout()
            bar_spacing = 2
            bar_cont.setSpacing(bar_spacing)

            # Simple stack bar logic: we just show total height relative to max
            relative_height = 100
            height = int((total / max_val) * relative_height)  # px relative
            min_height = 5
            height = max(height, min_height)

            bar = QFrame()
            bar_width = 30
            bar.setFixedWidth(bar_width)
            scale_factor = 2
            bar.setFixedHeight(height * scale_factor)  # Scale factor

            # Color based on dominant status
            bar_color = COLORS["success_dark"]  # green
            if err > 0:
                bar_color = COLORS["error_red"]  # red if any error
            elif warn > 0:
                bar_color = COLORS["warning_yellow"]  # yellow

            bar.setStyleSheet(f"background-color: {bar_color}; border-radius: 4px;")
            bar.setToolTip(f"{date_str}\nOK: {ok}\nERR: {err}\nWARN: {warn}")

            lbl = QLabel(date_str[5:])  # MM-DD
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"font-size: 10px; color: {COLORS['text_muted']};")

            bar_cont.addWidget(bar, alignment=Qt.AlignmentFlag.AlignBottom)
            bar_cont.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignHCenter)

            self.chart_container.addLayout(bar_cont)

    def _update_logs(self) -> None:
        log_limit = 10
        logs, _ = self.audit_manager.get_filtered_logs(
            limit=log_limit,
            levels=["error", "high", "warning"],  # Show only bad stuff
        )

        while self.log_layout.count():
            item = self.log_layout.takeAt(0)
            if item:
                w = item.widget()
                if w is not None:
                    w.deleteLater()

        if not logs:
            self.log_layout.addWidget(QLabel("Nessun evento critico recente."))
            return

        for log in logs:
            row = QFrame()
            # Use a light red background for critical logs
            bg_opacity = 0.08
            row.setStyleSheet(
                f"background: {hex_to_rgba(COLORS['error_red'], bg_opacity)}; border-radius: 5px; padding: 5px;"
            )
            layout = QHBoxLayout(row)

            # Estrae orario HH:MM:SS da ISO timestamp
            ts = log["timestamp"][11:19]
            act = log["action"]

            txt = QLabel(f"<b>{ts}</b> - {act}")
            layout.addWidget(txt)
            layout.addStretch()

            self.log_layout.addWidget(row)

    def _run_integrity_check(self) -> None:
        """Avvia il controllo di integrità in background."""
        worker = IntegrityWorker(self.audit_manager)
        worker.signals.finished.connect(self._on_integrity_checked)
        QThreadPool.globalInstance().start(worker)

    @Slot(bool)
    def _on_integrity_checked(self, valid: bool) -> None:
        """Callback al termine della verifica asincrona."""
        if valid:
            QMessageBox.information(
                self,
                "Integrità",
                "✅ Il registro di Audit è integro e non compromesso.",
            )
        else:
            QMessageBox.warning(
                self,
                "Integrità",
                "⚠️ Rilevata possibile manomissione nel registro di Audit!",
            )
