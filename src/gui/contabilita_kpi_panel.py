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
    QToolTip, QDialog, QPushButton
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QAbstractAnimation
from PyQt6.QtGui import QColor, QCursor, QFont

from src.core.contabilita_manager import ContabilitaManager

# Costante per il costo orario aziendale standard
HOURLY_COST_STD = 27.43

class DetailedInfoDialog(QDialog):
    """Dialogo modale per spiegazioni dettagliate KPI."""
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dettaglio KPI")
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setFixedWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 2px solid #0d6efd;
                border-radius: 8px;
            }
            QLabel {
                color: #212529;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)

        # Title
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #0d6efd; margin-bottom: 10px;")
        layout.addWidget(lbl_title)

        # Content (HTML)
        lbl_content = QLabel(content)
        lbl_content.setWordWrap(True)
        lbl_content.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(lbl_content)

        # Close info
        lbl_close = QLabel("\n(Clicca per chiudere)")
        lbl_close.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_close.setStyleSheet("color: #adb5bd; font-size: 11px;")
        layout.addWidget(lbl_close)

    def mousePressEvent(self, event):
        self.accept()

class InfoLabel(QLabel):
    """Etichetta informativa con icona che apre un popup al click."""
    def __init__(self, title, get_text_callback, parent=None):
        super().__init__("ⓘ", parent)
        self.title = title
        self.get_text_callback = get_text_callback # Funzione che restituisce il testo aggiornato
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-weight: bold;
                font-size: 16px;
                background: transparent;
                padding: 0px 5px;
            }
            QLabel:hover {
                color: #0d6efd;
            }
        """)

    def mousePressEvent(self, event):
        """Mostra il dialog con il testo aggiornato."""
        content = self.get_text_callback() if callable(self.get_text_callback) else str(self.get_text_callback)
        dlg = DetailedInfoDialog(self.title, content, self.window())
        # Posiziona il dialog vicino al mouse
        dlg.move(event.globalPosition().toPoint())
        dlg.exec()

    def enterEvent(self, event):
        """Opzionale: tooltip veloce."""
        pass

class KPIBigCard(QFrame):
    """Card per mostrare un KPI numerico principale."""
    def __init__(self, title, value, color="#0d6efd", parent=None, subtitle=None):
        super().__init__(parent)
        self.info_content_callback = lambda: "Nessuna informazione disponibile."

        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }}
        """)
        self.setMinimumWidth(200)
        self.setMinimumHeight(120)

        # Effetto ombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)

        # Header Layout (Title + Info Icon)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #6c757d; font-size: 13px; font-weight: bold; border: none; background: transparent;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(lbl_title)

        header_layout.addStretch()

        # Info Icon che chiama self.get_info_content
        self.info_icon = InfoLabel(title, self._get_info_content)
        header_layout.addWidget(self.info_icon)

        layout.addLayout(header_layout)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: 800; border: none; background: transparent;")
        self.lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_value)

        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setStyleSheet("color: #adb5bd; font-size: 11px; border: none; background: transparent;")
            lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_sub)

    def set_info_callback(self, callback):
        """Imposta la funzione per generare il testo informativo."""
        self.info_content_callback = callback

    def _get_info_content(self):
        return self.info_content_callback()


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
        lbl_sect2 = QLabel("ANALISI TECNICA PROFONDA")
        lbl_sect2.setStyleSheet("color: #495057; font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;")
        self.content_layout.addWidget(lbl_sect2)

        self.tech_cards_layout = QHBoxLayout()
        self.tech_cards_layout.setSpacing(20)

        self.card_margine = KPIBigCard(
            "MARGINE OPERATIVO STIMATO", "€ 0,00", "#20c997",
            subtitle=f"Base Costo Orario: € {HOURLY_COST_STD}"
        )
        self.card_margine_perc = KPIBigCard(
            "MARGINALITÀ %", "0.0 %", "#20c997",
            subtitle="Su Totale Preventivato"
        )

        # RINOMINATA DA EFFICIENZA DI RESA A UTILE NETTO ORARIO
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
            title="Margine Operativo vs Costo",
            info_callback=lambda: "Analisi redditività per tipologia (Verde=Margine, Rosso=Costo)."
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
            info_callback=lambda: "Percentuale di attività contabilizzate rispetto al totale."
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
            anim.setEasingCurve(QEasingCurve.Type.OutQuad)

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
            data = ContabilitaManager.get_data_by_year(year)

            # Converti in DataFrame
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

            # --- 1. Update General Scorecards ---
            tot_prev = df['totale_prev'].sum()
            tot_ore = df['ore_sp'].sum()
            avg_resa = df['resa'].mean() if not df.empty else 0
            count = len(df)

            self.card_totale.lbl_value.setText(f"€ {self._format_currency(tot_prev)}")
            self.card_totale.set_info_callback(lambda: f"Somma totale del valore economico di tutti i preventivi/commesse registrati per l'anno {year}.")

            self.card_ore.lbl_value.setText(f"{self._format_currency(tot_ore)}")
            self.card_ore.set_info_callback(lambda: f"Totale delle ore lavorate registrate su tutte le commesse nell'anno {year}.")

            self.card_resa.lbl_value.setText(f"{self._format_currency(avg_resa)}")
            self.card_count.lbl_value.setText(str(count))

            # --- 2. Update Technical Scorecards ---
            # Costo totale stimato
            costo_totale_stimato = tot_ore * HOURLY_COST_STD
            margine_operativo = tot_prev - costo_totale_stimato

            marginalita_perc = (margine_operativo / tot_prev * 100) if tot_prev > 0 else 0
            # CORREZIONE: Efficienza Resa NON è somma(resa) / ore se resa è un tasso.
            # Qui la useremo come UTILE NETTO ORARIO.
            valore_per_ora = (tot_prev / tot_ore) if tot_ore > 0 else 0
            utile_netto_orario = valore_per_ora - HOURLY_COST_STD

            # Margine Info
            self.card_margine.lbl_value.setText(f"€ {self._format_currency(margine_operativo)}")
            self.card_margine.lbl_value.setStyleSheet(f"color: {'#20c997' if margine_operativo >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;")
            self.card_margine.set_info_callback(lambda: (
                f"<b>CALCOLO ESEMPIO REALE ({year}):</b><br><br>"
                f"Totale Preventivato: € {self._format_currency(tot_prev)}<br>"
                f" - Costo Stimato: € {self._format_currency(costo_totale_stimato)} (Ore {self._format_currency(tot_ore)} * € {HOURLY_COST_STD})<br>"
                f"--------------------------------------------------<br>"
                f"<b>= Margine Operativo: € {self._format_currency(margine_operativo)}</b><br><br>"
                f"Indica l'utile lordo stimato dopo aver coperto i costi orari del personale."
            ))

            # Marginalita % Info
            self.card_margine_perc.lbl_value.setText(f"{marginalita_perc:.1f} %".replace(".", ","))
            self.card_margine_perc.lbl_value.setStyleSheet(f"color: {'#20c997' if marginalita_perc >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;")
            self.card_margine_perc.set_info_callback(lambda: (
                f"<b>CALCOLO ESEMPIO REALE ({year}):</b><br><br>"
                f"Margine Operativo: € {self._format_currency(margine_operativo)}<br>"
                f" / Totale Preventivato: € {self._format_currency(tot_prev)}<br>"
                f"--------------------------------------------------<br>"
                f"<b>= Marginalità: {marginalita_perc:.1f}%</b><br><br>"
                f"Per ogni 100€ fatturati, rimangono € {marginalita_perc:.1f} di margine."
            ))

            # UTILE NETTO ORARIO Info
            self.card_eff_resa.lbl_value.setText(f"€ {self._format_currency(utile_netto_orario)} / h")
            self.card_eff_resa.lbl_value.setStyleSheet(f"color: {'#20c997' if utile_netto_orario >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;")
            self.card_eff_resa.set_info_callback(lambda: (
                f"<b>CALCOLO ESEMPIO REALE ({year}):</b><br><br>"
                f"Valore per Ora Spesa: € {self._format_currency(valore_per_ora)}<br>"
                f" - Costo Orario Base: € {str(HOURLY_COST_STD).replace('.', ',')}<br>"
                f"--------------------------------------------------<br>"
                f"<b>= Utile Netto Orario: € {self._format_currency(utile_netto_orario)} / h</b><br><br>"
                f"Indica quanto guadagno netto genera ogni singola ora lavorata."
            ))

            # Valore per Ora Spesa Info
            self.card_val_ora.lbl_value.setText(f"€ {self._format_currency(valore_per_ora)} / h")
            self.card_val_ora.set_info_callback(lambda: (
                f"<b>CALCOLO ESEMPIO REALE ({year}):</b><br><br>"
                f"Totale Preventivato: € {self._format_currency(tot_prev)}<br>"
                f" / Ore Spese Totali: {self._format_currency(tot_ore)}<br>"
                f"--------------------------------------------------<br>"
                f"<b>= Valore Orario: € {self._format_currency(valore_per_ora)} / h</b><br><br>"
                f"Ogni ora lavorata ha generato un fatturato medio di € {self._format_currency(valore_per_ora)}.<br>"
                f"(Confrontalo con il costo orario base di € {HOURLY_COST_STD})"
            ))

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
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')

        ax.grid(True, axis='y', alpha=0.3)
        ax2.grid(False)

        self.fig2.tight_layout()
        self.canvas2.draw()

    def _plot_margine_tipologia(self, df):
        """Grafico a Barre: Margine Operativo vs Costo per Tipologia."""
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

        # Raggruppa e calcola Margine e Costo
        # Margine = Prev - (Ore * Costo_Std)
        # Costo = Ore * Costo_Std

        # FIX: Evita FutureWarning su groupby().apply() con colonne di raggruppamento
        # Raggruppiamo esplicitamente solo le colonne numeriche necessarie o usiamo include_groups=False se pandas > 2.2
        # Un modo robusto è calcolare le somme prima

        grouped_sums = filtered_df.groupby('tipologia_upper')[['totale_prev', 'ore_sp']].sum()
        grouped_sums['Margine'] = grouped_sums['totale_prev'] - (grouped_sums['ore_sp'] * HOURLY_COST_STD)
        grouped_sums['Costo'] = grouped_sums['ore_sp'] * HOURLY_COST_STD

        grouped = grouped_sums.sort_values(by='Margine', ascending=True)

        if grouped.empty:
            return

        y = np.arange(len(grouped))
        height = 0.35

        ax.barh(y - height/2, grouped['Margine'], height, label='Margine Operativo', color='#20c997', alpha=0.9)
        ax.barh(y + height/2, grouped['Costo'], height, label='Costo Stimato', color='#dc3545', alpha=0.6)

        ax.set_yticks(y)
        ax.set_yticklabels(grouped.index)
        ax.legend()

        # ax.set_title('Margine Operativo vs Costo per Tipologia', fontsize=14, fontweight='bold', color='#495057', pad=20)
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        self.fig3.tight_layout()
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
        self.fig5.clear()
        ax = self.fig5.add_axes([0.05, 0.3, 0.9, 0.4])

        if df.empty:
            self.canvas5.draw()
            return

        total = len(df)
        contabilizzate = len(df[df['stato_attivita'].str.contains('CONTABILIZZA', case=False, na=False)])
        percent = (contabilizzate / total * 100) if total > 0 else 0

        ax.barh(0, 100, height=0.5, color='#e9ecef', edgecolor='none')
        ax.barh(0, percent, height=0.5, color='#198754', edgecolor='none')

        ax.text(50, 0, f"{percent:.1f}% ATTIVITÀ CONTABILIZZATE", ha='center', va='center',
                color='white' if percent > 50 and percent < 60 else ('black' if percent < 50 else 'white'),
                fontweight='bold', fontsize=12)

        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.axis('off')

        # ax.set_title('Stato Avanzamento Globale', fontsize=14, fontweight='bold', color='#495057', pad=10)

        self.canvas5.draw()
