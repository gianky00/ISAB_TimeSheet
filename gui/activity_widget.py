from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QHBoxLayout, QMessageBox, QHeaderView)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Qt
from utils.database import init_db, insert_activity, get_all_activities, clear_activities

class ActivityWidget(QWidget):
    def __init__(self):
        super().__init__()
        init_db()  # Ensure DB exists
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        # Toolbar / Buttons
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Aggiorna")
        self.refresh_btn.clicked.connect(self.load_data)

        self.paste_btn = QPushButton("Incolla da Excel (Clipboard)")
        self.paste_btn.clicked.connect(self.paste_from_clipboard)

        self.clear_btn = QPushButton("Svuota Database")
        self.clear_btn.clicked.connect(self.clear_database)

        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.paste_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # Table
        self.table = QTableWidget()
        self.columns = [
            "Numero OdA", "Posizione OdA", "Codice Fiscale", "Ingresso", "Uscita",
            "Tipo Prestazione", "C", "M", "Str D", "Str N", "Str F D", "Str F N",
            "Sq", "Nota D", "Nota S", "F S", "G T"
        ]
        self.db_columns = [
            "numero_oda", "posizione_oda", "codice_fiscale", "ingresso", "uscita",
            "tipo_prestazione", "c", "m", "str_d", "str_n", "str_f_d", "str_f_n",
            "sq", "nota_d", "nota_s", "f_s", "g_t"
        ]

        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self):
        self.table.setRowCount(0)
        rows = get_all_activities()
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            # row is a sqlite3.Row object
            for j, db_col in enumerate(self.db_columns):
                val = str(row[db_col]) if row[db_col] is not None else ""
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable) # Make read-only for now? Or editable? User didn't specify, but DB is source of truth.
                self.table.setItem(i, j, item)

    def paste_from_clipboard(self):
        clipboard = self.gui_clipboard()
        if not clipboard:
            return

        text = clipboard.text()
        if not text:
            return

        rows = text.strip().split('\n')
        if not rows:
            return

        try:
            # We assume the user copies columns in the exact order requested
            count = 0
            for row_str in rows:
                cols = row_str.split('\t')

                # Create a dict for insertion
                data = {}
                # Map clipboard columns to DB columns by index
                # If clipboard has fewer columns, fill with empty string
                for idx, db_col in enumerate(self.db_columns):
                    val = cols[idx].strip() if idx < len(cols) else ""
                    data[db_col] = val

                insert_activity(data)
                count += 1

            self.load_data()
            QMessageBox.information(self, "Importazione", f"Importate {count} righe con successo.")

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante l'incolla: {str(e)}")

    def clear_database(self):
        reply = QMessageBox.question(self, "Conferma", "Sei sicuro di voler cancellare tutto il database?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            clear_activities()
            self.load_data()

    def gui_clipboard(self):
        from PySide6.QtWidgets import QApplication
        return QApplication.clipboard()
