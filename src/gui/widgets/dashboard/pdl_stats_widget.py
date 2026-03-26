# mypy: disable-error-code="no-untyped-def, no-untyped-call, unused-ignore, arg-type"
"""
SyncroJob - PDL Stats Widget
Card avanzata per la visualizzazione delle metriche PDL, trend e aree interattive.
V10.0: Logica colori invertita (Incremento=Rosso), percentuali intere e stile elegante.
"""

import logging
import math
import threading

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.stats.pdl_stats_engine import PDLMetrics, PDLStatsEngine
from src.gui.styles import COLORS
from src.gui.widgets.modern_card import ModernCard

logger = logging.getLogger(__name__)

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
"""Stringa CSS per la personalizzazione dei tooltip dell'applicazione."""


class AreaBadge(QPushButton):
    """Badge cliccabile per rappresentare un'area con statistiche live."""

    clicked_area = pyqtSignal(str)

    def __init__(self, name: str, count: int, trend: float, parent: QWidget | None = None) -> None:
        """Inizializza il badge dell'area con il nome, il conteggio e il trend."""
        # Formattazione: Percentuale intera e carattere elegante
        trend_int = round(trend)
        trend_str = f"+{trend_int}%" if trend_int > 0 else f"{trend_int}%"

        # Uso del bullet elegante • invece di |
        super().__init__(f"{name}\n({count} • {trend_str})", parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(
            f"<b>Area:</b> {name}<br><b>PDL Creati (Mese):</b> {count}<br><b>Andamento:</b> {trend_str}"
        )

        self.setFixedHeight(45)
        self.setMinimumWidth(75)

        # Logica Colori: Incremento = Rosso (Allerta carico)
        if trend_int > 30:  # noqa: PLR2004
            bg_color = "#fee2e2"  # Rosso chiaro
            text_color = "#991b1b"  # Rosso scuro
            border_color = "#fca5a5"
        elif trend_int > 0:
            bg_color = "#ffedd5"  # Arancio chiaro
            text_color = "#9a3412"  # Arancio scuro
            border_color = "#fdba74"
        else:
            bg_color = "#f0fdf4"  # Verde chiaro
            text_color = "#166534"  # Verde scuro
            border_color = "#bbf7d0"

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 1px;
                font-size: 12px;
                font-weight: 800;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {border_color};
            }}
            QToolTip {{
                background-color: {COLORS["bg_white"]};
                color: {COLORS["text_dark"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 4px;
                padding: 5px;
                font-size: 10px;
            }}
        """)
        self.clicked.connect(lambda: self.clicked_area.emit(name))


class PDLStatsWidget(ModernCard):
    """
    Widget premium per il monitoraggio dei PDL con logica di allerta carico.
    """

    stats_updated = pyqtSignal(object)
    area_selected = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il widget delle statistiche PDL e avvia il timer di aggiornamento."""
        super().__init__(elevation=5, parent=parent)
        self.setMinimumWidth(340)
        self._setup_ui()
        self.stats_updated.connect(self._update_ui)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(300000)
        QTimer.singleShot(1000, self.refresh_stats)

    def _setup_ui(self) -> None:
        """Inizializza l'interfaccia grafica e la disposizione dei widget."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)

        header_h = QHBoxLayout()
        self.lbl_title = QLabel("DATABASE PDL")
        self.lbl_title.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 800; letter-spacing: 1px;"
        )
        header_h.addWidget(self.lbl_title)
        header_h.addStretch()

        self.lbl_sync = QLabel("Sync: --")
        self.lbl_sync.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 9px;")
        header_h.addWidget(self.lbl_sync)
        layout.addLayout(header_h)

        kpi_h = QHBoxLayout()
        kpi_h.setSpacing(15)
        kpi_h.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.lbl_total = QLabel("0")
        self.lbl_total.setStyleSheet(f"font-size: 36px; font-weight: 900; color: {COLORS['text_dark']};")
        kpi_h.addWidget(self.lbl_total)

        trend_v = QVBoxLayout()
        trend_v.setSpacing(2)
        trend_v.setContentsMargins(0, 0, 0, 4)

        self.lbl_trend_month = QLabel("Mese: --")
        self.lbl_trend_week = QLabel("Settimana: --")
        trend_v.addWidget(self.lbl_trend_month)
        trend_v.addWidget(self.lbl_trend_week)

        kpi_h.addLayout(trend_v)
        kpi_h.addStretch()
        layout.addLayout(kpi_h)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {COLORS['border_light']}; border: none;")
        layout.addWidget(sep)

        area_label = QLabel("AREE ISAB SUD (VOLUME MENSILE)")
        area_label.setStyleSheet(
            f"font-size: 10px; font-weight: 800; color: {COLORS['text_muted']}; letter-spacing: 0.5px; margin-top: 2px;"
        )
        layout.addWidget(area_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")
        self.scroll_area.setMinimumHeight(200)

        self.area_container = QWidget()
        self.area_layout = QVBoxLayout(self.area_container)
        self.area_layout.setContentsMargins(0, 0, 5, 0)
        self.area_layout.setSpacing(6)
        self.scroll_area.setWidget(self.area_container)
        layout.addWidget(self.scroll_area)

    def refresh_stats(self) -> None:
        """Avvia un thread in background per ricalcolare le metriche PDL."""

        def run():  # noqa: ANN202
            """Funzione worker per l'esecuzione asincrona del calcolo metriche."""
            try:
                metrics = PDLStatsEngine.get_metrics()
                self.stats_updated.emit(metrics)
            except Exception as e:
                logger.error(f"PDL Refresh Error: {e}")  # noqa: TRY400

        threading.Thread(target=run, daemon=True).start()

    def _update_ui(self, metrics: PDLMetrics) -> None:
        """Aggiorna i widget grafici con i dati delle metriche ricevute."""
        self.lbl_total.setText(str(metrics.total_count))
        self.lbl_sync.setText(f"Sync: {metrics.last_sync}")

        def set_trend_style(label, trend, prefix):  # noqa: ANN001, ANN202
            """Applica lo stile cromatico basato sull'andamento del trend."""
            val = round(trend)
            if val > 0:
                # ROSSO per Incremento (più lavoro)
                label.setText(f"{prefix}: ▲ +{val}%")
                label.setStyleSheet(f"color: {COLORS['error_red']}; font-size: 11px; font-weight: 700;")
            elif val < 0:
                # VERDE per Calo
                label.setText(f"{prefix}: ▼ {val}%")
                label.setStyleSheet(f"color: {COLORS['success_dark']}; font-size: 11px; font-weight: 700;")
            else:
                label.setText(f"{prefix}: ▶ 0%")
                label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 700;")

        set_trend_style(self.lbl_trend_month, metrics.trend_percentage, "Vs Inizio Mese Prec.")
        set_trend_style(self.lbl_trend_week, metrics.weekly_trend_percentage, "Vs Settimana Prec.")

        while self.area_layout.count():
            child = self.area_layout.takeAt(0)
            if child:
                w = child.widget()
                if w:
                    w.deleteLater()
                elif lay := child.layout():
                    while lay.count():
                        item = lay.takeAt(0)
                        if item:
                            iw = item.widget()
                            if iw:
                                iw.deleteLater()

        cols = 4
        rows = math.ceil(len(metrics.areas_stats) / cols)
        for r in range(rows):
            row_h = QHBoxLayout()
            row_h.setSpacing(6)
            for c in range(cols):
                idx = r * cols + c
                if idx < len(metrics.areas_stats):
                    stat = metrics.areas_stats[idx]
                    badge = AreaBadge(stat.name, stat.current_count, stat.trend_percentage)
                    badge.clicked_area.connect(self.area_selected.emit)
                    row_h.addWidget(badge)
                else:
                    placeholder = QWidget()
                    placeholder.setFixedHeight(45)
                    row_h.addWidget(placeholder)
            self.area_layout.addLayout(row_h)
        self.area_layout.addStretch()
