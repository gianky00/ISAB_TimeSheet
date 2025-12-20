"""
Bot TS - Contabilita KPI Panel
Pannello per l'analisi KPI della Contabilità Strumentale.
"""
# Rimosso matplotlib.use('Qt5Agg') per lasciare auto-detection o default
# e usare il backend corretto per PyQt6
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QFrame, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from src.core.contabilita_manager import ContabilitaManager


class KPIBigCard(QFrame):
    """Card per mostrare un KPI numerico principale."""
    def __init__(self, title, value, color="#0d6efd", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                padding: 15px;
            }}
        """)
        self.setMinimumWidth(200)

        layout = QVBoxLayout(self)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #6c757d; font-size: 14px; font-weight: bold; border: none;")
        layout.addWidget(lbl_title)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold; border: none;")
        layout.addWidget(self.lbl_value)


class ContabilitaKPIPanel(QWidget):
    """Pannello Dashboard KPI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.refresh_years()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # --- Toolbar (Year Selector) ---
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("📅 Analisi per Anno:"))

        self.year_combo = QComboBox()
        self.year_combo.setFixedWidth(120)
        self.year_combo.currentTextChanged.connect(self._load_kpi_data)
        toolbar.addWidget(self.year_combo)

        toolbar.addStretch()
        main_layout.addLayout(toolbar)

        # --- Scroll Area for Dashboard ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(20)

        # 1. Scorecards Row
        self.cards_layout = QHBoxLayout()
        self.card_totale = KPIBigCard("TOTALE PREVENTIVATO", "€ 0,00", "#198754") # Green
        self.card_ore = KPIBigCard("ORE SPESE TOTALI", "0", "#0d6efd") # Blue
        self.card_resa = KPIBigCard("RESA MEDIA", "0", "#fd7e14") # Orange
        self.card_count = KPIBigCard("N° COMMESSE", "0", "#6f42c1") # Purple

        self.cards_layout.addWidget(self.card_totale)
        self.cards_layout.addWidget(self.card_ore)
        self.cards_layout.addWidget(self.card_resa)
        self.cards_layout.addWidget(self.card_count)
        self.content_layout.addLayout(self.cards_layout)

        # 2. Charts Grid
        charts_grid = QGridLayout()

        # Chart 1: Stato Attività (Pie)
        self.fig1 = Figure(figsize=(5, 4), dpi=100)
        self.canvas1 = FigureCanvas(self.fig1)
        self._style_chart_container(self.canvas1)
        charts_grid.addWidget(self.canvas1, 0, 0)

        # Chart 2: Preventivato vs Ore per Mese (Bar)
        self.fig2 = Figure(figsize=(5, 4), dpi=100)
        self.canvas2 = FigureCanvas(self.fig2)
        self._style_chart_container(self.canvas2)
        charts_grid.addWidget(self.canvas2, 0, 1)

        # Chart 3: Resa per Tipologia (Bar H)
        self.fig3 = Figure(figsize=(5, 4), dpi=100)
        self.canvas3 = FigureCanvas(self.fig3)
        self._style_chart_container(self.canvas3)
        charts_grid.addWidget(self.canvas3, 1, 0, 1, 2) # Span full width

        self.content_layout.addLayout(charts_grid)
        self.content_layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def _style_chart_container(self, widget):
        widget.setMinimumHeight(400)
        widget.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #dee2e6;")

    def refresh_years(self):
        """Aggiorna combo box anni."""
        years = ContabilitaManager.get_available_years()
        current = self.year_combo.currentText()
        self.year_combo.blockSignals(True)
        self.year_combo.clear()
        if years:
            self.year_combo.addItems([str(y) for y in years])
            if current in [str(y) for y in years]:
                self.year_combo.setCurrentText(current)
            else:
                self.year_combo.setCurrentIndex(0)
        self.year_combo.blockSignals(False)
        self._load_kpi_data()

    def _load_kpi_data(self):
        """Carica i dati e aggiorna grafici."""
        year_text = self.year_combo.currentText()
        if not year_text:
            return

        try:
            year = int(year_text)
            data = ContabilitaManager.get_data_by_year(year)

            # Converti in DataFrame per analisi facile
            # Indices match ContabilitaManager query order
            cols = [
                'data_prev', 'mese', 'n_prev', 'totale_prev', 'attivita', 'tcl', 'odc',
                'stato_attivita', 'tipologia', 'ore_sp', 'resa', 'annotazioni',
                'indirizzo_consuntivo', 'nome_file'
            ]
            df = pd.DataFrame(data, columns=cols)

            # Converti numerici
            df['totale_prev'] = pd.to_numeric(df['totale_prev'], errors='coerce').fillna(0)
            df['ore_sp'] = pd.to_numeric(df['ore_sp'], errors='coerce').fillna(0)
            df['resa'] = pd.to_numeric(df['resa'], errors='coerce').fillna(0)

            # 1. Update Scorecards
            tot_prev = df['totale_prev'].sum()
            tot_ore = df['ore_sp'].sum()
            avg_resa = df['resa'].mean() if not df.empty else 0
            count = len(df)

            self.card_totale.lbl_value.setText(f"€ {tot_prev:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            self.card_ore.lbl_value.setText(f"{tot_ore:,.2f}")
            self.card_resa.lbl_value.setText(f"{avg_resa:.2f}")
            self.card_count.lbl_value.setText(str(count))

            # 2. Update Charts
            self._plot_stato_attivita(df)
            self._plot_prev_ore_mese(df)
            self._plot_resa_tipologia(df)

        except Exception as e:
            print(f"Errore caricamento KPI: {e}")

    def _plot_stato_attivita(self, df):
        self.fig1.clear()
        ax = self.fig1.add_subplot(111)

        if df.empty:
            self.canvas1.draw()
            return

        counts = df['stato_attivita'].value_counts()
        if counts.empty:
            return

        # Professional palette
        colors = ['#0d6efd', '#198754', '#ffc107', '#dc3545', '#6f42c1', '#0dcaf0']

        wedges, texts, autotexts = ax.pie(
            counts, labels=counts.index, autopct='%1.1f%%', startangle=90,
            colors=colors[:len(counts)], textprops=dict(color="black")
        )
        ax.set_title('Distribuzione Stato Attività', fontsize=12, fontweight='bold', color='#495057')

        plt.setp(texts, fontsize=9)
        plt.setp(autotexts, size=9, weight="bold", color="white")

        self.fig1.tight_layout()
        self.canvas1.draw()

    def _plot_prev_ore_mese(self, df):
        self.fig2.clear()
        ax = self.fig2.add_subplot(111)

        if df.empty:
            self.canvas2.draw()
            return

        # Raggruppa per mese (Attenzione all'ordine dei mesi, servirebbe un sort custom,
        # per ora usiamo l'ordine di apparizione o alfabetico)
        months_order = [
            'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
            'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'
        ]
        df['mese_lower'] = df['mese'].str.lower().str.strip()
        df['mese_cat'] = pd.Categorical(df['mese_lower'], categories=months_order, ordered=True)

        grouped = df.groupby('mese_cat', observed=True)[['totale_prev', 'ore_sp']].sum()

        if grouped.empty:
            return

        # Dual axis? No, scale diverse (Euro vs Ore). Usiamo due barre ma normalizzate o dual axis.
        # Meglio dual axis per professionalità.

        x = range(len(grouped))
        ax.bar(x, grouped['totale_prev'], width=0.4, label='Totale Prev (€)', color='#198754', align='center')

        ax2 = ax.twinx()
        ax2.plot(x, grouped['ore_sp'], label='Ore Spese', color='#0d6efd', marker='o', linewidth=2)

        ax.set_xticks(x)
        ax.set_xticklabels([m.capitalize()[:3] for m in grouped.index], rotation=45)

        ax.set_title('Preventivato (€) e Ore Spese per Mese', fontsize=12, fontweight='bold', color='#495057')
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')

        self.fig2.tight_layout()
        self.canvas2.draw()

    def _plot_resa_tipologia(self, df):
        self.fig3.clear()
        ax = self.fig3.add_subplot(111)

        if df.empty:
            self.canvas3.draw()
            return

        # Top 10 tipologie per resa media
        grouped = df.groupby('tipologia')['resa'].mean().sort_values(ascending=True).tail(10)

        if grouped.empty:
            return

        ax.barh(grouped.index, grouped.values, color='#fd7e14')
        ax.set_title('Top 10 Tipologie per Resa Media', fontsize=12, fontweight='bold', color='#495057')
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        self.fig3.tight_layout()
        self.canvas3.draw()
