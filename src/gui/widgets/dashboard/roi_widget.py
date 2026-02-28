"""
SyncroJob - Bot Savings Widget (ROI)
Visualizza il tempo e le risorse risparmiate grazie alle automazioni.
V2.0: Design infografico con icone SVG e barra di progresso stress.
"""

import logging
import threading

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.core.stats.roi_engine import ROIEngine, ROIMetrics
from src.gui.styles import COLORS, LABEL_MUTED
from src.gui.widgets.animated_progress_bar import AnimatedProgressBar
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class BotSavingsWidget(ModernCard):
    """Widget che mostra le metriche di risparmio dei bot (ROI) con feedback visivo."""

    stats_updated = pyqtSignal(object)  # ROIMetrics

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(elevation=5, parent=parent)
        self.setMinimumWidth(320)
        self._setup_ui()

        self.stats_updated.connect(self._update_ui)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(300000)

        QTimer.singleShot(1500, self.refresh_stats)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(12)

        # Header
        lbl_title = QLabel("EFFICIENZA AUTOMAZIONI (30gg)")
        lbl_title.setStyleSheet(LABEL_MUTED)
        layout.addWidget(lbl_title)

        # Main Stats Row
        stats_h = QHBoxLayout()
        stats_h.setSpacing(20)

        # 1. Time Saved Block
        time_v = QVBoxLayout()
        time_v.setSpacing(2)

        time_icon_h = QHBoxLayout()
        clock_icon = get_asset_path(Icons.CLOCK)
        self.lbl_time = QLabel("Calcolo...")
        self.lbl_time.setStyleSheet(f"color: {COLORS['success_dark']}; font-size: 24px; font-weight: 900;")
        time_icon_h.addWidget(self.lbl_time)
        time_icon_h.addStretch()
        time_v.addLayout(time_icon_h)

        lbl_time_tag = QLabel(f"<img src='{clock_icon}' width='10' height='10'> TEMPO RISPARMIATO")
        lbl_time_tag.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 9px; font-weight: 700;")
        time_v.addWidget(lbl_time_tag)
        stats_h.addLayout(time_v)

        # 2. Operations Block
        ops_v = QVBoxLayout()
        ops_v.setSpacing(2)
        ops_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lbl_ops = QLabel("-")
        self.lbl_ops.setStyleSheet(f"color: {COLORS['primary_blue']}; font-size: 24px; font-weight: 900;")
        ops_v.addWidget(self.lbl_ops, alignment=Qt.AlignmentFlag.AlignRight)

        cpu_icon = get_asset_path(Icons.CPU)
        lbl_ops_tag = QLabel(f"TASK AUTOMATIZZATI <img src='{cpu_icon}' width='10' height='10'>")
        lbl_ops_tag.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 9px; font-weight: 700;")
        ops_v.addWidget(lbl_ops_tag, alignment=Qt.AlignmentFlag.AlignRight)
        stats_h.addLayout(ops_v)

        layout.addLayout(stats_h)

        # Stress Progress Area
        stress_v = QVBoxLayout()
        stress_v.setSpacing(5)

        stress_h = QHBoxLayout()
        self.lbl_stress = QLabel("Riduzione Stress: 0%")
        self.lbl_stress.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 11px; font-weight: 700;")
        stress_h.addWidget(self.lbl_stress)
        stress_h.addStretch()

        spark_icon = get_asset_path(Icons.SPARKLES)
        self.lbl_money = QLabel(f"<img src='{spark_icon}' width='12' height='12'> € 0.00 generati")
        self.lbl_money.setStyleSheet(f"color: {COLORS['teal_accent']}; font-size: 11px; font-weight: 700;")
        stress_h.addWidget(self.lbl_money)
        stress_v.addLayout(stress_h)

        self.progress_stress = AnimatedProgressBar()
        self.progress_stress.setFixedHeight(6)
        self.progress_stress.set_color(COLORS["teal_accent"])
        stress_v.addWidget(self.progress_stress)

        layout.addLayout(stress_v)

    def refresh_stats(self) -> None:
        def run():
            try:
                metrics = ROIEngine.calculate_savings()
                self.stats_updated.emit(metrics)
            except Exception as e:
                logger.error(f"ROI Update Error: {e}")

        threading.Thread(target=run, daemon=True).start()

    def _update_ui(self, metrics: ROIMetrics) -> None:
        self.lbl_time.setText(ROIEngine.format_time_saved(metrics.total_minutes_saved))
        self.lbl_ops.setText(str(metrics.total_operations))
        self.lbl_money.setText(f"€ {metrics.estimated_cost_saved:.2f} generati")
        self.lbl_stress.setText(f"Riduzione Stress: {metrics.stress_reduction_score}%")
        self.progress_stress.set_value(metrics.stress_reduction_score)
