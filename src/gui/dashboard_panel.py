"""
Bot TS - Dashboard Panel
Pannello "Mission Control" unificato.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

from src.gui.widgets import KPIBigCard, StatusIndicator
from src.core.contabilita_manager import ContabilitaManager

class DashboardPanel(QWidget):
    """Pannello principale (Home)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        # Aggiorna i dati ogni volta che viene mostrato o con un timer
        QTimer.singleShot(500, self.refresh_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QLabel("🚀 Dashboard Direzionale")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #495057;")
        layout.addWidget(header)

        subtitle = QLabel("Panoramica stato sistema e performance aziendali")
        subtitle.setStyleSheet("font-size: 16px; color: #6c757d;")
        layout.addWidget(subtitle)

        # --- KPI Section ---
        # First Row
        kpi_layout_1 = QHBoxLayout()
        kpi_layout_1.setSpacing(20)

        self.card_margin = KPIBigCard("MARGINE OPERATIVO (Anno Corrente)", "€ 0,00", "#20c997")
        self.card_ricavi = KPIBigCard("TOTALE RICAVI (Previsto)", "€ 0,00", "#0d6efd")
        self.card_costi = KPIBigCard("COSTO STIMATO (Ore)", "€ 0,00", "#dc3545")

        kpi_layout_1.addWidget(self.card_margin)
        kpi_layout_1.addWidget(self.card_ricavi)
        kpi_layout_1.addWidget(self.card_costi)

        layout.addLayout(kpi_layout_1)

        # Second Row
        kpi_layout_2 = QHBoxLayout()
        kpi_layout_2.setSpacing(20)

        self.card_ore = KPIBigCard("ORE SPESE TOTALI", "0", "#fd7e14")
        self.card_status = KPIBigCard("STATO SISTEMA", "OTTIMALE", "#198754")

        kpi_layout_2.addWidget(self.card_ore)
        kpi_layout_2.addWidget(self.card_status)
        # Spacer for layout balance if needed, or add another card
        self.card_timbrature = KPIBigCard("TIMBRATURE OGGI", "-", "#6f42c1") # Keep logic for future use
        kpi_layout_2.addWidget(self.card_timbrature)

        layout.addLayout(kpi_layout_2)

        # --- Quick Actions / Drag Drop Area ---
        drop_area = QFrame()
        drop_area.setStyleSheet("""
            QFrame {
                border: 2px dashed #ced4da;
                border-radius: 12px;
                background-color: #f8f9fa;
                min-height: 200px;
            }
            QFrame:hover {
                border-color: #0d6efd;
                background-color: #e7f1ff;
            }
        """)
        drop_layout = QVBoxLayout(drop_area)

        drop_icon = QLabel("📂")
        drop_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_icon.setStyleSheet("font-size: 48px;")
        drop_layout.addWidget(drop_icon)

        drop_text = QLabel("Trascina qui i file Excel (Timbrature o Contabilità)\nper l'importazione automatica")
        drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_text.setStyleSheet("font-size: 18px; color: #6c757d; font-weight: bold;")
        drop_layout.addWidget(drop_text)

        layout.addWidget(drop_area)

        layout.addStretch()

    def refresh_data(self):
        """Aggiorna i dati della dashboard."""
        try:
            years = ContabilitaManager.get_available_years()
            if years:
                latest_year = max(years)
                data = ContabilitaManager.get_data_by_year(latest_year)

                # Calcolo sommario (Totale Prev - Ore * 30)
                tot_prev = 0.0
                tot_ore = 0.0

                for row in data:
                    try:
                        if len(row) > 9: # Ensure columns exist
                            # Robust parsing for Totale Prev (col 3)
                            # Format expected: "€ 1.000,00" or "1.000,00"
                            p_str = str(row[3]).replace('€', '').strip()
                            # Remove thousand separators (.) and replace decimal (,) with (.)
                            if p_str:
                                p_str_clean = p_str.replace('.', '').replace(',', '.')
                                p = float(p_str_clean)
                            else:
                                p = 0.0

                            # Robust parsing for Ore (col 9)
                            # Format expected: "10,5" or "10"
                            o_str = str(row[9]).strip()
                            if o_str:
                                o_str_clean = o_str.replace(',', '.')
                                o = float(o_str_clean)
                            else:
                                o = 0.0

                            tot_prev += p
                            tot_ore += o
                    except Exception as e:
                        print(f"Error parsing row: {e}")
                        pass

                costo_stimato = tot_ore * 30.0
                margin = tot_prev - costo_stimato

                # Update Cards
                self._update_kpi(self.card_margin, margin, is_currency=True)
                self._update_kpi(self.card_ricavi, tot_prev, is_currency=True)
                self._update_kpi(self.card_costi, costo_stimato, is_currency=True)
                self._update_kpi(self.card_ore, tot_ore, is_currency=False)

                # Color logic for margin
                color = '#20c997' if margin >= 0 else '#dc3545'
                self.card_margin.lbl_value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: 800; border: none; background: transparent;")

        except Exception as e:
            print(f"Dashboard refresh error: {e}")
            self.card_margin.lbl_value.setText("N/D")

        # 3. Status
        self.card_status.lbl_value.setText("ATTIVO")

    def _update_kpi(self, card, value, is_currency=False):
        if is_currency:
            text = f"€ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            if value.is_integer():
                text = f"{int(value)}"
            else:
                text = f"{value:.2f}".replace('.', ',')
        card.lbl_value.setText(text)
