"""
Bot TS - GUI Widgets
Widget personalizzati riutilizzabili.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMenu, 
    QTextEdit, QFrame, QAbstractItemView, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QAction


class EditableDataTable(QWidget):
    """Tabella editabile con menu contestuale."""
    
    data_changed = pyqtSignal()
    
    def __init__(self, columns: list, parent=None):
        """
        Inizializza la tabella.
        
        Args:
            columns: Lista di dict con 'name' e 'type' per ogni colonna
        """
        super().__init__(parent)
        self.columns = columns
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura l'interfaccia."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tabella
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([c['name'] for c in self.columns])
        
        # Stile
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                gridline-color: #e9ecef;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                padding-left: 5px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # Configurazione header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Menu contestuale
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        
        # Traccia modifiche
        self.table.itemChanged.connect(self._on_item_changed)
        
        # Aggiungi una riga vuota iniziale
        self._add_row()
        
        layout.addWidget(self.table)
    
    def _show_context_menu(self, position):
        """Mostra il menu contestuale."""
        menu = QMenu()
        
        add_action = QAction("➕ Aggiungi riga", self)
        add_action.triggered.connect(self._add_row)
        menu.addAction(add_action)
        
        add_above_action = QAction("⬆️ Aggiungi riga sopra", self)
        add_above_action.triggered.connect(self._add_row_above)
        menu.addAction(add_above_action)
        
        menu.addSeparator()
        
        remove_action = QAction("🗑️ Rimuovi riga", self)
        remove_action.triggered.connect(self._remove_row)
        menu.addAction(remove_action)
        
        clear_action = QAction("🧹 Pulisci tutto", self)
        clear_action.triggered.connect(self._clear_all)
        menu.addAction(clear_action)
        
        menu.exec(self.table.viewport().mapToGlobal(position))
    
    def _add_row(self):
        """Aggiunge una riga alla fine."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self._populate_row(row)
        self.data_changed.emit()
    
    def _add_row_above(self):
        """Aggiunge una riga sopra quella selezionata."""
        current_row = self.table.currentRow()
        if current_row < 0:
            current_row = 0
        
        self.table.insertRow(current_row)
        self._populate_row(current_row)
        self.data_changed.emit()

    def _populate_row(self, row: int):
        """Popola una riga con widget o item di default."""
        for col, column in enumerate(self.columns):
            col_type = column.get('type', 'text')

            if col_type == 'combo':
                # Setup ComboBox
                combo = QComboBox()
                combo.setStyleSheet("border: none; background: transparent;")
                options = column.get('options', [])
                combo.addItems(options)

                # Seleziona default se presente
                default_val = column.get('default', "")
                if default_val and default_val in options:
                    combo.setCurrentText(default_val)

                # Collega segnale modifica
                combo.currentTextChanged.connect(lambda text: self.data_changed.emit())

                self.table.setCellWidget(row, col, combo)
            else:
                # Standard Text Item
                default_val = column.get('default', "")
                item = QTableWidgetItem(str(default_val))
                self.table.setItem(row, col, item)
    
    def _remove_row(self):
        """Rimuove la riga selezionata."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
            self.data_changed.emit()
    
    def _clear_all(self):
        """Pulisce tutte le righe."""
        self.table.setRowCount(0)
        self._add_row()  # Mantieni almeno una riga
        self.data_changed.emit()
    
    def _on_item_changed(self, item):
        """Chiamato quando un item viene modificato."""
        self.data_changed.emit()
    
    def get_data(self) -> list:
        """
        Restituisce i dati della tabella.
        
        Returns:
            Lista di dict con i dati di ogni riga
        """
        data = []
        for row in range(self.table.rowCount()):
            row_data = {}
            has_data = False
            
            for col, column in enumerate(self.columns):
                key = column['name'].lower().replace(' ', '_')

                # Gestione ComboBox vs Item
                widget = self.table.cellWidget(row, col)
                if isinstance(widget, QComboBox):
                    value = widget.currentText()
                else:
                    item = self.table.item(row, col)
                    value = item.text() if item else ""

                row_data[key] = value
                
                if value:
                    has_data = True
            
            # Aggiungi solo righe con almeno un dato
            if has_data:
                data.append(row_data)
        
        return data
    
    def set_data(self, data: list):
        """
        Imposta i dati della tabella.
        
        Args:
            data: Lista di dict con i dati
        """
        # Blocca segnali durante il caricamento
        self.table.blockSignals(True)
        
        self.table.setRowCount(0)
        
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._populate_row(row) # Crea i widget se necessario
            
            for col, column in enumerate(self.columns):
                key = column['name'].lower().replace(' ', '_')
                value = row_data.get(key, "")

                widget = self.table.cellWidget(row, col)
                if isinstance(widget, QComboBox):
                    if value:
                        # Se il valore non è nelle opzioni, lo aggiungiamo temporaneamente?
                        # O assumiamo sia corretto. Per sicurezza controlliamo index.
                        idx = widget.findText(str(value))
                        if idx >= 0:
                            widget.setCurrentIndex(idx)
                        else:
                            # Opzionale: aggiungi e seleziona
                            widget.addItem(str(value))
                            widget.setCurrentText(str(value))
                else:
                    item = self.table.item(row, col)
                    if item:
                        item.setText(str(value))
        
        # Se non ci sono dati, aggiungi una riga vuota
        if self.table.rowCount() == 0:
            self._add_row()
        
        self.table.blockSignals(False)

    def update_column_options(self, column_name: str, new_options: list):
        """Aggiorna le opzioni per una colonna di tipo combo."""
        # 1. Aggiorna definizione colonna
        target_col_idx = -1
        for i, col in enumerate(self.columns):
            if col['name'] == column_name:
                col['options'] = new_options
                target_col_idx = i
                break

        if target_col_idx == -1:
            return

        # 2. Aggiorna widget esistenti
        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, target_col_idx)
            if isinstance(widget, QComboBox):
                current_text = widget.currentText()
                widget.clear()
                widget.addItems(new_options)

                # Tenta di ripristinare il valore
                if current_text in new_options:
                    widget.setCurrentText(current_text)
                elif new_options:
                    # Se il vecchio valore non esiste più, metti il primo o lascia vuoto?
                    # Meglio lasciare il vecchio valore se non è nella lista?
                    # QComboBox non modificabile non lo permette.
                    # Se è modificabile sì. Qui assumiamo non modificabile strict.
                    # Se non trovato, mettiamo il primo.
                    widget.setCurrentIndex(0)
        self.table.blockSignals(False)


class LogWidget(QWidget):
    """Widget per visualizzare i log."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura l'interfaccia."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        
        label = QLabel("📋 Log")
        label.setStyleSheet("font-weight: bold; font-size: 13px;")
        header_layout.addWidget(label)
        
        header_layout.addStretch()
        
        clear_btn = QPushButton("🧹 Pulisci")
        clear_btn.setMaximumWidth(80)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        clear_btn.clicked.connect(self.clear)
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # Text area per i log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(150)
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #333;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.log_text)
    
    def append(self, message: str):
        """
        Aggiunge un messaggio al log.
        
        Args:
            message: Messaggio da aggiungere
        """
        # Colora in base al tipo di messaggio
        if "✓" in message or "successo" in message.lower():
            color = "#4ec9b0"  # Verde
        elif "✗" in message or "errore" in message.lower():
            color = "#f14c4c"  # Rosso
        elif "⚠" in message or "avviso" in message.lower():
            color = "#dcdcaa"  # Giallo
        elif "▶" in message:
            color = "#569cd6"  # Blu
        else:
            color = "#d4d4d4"  # Default
        
        self.log_text.append(f'<span style="color: {color};">{message}</span>')
        
        # Scroll automatico
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear(self):
        """Pulisce il log."""
        self.log_text.clear()


class StatusIndicator(QWidget):
    """Indicatore di stato con animazione."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._status = "idle"
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura l'interfaccia."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Indicatore colorato
        self.indicator = QFrame()
        self.indicator.setFixedSize(12, 12)
        self.indicator.setStyleSheet("""
            QFrame {
                background-color: #6c757d;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.indicator)
        
        # Testo stato
        self.status_label = QLabel("In attesa")
        self.status_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def set_status(self, status: str):
        """
        Imposta lo stato.
        
        Args:
            status: idle, running, completed, error, stopped
        """
        self._status = status
        
        status_config = {
            "idle": ("#6c757d", "In attesa"),
            "running": ("#ffc107", "In esecuzione..."),
            "completed": ("#28a745", "Completato"),
            "error": ("#dc3545", "Errore"),
            "stopped": ("#fd7e14", "Interrotto")
        }
        
        color, text = status_config.get(status, ("#6c757d", "Sconosciuto"))
        
        self.indicator.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 6px;
            }}
        """)
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: bold;")
