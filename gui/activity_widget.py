from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QHBoxLayout, QMessageBox, QHeaderView)
from PySide6.QtGui import QAction, QKeySequence, QColor, QBrush
from PySide6.QtCore import Qt
from utils.database import init_db, insert_activity, get_all_activities, clear_activities, reset_all_status

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
        
        self.reset_status_btn = QPushButton("Reset Stati")
        self.reset_status_btn.clicked.connect(self.reset_status)
        self.reset_status_btn.setToolTip("Resetta tutti gli stati a 'da_processare'")

        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.paste_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.reset_status_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # Table - Prima colonna è Stato (non editabile), seconda è Data TS
        self.table = QTableWidget()
        self.columns = [
            "Stato",  # Prima colonna - non editabile
            "Data TS",  # Seconda colonna - prima editabile
            "Numero OdA", "Posizione OdA", "Codice Fiscale", "Ingresso", "Uscita",
            "Tipo Prestazione", "C", "M", "Str D", "Str N", "Str F D", "Str F N",
            "Sq", "Nota D", "Nota S", "F S", "G T"
        ]
        self.db_columns = [
            "stato",  # Prima colonna nel DB
            "data_ts",  # Seconda colonna nel DB
            "numero_oda", "posizione_oda", "codice_fiscale", "ingresso", "uscita",
            "tipo_prestazione", "c", "m", "str_d", "str_n", "str_f_d", "str_f_n",
            "sq", "nota_d", "nota_s", "f_s", "g_t"
        ]

        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # Imposta larghezza minima per colonna Stato
        self.table.setColumnWidth(0, 150)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def get_row_color(self, stato):
        """
        Ritorna il colore di sfondo basato sullo stato.
        - completato: verde con trasparenza
        - errore: rosso con trasparenza
        - da_processare: nessun colore
        """
        if stato == "completato":
            return QColor(76, 175, 80, 80)  # Verde con trasparenza (alpha=80)
        elif stato and stato.startswith("errore"):
            return QColor(244, 67, 54, 80)  # Rosso con trasparenza (alpha=80)
        else:
            return None  # Nessun colore (default)

    def load_data(self):
        self.table.setRowCount(0)
        rows = get_all_activities()
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            # Ottieni lo stato per determinare il colore della riga
            stato = row["stato"] if row["stato"] else "da_processare"
            row_color = self.get_row_color(stato)
            
            for j, db_col in enumerate(self.db_columns):
                val = str(row[db_col]) if row[db_col] is not None else ""
                item = QTableWidgetItem(val)
                
                # Prima colonna (Stato) non è mai editabile
                if j == 0:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                else:
                    item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                
                # Applica il colore di sfondo se necessario
                if row_color:
                    item.setBackground(QBrush(row_color))
                
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
            # L'utente copia le colonne SENZA lo stato (che viene gestito automaticamente)
            # Quindi le colonne dalla clipboard sono: data_ts, numero_oda, posizione_oda, codice_fiscale, ecc.
            db_columns_without_stato = [
                "data_ts", "numero_oda", "posizione_oda", "codice_fiscale", "ingresso", "uscita",
                "tipo_prestazione", "c", "m", "str_d", "str_n", "str_f_d", "str_f_n",
                "sq", "nota_d", "nota_s", "f_s", "g_t"
            ]
            
            count = 0
            for row_str in rows:
                cols = row_str.split('\t')

                # Create a dict for insertion
                data = {}
                # Lo stato viene impostato automaticamente a 'da_processare'
                data["stato"] = "da_processare"
                
                # Map clipboard columns to DB columns by index (escludendo stato)
                for idx, db_col in enumerate(db_columns_without_stato):
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

    def reset_status(self):
        reply = QMessageBox.question(self, "Conferma", "Vuoi resettare tutti gli stati a 'da_processare'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            reset_all_status()
            self.load_data()

    def gui_clipboard(self):
        from PySide6.QtWidgets import QApplication
        return QApplication.clipboard()
