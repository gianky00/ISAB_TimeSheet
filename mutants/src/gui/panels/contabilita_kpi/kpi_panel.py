from contextlib import suppress

import matplotlib.pyplot as plt
import pandas as pd
from PyQt6.QtCore import (
    QAbstractAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.utils.helpers import get_asset_path, get_colored_icon

from .cards_row import KPICardsRow
from .charts import ChartContainer, KPIChartsManager

HOURLY_COST_STD = 28.50


class ContabilitaKPIPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        with suppress(Exception):
            plt.style.use("seaborn-v0_8-darkgrid")

        self.charts_manager = KPIChartsManager(HOURLY_COST_STD)
        self._setup_ui()
        self.refresh_years()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Toolbar (Year Selector) ---
        toolbar = QHBoxLayout()
        cal_icon = QLabel()
        cal_icon.setPixmap(
            get_colored_icon(get_asset_path(Icons.CALENDAR), "#000000").pixmap(18, 18)
        )
        toolbar.addWidget(cal_icon)
        toolbar.addWidget(QLabel("Analisi per Anno:"))

        self.year_combo = QComboBox()
        self.year_combo.setMinimumWidth(100)
        self.year_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.year_combo.setStyleSheet(
            "QComboBox { padding: 5px; border: 1px solid #ced4da; border-radius: 4px; font-size: 14px; }"
        )
        self.year_combo.currentTextChanged.connect(self._load_kpi_data)
        toolbar.addWidget(self.year_combo)
        toolbar.addStretch()
        main_layout.addLayout(toolbar)

        # --- Scroll Area ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background-color: #f8f9fa;")

        content = QWidget()
        content.setStyleSheet("background-color: #f8f9fa;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(30)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        # ROW 1: General Scorecards
        self._add_section_title("METRICHE GENERALI")
        self.row1 = KPICardsRow()
        self.card_totale = self.row1.add_card(
            "TOTALE PREVENTIVATO", "€ 0,00", "#198754"
        )
        self.card_ore = self.row1.add_card("ORE SPESE TOTALI", "0", "#0d6efd")
        self.card_resa = self.row1.add_card("RESA MEDIA", "0", "#fd7e14")
        self.card_count = self.row1.add_card("N° COMMESSE", "0", "#6f42c1")
        self.content_layout.addWidget(self.row1)

        # ROW 2: Deep Technical Analysis
        self._add_section_title("ANALISI REDDITIVITÀ E EFFICIENZA")
        self.row2 = KPICardsRow()
        self.card_margine = self.row2.add_card(
            "MARGINE OPERATIVO STIMATO",
            "€ 0,00",
            "#20c997",
            subtitle=f"Base Costo Orario: € {HOURLY_COST_STD:.2f}",
        )
        self.card_margine_perc = self.row2.add_card(
            "MARGINALITÀ %", "0.0 %", "#20c997", subtitle="Su Totale Preventivato"
        )
        self.card_eff_resa = self.row2.add_card(
            "UTILE NETTO ORARIO",
            "€ 0,00 / h",
            "#6610f2",
            subtitle="Valore Ora - Costo Base",
        )
        self.card_val_ora = self.row2.add_card(
            "VALORE PER ORA SPESA",
            "€ 0,00 / h",
            "#d63384",
            subtitle="Totale Prev / Ore Spese",
        )
        self.content_layout.addWidget(self.row2)

        # ROW 3: Charts Grid
        self._add_section_title("GRAFICI ANALITICI")
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        self.container1 = ChartContainer(
            self.charts_manager.canvas1,
            title="Distribuzione Stato Attività",
            info_callback=lambda: "Distribuzione percentuale delle attività per stato (esclusa FORNITURA).",
        )
        self.container2 = ChartContainer(
            self.charts_manager.canvas2,
            title="Preventivato vs Ore per Mese",
            info_callback=lambda: "Confronto mensile tra valore preventivato e ore spese.",
        )
        self.container3 = ChartContainer(
            self.charts_manager.canvas3,
            title="Redditività: Ricavi vs Costi",
            info_callback=lambda: "Confronto diretto tra Ricavi (Preventivato) e Costi Stimati per tipologia.",
        )
        self.container4 = ChartContainer(
            self.charts_manager.canvas4,
            title="Andamento Resa Media",
            info_callback=lambda: "Andamento mensile del valore medio di Resa.",
        )
        self.container5 = ChartContainer(
            self.charts_manager.canvas5,
            title="Stato Avanzamento Globale",
            height=200,
            info_callback=lambda: "Dettaglio avanzamento: Contabilizzate vs In Attesa/Da Completare.",
        )

        charts_grid.addWidget(self.container1, 0, 0)
        charts_grid.addWidget(self.container2, 0, 1)
        charts_grid.addWidget(self.container3, 1, 0)
        charts_grid.addWidget(self.container4, 1, 1)
        charts_grid.addWidget(self.container5, 2, 0, 1, 2)

        self.content_layout.addLayout(charts_grid)
        self.content_layout.addStretch()

        self.scroll.setWidget(content)
        main_layout.addWidget(self.scroll)

        # Animazione widgets
        self.all_widgets = (
            self.row1.cards
            + self.row2.cards
            + [
                self.container1,
                self.container2,
                self.container3,
                self.container4,
                self.container5,
            ]
        )

    def _add_section_title(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color: #495057; font-weight: bold; font-size: 16px; margin-top: 10px; margin-bottom: 10px;"
        )
        self.content_layout.addWidget(lbl)

    def refresh_years(self):
        years = ContabilitaManager.get_available_years()
        current = self.year_combo.currentText()
        self.year_combo.blockSignals(True)
        self.year_combo.clear()
        if years:
            year_strs = tuple(str(y) for y in years)
            self.year_combo.addItems(year_strs)
            if current in year_strs:
                self.year_combo.setCurrentText(current)
            else:
                self.year_combo.setCurrentIndex(0)
        self.year_combo.blockSignals(False)
        self._load_kpi_data()
        self._animate_entry()

    def _animate_entry(self):
        self.anim_group = QParallelAnimationGroup()
        for i, widget in enumerate(self.all_widgets):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(600 + (i * 100))
            anim.setStartValue(0)
            anim.setEndValue(1)
            anim.setEasingCurve(QEasingCurve.Type.OutQuad)
            self.anim_group.addAnimation(anim)
        self.anim_group.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def _format_currency(self, value):
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _load_kpi_data(self):
        year_text = self.year_combo.currentText()
        if not year_text:
            return
        try:
            year = int(year_text)
            stats = ContabilitaManager.get_year_stats(year)
            if not stats:
                return

            tot_prev = stats.get("total_prev", 0.0)
            tot_ore = stats.get("total_ore", 0.0)
            count = stats.get("count_total", 0)
            ore_dirette = stats.get("ore_dirette", 0.0)
            ore_indirette = stats.get("ore_indirette", 0.0)

            costo_tot = tot_ore * HOURLY_COST_STD
            margine = tot_prev - costo_tot
            marg_perc = (margine / tot_prev * 100) if tot_prev > 0 else 0
            val_ora = (tot_prev / tot_ore) if tot_ore > 0 else 0
            utile_ora = val_ora - HOURLY_COST_STD

            self.card_totale.lbl_value.setText(f"€ {self._format_currency(tot_prev)}")
            self.card_ore.lbl_value.setText(str(self._format_currency(tot_ore)))
            self.card_ore.set_info_callback(
                lambda: (
                    f"<b>Totale Ore: {self._format_currency(tot_ore)} h</b><br>"
                    f"--------------------------------<br>"
                    f"• Ore Dirette (su ODC/Prev): {self._format_currency(ore_dirette)} h<br>"
                    f"• Ore Indirette: {self._format_currency(ore_indirette)} h"
                )
            )

            data = ContabilitaManager.get_data_by_year(year)
            cols = [
                "data_prev",
                "mese",
                "n_prev",
                "totale_prev",
                "attivita",
                "tcl",
                "odc",
                "stato_attivita",
                "tipologia",
                "ore_sp",
                "resa",
                "annotazioni",
                "indirizzo_consuntivo",
                "nome_file",
            ]
            df = pd.DataFrame(data, columns=cols)
            df["totale_prev"] = pd.to_numeric(
                df["totale_prev"], errors="coerce"
            ).fillna(0)
            df["ore_sp"] = pd.to_numeric(df["ore_sp"], errors="coerce").fillna(0)
            df["resa"] = pd.to_numeric(df["resa"], errors="coerce")

            avg_resa = df["resa"].mean() or 0
            self.card_resa.lbl_value.setText(str(self._format_currency(avg_resa)))
            self.card_count.lbl_value.setText(str(count))

            # Style updates for margins
            self.card_margine.lbl_value.setText(f"€ {self._format_currency(margine)}")
            self.card_margine.lbl_value.setStyleSheet(
                f"color: {'#20c997' if margine >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;"
            )
            self.card_margine_perc.lbl_value.setText(
                f"{marg_perc:.1f} %".replace(".", ",")
            )
            self.card_margine_perc.lbl_value.setStyleSheet(
                f"color: {'#20c997' if marg_perc >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;"
            )
            self.card_eff_resa.lbl_value.setText(
                f"€ {self._format_currency(utile_ora)} / h"
            )
            self.card_eff_resa.lbl_value.setStyleSheet(
                f"color: {'#20c997' if utile_ora >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;"
            )
            self.card_val_ora.lbl_value.setText(
                f"€ {self._format_currency(val_ora)} / h"
            )

            self.charts_manager.plot_all(df)
        except Exception as e:
            print(f"Errore caricamento KPI: {e}")
