from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel
)
from src.gui.styles import COLORS
from src.gui.widgets.contabilita.preventivi.tab_nuovo import TabNuovoPreventivo
from src.gui.widgets.contabilita.preventivi.tab_esistente import TabGestioneEsistente

class PreventiviMainView(QWidget):
    """Contenitore principale per la gestione dei preventivi (Nuovo/Esistente)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Header elegante
        header = QWidget()
        h_lay = QVBoxLayout(header)
        h_lay.setContentsMargins(0, 0, 0, 0)
        h_lay.setSpacing(2)
        
        title = QLabel("GENERAZIONE E GESTIONE CONSUNTIVI")
        title.setStyleSheet(f"font-size: 22px; font-weight: 900; color: {COLORS['primary_dark']}; letter-spacing: 1px;")
        subtitle = QLabel("Crea nuovi documenti o automatizza file esistenti tramite Mappa VBA.")
        subtitle.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']};")
        
        h_lay.addWidget(title)
        h_lay.addWidget(subtitle)
        layout.addWidget(header)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {COLORS['border_light']};
                background: {COLORS['bg_white']};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background: {COLORS['bg_light']};
                padding: 12px 30px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                color: {COLORS['text_muted']};
                margin-right: 5px;
            }}
            QTabBar::tab:selected {{
                background: {COLORS['bg_white']};
                color: {COLORS['teal_accent']};
                border-left: 1px solid {COLORS['border_light']};
                border-right: 1px solid {COLORS['border_light']};
                border-top: 2px solid {COLORS['teal_accent']};
            }}
            QTabBar::tab:hover {{ background: {COLORS['bg_alt']}; }}
        """)

        self.tab_nuovo = TabNuovoPreventivo()
        self.tab_gestione = TabGestioneEsistente()

        self.tabs.addTab(self.tab_nuovo, "1. CREA NUOVO CONSUNTIVO")
        self.tabs.addTab(self.tab_gestione, "2. GESTISCI ESISTENTE (MAPPA VBA)")

        layout.addWidget(self.tabs)
