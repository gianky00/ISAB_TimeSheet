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
import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QFrame, QGridLayout, QScrollArea, QGraphicsDropShadowEffect, QSizePolicy, QGraphicsOpacityEffect,
    QToolTip, QPushButton, QApplication
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QAbstractAnimation, QPoint
from PyQt6.QtGui import QColor, QCursor, QFont, QScreen

from src.core.contabilita_manager import ContabilitaManager
from src.gui.widgets import InfoLabel, KPIBigCard

# Costante per il costo orario aziendale standard
HOURLY_COST_STD = 30.00


class ContabilitaKPIPanel(QWidget):
    """Pannello Dashboard KPI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Imposta stile matplotlib moderno
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
        except:
            pass

        self._setup_ui()
        self.refresh_years()

        # Variabili per annotazioni interattive
        self.annot = None

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
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background-color: #f8f9fa;")

        content = QWidget()
        content.setStyleSheet("background-color: #f8f9fa;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(30)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        # --- ROW 1: General Scorecards ---
        lbl_sect1 = QLabel("METRICHE GENERALI")
        lbl_sect1.setStyleSheet("color: #495057; font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        self.content_layout.addWidget(lbl_sect1)

        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(20)

        self.card_totale = KPIBigCard("TOTALE PREVENTIVATO", "€ 0,00", "#198754")
        self.card_ore = KPIBigCard("ORE SPESE TOTALI", "0", "#0d6efd")
        self.card_resa = KPIBigCard("RESA MEDIA", "0", "#fd7e14")
        self.card_count = KPIBigCard("N° COMMESSE", "0", "#6f42c1")

        self.cards_layout.addWidget(self.card_totale)
        self.cards_layout.addWidget(self.card_ore)
        self.cards_layout.addWidget(self.card_resa)
        self.cards_layout.addWidget(self.card_count)
        self.content_layout.addLayout(self.cards_layout)

        # --- ROW 2: Deep Technical Analysis ---
        # RENAMED from "ANALISI TECNICA PROFONDA"
        lbl_sect2 = QLabel("ANALISI REDDITIVITÀ E EFFICIENZA")
        lbl_sect2.setStyleSheet("color: #495057; font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;")
        self.content_layout.addWidget(lbl_sect2)

        self.tech_cards_layout = QHBoxLayout()
        self.tech_cards_layout.setSpacing(20)

        self.card_margine = KPIBigCard(
            "MARGINE OPERATIVO STIMATO", "€ 0,00", "#20c997",
            subtitle=f"Base Costo Orario: € {HOURLY_COST_STD:.2f}"
        )
        self.card_margine_perc = KPIBigCard(
            "MARGINALITÀ %", "0.0 %", "#20c997",
            subtitle="Su Totale Preventivato"
        )

        self.card_eff_resa = KPIBigCard(
            "UTILE NETTO ORARIO", "€ 0,00 / h", "#6610f2",
            subtitle="Valore Ora - Costo Base"
        )

        self.card_val_ora = KPIBigCard(
            "VALORE PER ORA SPESA", "€ 0,00 / h", "#d63384",
            subtitle="Totale Prev / Ore Spese"
        )

        self.tech_cards_layout.addWidget(self.card_margine)
        self.tech_cards_layout.addWidget(self.card_margine_perc)
        self.tech_cards_layout.addWidget(self.card_eff_resa)
        self.tech_cards_layout.addWidget(self.card_val_ora)
        self.content_layout.addLayout(self.tech_cards_layout)

        # --- ROW 3: Charts Grid ---
        lbl_sect3 = QLabel("GRAFICI ANALITICI")
        lbl_sect3.setStyleSheet("color: #495057; font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;")
        self.content_layout.addWidget(lbl_sect3)

        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        # Chart 1: Stato Attività (Pie) - Interactive
        self.fig1 = Figure(figsize=(5, 4), dpi=100)
        self.fig1.patch.set_alpha(0)
        self.canvas1 = FigureCanvas(self.fig1)
        self.container1 = self._create_chart_container(
            self.canvas1,
            title="Distribuzione Stato Attività",
            info_callback=lambda: "Distribuzione percentuale delle attività per stato (esclusa FORNITURA)."
        )
        charts_grid.addWidget(self.container1, 0, 0)

        # Chart 2: Preventivato vs Ore per Mese (Bar)
        self.fig2 = Figure(figsize=(5, 4), dpi=100)
        self.fig2.patch.set_alpha(0)
        self.canvas2 = FigureCanvas(self.fig2)
        self.container2 = self._create_chart_container(
            self.canvas2,
            title="Preventivato vs Ore per Mese",
            info_callback=lambda: "Confronto mensile tra valore preventivato e ore spese."
        )
        charts_grid.addWidget(self.container2, 0, 1)

        # Chart 3: Analisi Margine per Tipologia (Nuovo Chart)
        self.fig3 = Figure(figsize=(5, 4), dpi=100)
        self.fig3.patch.set_alpha(0)
        self.canvas3 = FigureCanvas(self.fig3)
        self.container3 = self._create_chart_container(
            self.canvas3,
            title="Redditività: Ricavi vs Costi",
            info_callback=lambda: "Confronto diretto tra Ricavi (Preventivato) e Costi Stimati per tipologia."
        )
        charts_grid.addWidget(self.container3, 1, 0)

        # Chart 4: Andamento Resa Mensile (Line)
        self.fig4 = Figure(figsize=(5, 4), dpi=100)
        self.fig4.patch.set_alpha(0)
        self.canvas4 = FigureCanvas(self.fig4)
        self.container4 = self._create_chart_container(
            self.canvas4,
            title="Andamento Resa Media",
            info_callback=lambda: "Andamento mensile del valore medio di Resa."
        )
        charts_grid.addWidget(self.container4, 1, 1)

        # Chart 5: Completamento Attività
        self.fig5 = Figure(figsize=(5, 2), dpi=100)
        self.fig5.patch.set_alpha(0)
        self.canvas5 = FigureCanvas(self.fig5)
        self.container5 = self._create_chart_container(
            self.canvas5,
            height=200,
            title="Stato Avanzamento Globale",
            info_callback=lambda: "Dettaglio avanzamento: Contabilizzate vs In Attesa/Da Completare."
        )
        charts_grid.addWidget(self.container5, 2, 0, 1, 2)

        self.content_layout.addLayout(charts_grid)
        self.content_layout.addStretch()

        self.scroll.setWidget(content)
        main_layout.addWidget(self.scroll)

        # Preparazione lista widget per animazioni
        self.cards = [self.card_totale, self.card_ore, self.card_resa, self.card_count,
                      self.card_margine, self.card_margine_perc, self.card_eff_resa, self.card_val_ora]
        self.charts = [self.container1, self.container2, self.container3, self.container4, self.container5]

    def _create_chart_container(self, widget, height=450, title="", info_callback=None):
        """Crea un container stilizzato per il grafico."""
        container = QWidget()
        container.setMinimumHeight(height)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)

        # Ombra
        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Info icon overlay/header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 10, 15, 0)

        if title:
            lbl = QLabel(title)
            lbl.setStyleSheet("font-weight: bold; color: #495057; font-size: 14px; border: none;")
            header_layout.addWidget(lbl)

        header_layout.addStretch()
        if info_callback:
            info_icon = InfoLabel("Dettaglio Grafico", info_callback)
            header_layout.addWidget(info_icon)

        layout.addLayout(header_layout)
        layout.addWidget(widget)

        return container

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

        # Avvia animazione
        self._animate_entry()

    def _animate_entry(self):
        """Esegue animazione di entrata per cards e grafici (FadeIn)."""
        self.anim_group = QParallelAnimationGroup()

        all_widgets = self.cards + self.charts

        for i, widget in enumerate(all_widgets):
            # Crea effetto opacità
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

            # Animazione Opacity 0 -> 1
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(600 + (i * 100)) # Staggered
            anim.setStartValue(0)
            anim.setEndValue(1)
            anim.setEasingCurve(QEasingCurve(QEasingCurve.Type.OutQuad))

            self.anim_group.addAnimation(anim)

        self.anim_group.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def _format_currency(self, value):
        """Formatta valuta in italiano: 1.000,00"""
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _load_kpi_data(self):
        """Carica i dati e aggiorna grafici."""
        year_text = self.year_combo.currentText()
        if not year_text:
            return

        try:
            year = int(year_text)
            # Use get_year_stats which now computes direct/indirect hours
            stats = ContabilitaManager.get_year_stats(year)

            if not stats: return

            # Extract metrics
            tot_prev = stats.get('total_prev', 0.0)
            tot_ore = stats.get('total_ore', 0.0)
            count = stats.get('count_total', 0)
            ore_dirette = stats.get('ore_dirette', 0.0)
            ore_indirette = stats.get('ore_indirette', 0.0)

            # Recalculate derived metrics for display (some might duplicate get_year_stats logic but safer here for display formatting)
            costo_totale_stimato = tot_ore * HOURLY_COST_STD
            margine_operativo = tot_prev - costo_totale_stimato
            marginalita_perc = (margine_operativo / tot_prev * 100) if tot_prev > 0 else 0
            valore_per_ora = (tot_prev / tot_ore) if tot_ore > 0 else 0
            utile_netto_orario = valore_per_ora - HOURLY_COST_STD

            # --- 1. Update General Scorecards ---
            self.card_totale.lbl_value.setText(f"€ {self._format_currency(tot_prev)}")

            # Aggiorna la card Ore con il breakdown dirette/indirette
            self.card_ore.lbl_value.setText(f"{self._format_currency(tot_ore)}")
            self.card_ore.set_info_callback(lambda: (
                f"<b>Totale Ore: {self._format_currency(tot_ore)} h</b><br>"
                f"--------------------------------<br>"
                f"• Ore Dirette (su ODC/Prev): {self._format_currency(ore_dirette)} h<br>"
                f"• Ore Indirette: {self._format_currency(ore_indirette)} h"
            ))

            # Resa media (calcolata nel manager? No, qui dobbiamo ricalcolarla o prenderla se disponibile.
            # get_year_stats non ritorna avg_resa. Ricalcoliamo dai dati raw per coerenza col vecchio codice o aggiungiamo a stats.
            # Per ora lasciamo 0 se non disponibile, o facciamo query rapida.
            # Dato che get_year_stats è ottimizzato, meglio aggiungere lì se serve.
            # Ma il vecchio codice caricava TUTTO il dataframe qui.
            # Per performance, meglio usare stats già pronte.
            # Se avg_resa non c'è, mettiamo N/D o 0.
            # *Correction*: The user didn't explicitly ask for Resa update, just Direct/Indirect.
            # I will reuse the existing logic for Resa if possible, but I replaced `_load_kpi_data` logic with `get_year_stats`.
            # Let's restore full data loading if needed for charts?
            # Yes, the charts need the DF. `get_year_stats` is good for summary cards but charts need data.
            # So I will call `get_data_by_year` again to get the DF for charts.

            data = ContabilitaManager.get_data_by_year(year)
            cols = [
                'data_prev', 'mese', 'n_prev', 'totale_prev', 'attivita', 'tcl', 'odc',
                'stato_attivita', 'tipologia', 'ore_sp', 'resa', 'annotazioni',
                'indirizzo_consuntivo', 'nome_file'
            ]
            df = pd.DataFrame(data, columns=cols)

            # Clean DF as before
            df['totale_prev'] = pd.to_numeric(df['totale_prev'], errors='coerce').fillna(0)
            df['ore_sp'] = pd.to_numeric(df['ore_sp'], errors='coerce').fillna(0)
            df['resa'] = pd.to_numeric(df['resa'], errors='coerce')

            avg_resa = df['resa'].mean()
            if pd.isna(avg_resa): avg_resa = 0

            self.card_resa.lbl_value.setText(f"{self._format_currency(avg_resa)}")
            self.card_count.lbl_value.setText(str(count))

            # --- 2. Update Technical Scorecards ---
            self.card_margine.lbl_value.setText(f"€ {self._format_currency(margine_operativo)}")
            self.card_margine.lbl_value.setStyleSheet(f"color: {'#20c997' if margine_operativo >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;")

            self.card_margine_perc.lbl_value.setText(f"{marginalita_perc:.1f} %".replace(".", ","))
            self.card_margine_perc.lbl_value.setStyleSheet(f"color: {'#20c997' if marginalita_perc >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;")

            self.card_eff_resa.lbl_value.setText(f"€ {self._format_currency(utile_netto_orario)} / h")
            self.card_eff_resa.lbl_value.setStyleSheet(f"color: {'#20c997' if utile_netto_orario >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;")

            self.card_val_ora.lbl_value.setText(f"€ {self._format_currency(valore_per_ora)} / h")

            # --- 3. Update Charts ---
            self._plot_stato_attivita(df)
            self._plot_prev_ore_mese(df)
            self._plot_margine_tipologia(df)
            self._plot_andamento_resa(df)
            self._plot_completamento(df)

        except Exception as e:
            print(f"Errore caricamento KPI: {e}")

    def _plot_stato_attivita(self, df):
        """Pie chart interattivo: mostra etichette solo al passaggio del mouse."""
        self.fig1.clear()
        ax = self.fig1.add_subplot(111)

        if df.empty:
            self.canvas1.draw()
            return

        # FILTRO ESCLUSIONE FORNITURA
        df_filtered = df[~df['stato_attivita'].str.contains('FORNITURA', case=False, na=False)]

        counts = df_filtered['stato_attivita'].value_counts()
        if counts.empty:
            ax.text(0.5, 0.5, 'Nessun dato', ha='center', va='center')
            self.canvas1.draw()
            return

        colors = ['#0d6efd', '#198754', '#ffc107', '#dc3545', '#6f42c1', '#0dcaf0']

        # Create pie without labels and autopct (hidden by default)
        wedges, texts = ax.pie(
            counts,
            labels=None, # No static labels
            startangle=90,
            colors=colors[:len(counts)],
            wedgeprops=dict(width=0.6, edgecolor='w') # Donut style for cleaner look
        )

        # ax.set_title('Distribuzione Stato Attività', fontsize=14, fontweight='bold', color='#495057', pad=20)

        # --- Interactive Annotation ---
        self.annot = ax.annotate("", xy=(0,0), xytext=(0,0), textcoords="offset points",
                                bbox=dict(boxstyle="round", fc="black", ec="none", alpha=0.9),
                                color="white", fontweight="bold", fontsize=10,
                                arrowprops=dict(arrowstyle="-", color="black"))
        self.annot.set_visible(False)

        def update_annot(wedge, idx):
            # Posizione angolare media
            ang = (wedge.theta2 - wedge.theta1)/2. + wedge.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))

            # Posiziona annotazione un po' fuori dal centro
            self.annot.xy = (x*0.7, y*0.7)

            count = counts.iloc[idx]
            total = counts.sum()
            percent = count / total * 100
            label = counts.index[idx]

            text = f"{label}\n{percent:.1f}% ({count})"
            self.annot.set_text(text)
            self.annot.get_bbox_patch().set_alpha(0.9)

        def hover(event):
            vis = self.annot.get_visible()
            if event.inaxes == ax:
                found = False
                for i, wedge in enumerate(wedges):
                    contains, _ = wedge.contains(event)
                    if contains:
                        update_annot(wedge, i)
                        self.annot.set_visible(True)
                        self.fig1.canvas.draw_idle()
                        found = True
                        break
                if not found and vis:
                    self.annot.set_visible(False)
                    self.fig1.canvas.draw_idle()

        self.fig1.canvas.mpl_connect("motion_notify_event", hover)

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
        ax.bar(x, grouped['totale_prev'], width=0.4, label='Totale Prev (€)', color='#198754', align='center', alpha=0.9)

        ax2 = ax.twinx()
        line = ax2.plot(x, grouped['ore_sp'], label='Ore Spese', color='#0d6efd', marker='o', linewidth=3, markersize=8)

        ax.set_xticks(x)
        ax.set_xticklabels([m.capitalize()[:3] for m in grouped.index], rotation=45)

        # ax.set_title('Preventivato (€) e Ore Spese per Mese', fontsize=14, fontweight='bold', color='#495057', pad=20)

        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        # LEGEND UPPER RIGHT as requested
        ax2.legend(lines + lines2, labels + labels2, loc='upper right')

        ax.grid(True, axis='y', alpha=0.3)
        ax2.grid(False)

        self.fig2.tight_layout()
        self.canvas2.draw()

    def _plot_margine_tipologia(self, df):
        """Grafico a Barre: Ricavi vs Costi per Tipologia."""
        self.fig3.clear()
        ax = self.fig3.add_subplot(111)

        if df.empty:
            self.canvas3.draw()
            return

        target_types = ['SQUADRA', 'FERMATA', 'CANONE', 'MISURA', 'CHIAMATA']
        df['tipologia_upper'] = df['tipologia'].str.upper().str.strip()

        filtered_df = df[df['tipologia_upper'].isin(target_types)]

        if filtered_df.empty:
            ax.text(0.5, 0.5, 'Nessun dato per le tipologie target',
                    ha='center', va='center')
            self.canvas3.draw()
            return

        # Raggruppa e calcola Ricavi (Prev) e Costi
        grouped_sums = filtered_df.groupby('tipologia_upper')[['totale_prev', 'ore_sp']].sum()
        grouped_sums['Costo'] = grouped_sums['ore_sp'] * HOURLY_COST_STD
        grouped_sums['Margine'] = grouped_sums['totale_prev'] - grouped_sums['Costo']

        # Ordina per Ricavi descrescente
        grouped = grouped_sums.sort_values(by='totale_prev', ascending=True)

        if grouped.empty:
            return

        y = np.arange(len(grouped))
        height = 0.35

        # Bar 1: Ricavi (Totale Preventivato) - Green/Teal
        ax.barh(y + height/2, grouped['totale_prev'], height, label='Totale Preventivato (Ricavi)', color='#20c997', alpha=0.9)

        # Bar 2: Costi (Ore * Standard) - Red
        ax.barh(y - height/2, grouped['Costo'], height, label='Costo Stimato', color='#dc3545', alpha=0.8)

        ax.set_yticks(y)
        ax.set_yticklabels(grouped.index)
        # Legenda posizionata in basso a destra con frame semi-trasparente
        ax.legend(loc='lower right', framealpha=0.8)

        # Aggiunge etichette numeriche
        for i, (idx, row) in enumerate(grouped.iterrows()):
            # Etichetta Ricavi + Margine
            margine_k = row['Margine'] / 1000
            txt_ric = f" € {row['totale_prev']/1000:.1f}k (Margine: {margine_k:+.1f}k)"
            ax.text(row['totale_prev'], i + height/2, txt_ric,
                    va='center', fontsize=9, color='#198754', fontweight='bold')

            # Etichetta Costi
            ax.text(row['Costo'], i - height/2, f" € {row['Costo']/1000:.1f}k",
                    va='center', fontsize=9, color='#dc3545')

        ax.grid(axis='x', linestyle='--', alpha=0.5)

        # Ottimizzazione spazi: riduce i margini per riempire la card
        # Lascia spazio a sinistra per le etichette (tipologie)
        self.fig3.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1)
        self.canvas3.draw()

    def _plot_andamento_resa(self, df):
        self.fig4.clear()
        ax = self.fig4.add_subplot(111)

        if df.empty:
            self.canvas4.draw()
            return

        months_order = [
            'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
            'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'
        ]
        df['mese_lower'] = df['mese'].str.lower().str.strip()
        df['mese_cat'] = pd.Categorical(df['mese_lower'], categories=months_order, ordered=True)

        # Qui usiamo dropna() implicito se ci sono NaN in resa
        df_resa = df[df['resa'] > 0]
        grouped = df_resa.groupby('mese_cat', observed=True)['resa'].mean()

        if grouped.empty:
            ax.text(0.5, 0.5, 'Nessun dato Resa', ha='center', va='center')
            self.canvas4.draw()
            return

        x = range(len(grouped))
        ax.plot(x, grouped.values, color='#6f42c1', marker='o', linewidth=3, markersize=8)

        ax.fill_between(x, grouped.values, color='#6f42c1', alpha=0.1)

        ax.set_xticks(x)
        ax.set_xticklabels([m.capitalize()[:3] for m in grouped.index], rotation=45)

        for i, v in enumerate(grouped.values):
            ax.text(i, v + (v*0.05), f"{v:.1f}", ha='center', fontsize=9, fontweight='bold', color='#6f42c1')

        # ax.set_title('Andamento Resa Media Mensile', fontsize=14, fontweight='bold', color='#495057', pad=20)
        ax.grid(True, linestyle='--', alpha=0.5)

        self.fig4.tight_layout()
        self.canvas4.draw()

    def _plot_completamento(self, df):
        """Barra di avanzamento impilata."""
        self.fig5.clear()
        ax = self.fig5.add_axes([0.05, 0.4, 0.9, 0.3]) # Adjust layout

        if df.empty:
            self.canvas5.draw()
            return

        total = len(df)
        if total == 0:
            return

        # Definisci categorie
        completed = df[df['stato_attivita'].str.contains('CONTABILIZZA|CHIUSA', case=False, na=False)]
        pending_tcl = df[df['stato_attivita'].str.contains('IN ATTESA TCL', case=False, na=False)]
        to_complete = df[df['stato_attivita'].str.contains('DA COMPLETARE', case=False, na=False)]

        count_completed = len(completed)
        count_tcl = len(pending_tcl)
        count_todo = len(to_complete)
        # Il resto sono "Altro" o "Aperta" generica
        count_other = total - count_completed - count_tcl - count_todo

        # Percentuali
        pct_completed = (count_completed / total) * 100
        pct_tcl = (count_tcl / total) * 100
        pct_todo = (count_todo / total) * 100
        pct_other = (count_other / total) * 100

        # Plot Stacked Bar
        # Order: Completed (Green), TCL (Yellow), Todo (Red), Other (Gray)

        p1 = ax.barh(0, pct_completed, height=0.6, color='#198754', label='Contabilizzate', edgecolor='white')
        p2 = ax.barh(0, pct_tcl, left=pct_completed, height=0.6, color='#ffc107', label='In Attesa TCL', edgecolor='white')
        p3 = ax.barh(0, pct_todo, left=pct_completed + pct_tcl, height=0.6, color='#dc3545', label='Da Completare', edgecolor='white')
        p4 = ax.barh(0, pct_other, left=pct_completed + pct_tcl + pct_todo, height=0.6, color='#e9ecef', label='Altro', edgecolor='white')

        # Label Helper Function to prevent overlap
        def add_label(pct, current_left, color='white'):
            # Only show if at least 2% width to avoid clutter (reduced from 5% to show TCL)
            if pct > 2:
                ax.text(current_left + pct/2, 0, f"{pct:.1f}%", ha='center', va='center', color=color, fontweight='bold')

        add_label(pct_completed, 0)
        add_label(pct_tcl, pct_completed, color='black') # Yellow bg needs black text
        add_label(pct_todo, pct_completed + pct_tcl)

        # Other might be small, skip if tiny
        add_label(pct_other, pct_completed + pct_tcl + pct_todo, color='black')

        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.axis('off')

        # Legend below
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=4, frameon=False, fontsize=9)

        self.canvas5.draw()
