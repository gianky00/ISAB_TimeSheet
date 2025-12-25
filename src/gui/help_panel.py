"""
Bot TS - Help Panel
Pannello Guida rivisitato con stile moderno e coinvolgente.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QGridLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette

class HelpCard(QFrame):
    """Card stilizzata per sezioni della guida."""
    def __init__(self, title, icon, content_html, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 10px;
            }
            QFrame:hover {
                border-color: #0d6efd;
                background-color: #f8f9fa;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 24px; border: none; background: transparent;")
        header_layout.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #495057; border: none; background: transparent;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Content
        content_lbl = QLabel(content_html)
        content_lbl.setWordWrap(True)
        content_lbl.setTextFormat(Qt.TextFormat.RichText)
        content_lbl.setStyleSheet("color: #6c757d; font-size: 14px; border: none; background: transparent;")
        layout.addWidget(content_lbl)

class HelpPanel(QWidget):
    """Pannello Guida moderno."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header Hero Section
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2);
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("📚 Centro Assistenza")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: 800;")
        header_layout.addWidget(title)

        desc = QLabel("Scopri come ottenere il massimo dal tuo assistente digitale.")
        desc.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 16px;")
        header_layout.addWidget(desc)

        layout.addWidget(header)

        # Scroll Area per le card
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Grid per le card
        grid = QGridLayout()
        grid.setSpacing(20)

        # Card 1: Scorciatoie
        shortcuts_html = """
        <ul style="margin-left: -20px;">
            <li><b>F5</b>: Aggiorna / Avvia</li>
            <li><b>Ctrl + F</b>: Cerca nel database</li>
            <li><b>Ctrl + S</b>: Salva impostazioni</li>
            <li><b>Ctrl + C</b>: Copia righe</li>
        </ul>
        """
        grid.addWidget(HelpCard("Scorciatoie Rapide", "⚡", shortcuts_html), 0, 0)

        # Card 2: Workflow
        workflow_html = """
        <p>Il flusso di lavoro ideale:</p>
        <ol style="margin-left: -20px;">
            <li>Scarica i <b>Dettagli OdA</b>.</li>
            <li>Esegui lo <b>Scarico TS</b>.</li>
            <li>Verifica le <b>Timbrature</b>.</li>
            <li>Effettua il <b>Carico TS</b>.</li>
        </ol>
        """
        grid.addWidget(HelpCard("Workflow Ottimizzato", "🔄", workflow_html), 0, 1)

        # Card 3: Lyra AI
        lyra_html = """
        <p>Chiedi a <b>Lyra</b> di analizzare i dati per te.</p>
        <p>Usa il tasto destro su una riga e seleziona <i>"Analizza con Lyra"</i> per ottenere insight immediati.</p>
        """
        grid.addWidget(HelpCard("Intelligenza Artificiale", "✨", lyra_html), 1, 0)

        # Card 4: Supporto
        support_html = """
        <p>Hai bisogno di aiuto?</p>
        <p>Controlla la sezione <b>Impostazioni > Diagnostica</b> per visualizzare i log dettagliati e verificare la licenza.</p>
        """
        grid.addWidget(HelpCard("Supporto Tecnico", "🛠️", support_html), 1, 1)

        content_layout.addLayout(grid)
        content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
