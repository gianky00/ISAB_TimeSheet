"""
Bot TS - Dashboard Panel
Pannello "Mappa Applicazione" interattiva.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout,
    QScrollArea, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor, QIcon

class DashboardPanel(QWidget):
    """Pannello Home con Mappa Interattiva."""

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

        subtitle = QLabel("Seleziona un'attività per iniziare. Il flusso di lavoro consigliato procede da sinistra a destra.")
        subtitle.setStyleSheet("font-size: 18px; color: #6c757d;")
        header_layout.addWidget(subtitle)

        layout.addLayout(header_layout)

        # Map Container
        map_frame = QFrame()
        map_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e9ecef;
            }
        """)
        map_layout = QHBoxLayout(map_frame)
        map_layout.setContentsMargins(40, 40, 40, 40)
        map_layout.setSpacing(40)

        # Step 1: Dettagli OdA
        map_layout.addWidget(self._create_step_card(
            "1. Dettagli OdA",
            "Scarica i dettagli degli ordini.",
            "📋",
            "#6f42c1",
            "dettagli_oda"
        ))

        # Arrow
        map_layout.addWidget(self._create_arrow())

        # Step 2: Scarico TS
        map_layout.addWidget(self._create_step_card(
            "2. Scarico TS",
            "Scarica i timesheet dal portale.",
            "📥",
            "#0d6efd",
            "scarico_ts"
        ))

        # Arrow
        map_layout.addWidget(self._create_arrow())

        # Step 3: Timbrature
        map_layout.addWidget(self._create_step_card(
            "3. Timbrature",
            "Controlla e valida le timbrature.",
            "⏱️",
            "#fd7e14",
            "timbrature"
        ))

        # Arrow
        map_layout.addWidget(self._create_arrow())

        # Step 4: Carico TS
        map_layout.addWidget(self._create_step_card(
            "4. Carico TS",
            "Carica i dati finali sul portale.",
            "📤",
            "#198754",
            "carico_ts"
        ))

        layout.addWidget(map_frame)
        layout.addStretch()

    def _create_step_card(self, title, desc, icon, color, action_key):
        card = QFrame()
        card.setFixedSize(220, 280)
        card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        card.setObjectName("stepCard") # For potential future styling

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
            }}
        """)

        # Click handler hack using event filter or button overlay
        # Using a layout with a button that fills the frame is easier
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 30)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"font-size: 48px; color: {color}; border: none; background: transparent;")
        card_layout.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #343a40; margin-top: 10px; border: none; background: transparent;")
        card_layout.addWidget(title_lbl)

        desc_lbl = QLabel(desc)
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("font-size: 13px; color: #6c757d; border: none; background: transparent;")
        card_layout.addWidget(desc_lbl)

        # Make the whole card clickable logic
        # We can simulate this by putting a transparent button on top or
        # just using mouseReleaseEvent override if we subclassed.
        # Simpler: Create a big button inside.

        btn = QPushButton(card)
        btn.setGeometry(0, 0, 220, 280)
        btn.setStyleSheet("background: transparent; border: none;")
        btn.clicked.connect(lambda: self._navigate_to(action_key))

        return card

    def _create_arrow(self):
        lbl = QLabel("➜")
        lbl.setStyleSheet("font-size: 24px; color: #dee2e6; font-weight: bold;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return lbl

    def _navigate_to(self, key):
        """Naviga alla tab specificata."""
        main_window = self.window()
        if hasattr(main_window, 'navigate_to_panel'):
            main_window.navigate_to_panel(key)
