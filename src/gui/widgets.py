"""
Bot TS - GUI Widgets
Widget riutilizzabili per l'interfaccia grafica.
"""
from typing import List, Dict, Any, Optional, Callable
from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QMenu, QHeaderView, QStyledItemDelegate,
    QStyleOptionViewItem, QComboBox, QSpinBox, QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal, QModelIndex
from PyQt6.QtGui import QPainter, QColor, QBrush, QAction


class HoverRowDelegate(QStyledItemDelegate):
    """Delegate per evidenziare la riga al passaggio del mouse."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hover_row = -1
    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        # Highlight row on hover
        if index.row() == self.hover_row:
            painter.save()
            painter.fillRect(option.rect, QColor(52, 73, 94, 40))
            painter.restore()
        
        super().paint(painter, option, index)
    
    def set_hover_row(self, row: int):
        self.hover_row = row


class EditableDataTable(QWidget):
    """
    Tabella dati editabile con menu contestuale.
    
    Features:
    - NO pulsanti esterni per aggiungi/rimuovi
    - Tasto destro per menu contestuale
    - Aggiungi riga, Inserisci sopra/sotto, Duplica, Elimina
    - Hover highlight sulla riga
    - Auto-save su modifica
    """
    
    data_changed = pyqtSignal(list)  # Emitted when data changes
    
    def __init__(
        self,
        columns: List[Dict[str, str]],
        parent: Optional[QWidget] = None
    ):
        """
        Args:
            columns: Lista di dict con keys: name, type
                     type può essere: text, month, year
        """
        super().__init__(parent)
        # Normalize columns to have consistent keys
        self.columns = []
        for col in columns:
            name = col.get("name", col.get("label", ""))
            key = col.get("key", name.lower().replace(" ", "_"))
            self.columns.append({
                "name": name,
                "key": key,
                "type": col.get("type", "text")
            })
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([c["name"] for c in self.columns])
        
        # Styling
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        # Enable mouse tracking for hover effect
        self.table.setMouseTracking(True)
        self.table.viewport().setMouseTracking(True)
        
        # Delegate for hover
        self.delegate = HoverRowDelegate(self.table)
        self.table.setItemDelegate(self.delegate)
        
        # Context menu
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        
        # Connect signals
        self.table.cellChanged.connect(self._on_cell_changed)
        self.table.cellEntered.connect(self._on_cell_entered)
        
        # Style - Light Theme
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                color: #333333;
                gridline-color: #dee2e6;
                border: 1px solid #dee2e6;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
            QTableWidget::item:selected {
                background-color: #0d6efd;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: rgba(13, 110, 253, 0.1);
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #495057;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #0d6efd;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)
        
        # Hint label
        hint = QLabel("💡 Tasto destro per aggiungere/rimuovere righe")
        hint.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                font-style: italic;
                padding: 4px;
            }
        """)
        hint.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(hint)
        
        # Start with one empty row
        self._add_row()
    
    def _on_cell_entered(self, row: int, column: int):
        """Aggiorna l'evidenziazione al passaggio del mouse."""
        self.delegate.set_hover_row(row)
        self.table.viewport().update()
    
    def _on_cell_changed(self, row: int, column: int):
        """Emette il segnale data_changed quando una cella viene modificata."""
        self.data_changed.emit(self.get_data())
    
    def _show_context_menu(self, position):
        """Mostra il menu contestuale."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #0d6efd;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background-color: #dee2e6;
                margin: 4px 8px;
            }
        """)
        
        # Get clicked row
        index = self.table.indexAt(position)
        current_row = index.row() if index.isValid() else -1
        
        # Actions
        add_action = QAction("➕ Aggiungi riga", self)
        add_action.triggered.connect(self._add_row)
        menu.addAction(add_action)
        
        if current_row >= 0:
            menu.addSeparator()
            
            insert_above = QAction("⬆️ Inserisci sopra", self)
            insert_above.triggered.connect(lambda: self._insert_row(current_row))
            menu.addAction(insert_above)
            
            insert_below = QAction("⬇️ Inserisci sotto", self)
            insert_below.triggered.connect(lambda: self._insert_row(current_row + 1))
            menu.addAction(insert_below)
            
            duplicate = QAction("📋 Duplica", self)
            duplicate.triggered.connect(lambda: self._duplicate_row(current_row))
            menu.addAction(duplicate)
            
            menu.addSeparator()
            
            delete_action = QAction("🗑️ Elimina", self)
            delete_action.triggered.connect(lambda: self._delete_row(current_row))
            menu.addAction(delete_action)
        
        menu.exec(self.table.viewport().mapToGlobal(position))
    
    def _add_row(self):
        """Aggiunge una riga vuota alla fine."""
        self.table.blockSignals(True)
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        for col, col_info in enumerate(self.columns):
            item = QTableWidgetItem("")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col, item)
        
        self.table.blockSignals(False)
        self.data_changed.emit(self.get_data())
    
    def _insert_row(self, at_row: int):
        """Inserisce una riga vuota alla posizione specificata."""
        self.table.blockSignals(True)
        self.table.insertRow(at_row)
        
        for col, col_info in enumerate(self.columns):
            item = QTableWidgetItem("")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(at_row, col, item)
        
        self.table.blockSignals(False)
        self.data_changed.emit(self.get_data())
    
    def _duplicate_row(self, row: int):
        """Duplica la riga specificata."""
        if row < 0 or row >= self.table.rowCount():
            return
        
        self.table.blockSignals(True)
        new_row = row + 1
        self.table.insertRow(new_row)
        
        for col in range(self.table.columnCount()):
            original_item = self.table.item(row, col)
            text = original_item.text() if original_item else ""
            new_item = QTableWidgetItem(text)
            new_item.setFlags(new_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(new_row, col, new_item)
        
        self.table.blockSignals(False)
        self.data_changed.emit(self.get_data())
    
    def _delete_row(self, row: int):
        """Elimina la riga specificata."""
        if row < 0 or row >= self.table.rowCount():
            return
        
        # Keep at least one row
        if self.table.rowCount() <= 1:
            # Clear the row instead of deleting
            self.table.blockSignals(True)
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setText("")
            self.table.blockSignals(False)
        else:
            self.table.removeRow(row)
        
        self.data_changed.emit(self.get_data())
    
    def get_data(self) -> List[Dict[str, str]]:
        """Restituisce i dati della tabella."""
        data = []
        for row in range(self.table.rowCount()):
            row_data = {}
            has_data = False
            
            for col, col_info in enumerate(self.columns):
                item = self.table.item(row, col)
                value = item.text().strip() if item else ""
                row_data[col_info["key"]] = value
                if value:
                    has_data = True
            
            if has_data:
                data.append(row_data)
        
        return data
    
    def set_data(self, data: List[Dict[str, str]]):
        """Imposta i dati della tabella."""
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        
        if not data:
            # Add one empty row
            self._add_row()
            self.table.blockSignals(False)
            return
        
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            for col, col_info in enumerate(self.columns):
                value = row_data.get(col_info["key"], "")
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
        
        self.table.blockSignals(False)
    
    def clear(self):
        """Pulisce la tabella."""
        self.table.setRowCount(0)
        self._add_row()


class LogWidget(QWidget):
    """Widget per la visualizzazione dei log."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("📋 Log")
        header.setStyleSheet("""
            QLabel {
                color: #495057;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 0;
            }
        """)
        layout.addWidget(header)
        
        # Log text area - Console style (dark background for readability)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00d26a;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.log_area)
    
    def append_log(self, message: str):
        """Aggiunge un messaggio al log."""
        self.log_area.append(message)
        # Scroll to bottom
        scrollbar = self.log_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def append(self, message: str):
        """Alias per append_log."""
        self.append_log(message)
    
    def clear(self):
        """Pulisce il log."""
        self.log_area.clear()


class StatusIndicator(QWidget):
    """Indicatore di stato con colore e testo."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Status dot
        self.dot = QLabel("●")
        self.dot.setStyleSheet("color: #888888; font-size: 16px;")
        layout.addWidget(self.dot)
        
        # Status text
        self.text = QLabel("Pronto")
        self.text.setStyleSheet("color: #888888; font-size: 12px;")
        layout.addWidget(self.text)
        
        layout.addStretch()
    
    def set_status(self, status: str, color: str = None):
        """
        Imposta lo stato.
        
        Args:
            status: Codice stato (idle, running, completed, error, stopped) o testo libero
            color: Colore CSS (opzionale)
        """
        # Map status codes to text and colors
        status_map = {
            "idle": ("Pronto", "#6c757d"),
            "running": ("In esecuzione...", "#f39c12"),
            "completed": ("Completato", "#28a745"),
            "error": ("Errore", "#dc3545"),
            "stopped": ("Interrotto", "#fd7e14"),
        }
        
        if status.lower() in status_map:
            text, default_color = status_map[status.lower()]
            color = color or default_color
        else:
            text = status
            color = color or "#6c757d"
        
        self.dot.setStyleSheet(f"color: {color}; font-size: 16px;")
        self.text.setStyleSheet(f"color: {color}; font-size: 12px;")
        self.text.setText(text)
    
    def set_idle(self):
        self.set_status("idle")
    
    def set_running(self):
        self.set_status("running")
    
    def set_success(self):
        self.set_status("completed")
    
    def set_error(self):
        self.set_status("error")
    
    def set_stopped(self):
        self.set_status("stopped")
