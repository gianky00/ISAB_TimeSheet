"""
Tabella dati con sorting, filtering e row styling, basata su ExcelTableWidget.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QHeaderView, QTableWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QBrush
# Use explicit import from old_widgets to avoid circular dependency via src.gui.widgets
from src.gui.old_widgets import ExcelTableWidget
from ..design.colors import get_palette
from ..design.spacing import Spacing

class DataTable(QWidget):
    """Tabella dati con funzionalità avanzate (search, refresh) che wrappa ExcelTableWidget."""

    rowDoubleClicked = pyqtSignal(int, dict)  # row_index, row_data

    # Status colors
    STATUS_COLORS = {
        "completato": "#C8E6C9",    # Green
        "errore": "#FFCDD2",        # Red
        "in_corso": "#FFF9C4",      # Yellow
        "pending": "#E3F2FD",       # Blue
        "da_processare": "#FFFFFF", # White
    }

    def __init__(self, columns: list[dict], parent=None):
        """
        Args:
            columns: Lista di dict con keys: 'name', 'key', 'width', 'editable'
        """
        super().__init__(parent)
        self._columns = columns
        self._data = []
        self._palette = get_palette()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.xs)

        # Toolbar
        toolbar = QHBoxLayout()

        # Search
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("🔍 Cerca...")
        self._search_input.setClearButtonEnabled(True)
        self._search_input.textChanged.connect(self._filter_rows)
        # Apply modern style
        self._search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self._palette.border};
                border-radius: 6px;
                padding: 6px 10px;
                background: {self._palette.surface};
            }}
            QLineEdit:focus {{
                border: 2px solid {self._palette.primary};
            }}
        """)
        toolbar.addWidget(self._search_input, 1)

        # Actions
        self._refresh_btn = QPushButton("↻ Aggiorna")
        self._refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._refresh_btn.clicked.connect(lambda: self.refresh())
        self._refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._palette.surface};
                border: 1px solid {self._palette.border};
                border-radius: 6px;
                padding: 6px 12px;
                color: {self._palette.on_surface};
            }}
            QPushButton:hover {{
                background-color: {self._palette.hover};
            }}
        """)
        toolbar.addWidget(self._refresh_btn)

        layout.addLayout(toolbar)

        # Table (ExcelTableWidget)
        self._table = ExcelTableWidget()
        self._table.setColumnCount(len(self._columns))
        self._table.setHorizontalHeaderLabels([c['name'] for c in self._columns])
        # ExcelTableWidget handles SelectionBehavior and SelectionMode already
        self._table.setAlternatingRowColors(True)
        self._table.setSortingEnabled(True)
        self._table.doubleClicked.connect(self._on_double_click)

        # Header sizing
        header = self._table.horizontalHeader()
        for i, col in enumerate(self._columns):
            if 'width' in col:
                self._table.setColumnWidth(i, col['width'])
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        self._apply_table_style()
        layout.addWidget(self._table)

    def _apply_table_style(self):
        p = self._palette
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {p.surface};
                alternate-background-color: {p.surface_variant};
                gridline-color: {p.divider};
                border: 1px solid {p.border};
                border-radius: 8px;
                selection-background-color: {p.primary}33; /* 20% opacity approx */
                selection-color: {p.on_surface};
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
            }}
            QTableWidget::item:focus {{
                background-color: {p.primary}33;
                color: {p.on_surface};
            }}
            QHeaderView::section {{
                background-color: {p.surface_variant};
                padding: 10px;
                border: none;
                border-bottom: 2px solid {p.primary};
                font-weight: 600;
            }}
        """)

    def setData(self, data: list[dict]):
        """Popola la tabella con dati."""
        self._data = data
        self._populate_table(data)

    def _populate_table(self, data: list[dict]):
        self._table.setSortingEnabled(False) # Optimization
        self._table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            # Determina colore riga basato su stato
            status = str(row_data.get('stato', '')).lower()
            row_color = self._get_row_color(status)

            for col_idx, col in enumerate(self._columns):
                key = col.get('key', col['name'].lower())
                value = str(row_data.get(key, ''))

                item = QTableWidgetItem(value)

                # Editabilità
                if not col.get('editable', True):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                # Colore sfondo (ExcelTableWidget uses specific logic but we override it here if needed)
                if row_color:
                    item.setBackground(QBrush(QColor(row_color)))
                    item.setForeground(QBrush(QColor("black"))) # Force contrast

                self._table.setItem(row_idx, col_idx, item)

        self._table.setSortingEnabled(True)

    def _get_row_color(self, status: str) -> str | None:
        if status in self.STATUS_COLORS:
            return self.STATUS_COLORS[status]
        # Check prefix
        for key, color in self.STATUS_COLORS.items():
            if status.startswith(key):
                return color
        return None

    def _filter_rows(self, text: str):
        """Filtra righe in base al testo di ricerca."""
        text = text.lower()
        for row in range(self._table.rowCount()):
            match = False
            for col in range(self._table.columnCount()):
                item = self._table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
            self._table.setRowHidden(row, not match)

    def _on_double_click(self, index):
        row = index.row()
        if 0 <= row < len(self._data):
            self.rowDoubleClicked.emit(row, self._data[row])

    def getSelectedRows(self) -> list[dict]:
        """Ritorna i dati delle righe selezionate."""
        rows = set()
        for item in self._table.selectedItems():
            rows.add(item.row())
        # Map table row back to data index?
        # CAUTION: If sorted, index.row() refers to visual row.
        # We need to get the item and find it in data?
        # Or better: construct dict from the table row content since it matches `columns`

        selected_data = []
        for r in rows:
            row_dict = {}
            for c, col in enumerate(self._columns):
                item = self._table.item(r, c)
                key = col.get('key', col['name'].lower())
                row_dict[key] = item.text() if item else ""
            selected_data.append(row_dict)

        return selected_data

    def refresh(self):
        """Ricarica dati (da sovrascrivere o connettere)."""
        pass

    def get_table_widget(self):
        """Returns the internal ExcelTableWidget."""
        return self._table
