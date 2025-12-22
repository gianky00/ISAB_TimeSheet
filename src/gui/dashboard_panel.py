"""
Bot TS - Dashboard Panel
Pannello "Mission Control" unificato con grafici finanziari e metriche operative.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout,
    QScrollArea, QSizePolicy, QGraphicsDropShadowEffect, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

# Matplotlib imports for charts
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from src.gui.widgets import KPIBigCard, StatusIndicator, InfoLabel
from src.core.contabilita_manager import ContabilitaManager

# Standard constants
HOURLY_COST_STD = 30.00

class DashboardPanel(QWidget):
    """Pannello principale (Home)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Use modern matplotlib style if available
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
        except:
            pass

        self._setup_ui()
        # Aggiorna i dati ogni volta che viene mostrato o con un timer
        QTimer.singleShot(500, self.refresh_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # --- Header ---
        header_layout = QHBoxLayout()
        header_text_layout = QVBoxLayout()

        header = QLabel("🚀 Dashboard Direzionale")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #495057;")
        header_text_layout.addWidget(header)

        subtitle = QLabel("Panoramica stato sistema e performance aziendali")
        subtitle.setStyleSheet("font-size: 16px; color: #6c757d;")
        header_text_layout.addWidget(subtitle)

        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # --- Content Scroll Area ---
        # Using scroll area to prevent issues on smaller screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(25)
        content_layout.setContentsMargins(0, 0, 10, 0) # Right margin for scrollbar

        # --- SECTION 1: Financial Analysis (Chart) ---
        financial_group = QGroupBox("Analisi Finanziaria")
        financial_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        fin_layout = QVBoxLayout(financial_group)
        fin_layout.setContentsMargins(15, 25, 15, 15)

        # Chart Widget
        self.fig = Figure(figsize=(8, 3.5), dpi=100) # Wide aspect ratio
        self.fig.patch.set_alpha(0) # Transparent background
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.canvas.setMinimumHeight(250)
        fin_layout.addWidget(self.canvas)

        content_layout.addWidget(financial_group)

        # --- SECTION 2: Operational Metrics (Cards) ---
        ops_group = QGroupBox("Operatività")
        ops_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        ops_layout = QHBoxLayout(ops_group)
        ops_layout.setContentsMargins(15, 25, 15, 15)
        ops_layout.setSpacing(20)

        self.card_ore = KPIBigCard("ORE SPESE TOTALI", "0", "#fd7e14")
        self.card_status = KPIBigCard("STATO SISTEMA", "OTTIMALE", "#198754")
        # Placeholder for future expansion
        self.card_timbrature = KPIBigCard("TIMBRATURE OGGI", "-", "#6f42c1")

        ops_layout.addWidget(self.card_ore)
        ops_layout.addWidget(self.card_status)
        ops_layout.addWidget(self.card_timbrature)

        content_layout.addWidget(ops_group)

        # --- SECTION 3: Quick Actions / Drag Drop ---
        drop_area = QFrame()
        drop_area.setStyleSheet("""
            QFrame {
                border: 2px dashed #ced4da;
                border-radius: 12px;
                background-color: #f8f9fa;
                min-height: 120px;
            }
            QFrame:hover {
                border-color: #0d6efd;
                background-color: #e7f1ff;
            }
        """)
        drop_layout = QHBoxLayout(drop_area)

        drop_icon = QLabel("📂")
        drop_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_icon.setStyleSheet("font-size: 32px;")
        drop_layout.addWidget(drop_icon)

        drop_text = QLabel("Trascina qui i file Excel (Timbrature o Contabilità)\nper l'importazione automatica")
        drop_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        drop_text.setStyleSheet("font-size: 16px; color: #6c757d; font-weight: bold;")
        drop_layout.addWidget(drop_text)

        drop_layout.addStretch()

        content_layout.addWidget(drop_area)
        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def refresh_data(self):
        """Aggiorna i dati della dashboard con logica di filtro rigorosa."""
        try:
            years = ContabilitaManager.get_available_years()
            if years:
                latest_year = max(years)
                data = ContabilitaManager.get_data_by_year(latest_year)

                tot_prev = 0.0
                tot_ore = 0.0

                # Data structure based on ContabilitaManager.get_data_by_year columns:
                # 0: data_prev, 1: mese, 2: n_prev, 3: totale_prev, 4: attivita, 5: tcl, 6: odc,
                # 7: stato_attivita, 8: tipologia, 9: ore_sp, 10: resa, ...

                for row in data:
                    try:
                        if len(row) > 10:
                            # 1. Strict Filter: Check 'N° PREV.' (col 2)
                            n_prev = str(row[2]).strip()
                            if not n_prev:
                                continue # Skip empty rows
                            if "totale" in n_prev.lower():
                                continue # Skip total rows from Excel

                            # 2. Strict Filter: Check 'RESA' (col 10) for "INS.ORE SP"
                            # These rows often duplicate ore/cost information or are just logging lines
                            resa_val = str(row[10]).strip().upper()
                            if "INS.ORE SP" in resa_val:
                                # Often these rows have 0 prev anyway, but let's be safe.
                                # If it's just hours logging, we might want the hours but NOT the prev sum if it's duplicated.
                                # Assuming standard logic: valid Prev has a valid N_PREV.
                                pass

                            # Parse Totale Prev (col 3)
                            p_str = str(row[3]).replace('€', '').strip()
                            p = 0.0
                            if p_str:
                                p_str_clean = p_str.replace('.', '').replace(',', '.')
                                try:
                                    p = float(p_str_clean)
                                except ValueError:
                                    p = 0.0

                            # Parse Ore (col 9)
                            o_str = str(row[9]).strip()
                            o = 0.0
                            if o_str:
                                o_str_clean = o_str.replace(',', '.')
                                try:
                                    o = float(o_str_clean)
                                except ValueError:
                                    o = 0.0

                            tot_prev += p
                            tot_ore += o
                    except Exception as e:
                        # print(f"Error parsing row: {e}") # Debug only
                        pass

                costo_stimato = tot_ore * HOURLY_COST_STD
                margin = tot_prev - costo_stimato

                # Update Charts
                self._update_financial_chart(tot_prev, costo_stimato, margin)

                # Update Cards
                self.card_ore.lbl_value.setText(f"{tot_ore:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."))

                # Status Logic
                self.card_status.lbl_value.setText("ATTIVO")
                self.card_timbrature.lbl_value.setText(f"Anno {latest_year}") # Info placeholder

            else:
                # No data
                self._update_financial_chart(0, 0, 0)
                self.card_ore.lbl_value.setText("-")

        except Exception as e:
            print(f"Dashboard refresh error: {e}")
            self.card_status.lbl_value.setText("ERRORE")

    def _update_financial_chart(self, ricavi, costi, margine):
        """Disegna il grafico finanziario a barre."""
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Data
        labels = ['Totale Ricavi', 'Costo Stimato', 'Margine Operativo']
        values = [ricavi, costi, margine]
        colors = ['#0d6efd', '#dc3545', '#20c997' if margine >= 0 else '#dc3545']

        # Horizontal Bars for better readability of labels
        y_pos = np.arange(len(labels))

        bars = ax.barh(y_pos, values, align='center', color=colors, height=0.6)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=12, fontweight='bold', color='#495057')
        ax.invert_yaxis()  # Labels read top-to-bottom

        # Hide X axis (numbers will be on bars)
        ax.xaxis.set_visible(False)
        ax.set_frame_on(False) # Remove border

        # Add value labels
        for i, bar in enumerate(bars):
            val = values[i]
            # Format: € 1.234,56
            val_str = f"€ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # Text position
            # If positive, right of bar. If negative (margin), left of bar?
            # Simple approach: slightly offset
            x_offset = bar.get_width()

            align = 'left' if val >= 0 else 'right'
            padding = 5 if val >= 0 else -5

            ax.text(x_offset + padding, bar.get_y() + bar.get_height()/2,
                    val_str,
                    va='center', ha=align,
                    fontsize=12, fontweight='bold', color=colors[i])

        self.fig.tight_layout()
        self.canvas.draw()
