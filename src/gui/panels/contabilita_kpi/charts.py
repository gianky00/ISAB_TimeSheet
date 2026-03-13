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

    def __init__(self, canvas, title="", height=450, info_callback=None, parent=None):
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

    def __init__(self, HOURLY_COST_STD):
        self.HOURLY_COST_STD = HOURLY_COST_STD
        self.annot = None

        # Inizializzazione Figure e Canvas
        self.fig1, self.canvas1 = self._init_figure()
        self.fig2, self.canvas2 = self._init_figure()
        self.fig3, self.canvas3 = self._init_figure()
        self.fig4, self.canvas4 = self._init_figure()
        self.fig5, self.canvas5 = self._init_figure()

    def _init_figure(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_alpha(0)
        canvas = FigureCanvas(fig)
        return fig, canvas

    def plot_all(self, df):
        """Aggiorna tutti i grafici con il dataframe fornito."""
        self._plot_stato_attivita(df)
        self._plot_prev_ore_mese(df)
        self._plot_margine_tipologia(df)
        self._plot_andamento_resa(df)
        self._plot_completamento(df)

    def _plot_stato_attivita(self, df):
        self.fig1.clear()
        ax = self.fig1.add_subplot(111)
        if df.empty:
            self.canvas1.draw()
            return

        df_filtered = df[~df["stato_attivita"].str.contains("FORNITURA", case=False, na=False)]
        counts = df_filtered["stato_attivita"].value_counts()
        if counts.empty:
            ax.text(0.5, 0.5, "Nessun dato", ha="center", va="center")
            self.canvas1.draw()
            return

        colors = [
            COLORS["primary_blue"],
            COLORS["success_dark"],
            COLORS["warning_yellow"],
            COLORS["error_red"],
            COLORS["purple"],
            COLORS["cyan_info"],
        ]
        wedges, _texts = ax.pie(
            counts,
            labels=None,
            startangle=90,
            colors=colors[: len(counts)],
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

        def update_annot(wedge, idx):
            if not self.annot:
                return
            ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            self.annot.xy = (x * 0.7, y * 0.7)
            count = counts.iloc[idx]
            percent = count / counts.sum() * 100
            self.annot.set_text(f"{counts.index[idx]}\n{percent:.1f}% ({count})")

        def hover(event):
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

    def _plot_prev_ore_mese(self, df):
        import pandas as pd

        self.fig2.clear()
        ax = self.fig2.add_subplot(111)
        if df.empty:
            self.canvas2.draw()
            return

        months_order = [
            "gennaio",
            "febbraio",
            "marzo",
            "aprile",
            "maggio",
            "giugno",
            "luglio",
            "agosto",
            "settembre",
            "ottobre",
            "novembre",
            "dicembre",
        ]
        df["mese_lower"] = df["mese"].str.lower().str.strip()
        df["mese_cat"] = pd.Categorical(df["mese_lower"], categories=months_order, ordered=True)
        grouped = df.groupby("mese_cat", observed=True)[["totale_prev", "ore_sp"]].sum()

        if grouped.empty:
            return

        x = range(len(grouped))
        ax.bar(
            x,
            grouped["totale_prev"],
            width=0.4,
            label="Totale Prev (€)",
            color=COLORS["success_dark"],
            alpha=0.8,
        )
        ax2 = ax.twinx()
        ax2.plot(
            x,
            grouped["ore_sp"],
            label="Ore Spese",
            color=COLORS["primary_blue"],
            marker="o",
            linewidth=3,
        )
        ax.set_xticks(x)
        ax.set_xticklabels([m.capitalize()[:3] for m in grouped.index], rotation=45)
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc="upper right")
        ax.grid(True, axis="y", alpha=0.3)
        self.fig2.tight_layout()
        self.canvas2.draw()

    def _plot_margine_tipologia(self, df):
        self.fig3.clear()
        ax = self.fig3.add_subplot(111)
        if df.empty:
            self.canvas3.draw()
            return

        target_types = ["SQUADRA", "FERMATA", "CANONE", "MISURA", "CHIAMATA"]
        df["tipologia_upper"] = df["tipologia"].str.upper().str.strip()
        filtered_df = df[df["tipologia_upper"].isin(target_types)]

        if filtered_df.empty:
            ax.text(0.5, 0.5, "Nessun dato", ha="center", va="center")
            self.canvas3.draw()
            return

        grouped = filtered_df.groupby("tipologia_upper")[["totale_prev", "ore_sp"]].sum()
        grouped["Costo"] = grouped["ore_sp"] * self.HOURLY_COST_STD
        grouped["Margine"] = grouped["totale_prev"] - grouped["Costo"]
        grouped = grouped.sort_values(by="totale_prev", ascending=True)

        y = np.arange(len(grouped))
        height = 0.35
        ax.barh(
            y + height / 2,
            grouped["totale_prev"],
            height,
            label="Ricavi (Prev.)",
            color=COLORS["success_dark"],
            alpha=0.8,
        )
        ax.barh(
            y - height / 2,
            grouped["Costo"],
            height,
            label="Costi Stimati",
            color=COLORS["error_red"],
            alpha=0.7,
        )
        ax.set_yticks(y)
        ax.set_yticklabels(grouped.index)
        ax.legend(loc="lower right", framealpha=0.8)

        for i, (_idx, row) in enumerate(grouped.iterrows()):
            ax.text(
                row["totale_prev"],
                i + height / 2,
                f" € {row['totale_prev'] / 1000:.1f}k",
                va="center",
                fontsize=9,
                color=COLORS["success_dark"],
            )
            ax.text(
                row["Costo"],
                i - height / 2,
                f" € {row['Costo'] / 1000:.1f}k",
                va="center",
                fontsize=9,
                color=COLORS["error_red"],
            )

        ax.grid(axis="x", linestyle="--", alpha=0.5)
        self.fig3.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1)
        self.canvas3.draw()

    def _plot_andamento_resa(self, df):
        import pandas as pd

        self.fig4.clear()
        ax = self.fig4.add_subplot(111)
        if df.empty:
            self.canvas4.draw()
            return

        months_order = [
            "gennaio",
            "febbraio",
            "marzo",
            "aprile",
            "maggio",
            "giugno",
            "luglio",
            "agosto",
            "settembre",
            "ottobre",
            "novembre",
            "dicembre",
        ]
        df["mese_lower"] = df["mese"].str.lower().str.strip()
        df["mese_cat"] = pd.Categorical(df["mese_lower"], categories=months_order, ordered=True)
        df_resa = df[df["resa"] > 0]
        grouped = df_resa.groupby("mese_cat", observed=True)["resa"].mean()

        if grouped.empty:
            ax.text(0.5, 0.5, "Nessun dato Resa", ha="center", va="center")
            self.canvas4.draw()
            return

        x = range(len(grouped))
        ax.plot(x, grouped.values, color=COLORS["glass_deep"], marker="o", linewidth=3)
        ax.fill_between(x, grouped.values, color=COLORS["primary_blue"], alpha=0.1)
        ax.set_xticks(x)
        ax.set_xticklabels([m.capitalize()[:3] for m in grouped.index], rotation=45)
        ax.grid(True, linestyle="--", alpha=0.5)
        self.fig4.tight_layout()
        self.canvas4.draw()

    def _plot_completamento(self, df):
        self.fig5.clear()
        ax = self.fig5.add_axes([0.05, 0.4, 0.9, 0.3])
        if df.empty:
            self.canvas5.draw()
            return

        total = len(df)
        completed = len(df[df["stato_attivita"].str.contains("CONTABILIZZA|CHIUSA", case=False, na=False)])
        pending_tcl = len(df[df["stato_attivita"].str.contains("IN ATTESA TCL", case=False, na=False)])
        to_complete = len(df[df["stato_attivita"].str.contains("DA COMPLETARE", case=False, na=False)])
        other = total - completed - pending_tcl - to_complete

        p_comp = (completed / total) * 100
        p_tcl = (pending_tcl / total) * 100
        p_todo = (to_complete / total) * 100
        p_other = (other / total) * 100

        ax.barh(0, p_comp, height=0.6, color=COLORS["success_dark"], label="Contabilizzate")
        ax.barh(0, p_tcl, left=p_comp, height=0.6, color=COLORS["warning_yellow"], label="In Attesa TCL")
        ax.barh(
            0,
            p_todo,
            left=p_comp + p_tcl,
            height=0.6,
            color=COLORS["error_red"],
            label="Da Completare",
        )
        ax.barh(
            0,
            p_other,
            left=p_comp + p_tcl + p_todo,
            height=0.6,
            color=COLORS["bg_hover"],
            label="Altro",
        )

        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.axis("off")
        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.2),
            ncol=4,
            frameon=False,
            fontsize=9,
        )
        self.canvas5.draw()
