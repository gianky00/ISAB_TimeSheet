from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon


class SecurityDashboard(QWidget):
    """
    Dashboard di sicurezza e audit log.
    Visualizza statistiche, grafici semplificati e log critici.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.audit_manager = AuditManager.instance()

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
        self.timer.start(60000)

        # Timer single shot per caricamento iniziale
        QTimer.singleShot(100, self.refresh)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # 1. Header & KPI
        header_layout = QHBoxLayout()
        title = QLabel("🛡️ Security Center")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #212529;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        integrity_btn = QPushButton("Verifica Integrità")
        integrity_btn.setIcon(get_colored_icon(get_asset_path(Icons.SHIELD), "white"))
        integrity_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #198754; color: white; border: none;
                padding: 8px 15px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #157347; }
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
        chart_frame.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #dee2e6;")
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
            """
            QScrollArea { border: 1px solid #dee2e6; border-radius: 8px; background: white; }
            QWidget { background: white; }
        """
        )
        layout.addWidget(self.log_area)

    def refresh(self):
        """Aggiorna tutti i componenti della dashboard (KPI, Grafico, Log)."""
        stats = self.audit_manager.get_stats_by_day(days=7)
        self._update_kpi(stats)
        self._update_chart(stats)
        self._update_logs()

    def _update_kpi(self, stats):
        # Calcola totali
        total_err = sum(d.get("error", 0) for d in stats.values())
        total_warn = sum(d.get("warning", 0) for d in stats.values())
        total_ok = sum(d.get("success", 0) for d in stats.values())
        total = total_err + total_warn + total_ok

        rate = (total_ok / total * 100) if total > 0 else 100

        # Clear layout
        while self.kpi_layout.count():
            item = self.kpi_layout.takeAt(0)
            if item:
                w = item.widget()
                if w is not None:
                    w.deleteLater()

        self.kpi_layout.addWidget(self._create_kpi_card("Success Rate", f"{rate:.1f}%", "#198754"))
        self.kpi_layout.addWidget(self._create_kpi_card("Errori (7gg)", str(total_err), "#dc3545"))
        self.kpi_layout.addWidget(self._create_kpi_card("Warning (7gg)", str(total_warn), "#ffc107"))

    def _create_kpi_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(
            f"""
            background: white; border-radius: 8px;
            border: 1px solid #dee2e6; border-left: 5px solid {color};
        """
        )
        layout = QVBoxLayout(card)
        t = QLabel(title)
        t.setStyleSheet("color: #6c757d; font-size: 12px;")
        v = QLabel(value)
        v.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        layout.addWidget(t)
        layout.addWidget(v)
        return card

    def _update_chart(self, stats):
        while self.chart_container.count():
            item = self.chart_container.takeAt(0)
            if item:
                w = item.widget()
                if w is not None:
                    w.deleteLater()

        max_val = 0
        for d in stats.values():
            tot = d.get("error", 0) + d.get("success", 0) + d.get("warning", 0)
            if tot > max_val:
                max_val = tot

        if max_val == 0:
            max_val = 1

        for date_str, data in stats.items():
            err = data.get("error", 0)
            ok = data.get("success", 0)
            warn = data.get("warning", 0)
            total = err + ok + warn

            # Bar Container
            bar_cont = QVBoxLayout()
            bar_cont.setSpacing(2)

            # Simple stack bar logic: we just show total height relative to max
            height = int((total / max_val) * 100)  # px relative
            if height < 5:
                height = 5

            bar = QFrame()
            bar.setFixedWidth(30)
            bar.setFixedHeight(height * 2)  # Scale factor

            # Color based on dominant status
            color = "#198754"  # green
            if err > 0:
                color = "#dc3545"  # red if any error
            elif warn > 0:
                color = "#ffc107"  # yellow

            bar.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
            bar.setToolTip(f"{date_str}\nOK: {ok}\nERR: {err}\nWARN: {warn}")

            lbl = QLabel(date_str[5:])  # MM-DD
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 10px; color: #6c757d;")

            bar_cont.addWidget(bar, alignment=Qt.AlignmentFlag.AlignBottom)
            bar_cont.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignHCenter)

            self.chart_container.addLayout(bar_cont)

    def _update_logs(self):
        logs, _ = self.audit_manager.get_filtered_logs(
            limit=10,
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
            row.setStyleSheet("background: #fff0f0; border-radius: 5px; padding: 5px;")
            layout = QHBoxLayout(row)

            ts = log["timestamp"][11:19]
            act = log["action"]

            txt = QLabel(f"<b>{ts}</b> - {act}")
            layout.addWidget(txt)
            layout.addStretch()

            self.log_layout.addWidget(row)

    def _run_integrity_check(self):
        valid = self.audit_manager.verify_integrity()
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
