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
    QFrame, QGridLayout, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QParallelAnimationGroup
from PyQt6.QtGui import QFont, QColor

from src.core.contabilita_manager import ContabilitaManager


class KPIBigCard(QFrame):
    """Card per mostrare un KPI numerico principale."""
    def __init__(self, title, value, color="#0d6efd", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }}
        """)
        self.setMinimumWidth(200)

        # Effetto ombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #6c757d; font-size: 14px; font-weight: bold; border: none; background: transparent;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"color: {color}; font-size: 32px; font-weight: 800; border: none; background: transparent;")
        self.lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_value)


class ContabilitaKPIPanel(QWidget):
    """Pannello Dashboard KPI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Imposta stile matplotlib moderno
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
        except:
            # Fallback se lo stile non esiste
            pass

        self._setup_ui()
        self.refresh_years()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Toolbar (Year Selector) ---
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("📅 Analisi per Anno:"))

        self.year_combo = QComboBox()
        self.year_combo.setFixedWidth(150)
        self.year_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        self.year_combo.currentTextChanged.connect(self._load_kpi_data)
        toolbar.addWidget(self.year_combo)

        toolbar.addStretch()
        main_layout.addLayout(toolbar)

        # --- Scroll Area for Dashboard ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: #f8f9fa;")

        content = QWidget()
        content.setStyleSheet("background-color: #f8f9fa;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(30)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        # 1. Scorecards Row
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(20)
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
        charts_grid.setSpacing(20)

        # Chart 1: Stato Attività (Pie)
        self.fig1 = Figure(figsize=(5, 4), dpi=100)
        self.fig1.patch.set_alpha(0) # Trasparente
        self.canvas1 = FigureCanvas(self.fig1)
        self._style_chart_container(self.canvas1)
        charts_grid.addWidget(self.canvas1, 0, 0)

        # Chart 2: Preventivato vs Ore per Mese (Bar)
        self.fig2 = Figure(figsize=(5, 4), dpi=100)
        self.fig2.patch.set_alpha(0)
        self.canvas2 = FigureCanvas(self.fig2)
        self._style_chart_container(self.canvas2)
        charts_grid.addWidget(self.canvas2, 0, 1)

        # Chart 3: Resa per Tipologia Specifiche (Bar H)
        self.fig3 = Figure(figsize=(5, 4), dpi=100)
        self.fig3.patch.set_alpha(0)
        self.canvas3 = FigureCanvas(self.fig3)
        self._style_chart_container(self.canvas3)
        charts_grid.addWidget(self.canvas3, 1, 0, 1, 2) # Span full width

        self.content_layout.addLayout(charts_grid)
        self.content_layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Preparazione animazioni
        self.cards = [self.card_totale, self.card_ore, self.card_resa, self.card_count]
        self.charts = [self.canvas1, self.canvas2, self.canvas3]

    def _style_chart_container(self, widget):
        widget.setMinimumHeight(450)
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        # Ombra anche per i grafici
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        widget.setGraphicsEffect(shadow)

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

        # Trigger animations on first load or refresh
        self._animate_entry()

    def _animate_entry(self):
        """Esegue animazione di entrata per cards e grafici."""
        self.anim_group = QParallelAnimationGroup()

        widgets = self.cards + self.charts

        for i, widget in enumerate(widgets):
            # Animazione Opacity (non supportata direttamente su tutti i widget Qt senza QGraphicsOpacityEffect)
            # Faremo animazione Slide Up

            start_geo = widget.geometry()
            # Non possiamo fidarci della geometry se non è mostrato, ma in un layout è gestito dal layout.
            # Alternativa: Animiamo una proprietà custom o usiamo solo dissolvenza se possibile.
            # Semplice: non facciamo animazione complessa che rompe il layout.
            # Facciamo solo un repaint forzato o lasciamo stare per stabilità se non siamo sicuri delle coordinate.
            pass

        # Nota: Animare widget in un layout QVBox è complesso perché il layout controlla la posizione.
        # Meglio non rischiare glitch visivi senza un container assoluto.
        # Lascio la struttura pronta per il futuro.

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
            colors=colors[:len(counts)], textprops=dict(color="black", fontsize=9)
        )
        ax.set_title('Distribuzione Stato Attività', fontsize=14, fontweight='bold', color='#495057', pad=20)

        plt.setp(texts, fontsize=9)
        plt.setp(autotexts, size=10, weight="bold", color="white")

        self.fig1.tight_layout()
        self.canvas1.draw()

    def _plot_prev_ore_mese(self, df):
        self.fig2.clear()
        ax = self.fig2.add_subplot(111)

        if df.empty:
            self.canvas2.draw()
            return

        months_order = [
            'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
            'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'
        ]
        df['mese_lower'] = df['mese'].str.lower().str.strip()
        df['mese_cat'] = pd.Categorical(df['mese_lower'], categories=months_order, ordered=True)

        grouped = df.groupby('mese_cat', observed=True)[['totale_prev', 'ore_sp']].sum()

        if grouped.empty:
            return

        x = range(len(grouped))
        # Bar chart for Money
        bars = ax.bar(x, grouped['totale_prev'], width=0.4, label='Totale Prev (€)', color='#198754', align='center', alpha=0.9)

        # Line chart for Hours
        ax2 = ax.twinx()
        line = ax2.plot(x, grouped['ore_sp'], label='Ore Spese', color='#0d6efd', marker='o', linewidth=3, markersize=8)

        ax.set_xticks(x)
        ax.set_xticklabels([m.capitalize()[:3] for m in grouped.index], rotation=45)

        ax.set_title('Preventivato (€) e Ore Spese per Mese', fontsize=14, fontweight='bold', color='#495057', pad=20)

        # Legend combinata
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')

        ax.grid(True, axis='y', alpha=0.3)
        ax2.grid(False) # Disable grid for second axis to avoid clutter

        self.fig2.tight_layout()
        self.canvas2.draw()

    def _plot_resa_tipologia(self, df):
        self.fig3.clear()
        ax = self.fig3.add_subplot(111)

        if df.empty:
            self.canvas3.draw()
            return

        # Filtra solo le tipologie richieste
        target_types = ['SQUADRA', 'FERMATA', 'CANONE', 'MISURA', 'CHIAMATA']
        # Converti a upper per confronto case-insensitive
        df['tipologia_upper'] = df['tipologia'].str.upper().str.strip()

        # Filtra il dataframe
        filtered_df = df[df['tipologia_upper'].isin(target_types)]

        if filtered_df.empty:
            # Se vuoto, mostra messaggio o grafico vuoto
            ax.text(0.5, 0.5, 'Nessun dato per le tipologie selezionate',
                    horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            self.canvas3.draw()
            return

        # Raggruppa e calcola media resa
        grouped = filtered_df.groupby('tipologia_upper')['resa'].mean().sort_values(ascending=True)

        if grouped.empty:
            return

        # Colori custom per ogni tipologia (opzionale, o unico colore)
        bars = ax.barh(grouped.index, grouped.values, color='#fd7e14', alpha=0.9, height=0.6)

        # Aggiungi etichette valore sulle barre
        for i, v in enumerate(grouped.values):
            ax.text(v + 0.5, i, f"{v:.2f}", color='black', va='center', fontweight='bold')

        ax.set_title('Resa Media per Tipologia (Target)', fontsize=14, fontweight='bold', color='#495057', pad=20)
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        # Imposta limite x per spazio etichette
        if not grouped.empty:
            ax.set_xlim(0, grouped.max() * 1.15)

        self.fig3.tight_layout()
        self.canvas3.draw()
