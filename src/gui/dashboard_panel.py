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
        header = QLabel("🚀 Mission Control")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #495057;")
        layout.addWidget(header)

        subtitle = QLabel("Panoramica stato sistema e performance aziendali")
        subtitle.setStyleSheet("font-size: 16px; color: #6c757d;")
        layout.addWidget(subtitle)

        # --- KPI Section ---
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(20)

        self.card_margin = KPIBigCard("MARGINE OPERATIVO (Anno Corrente)", "€ 0,00", "#20c997")
        self.card_timbrature = KPIBigCard("TIMBRATURE OGGI", "0", "#0d6efd")
        self.card_status = KPIBigCard("STATO SISTEMA", "OTTIMALE", "#198754")

        kpi_layout.addWidget(self.card_margin)
        kpi_layout.addWidget(self.card_timbrature)
        kpi_layout.addWidget(self.card_status)

        layout.addLayout(kpi_layout)

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
        # 1. Margine
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
                            p = float(str(row[3]).replace('.','').replace(',','.').replace('€','').strip()) if row[3] else 0
                            o = float(str(row[9]).replace(',','.').strip()) if row[9] else 0
                            tot_prev += p
                            tot_ore += o
                    except: pass

                margin = tot_prev - (tot_ore * 30.0)
                self.card_margin.lbl_value.setText(f"€ {margin:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                self.card_margin.lbl_value.setStyleSheet(f"color: {'#20c997' if margin >= 0 else '#dc3545'}; font-size: 28px; font-weight: 800; border: none; background: transparent;")
        except:
            self.card_margin.lbl_value.setText("N/D")

        # 2. Timbrature (Simulato o count last import)
        # Qui potremmo leggere dal DB Timbrature l'ultimo count
        self.card_timbrature.lbl_value.setText("-") # Placeholder

        # 3. Status
        self.card_status.lbl_value.setText("ATTIVO")
