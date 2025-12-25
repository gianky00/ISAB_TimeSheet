"""
Bot TS - Dashboard Panel
Pannello "Mappa Applicazione" interattiva e modulare.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout,
    QScrollArea, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor, QIcon

class DashboardPanel(QWidget):
    """Pannello Home con Mappa Modulare Interattiva."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)

        # Header
        header_layout = QVBoxLayout()
        title = QLabel("👋 Benvenuto in Timesheet Manager")
        title.setStyleSheet("font-size: 32px; font-weight: 800; color: #343a40;")
        header_layout.addWidget(title)

        subtitle = QLabel("Seleziona il modulo che desideri utilizzare.")
        subtitle.setStyleSheet("font-size: 18px; color: #6c757d;")
        header_layout.addWidget(subtitle)

        layout.addLayout(header_layout)

        # Map Container (Grid Layout for Independence)
        map_frame = QFrame()
        map_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e9ecef;
            }
        """)
        # Use Grid Layout for 2x2 matrix
        map_layout = QGridLayout(map_frame)
        map_layout.setContentsMargins(40, 40, 40, 40)
        map_layout.setSpacing(30)

        # --- Moduli Automazione ---

        # Dettagli OdA
        map_layout.addWidget(self._create_module_card(
            "Dettagli OdA",
            "Scarica i dettagli degli ordini d'acquisto.",
            "📋",
            "#6f42c1",
            "dettagli_oda"
        ), 0, 0)

        # Scarico TS
        map_layout.addWidget(self._create_module_card(
            "Scarico TS",
            "Scarica i timesheet dal portale.",
            "📥",
            "#0d6efd",
            "scarico_ts"
        ), 0, 1)

        # Timbrature
        map_layout.addWidget(self._create_module_card(
            "Timbrature",
            "Controlla e valida le timbrature.",
            "⏱️",
            "#fd7e14",
            "timbrature"
        ), 1, 0)

        # Carico TS
        map_layout.addWidget(self._create_module_card(
            "Carico TS",
            "Carica i dati finali sul portale.",
            "📤",
            "#198754",
            "carico_ts"
        ), 1, 1)

        layout.addWidget(map_frame)
        layout.addStretch()

    def _create_module_card(self, title, desc, icon, color, action_key):
        """Crea una card cliccabile per un singolo modulo."""
        card = QFrame()
        card.setFixedSize(280, 200) # Wider, shorter cards for grid
        card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Stile dinamico per hover
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #f8f9fa;
                border: 2px solid transparent;
                border-radius: 12px;
            }}
            QFrame:hover {{
                background-color: white;
                border-color: {color};
                margin-top: -5px; /* Lift effect */
                /* Box Shadow simulated via border for now, or could add shadow effect */
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 25, 20, 25)

        # Top: Icon + Title
        top_layout = QHBoxLayout()

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"font-size: 36px; color: {color}; border: none; background: transparent;")
        top_layout.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #343a40; border: none; background: transparent;")
        top_layout.addWidget(title_lbl)

        top_layout.addStretch()
        card_layout.addLayout(top_layout)

        # Description
        desc_lbl = QLabel(desc)
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("font-size: 14px; color: #6c757d; border: none; background: transparent; margin-top: 10px;")
        card_layout.addWidget(desc_lbl)

        card_layout.addStretch()

        # Action Hint (bottom right)
        hint_lbl = QLabel("Apri ➜")
        hint_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        hint_lbl.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {color}; border: none; background: transparent;")
        card_layout.addWidget(hint_lbl)

        # Full Card Click Button Overlay
        btn = QPushButton(card)
        btn.setGeometry(0, 0, 280, 200)
        btn.setStyleSheet("background: transparent; border: none;")
        btn.clicked.connect(lambda: self._navigate_to(action_key))

        return card

    def _navigate_to(self, key):
        """Naviga alla tab specificata."""
        main_window = self.window()
        if hasattr(main_window, 'navigate_to_panel'):
            main_window.navigate_to_panel(key)
