"""Modulo Kpi Panel."""

from contextlib import suppress
from typing import Any

from PySide6.QtCore import (
    QAbstractAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
)
from PySide6.QtWidgets import (
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

from src.core.constants import Business, Icons
from src.core.contabilita_manager import ContabilitaManager
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import FilterComboBox
from src.gui.workers.kpi_worker import KPIWorker
from src.utils.helpers import get_asset_path, get_colored_icon

from .cards_row import KPICardsRow
from .charts import ChartContainer, KPIChartsManager


class ContabilitaKPIPanel(QWidget):
    """Pannello dashboard per la visualizzazione dei KPiùdella contabilità strumentale."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il pannello e prepara i grafici."""
        super().__init__(parent)
        self.HOURLY_COST_STD = Business.HOURLY_COST_STD
        self.worker: KPIWorker | None = None

        # Member declarations
        self.year_combo: QComboBox
        self.scroll_area_area: QScrollArea
        self.content_layout: QVBoxLayout
        self.row1: KPICardsRow
        self.row2: KPICardsRow

        self.container1: ChartContainer
        self.container2: ChartContainer
        self.container3: ChartContainer
        self.container4: ChartContainer
        self.container5: ChartContainer

        self.all_widgets: list[QWidget] = []
        self.anim_group: QParallelAnimationGroup | None = None

        with suppress(Exception):
            import matplotlib.pyplot as plt

            plt.style.use("seaborn-v0_8-darkgrid")

        self.charts_manager = KPIChartsManager(self.HOURLY_COST_STD)
        self._setup_ui()
        self.refresh_years()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        self._setup_toolbar(main_layout)
        self._setup_scroll_area(main_layout)

    def _setup_toolbar(self, layout: QVBoxLayout) -> None:
        """Configura la barra degli strumenti superiore."""
        toolbar = QHBoxLayout()
        cal_icon = QLabel()
        cal_icon.setPixmap(
            get_colored_icon(get_asset_path(Icons.CALENDAR), COLORS["text_dark"]).pixmap(18, 18)
        )
        toolbar.addWidget(cal_icon)
        toolbar.addWidget(QLabel("Analisi per Anno:"))

        self.year_combo = FilterComboBox()
        self.year_combo.setMinimumWidth(100)
        self.year_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.year_combo.setStyleSheet(
            f"QComboBox {{ padding: 5px; border: 1px solid {COLORS['border_medium']}; border-radius: 4px; font-size: 14px; }}"
        )
        self.year_combo.currentTextChanged.connect(self._load_kpi_data)
        toolbar.addWidget(self.year_combo)
        toolbar.addStretch()
        layout.addLayout(toolbar)

    def _setup_scroll_area(self, layout: QVBoxLayout) -> None:
        """Configura l'area a scorrimento centrale."""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet(f"background-color: {COLORS['bg_light']};")

        content = QWidget()
        content.setStyleSheet(f"background-color: {COLORS['bg_light']};")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(30)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        self._setup_scorecards()
        self._setup_charts_grid()

        self.content_layout.addStretch()
        self.scroll_area.setWidget(content)
        layout.addWidget(self.scroll_area)

    def _setup_scorecards(self) -> None:
        """Configura le schede riassuntive (Scorecards) con stile Modern Card."""
        from src.gui.styles.ui_effects import UIEffectsManager
        from src.gui.styles.widget_styles import CARD_SHADOW_BLUR, CARD_SHADOW_COLOR, CARD_STYLE

        # ROW 1: General Scorecards
        self._add_section_title("METRICHE GENERALI")
        self.row1 = KPICardsRow()
        self.row1.setStyleSheet(CARD_STYLE)
        UIEffectsManager.apply_shadow(self.row1, blur=CARD_SHADOW_BLUR, color=CARD_SHADOW_COLOR)
        UIEffectsManager.animate_fade(self.row1, duration=500)

        self.card_totale = self.row1.add_card("TOTALE PREVENTIVATO", "  0,00", COLORS["success_dark"])
        self.card_ore = self.row1.add_card("ORE SPESE TOTALI", "0", COLORS["primary_dark"])
        self.card_resa = self.row1.add_card("RESA MEDIA", "0", COLORS["warning_orange"])
        self.card_count = self.row1.add_card("N  COMMESSE", "0", COLORS["purple"])
        self.content_layout.addWidget(self.row1)

        # ROW 2: Deep Technical Analysis
        self._add_section_title("ANALISI REDDITIVIT  E EFFICIENZA")
        self.row2 = KPICardsRow()
        self.row2.setStyleSheet(CARD_STYLE)
        UIEffectsManager.apply_shadow(self.row2, blur=CARD_SHADOW_BLUR, color=CARD_SHADOW_COLOR)
        UIEffectsManager.animate_fade(self.row2, duration=700)

        self.card_margine = self.row2.add_card(
            "MARGINE OPERATIVO STIMATO",
            "  0,00",
            COLORS["teal_light"],
            subtitle=f"Base Costo Orario:   {self.HOURLY_COST_STD:.2f}",
        )
        self.card_margine_perc = self.row2.add_card(
            "MARGINALIT  %", "0.0 %", COLORS["teal_light"], subtitle="Su Totale Preventivato"
        )
        self.card_eff_resa = self.row2.add_card(
            "UTILE NETTO ORARIO",
            "  0,00 / h",
            COLORS["purple_deep"],
            subtitle="Valore Ora - Costo Base",
        )
        self.card_val_ora = self.row2.add_card(
            "VALORE PER ORA SPESA",
            "  0,00 / h",
            COLORS["magenta_pink"],
            subtitle="Totale Prev / Ore Spese",
        )
        self.content_layout.addWidget(self.row2)

    def _setup_charts_grid(self) -> None:
        """Configura la griglia dei grafici."""
        self._add_section_title("GRAFICI ANALITICI")
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        self.container1 = ChartContainer(
            self.charts_manager.canvas1,
            title="Distribuzione Stato Attività",
            info_callback=lambda: "Distribuzione percentuale delle attivitàper stato (esclusa FORNITURA).",
        )
        self.container2 = ChartContainer(
            self.charts_manager.canvas2,
            title="Preventivato vs Ore per Mese",
            info_callback=lambda: "Confronto mensile tra valore preventivato e ore spese.",
        )
        self.container3 = ChartContainer(
            self.charts_manager.canvas3,
            title="Redditivit : Ricavi vs Costi",
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

        # Registrazione widgets per animazione
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

    def _add_section_title(self, text: str) -> None:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-weight: bold; font-size: 16px; margin-top: 10px; margin-bottom: 10px;"
        )
        self.content_layout.addWidget(lbl)

    def refresh_years(self) -> None:
        """Aggiorna la lista degli anni disponibili nella combo box dal database."""
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
        self._load_kpi_data(self.year_combo.currentText())
        self._animate_entry()

    def _animate_entry(self) -> None:
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

    def _format_currency(self, value: float) -> str:
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _load_kpi_data(self, year_text: str) -> None:
        """Avvia il worker asincrono per il caricamento dei dati KPI."""
        if not year_text:
            return

        with suppress(ValueError):
            year = int(year_text)

            # Ferma eventuale worker precedente
            if self.worker and self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait()

            # Mostra stato caricamento (opzionale, ma utile per UX)
            self.card_totale.lbl_value.setText("...")
            self.card_ore.lbl_value.setText("...")

            self.worker = KPIWorker(year, self.HOURLY_COST_STD)
            self.worker.finished_signal.connect(self._on_kpi_data_ready)
            self.worker.error_signal.connect(lambda msg: print(f"Errore KPI: {msg}"))
            self.worker.start()

    def _on_kpi_data_ready(self, result: dict[str, Any]) -> None:
        """Aggiorna i widget della UI con i dati elaborati dal worker."""
        summary = result["summary"]
        chart_data = result["chart_data"]

        # 1. Update Scorecards
        self.card_totale.lbl_value.setText(f"  {self._format_currency(summary['tot_prev'])}")
        self.card_ore.lbl_value.setText(self._format_currency(summary["tot_ore"]))
        self.card_ore.set_info_callback(
            lambda: (
                f"<b>Totale Ore: {self._format_currency(summary['tot_ore'])} h</b><br>"
                f"--------------------------------<br>"
                f"  Ore Dirette (su ODC/Prev): {self._format_currency(summary['ore_dirette'])} h<br>"
                f"  Ore Indirette: {self._format_currency(summary['ore_indirette'])} h"
            )
        )

        self.card_resa.lbl_value.setText(self._format_currency(summary["avg_resa"]))
        self.card_count.lbl_value.setText(str(summary["count"]))

        # Margini
        margine = summary["margine"]
        marg_perc = summary["marg_perc"]
        utile_ora = summary["utile_ora"]
        val_ora = summary["val_ora"]

        self.card_margine.lbl_value.setText(f"  {self._format_currency(margine)}")
        self.card_margine.lbl_value.setStyleSheet(
            f"color: {COLORS['teal_light'] if margine >= 0 else COLORS['error_red']}; font-size: 28px; font-weight: 800; border: none; background: transparent;"
        )
        self.card_margine_perc.lbl_value.setText(f"{marg_perc:.1f} %".replace(".", ","))
        self.card_margine_perc.lbl_value.setStyleSheet(
            f"color: {COLORS['teal_light'] if marg_perc >= 0 else COLORS['error_red']}; font-size: 28px; font-weight: 800; border: none; background: transparent;"
        )
        self.card_eff_resa.lbl_value.setText(f"  {self._format_currency(utile_ora)} / h")
        self.card_eff_resa.lbl_value.setStyleSheet(
            f"color: {COLORS['purple_deep'] if utile_ora >= 0 else COLORS['error_red']}; font-size: 28px; font-weight: 800; border: none; background: transparent;"
        )
        self.card_val_ora.lbl_value.setText(f"  {self._format_currency(val_ora)} / h")

        # 2. Update Charts
        self.charts_manager.plot_all(chart_data)
