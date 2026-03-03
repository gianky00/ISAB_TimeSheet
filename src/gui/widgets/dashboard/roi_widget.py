"""
SyncroJob - Bot Efficiency Widget
Visualizza le metriche di efficienza e affidabilità delle automazioni su tutto lo storico.
V4.0: Storico totale, nuove metriche di successo e affidabilità con barre di progresso.
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
    Widget premium per la visualizzazione dell'efficienza delle automazioni.
    Calcola il tempo risparmiato, il tasso di successo e l'affidabilità basandosi sullo storico totale.
    """

    stats_updated = pyqtSignal(object)  # ROIMetrics

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il widget Efficienza.

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

        # 4. Detail Section (Success Rate + Reliability)
        self._build_detail_section(layout)

        # 5. Footer
        self._build_footer(layout)

    def _build_header(self, layout: QVBoxLayout) -> None:
        """Costruisce l'intestazione con icona badge e titolo."""
        header_h = QHBoxLayout()
        header_h.setSpacing(10)

        badge = self._create_icon_badge(Icons.CPU, COLORS["teal_accent"], "#e0f2f1")
        header_h.addWidget(badge)

        self.lbl_title = QLabel("EFFICIENZA AUTOMAZIONI")
        self.lbl_title.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: 800;"
            " letter-spacing: 1.2px; background: transparent; border: none;"
        )
        header_h.addWidget(self.lbl_title)
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
            tag_text="RISPARMIO TOTALE",
        )
        self.lbl_time = time_card.findChild(QLabel, "kpi_value")
        self.lbl_trend = time_card.findChild(QLabel, "kpi_sub")
        kpi_h.addWidget(time_card)

        # KPI 2: Task Automatizzati
        ops_card = self._create_kpi_card(
            icon_key=Icons.ROCKET,
            icon_color=COLORS["primary_blue"],
            bg_color="#eff6ff",
            value_text="-",
            value_color=COLORS["primary_blue"],
            tag_text="TASK COMPLETATI",
        )
        self.lbl_ops = ops_card.findChild(QLabel, "kpi_value")
        self.lbl_top_task = ops_card.findChild(QLabel, "kpi_sub")
        kpi_h.addWidget(ops_card)

        layout.addLayout(kpi_h)

    def _build_detail_section(self, layout: QVBoxLayout) -> None:
        """Costruisce la sezione di dettaglio con barre di successo e affidabilità."""
        # -- Success Rate Row --
        success_h = QHBoxLayout()
        success_h.setSpacing(10)

        lbl_success_icon = QLabel()
        lbl_success_icon.setFixedSize(16, 16)
        lbl_success_icon.setPixmap(
            get_colored_icon(get_asset_path(Icons.CHECK_CIRCLE), COLORS["success_dark"]).pixmap(14, 14)
        )
        lbl_success_icon.setStyleSheet("background: transparent; border: none;")
        success_h.addWidget(lbl_success_icon)

        lbl_success_tag = QLabel("Tasso di Successo")
        lbl_success_tag.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: 700;"
            " background: transparent; border: none;"
        )
        success_h.addWidget(lbl_success_tag)
        success_h.addStretch()

        self.lbl_success_pct = QLabel("0%")
        self.lbl_success_pct.setStyleSheet(
            f"color: {COLORS['success_dark']}; font-size: 13px; font-weight: 800;"
            " background: transparent; border: none;"
        )
        success_h.addWidget(self.lbl_success_pct)
        layout.addLayout(success_h)

        # Progress Bar Success
        self.progress_success = AnimatedProgressBar()
        self.progress_success.setFixedHeight(8)
        self.progress_success.set_color(COLORS["success_dark"])
        layout.addWidget(self.progress_success)

        layout.addSpacing(4)

        # -- Reliability Row --
        rel_h = QHBoxLayout()
        rel_h.setSpacing(10)

        lbl_rel_icon = QLabel()
        lbl_rel_icon.setFixedSize(16, 16)
        lbl_rel_icon.setPixmap(
            get_colored_icon(get_asset_path(Icons.SHIELD), COLORS["primary_blue"]).pixmap(14, 14)
        )
        lbl_rel_icon.setStyleSheet("background: transparent; border: none;")
        rel_h.addWidget(lbl_rel_icon)

        lbl_rel_tag = QLabel("Affidabilità Sistema")
        lbl_rel_tag.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: 700;"
            " background: transparent; border: none;"
        )
        rel_h.addWidget(lbl_rel_tag)
        rel_h.addStretch()

        self.lbl_rel_pct = QLabel("0%")
        self.lbl_rel_pct.setStyleSheet(
            f"color: {COLORS['primary_blue']}; font-size: 13px; font-weight: 800;"
            " background: transparent; border: none;"
        )
        rel_h.addWidget(self.lbl_rel_pct)
        layout.addLayout(rel_h)

        # Progress Bar Reliability
        self.progress_rel = AnimatedProgressBar()
        self.progress_rel.setFixedHeight(8)
        self.progress_rel.set_color(COLORS["primary_blue"])
        layout.addWidget(self.progress_rel)

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

        # Row for Value and Sub (Horizontal Alignment)
        row_h = QHBoxLayout()
        row_h.setSpacing(10)
        row_h.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Value
        lbl_val = QLabel(value_text)
        lbl_val.setObjectName("kpi_value")
        lbl_val.setStyleSheet(
            f"color: {value_color}; font-size: 24px; font-weight: 900; background: transparent; border: none;"
        )
        row_h.addWidget(lbl_val)

        # Sub (Trend / Top Task)
        lbl_sub = QLabel("")
        lbl_sub.setObjectName("kpi_sub")
        lbl_sub.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600; background: transparent; border: none;"
        )
        row_h.addWidget(lbl_sub)
        row_h.addStretch()
        v.addLayout(row_h)

        # Tag
        lbl_tag = QLabel(tag_text)
        lbl_tag.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 10px; font-weight: 800;"
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
        """Avvia il thread di calcolo delle statistiche in background per non bloccare la UI."""

        def run():
            """Esegue il calcolo effettivo del ROI tramite ROIEngine."""
            try:
                metrics = ROIEngine.calculate_savings()
                self.stats_updated.emit(metrics)
            except Exception as e:
                logger.error(f"Efficiency Update Error: {e}")

        threading.Thread(target=run, daemon=True).start()

    def _update_ui(self, metrics: ROIMetrics) -> None:
        """
        Aggiorna gli elementi grafici con le nuove metriche calcolate.

        Args:
            metrics: Oggetto ROIMetrics contenente i dati elaborati.
        """
        if hasattr(self, "lbl_time") and self.lbl_time:
            self.lbl_time.setText(ROIEngine.format_time_saved(metrics.total_minutes_saved))

            # Aggiorna Trend
            trend = metrics.trend_percentage
            if trend > 0:
                trend_text = f"▲ +{trend}% vs 30gg prec."
                color = COLORS["success_dark"]
            elif trend < 0:
                trend_text = f"▼ {trend}% vs 30gg prec."
                color = COLORS["error_red"]
            else:
                trend_text = "▶ 0% vs 30gg prec."
                color = COLORS["text_muted"]

            self.lbl_trend.setText(trend_text)
            self.lbl_trend.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: 700; background: transparent; border: none;")

        if hasattr(self, "lbl_ops") and self.lbl_ops:
            self.lbl_ops.setText(str(metrics.total_operations))

            # Aggiorna Top Task (Top 3)
            if metrics.top_tasks:
                icons = ["🥇", "🥈", "🥉"]
                top_text_lines = []
                for i, (name, pct) in enumerate(metrics.top_tasks):
                    icon = icons[i] if i < len(icons) else "•"
                    top_text_lines.append(f"{icon} {name} ({pct}%)")

                self.lbl_top_task.setText("\n".join(top_text_lines))
                self.lbl_top_task.setStyleSheet(
                    f"color: {COLORS['primary_blue']}; font-size: 10px; font-weight: 700;"
                    " background: transparent; border: none; line-height: 1.2;"
                )
            else:
                self.lbl_top_task.setText("Nessun dato")

        # Update Progress Bars
        self.lbl_success_pct.setText(f"{metrics.success_rate}%")
        self.progress_success.set_value(int(metrics.success_rate))

        self.lbl_rel_pct.setText(f"{metrics.reliability_score}%")
        self.progress_rel.set_value(metrics.reliability_score)

        # Media giornaliera basata sullo storico reale
        days = max(1, metrics.total_days)
        avg = round(metrics.total_operations / days, 1) if metrics.total_operations > 0 else 0
        self.lbl_avg.setText(f"Media: ~{avg} task/giorno (su {days} gg)")
