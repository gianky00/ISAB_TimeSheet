"""
Bot TS - Help Panel
Pannello Guida e Scorciatoie.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, QHeaderView,
    QTableWidgetItem, QLabel, QFrame
)
from PyQt6.QtCore import Qt

class HelpPanel(QWidget):
    """Pannello principale per la Guida."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                padding: 20px;
            }
        """)
        header_layout = QVBoxLayout(header)

        title = QLabel("📚 Guida")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)

        desc = QLabel("Manuale utente e riferimenti rapidi")
        desc.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 16px;")
        header_layout.addWidget(desc)

        layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
            }
            QTabBar::tab {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 10px 20px;
                margin-right: 2px;
                color: #495057;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #0d6efd;
            }
        """)

        # Tab Scorciatoie
        self.shortcuts_tab = self._create_shortcuts_tab()
        self.tabs.addTab(self.shortcuts_tab, "⌨️ Scorciatoie")

        layout.addWidget(self.tabs)

    def _create_shortcuts_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Tasto / Combinazione", "Azione"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #e9ecef;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

        shortcuts = [
            ("F5", "Aggiorna i dati o avvia l'operazione corrente"),
            ("Ctrl + F", "Attiva la barra di ricerca (se disponibile)"),
            ("Ctrl + S", "Salva le impostazioni (se nel pannello Impostazioni)"),
            ("Ctrl + C", "Copia le righe selezionate nelle tabelle"),
            ("Ctrl + A", "Seleziona tutte le righe nelle tabelle")
        ]

        table.setRowCount(len(shortcuts))
        for i, (keys, desc) in enumerate(shortcuts):
            k_item = QTableWidgetItem(keys)
            k_item.setFont(self.font()) # Reset font
            k_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            k_item.setBackground(Qt.GlobalColor.white)

            # Badge style for keys
            # Can't style single item easily with CSS badge, so just text for now.
            # Maybe bold?
            f = k_item.font()
            f.setBold(True)
            k_item.setFont(f)

            d_item = QTableWidgetItem(desc)

            table.setItem(i, 0, k_item)
            table.setItem(i, 1, d_item)

        layout.addWidget(table)
        return widget
