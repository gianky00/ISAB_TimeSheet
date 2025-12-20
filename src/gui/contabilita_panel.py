"""
Bot TS - Contabilita Panel
Pannello per la visualizzazione della Contabilità Strumentale.
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QMessageBox, QMenu, QTableWidget,
    QHeaderView, QTableWidgetItem, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QAction

from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.widgets import ExcelTableWidget, StatusIndicator


class ContabilitaWorker(QThread):
    """Worker per l'importazione in background."""
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        # Inizializza DB se necessario
        ContabilitaManager.init_db()
        success, msg = ContabilitaManager.import_data_from_excel(self.file_path)
        self.finished_signal.emit(success, msg)


class ContabilitaPanel(QWidget):
    """Pannello principale Contabilità Strumentale."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._setup_ui()

        # Carica i dati iniziali
        self.refresh_tabs()

    def _setup_ui(self):
        """Configura l'interfaccia."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Header / Status
        self.status_label = QLabel("Pronto")
        self.status_label.setStyleSheet("color: #6c757d; font-size: 13px;")
        layout.addWidget(self.status_label)

        # Tab Widget per gli anni
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
            }
            QTabBar::tab {
                background: #f1f3f5;
                border: 1px solid #dee2e6;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: #495057;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #0d6efd;
            }
        """)
        layout.addWidget(self.tabs)

    def refresh_tabs(self):
        """Ricarica i tab in base agli anni nel DB."""
        # Salva l'anno corrente selezionato per ripristinarlo
        current_year = self.tabs.tabText(self.tabs.currentIndex())

        self.tabs.clear()

        years = ContabilitaManager.get_available_years()
        if not years:
            # Se non ci sono dati, mostra un tab placeholder o vuoto
            no_data = QLabel("Nessun dato disponibile. Configura il file nelle impostazioni e riavvia/aggiorna.")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabs.addTab(no_data, "Info")
            return

        for year in years:
            tab = ContabilitaYearTab(year)
            self.tabs.addTab(tab, str(year))

        # Ripristina selezione
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == current_year:
                self.tabs.setCurrentIndex(i)
                break

    def start_import_process(self):
        """Avvia il processo di importazione (chiamato dall'esterno o init)."""
        config = config_manager.load_config()
        path = config.get("contabilita_file_path", "")

        if not path or not os.path.exists(path):
            self.status_label.setText("⚠️ File contabilità non configurato o non trovato.")
            return

        self.status_label.setText("🔄 Aggiornamento contabilità in corso...")

        self.worker = ContabilitaWorker(path)
        self.worker.finished_signal.connect(self._on_import_finished)
        self.worker.start()

    def _on_import_finished(self, success: bool, msg: str):
        if success:
            self.status_label.setText(f"✅ Aggiornamento completato: {msg}")
            self.refresh_tabs()
        else:
            self.status_label.setText(f"❌ Errore aggiornamento: {msg}")

        self.worker = None


class ContabilitaYearTab(QWidget):
    """Tab per un singolo anno."""

    COLUMNS = [
        'DATA PREV.', 'MESE', 'N°PREV.', 'TOTALE PREV.', "ATTIVITA'",
        'TCL', 'ODC', "STATO ATTIVITA'", 'TIPOLOGIA', 'ORE SP', 'RESA', 'ANNOTAZIONI'
    ]

    # Indici colonne nascoste nei dati ritornati dal manager
    # I dati dal manager sono: [Visible Cols...] + [Indirizzo, NomeFile]
    IDX_INDIRIZZO = 12
    IDX_NOMEFILE = 13

    def __init__(self, year: int, parent=None):
        super().__init__(parent)
        self.year = year
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        layout.addWidget(self.table)

    def _load_data(self):
        data = ContabilitaManager.get_data_by_year(self.year)
        self.table.setRowCount(0)

        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)

            # Popola colonne visibili
            for col_idx in range(len(self.COLUMNS)):
                val = row_data[col_idx]
                item = QTableWidgetItem(str(val))
                self.table.setItem(row_idx, col_idx, item)

            # Salva dati nascosti (Indirizzo, Nome File) come UserData nel primo item della riga
            indirizzo = row_data[self.IDX_INDIRIZZO]
            nome_file = row_data[self.IDX_NOMEFILE]

            # Costruiamo il full path se necessario, o usiamo solo indirizzo se è già full.
            # Richiesta: "INDIRIZZO CONSUNTIVO contiene il percorso... NOME FILE non li farai vedere...
            # utente clicca... aprire il file avendo l'indirizzo"
            # Assumiamo che Indirizzo sia il path completo o directory.
            # Dalla chat di chiarimento:
            # "INDIRIZZO CONSUNTIVO contiene: \\192.168.11.251\...\file.xlsm" (quindi FULL PATH)
            # Quindi usiamo quello.

            self.table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, indirizzo)

    def _show_context_menu(self, pos):
        """Mostra menu contestuale."""
        item = self.table.itemAt(pos)
        if not item:
            return

        row = item.row()
        # Recupera il path dal primo item della riga
        first_item = self.table.item(row, 0)
        file_path = first_item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu(self)

        action_open = QAction("📂 Apri File", self)

        if file_path:
             action_open.triggered.connect(lambda: self._open_file(file_path))
        else:
            action_open.setEnabled(False)
            action_open.setText("📂 Apri File (Percorso non disponibile)")

        menu.addAction(action_open)
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _open_file(self, path_str):
        """Apre il file con l'applicazione di default."""
        if not path_str:
            return

        try:
            # os.startfile funziona solo su Windows, che è il target
            os.startfile(path_str)
        except Exception as e:
            QMessageBox.warning(self, "Errore Apertura", f"Impossibile aprire il file:\n{path_str}\n\nErrore: {e}")
