"""
SyncroJob - Bot Savings Widget (ROI)
Visualizza il tempo e le risorse risparmiate grazie alle automazioni.
V3.0: Design premium con badge circolari, separatore gradient, dettagli espansi.
"""

import logging
import threading

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.core.stats.roi_engine import ROIEngine, ROIMetrics
from src.gui.styles import COLORS
from src.gui.widgets.animated_progress_bar import AnimatedProgressBar
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class BotSavingsWidget(ModernCard):
    """
    Widget che mostra le metriche di risparmio dei bot (ROI) con design premium.
    Calcola il tempo risparmiato, i task automatizzati e la riduzione dello stress operativo.
    """

    stats_updated = pyqtSignal(object)  # ROIMetrics

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il widget ROI.

        Args:
            parent: Widget genitore opzionale.
        """
        super().__init__(elevation=5, parent=parent)
        self.setMinimumWidth(340)
        self._setup_ui()

        self.stats_updated.connect(self._update_ui)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(300000)

        QTimer.singleShot(1500, self.refresh_stats)

    # ── UI Setup ──────────────────────────────────────────────────────────

    def _setup_ui(self) -> None:
        """Configura l'architettura visiva del widget (Header, KPI, Dettagli, Footer)."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 10)
        layout.setSpacing(8)

        # 1. Header: Badge + Title
        self._build_header(layout)

        # 2. KPI Cards Row (Tempo + Task)
        self._build_kpi_row(layout)

        # 3. Gradient Separator
        self._add_gradient_separator(layout)

        # 4. Detail Section (Stress + Money)
        self._build_detail_section(layout)

        # 5. Footer
        self._build_footer(layout)

    def _build_header(self, layout: QVBoxLayout) -> None:
        """Costruisce l'intestazione con icona badge e titolo."""
        header_h = QHBoxLayout()
        header_h.setSpacing(10)

        badge = self._create_icon_badge(Icons.CPU, COLORS["teal_accent"], "#e0f2f1")
        header_h.addWidget(badge)

        lbl_title = QLabel("EFFICIENZA AUTOMAZIONI (30gg)")
        lbl_title.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: 800;"
            " letter-spacing: 1.2px; background: transparent; border: none;"
        )
        header_h.addWidget(lbl_title)
        header_h.addStretch()
        layout.addLayout(header_h)

    def _build_kpi_row(self, layout: QVBoxLayout) -> None:
        """Costruisce la riga dei Key Performance Indicators principali."""
        kpi_h = QHBoxLayout()
        kpi_h.setSpacing(16)

        # KPI 1: Tempo Risparmiato
        time_card = self._create_kpi_card(
            icon_key=Icons.CLOCK,
            icon_color=COLORS["success_dark"],
            bg_color="#f0fdf4",
            value_text="Calcolo...",
            value_color=COLORS["success_dark"],
            tag_text="TEMPO RISPARMIATO",
        )
        self.lbl_time = time_card.findChild(QLabel, "kpi_value")
        kpi_h.addWidget(time_card)

        # KPI 2: Task Automatizzati
        ops_card = self._create_kpi_card(
            icon_key=Icons.ROCKET,
            icon_color=COLORS["primary_blue"],
            bg_color="#eff6ff",
            value_text="-",
            value_color=COLORS["primary_blue"],
            tag_text="TASK AUTOMATIZZATI",
        )
        self.lbl_ops = ops_card.findChild(QLabel, "kpi_value")
        kpi_h.addWidget(ops_card)

        layout.addLayout(kpi_h)

    def _build_detail_section(self, layout: QVBoxLayout) -> None:
        """Costruisce la sezione di dettaglio con stress bar e risparmio economico."""
        # -- Stress Row --
        stress_h = QHBoxLayout()
        stress_h.setSpacing(10)

        lbl_stress_icon = QLabel()
        lbl_stress_icon.setFixedSize(16, 16)
        lbl_stress_icon.setPixmap(
            get_colored_icon(get_asset_path(Icons.HEART), COLORS["error_red"]).pixmap(14, 14)
        )
        lbl_stress_icon.setStyleSheet("background: transparent; border: none;")
        stress_h.addWidget(lbl_stress_icon)

        self.lbl_stress = QLabel("Riduzione Stress: 0%")
        self.lbl_stress.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: 700;"
            " background: transparent; border: none;"
        )
        stress_h.addWidget(self.lbl_stress)
        stress_h.addStretch()

        self.lbl_stress_pct = QLabel("0%")
        self.lbl_stress_pct.setStyleSheet(
            f"color: {COLORS['teal_accent']}; font-size: 13px; font-weight: 800;"
            " background: transparent; border: none;"
        )
        stress_h.addWidget(self.lbl_stress_pct)
        layout.addLayout(stress_h)

        # Progress Bar
        self.progress_stress = AnimatedProgressBar()
        self.progress_stress.setFixedHeight(10)
        self.progress_stress.set_color(COLORS["teal_accent"])
        layout.addWidget(self.progress_stress)

        # -- Money Row --
        money_h = QHBoxLayout()
        money_h.setSpacing(10)

        lbl_money_icon = QLabel()
        lbl_money_icon.setFixedSize(16, 16)
        lbl_money_icon.setPixmap(
            get_colored_icon(get_asset_path(Icons.SPARKLES), COLORS["teal_accent"]).pixmap(14, 14)
        )
        lbl_money_icon.setStyleSheet("background: transparent; border: none;")
        money_h.addWidget(lbl_money_icon)

        lbl_money_tag = QLabel("Risparmio Economico")
        lbl_money_tag.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 12px; font-weight: 700;"
            " background: transparent; border: none;"
        )
        money_h.addWidget(lbl_money_tag)
        money_h.addStretch()

        self.lbl_money = QLabel("€ 0.00")
        self.lbl_money.setStyleSheet(
            f"color: {COLORS['success_dark']}; font-size: 16px; font-weight: 800;"
            " background: transparent; border: none;"
        )
        money_h.addWidget(self.lbl_money)
        layout.addLayout(money_h)

    def _build_footer(self, layout: QVBoxLayout) -> None:
        """Costruisce il piè di pagina con la media giornaliera dei task."""
        self.lbl_avg = QLabel("Media giornaliera: -- task/giorno")
        self.lbl_avg.setStyleSheet(
            f"color: {COLORS['text_light']}; font-size: 11px; font-style: italic;"
            " background: transparent; border: none;"
        )
        self.lbl_avg.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.lbl_avg)

    # ── Helper Widget Builders ────────────────────────────────────────────

    def _create_icon_badge(self, icon_key: str, icon_color: str, bg_color: str) -> QLabel:
        """Badge circolare con icona SVG colorata."""
        badge = QLabel()
        badge.setFixedSize(28, 28)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"background-color: {bg_color}; border-radius: 14px; border: none;")
        icon_path = get_asset_path(icon_key)
        badge.setPixmap(get_colored_icon(icon_path, icon_color).pixmap(14, 14))
        return badge

    def _create_kpi_card(
        self,
        icon_key: str,
        icon_color: str,
        bg_color: str,
        value_text: str,
        value_color: str,
        tag_text: str,
    ) -> QFrame:
        """Card KPI con badge icona, valore grande e sottotitolo."""
        card = QFrame()
        card.setStyleSheet(
            f"QFrame {{ background-color: {bg_color}; border-radius: 10px;"
            f" border: 1px solid {COLORS['border_light']}; }}"
        )

        v = QVBoxLayout(card)
        v.setContentsMargins(10, 8, 10, 8)
        v.setSpacing(4)

        # Badge row
        badge_h = QHBoxLayout()
        badge = self._create_icon_badge(icon_key, icon_color, COLORS["bg_white"])
        badge_h.addWidget(badge)
        badge_h.addStretch()
        v.addLayout(badge_h)

        # Value
        lbl_val = QLabel(value_text)
        lbl_val.setObjectName("kpi_value")
        lbl_val.setStyleSheet(
            f"color: {value_color}; font-size: 26px; font-weight: 900; background: transparent; border: none;"
        )
        v.addWidget(lbl_val)

        # Tag
        lbl_tag = QLabel(tag_text)
        lbl_tag.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 800;"
            " letter-spacing: 0.5px; background: transparent; border: none;"
        )
        v.addWidget(lbl_tag)
        return card

    def _add_gradient_separator(self, layout: QVBoxLayout) -> None:
        """Linea separatrice con gradient orizzontale."""
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
            f" stop:0 transparent, stop:0.2 {COLORS['border_light']},"
            f" stop:0.8 {COLORS['border_light']}, stop:1 transparent);"
            " border: none;"
        )
        layout.addWidget(sep)

    # ── Data ──────────────────────────────────────────────────────────────

    def refresh_stats(self) -> None:
        """Avvia il thread di calcolo delle statistiche ROI in background."""

        def run():
            try:
                metrics = ROIEngine.calculate_savings()
                self.stats_updated.emit(metrics)
            except Exception as e:
                logger.error(f"ROI Update Error: {e}")

        threading.Thread(target=run, daemon=True).start()

    def _update_ui(self, metrics: ROIMetrics) -> None:
        """
        Aggiorna gli elementi grafici con le nuove metriche calcolate.

        Args:
            metrics: Oggetto ROIMetrics contenente i dati elaborati.
        """
        if hasattr(self, "lbl_time") and self.lbl_time:
            self.lbl_time.setText(ROIEngine.format_time_saved(metrics.total_minutes_saved))
        if hasattr(self, "lbl_ops") and self.lbl_ops:
            self.lbl_ops.setText(str(metrics.total_operations))

        self.lbl_money.setText(f"€ {metrics.estimated_cost_saved:.2f}")
        self.lbl_stress.setText(f"Riduzione Stress: {metrics.stress_reduction_score}%")
        self.lbl_stress_pct.setText(f"{metrics.stress_reduction_score}%")
        self.progress_stress.set_value(metrics.stress_reduction_score)

        # Media giornaliera
        avg = round(metrics.total_operations / 30, 1) if metrics.total_operations > 0 else 0
        self.lbl_avg.setText(f"Media giornaliera: ~{avg} task/giorno")
