"""
Bot TS - GUI Widgets
Widget personalizzati riutilizzabili.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMenu, 
    QTextEdit, QFrame, QAbstractItemView, QComboBox, QApplication,
    QToolTip, QGraphicsOpacityEffect, QDateEdit, QDialog, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QAbstractAnimation, QPoint
from PyQt6.QtGui import QColor, QAction, QKeySequence, QCursor, QPainter, QBrush


class StatusIndicator(QWidget):
    """
    Indicatore di stato circolare con animazione di pulsazione.
    Stati supportati: 'idle', 'running', 'success', 'error'.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)

        # Configurazione animazione pulsazione (opacità)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)  # 1 secondo per ciclo
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.4)
        self.animation.setLoopCount(-1)  # Infinito
        # Effetto yo-yo: 1.0 -> 0.4 -> 1.0
        self.animation.setKeyValueAt(0.0, 1.0)
        self.animation.setKeyValueAt(0.5, 0.4)
        self.animation.setKeyValueAt(1.0, 1.0)

        self.current_color = QColor("#6c757d")  # Grigio (Idle)
        self.setToolTip("Pronto")

    def set_status(self, status: str, message: str = ""):
        """
        Imposta lo stato e il tooltip.

        Args:
            status: 'idle', 'running', 'success', 'error'
            message: Messaggio per il tooltip
        """
        self.setToolTip(message)

        if status == 'running':
            self.current_color = QColor("#0d6efd")  # Blu
            if self.animation.state() == QAbstractAnimation.State.Stopped:
                self.animation.start()
        elif status == 'success':
            self.current_color = QColor("#198754")  # Verde
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)
        elif status == 'error':
            self.current_color = QColor("#dc3545")  # Rosso
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)
        else:  # idle
            self.current_color = QColor("#6c757d")  # Grigio
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)

        self.update()  # Forza repaint

    def paintEvent(self, event):
        """Disegna il cerchio colorato."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.current_color))
        painter.setPen(Qt.PenStyle.NoPen)

        # Disegna cerchio centrato con margine
        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawEllipse(rect)


class CalendarDateEdit(QDateEdit):
    """QDateEdit con popup calendario e stile personalizzato."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setMinimumWidth(150)
        self.setStyleSheet("""
            QDateEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 14px;
                background-color: white;
            }
            QDateEdit:focus {
                border-color: #0d6efd;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: #ced4da;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QDateEdit::down-arrow {
                image: none; /* Fallback to standard arrow */
                width: 16px;
                height: 16px;
            }
        """)


class ExcelTableWidget(QTableWidget):
    """QTableWidget potenziato con funzionalità copia stile Excel."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Abilita la selezione di intere righe ma permettendo selezioni multiple
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def keyPressEvent(self, event):
        """Gestisce la pressione dei tasti, in particolare CTRL+C."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection()
        else:
            super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        """Menu contestuale predefinito per copia veloce (per tabelle read-only)."""
        menu = QMenu(self)

        # Action: Analyze ROW with Lyra
        # This is context-aware for the specific row clicked
        lyra_row_action = QAction("✨ Analizza Riga con Lyra", self)
        lyra_row_action.triggered.connect(lambda: self._analyze_row_at(event.pos()))
        menu.addAction(lyra_row_action)

        lyra_selection_action = QAction("✨ Analizza Selezione con Lyra", self)
        lyra_selection_action.triggered.connect(self._analyze_selection)
        menu.addAction(lyra_selection_action)

        menu.addSeparator()

        copy_action = QAction("📋 Copia", self)
        copy_action.triggered.connect(self.copy_selection)
        menu.addAction(copy_action)
        menu.exec(event.globalPos())

    def _analyze_row_at(self, pos):
        """Analizza la riga specifica sotto il cursore."""
        item = self.itemAt(pos)
        if not item: return
        row = item.row()

        row_data = []
        for c in range(self.columnCount()):
            if not self.isColumnHidden(c):
                header = self.horizontalHeaderItem(c).text() if self.horizontalHeaderItem(c) else f"Col {c}"
                # Handle cell widgets (combos) or text items
                widget = self.cellWidget(row, c)
                if isinstance(widget, QComboBox):
                    text = widget.currentText()
                else:
                    it = self.item(row, c)
                    text = it.text() if it else ""

                row_data.append(f"**{header}**: {text}")

        context = " | ".join(row_data)

        # Call Main Window
        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra(context)

    def _analyze_selection(self):
        """Invia la selezione a Lyra."""
        selection = self.selectedRanges()
        if not selection: return

        # Estrai testo
        rows_text = []
        for r in range(selection[0].topRow(), selection[0].bottomRow() + 1):
            row_data = []
            for c in range(self.columnCount()):
                item = self.item(r, c)
                if item and not self.isColumnHidden(c):
                    row_data.append(f"{self.horizontalHeaderItem(c).text()}: {item.text()}")
            rows_text.append(" | ".join(row_data))

        context = "\n".join(rows_text)

        # Chiamata alla Main Window (metodo dinamico)
        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra(context)

    def copy_selection(self):
        """Copia la selezione negli appunti in formato compatibile con Excel."""
        selection = self.selectedRanges()
        if not selection:
            # Fallback: se ci sono item selezionati ma non un range completo (es. celle singole)
            items = self.selectedItems()
            if not items:
                return
            # Se ci sono item selezionati, usiamo una logica diversa o semplicemente copiamo
            # Per ora supportiamo Ranges (che è il default per selezione utente via mouse/shift)
            return

        # Determina i limiti della selezione
        rows = sorted(list(set(r for range_ in selection for r in range(range_.topRow(), range_.bottomRow() + 1))))
        cols = sorted(list(set(c for range_ in selection for c in range(range_.leftColumn(), range_.rightColumn() + 1))))

        if not rows or not cols:
            return

        tsv_rows = []
        for r in rows:
            # Non copiare le righe nascoste (es. se filtrate)
            if self.isRowHidden(r):
                continue

            row_data = []
            for c in cols:
                # Controlla se c'è un widget (es. ComboBox)
                widget = self.cellWidget(r, c)
                if isinstance(widget, QComboBox):
                    text = widget.currentText()
                else:
                    item = self.item(r, c)
                    text = item.text() if item else ""

                # Escape per Excel se necessario (es. tab o newline nel testo)
                text = text.replace('\t', ' ').replace('\n', ' ')
                row_data.append(text)
            tsv_rows.append("\t".join(row_data))

        if tsv_rows:
            tsv_data = "\n".join(tsv_rows)
            QApplication.clipboard().setText(tsv_data)
            # Visual feedback
            QToolTip.showText(QCursor.pos(), "✨ Copiato!", self)


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
        
        # Tabella (Usa ExcelTableWidget invece di QTableWidget)
        self.table = ExcelTableWidget()
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

        lyra_action = QAction("✨ Analizza con Lyra", self)
        lyra_action.triggered.connect(self.table._analyze_selection)
        menu.addAction(lyra_action)
        menu.addSeparator()

        copy_action = QAction("📋 Copia", self)
        copy_action.triggered.connect(self.table.copy_selection)
        menu.addAction(copy_action)
        menu.addSeparator()
        
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
                # Fix colore testo bianco su sfondo bianco
                combo.setStyleSheet("""
                    QComboBox {
                        border: none;
                        background: transparent;
                        color: black;
                        padding-left: 5px;
                    }
                    QComboBox QAbstractItemView {
                        background-color: white;
                        color: black;
                        selection-background-color: #e7f1ff;
                        selection-color: #0d6efd;
                    }
                    /* Forza il colore del testo nero anche durante l'hover/selezione */
                    QComboBox QAbstractItemView::item:hover {
                        background-color: #e7f1ff;
                        color: black;
                    }
                    QComboBox QAbstractItemView::item:selected {
                        background-color: #e7f1ff;
                        color: black;
                    }
                """)
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


class DetailedInfoDialog(QDialog):
    """Dialogo modale per spiegazioni dettagliate KPI."""
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dettaglio KPI")
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setFixedWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 2px solid #0d6efd;
                border-radius: 8px;
            }
            QLabel {
                color: #212529;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)

        # Title
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #0d6efd; margin-bottom: 10px;")
        layout.addWidget(lbl_title)

        # Content (HTML)
        lbl_content = QLabel(content)
        lbl_content.setWordWrap(True)
        lbl_content.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(lbl_content)

        # Close info
        lbl_close = QLabel("\n(Clicca per chiudere)")
        lbl_close.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_close.setStyleSheet("color: #adb5bd; font-size: 11px;")
        layout.addWidget(lbl_close)

    def mousePressEvent(self, event):
        self.accept()


class InfoLabel(QLabel):
    """Etichetta informativa con icona che apre un popup al click."""
    def __init__(self, title, get_text_callback, parent=None):
        super().__init__("ⓘ", parent)
        self.title = title
        self.get_text_callback = get_text_callback # Funzione che restituisce il testo aggiornato
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-weight: bold;
                font-size: 16px;
                background: transparent;
                padding: 0px 5px;
            }
            QLabel:hover {
                color: #0d6efd;
            }
        """)

    def mousePressEvent(self, event):
        """Mostra il dialog con il testo aggiornato, posizionato in modo intelligente."""
        content = self.get_text_callback() if callable(self.get_text_callback) else str(self.get_text_callback)
        dlg = DetailedInfoDialog(self.title, content, self.window())

        # Smart Positioning Logic
        cursor_pos = event.globalPosition().toPoint()
        screen = QApplication.screenAt(cursor_pos)

        if screen:
            screen_geo = screen.availableGeometry()
            dlg_width = dlg.width()
            dlg_height = dlg.sizeHint().height() # approssimato, il layout non è ancora calcolato

            # Calcola posizione X
            x = cursor_pos.x()
            # Se il dialog esce a destra dello schermo, spostalo a sinistra del cursore
            if x + dlg_width > screen_geo.right():
                x = cursor_pos.x() - dlg_width - 10 # 10px di margine
            else:
                x = cursor_pos.x() + 10 # 10px offset standard

            # Calcola posizione Y (evita di uscire sotto)
            y = cursor_pos.y()
            if y + dlg_height > screen_geo.bottom():
                y = cursor_pos.y() - dlg_height - 10
            else:
                y = cursor_pos.y() + 10

            dlg.move(x, y)
        else:
            # Fallback se screen non trovato
            dlg.move(cursor_pos)

        dlg.exec()


class KPIBigCard(QFrame):
    """Card per mostrare un KPI numerico principale."""
    def __init__(self, title, value, color="#0d6efd", parent=None, subtitle=None):
        super().__init__(parent)
        self.info_content_callback = lambda: "Nessuna informazione disponibile."

        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }}
        """)
        self.setMinimumWidth(200)
        self.setMinimumHeight(120)

        # Effetto ombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)

        # Header Layout (Title + Info Icon)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #6c757d; font-size: 13px; font-weight: bold; border: none; background: transparent;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(lbl_title)

        header_layout.addStretch()

        # Info Icon che chiama self.get_info_content
        self.info_icon = InfoLabel(title, self._get_info_content)
        header_layout.addWidget(self.info_icon)

        layout.addLayout(header_layout)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: 800; border: none; background: transparent;")
        self.lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_value)

        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setStyleSheet("color: #adb5bd; font-size: 11px; border: none; background: transparent;")
            lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_sub)

    def set_info_callback(self, callback):
        """Imposta la funzione per generare il testo informativo."""
        self.info_content_callback = callback

    def _get_info_content(self):
        return self.info_content_callback()
