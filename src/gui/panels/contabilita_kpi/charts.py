import os
import sys
from typing import Any

import numpy as np
from matplotlib.figure import Figure
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS
from src.gui.widgets.info_widgets import InfoLabel

FigureCanvas: Any = None

# Evita il caricamento dei backend Matplotlib Qt durante i test per prevenire Access Violation nativi
if "pytest" in sys.modules or os.environ.get("PYTEST_CURRENT_TEST"):
    from unittest.mock import MagicMock

    FigureCanvas = MagicMock
else:
    try:
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

        FigureCanvas = FigureCanvasQTAgg
    except (ImportError, RuntimeError):
        from unittest.mock import MagicMock

        FigureCanvas = MagicMock


class ChartContainer(QWidget):
    """Container stilizzato per i grafici Matplotlib."""

    def __init__(self, canvas, title="", height=450, info_callback=None, parent=None):  # noqa: ANN001, ANN204
        super().__init__(parent)
        self.canvas = canvas
        self.setMinimumHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {COLORS["bg_white"]};
                border-radius: 15px;
                border: 1px solid {COLORS["border_light"]};
            }}
        """
        )

        # Ombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header con Titolo e Info
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 10, 15, 0)

        if title:
            lbl = QLabel(title)
            lbl.setStyleSheet(
                f"font-weight: bold; color: {COLORS['text_dark']}; font-size: 14px; border: none;"
            )
            header_layout.addWidget(lbl)

        header_layout.addStretch()
        if info_callback:
            info_icon = InfoLabel("Dettaglio Grafico", info_callback)
            header_layout.addWidget(info_icon)

        layout.addLayout(header_layout)
        layout.addWidget(self.canvas)


class KPIChartsManager:
    """Gestore per la creazione e l'aggiornamento dei grafici KPI."""

    def __init__(self, HOURLY_COST_STD):  # noqa: ANN001, ANN204, N803
        self.HOURLY_COST_STD = HOURLY_COST_STD
        self.annot = None

        # Inizializzazione Figure e Canvas
        self.fig1, self.canvas1 = self._init_figure()
        self.fig2, self.canvas2 = self._init_figure()
        self.fig3, self.canvas3 = self._init_figure()
        self.fig4, self.canvas4 = self._init_figure()
        self.fig5, self.canvas5 = self._init_figure()

    def _init_figure(self):  # noqa: ANN202
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_alpha(0)
        canvas = FigureCanvas(fig)
        return fig, canvas

    def plot_all(self, kpi_data):  # noqa: ANN001, ANN201
        """Aggiorna tutti i grafici con i dati pre-processati dal service."""
        self._plot_stato_attivita(kpi_data.get("stato_attivita", {}))
        self._plot_prev_ore_mese(kpi_data.get("prev_ore_mese", {}))
        self._plot_margine_tipologia(kpi_data.get("margine_tipologia", {}))
        self._plot_andamento_resa(kpi_data.get("andamento_resa", {}))
        self._plot_completamento(kpi_data.get("completamento", {}))

    def _plot_stato_attivita(self, counts):  # noqa: ANN001, ANN202
        self.fig1.clear()
        ax = self.fig1.add_subplot(111)
        if not counts:
            self.canvas1.draw()
            return

        labels = list(counts.keys())
        values = list(counts.values())

        colors = [
            COLORS["primary_blue"],
            COLORS["success_dark"],
            COLORS["warning_yellow"],
            COLORS["error_red"],
            COLORS["purple"],
            COLORS["cyan_info"],
        ]
        wedges, _texts = ax.pie(
            values,
            labels=None,
            startangle=90,
            colors=colors[: len(values)],
            wedgeprops={"width": 0.5, "edgecolor": "w", "linewidth": 2},
        )

        self.annot = ax.annotate(
            "",
            xy=(0, 0),
            xytext=(0, 0),
            textcoords="offset points",
            bbox={"boxstyle": "round", "fc": "black", "ec": "none", "alpha": 0.9},
            color="white",
            fontweight="bold",
            fontsize=10,
            arrowprops={"arrowstyle": "-", "color": "black"},
        )
        self.annot.set_visible(False)

        total_sum = sum(values)

        def update_annot(wedge, idx):  # noqa: ANN001, ANN202
            if not self.annot:
                return
            ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            self.annot.xy = (x * 0.7, y * 0.7)
            count = values[idx]
            percent = (count / total_sum) * 100
            self.annot.set_text(f"{labels[idx]}\n{percent:.1f}% ({count})")

        def hover(event):  # noqa: ANN001, ANN202
            if event.inaxes == ax:
                found = False
                for i, wedge in enumerate(wedges):
                    contains, _ = wedge.contains(event)
                    if contains:
                        update_annot(wedge, i)
                        if self.annot:
                            self.annot.set_visible(True)
                        self.fig1.canvas.draw_idle()
                        found = True
                        break
                if not found and self.annot and self.annot.get_visible():
                    self.annot.set_visible(False)
                    self.fig1.canvas.draw_idle()

        self.fig1.canvas.mpl_connect("motion_notify_event", hover)
        self.fig1.tight_layout()
        self.canvas1.draw()

    def _plot_prev_ore_mese(self, data):  # noqa: ANN001, ANN202
        self.fig2.clear()
        ax = self.fig2.add_subplot(111)
        if not data:
            self.canvas2.draw()
            return

        x = range(len(data["labels"]))
        ax.bar(
            x,
            data["totale_prev"],
            width=0.4,
            label="Totale Prev (\u20ac)",
            color=COLORS["success_dark"],
            alpha=0.8,
        )
        ax2 = ax.twinx()
        ax2.plot(
            x,
            data["ore_sp"],
            label="Ore Spese",
            color=COLORS["primary_blue"],
            marker="o",
            linewidth=3,
        )
        ax.set_xticks(x)
        ax.set_xticklabels(data["labels"], rotation=45)
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc="upper right")
        ax.grid(True, axis="y", alpha=0.3)
        self.fig2.tight_layout()
        self.canvas2.draw()

    def _plot_margine_tipologia(self, data):  # noqa: ANN001, ANN202
        self.fig3.clear()
        ax = self.fig3.add_subplot(111)
        if not data:
            ax.text(0.5, 0.5, "Nessun dato", ha="center", va="center")
            self.canvas3.draw()
            return

        labels = data["labels"]
        y = np.arange(len(labels))
        height = 0.35
        ax.barh(
            y + height / 2,
            data["ricavi"],
            height,
            label="Ricavi (Prev.)",
            color=COLORS["success_dark"],
            alpha=0.8,
        )
        ax.barh(
            y - height / 2,
            data["costi"],
            height,
            label="Costi Stimati",
            color=COLORS["error_red"],
            alpha=0.7,
        )
        ax.set_yticks(y)
        ax.set_yticklabels(labels)
        ax.legend(loc="lower right", framealpha=0.8)

        for i, val in enumerate(data["ricavi"]):
            ax.text(
                val,
                i + height / 2,
                f" \u20ac {val / 1000:.1f}k",
                va="center",
                fontsize=9,
                color=COLORS["success_dark"],
            )
        for i, val in enumerate(data["costi"]):
            ax.text(
                val,
                i - height / 2,
                f" \u20ac {val / 1000:.1f}k",
                va="center",
                fontsize=9,
                color=COLORS["error_red"],
            )

        ax.grid(axis="x", linestyle="--", alpha=0.5)
        self.fig3.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1)
        self.canvas3.draw()

    def _plot_andamento_resa(self, data):  # noqa: ANN001, ANN202
        self.fig4.clear()
        ax = self.fig4.add_subplot(111)
        if not data or not data["values"]:
            ax.text(0.5, 0.5, "Nessun dato Resa", ha="center", va="center")
            self.canvas4.draw()
            return

        x = range(len(data["labels"]))
        ax.plot(x, data["values"], color=COLORS["glass_deep"], marker="o", linewidth=3)
        ax.fill_between(x, data["values"], color=COLORS["primary_blue"], alpha=0.1)
        ax.set_xticks(x)
        ax.set_xticklabels(data["labels"], rotation=45)
        ax.grid(True, linestyle="--", alpha=0.5)
        self.fig4.tight_layout()
        self.canvas4.draw()

    def _plot_completamento(self, data):  # noqa: ANN001, ANN202
        self.fig5.clear()
        ax = self.fig5.add_axes([0.05, 0.4, 0.9, 0.3])
        if not data:
            self.canvas5.draw()
            return

        p_comp = data["p_comp"]
        p_tcl = data["p_tcl"]
        p_todo = data["p_todo"]
        p_other = data["p_other"]

        ax.barh(0, p_comp, height=0.6, color=COLORS["success_dark"], label="Contabilizzate")
        ax.barh(0, p_tcl, left=p_comp, height=0.6, color=COLORS["warning_yellow"], label="In Attesa TCL")
        ax.barh(0, p_todo, left=p_comp + p_tcl, height=0.6, color=COLORS["error_red"], label="Da Completare")
        ax.barh(0, p_other, left=p_comp + p_tcl + p_todo, height=0.6, color=COLORS["bg_hover"], label="Altro")
