"""
Bot TS - Bot Panels
Pannelli specifici per ogni bot.
"""
import sqlite3
import traceback
import threading
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QFrame, QMessageBox, QSizePolicy, QFileDialog,
    QDateEdit, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QCheckBox, QTimeEdit, QInputDialog, QApplication, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QDate, QTime
from datetime import datetime

from src.gui.widgets import (
    EditableDataTable, LogWidget, StatusIndicator, ExcelTableWidget,
    CalendarDateEdit, MissionReportCard
)
from src.core import config_manager


class BotWorker(QThread):
    """Thread worker per eseguire i bot in background."""
    
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    request_input_signal = pyqtSignal(str, dict, threading.Event)
    
    def __init__(self, bot, data):
        super().__init__()
        self.bot = bot
        self.data = data
        self._is_running = True
    
    def run(self):
        """Esegue il bot."""
        try:
            # Collega i callback
            self.bot.set_log_callback(self.log_signal.emit)
            
            # Setup input callback se supportato dal bot
            if hasattr(self.bot, 'set_input_callback'):
                self.bot.set_input_callback(self._request_input_wrapper)

            result = self.bot.execute(self.data)
            self.finished_signal.emit(result)
        except Exception as e:
            error_trace = traceback.format_exc()
            self.log_signal.emit(f"[ERRORE CRITICO] {e}\n{error_trace}")
            self.finished_signal.emit(False)

    def _request_input_wrapper(self, prompt: str) -> str:
        """Wrapper thread-safe per chiedere input alla GUI."""
        result_container = {}
        event = threading.Event()
        self.request_input_signal.emit(prompt, result_container, event)
        event.wait()
        return result_container.get('value', '')
    
    def stop(self):
        """Richiede lo stop del bot."""
        self._is_running = False
        if self.bot:
            self.bot.request_stop()


class BaseBotPanel(QWidget):
    """Pannello base per tutti i bot."""
    
    bot_started = pyqtSignal()
    bot_stopped = pyqtSignal()
    bot_finished = pyqtSignal(bool)
    
    def __init__(self, bot_name: str, bot_description: str, parent=None):
        super().__init__(parent)
        self.bot_name = bot_name
        self.bot_description = bot_description
        self.worker = None
        self.start_time = None
        self._setup_base_ui()
    
    def _setup_base_ui(self):
        """Setup base UI."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(15)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header)
        
        title = QLabel(self.bot_name)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)
        
        desc = QLabel(self.bot_description)
        desc.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 16px;")
        header_layout.addWidget(desc)
        
        self.main_layout.addWidget(header)
        
        # Status
        self.status_indicator = StatusIndicator()
        self.main_layout.addWidget(self.status_indicator)
        
        # Content area (da sovrascrivere nelle sottoclassi)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
        
        # Log
        self.log_widget = LogWidget()
        self.main_layout.addWidget(self.log_widget)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.start_btn = QPushButton("▶ Avvia")
        self.start_btn.setMinimumWidth(120)
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.start_btn.clicked.connect(self._on_start)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setMinimumWidth(100)
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.stop_btn.clicked.connect(self._on_stop)
        btn_layout.addWidget(self.stop_btn)
        
        self.main_layout.addLayout(btn_layout)
    
    def _on_start(self):
        """Gestisce l'avvio del bot. Da implementare nelle sottoclassi."""
        self.start_time = datetime.now()
        self.log_widget.timeline.set_mood("running")
    
    def _on_stop(self):
        """Gestisce lo stop del bot."""
        if self.worker:
            self.worker.stop()
            self.log_widget.append("[AVVISO] Stop richiesto...")
    
    def _on_worker_finished(self, success: bool):
        """Gestisce il completamento del worker."""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Calculate duration
        duration_str = "--:--"
        if self.start_time:
            delta = datetime.now() - self.start_time
            total_seconds = int(delta.total_seconds())
            m, s = divmod(total_seconds, 60)
            duration_str = f"{m}m {s}s"

        # Mission Report (#3)
        # Using the timeline widget exposed via log_widget
        report = MissionReportCard(duration_str, success)
        self.log_widget.timeline.add_widget(report)

        if success:
            self.status_indicator.set_status("success")
            self.log_widget.timeline.set_mood("success")
        else:
            self.status_indicator.set_status("error")
            self.log_widget.timeline.set_mood("error")
        
        self.bot_finished.emit(success)

        # Taskbar Flash (#4)
        QApplication.alert(self, 0) # 0 = infinite flash until focused

        # Attendi che il thread sia effettivamente terminato per evitare crash
        if self.worker:
            self.worker.wait()
            self.worker = None
    
    def _on_log(self, message: str):
        """Aggiunge un messaggio al log."""
        self.log_widget.append(message)
    
    def _on_status(self, status: str):
        """Aggiorna lo stato."""
        self.status_indicator.set_status(status)
    
    def get_credentials(self) -> tuple:
        """Ottiene le credenziali dall'account di default."""
        account = config_manager.get_default_account()
        if account:
            return account.get("username", ""), account.get("password", "")
        return "", ""


class ScaricaTSPanel(BaseBotPanel):
    """Pannello per il bot Scarico TS."""
    
    def __init__(self, parent=None):
        super().__init__(
            bot_name="📥 Scarico TS",
            bot_description="Download automatico dei Timesheet dal portale ISAB",
            parent=parent
        )
        self._setup_content()
        self._load_saved_data()
    
    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        # --- Sezione Parametri ---
        params_group = QGroupBox("⚙️ Parametri")
        params_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        params_layout = QVBoxLayout(params_group)
        
        # Riga 1: Fornitore (ComboBox)
        fornitore_layout = QHBoxLayout()
        fornitore_label = QLabel("Fornitore:")
        fornitore_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        fornitore_label.setMinimumWidth(80)
        fornitore_layout.addWidget(fornitore_label)
        
        self.fornitore_combo = QComboBox()
        self.fornitore_combo.setMinimumHeight(40)
        self.fornitore_combo.setEditable(False)
        self.fornitore_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 15px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #0d6efd;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ced4da;
                selection-background-color: #e7f1ff;
                selection-color: #0d6efd;
                font-size: 15px;
            }
        """)
        fornitore_layout.addWidget(self.fornitore_combo)
        
        # Pulsante per aprire impostazioni
        self.open_settings_btn = QPushButton("⚙️")
        self.open_settings_btn.setToolTip("Gestisci fornitori nelle Impostazioni")
        self.open_settings_btn.setFixedSize(35, 35)
        self.open_settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.open_settings_btn.clicked.connect(self._open_settings)
        fornitore_layout.addWidget(self.open_settings_btn)
        
        params_layout.addLayout(fornitore_layout)
        
        # Riga 2: Data
        date_layout = QHBoxLayout()
        date_label = QLabel("Data Da:")
        date_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        date_label.setMinimumWidth(80)
        date_layout.addWidget(date_label)
        
        self.date_edit = CalendarDateEdit()
        # Default: 01.01.2025
        self.date_edit.setDate(QDate(2025, 1, 1))
        date_layout.addWidget(self.date_edit)
        
        date_hint = QLabel("(Formato: gg.mm.aaaa)")
        date_hint.setStyleSheet("color: #6c757d; font-size: 13px; font-weight: normal;")
        date_layout.addWidget(date_hint)
        
        date_layout.addStretch()
        
        params_layout.addLayout(date_layout)
        
        # Riga 3: Percorso destinazione
        dest_layout = QHBoxLayout()
        dest_label = QLabel("Destinazione:")
        dest_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        dest_label.setMinimumWidth(80)
        dest_layout.addWidget(dest_label)

        self.dest_path_edit = QLineEdit()
        self.dest_path_edit.setPlaceholderText("Download utente (default)")
        self.dest_path_edit.setReadOnly(True)
        dest_layout.addWidget(self.dest_path_edit)

        browse_btn = QPushButton("📂")
        browse_btn.setFixedSize(35, 35)
        browse_btn.clicked.connect(self._browse_dest_path)
        dest_layout.addWidget(browse_btn)

        params_layout.addLayout(dest_layout)

        # Riga 4: Flag Elabora TS
        self.elabora_ts_check = QCheckBox("Elabora TS (Rinomina e Sposta)")
        self.elabora_ts_check.setStyleSheet("font-size: 15px; margin-top: 5px;")
        # Auto-save settings on change
        self.elabora_ts_check.stateChanged.connect(self._save_data)
        self.dest_path_edit.textChanged.connect(self._save_data)
        params_layout.addWidget(self.elabora_ts_check)

        self.content_layout.addWidget(params_group)
        
        # --- Sezione Tabella Dati ---
        group = QGroupBox("📋 Dati Timesheet")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        group_layout = QVBoxLayout(group)
        
        # Istruzioni
        instructions = QLabel(
            "💡 Tasto destro per aggiungere/rimuovere righe. "
            "Modifica i valori direttamente nelle celle."
        )
        instructions.setStyleSheet("color: #6c757d; font-size: 14px; padding: 5px;")
        instructions.setWordWrap(True)
        group_layout.addWidget(instructions)

        # Toolbar per la tabella
        table_toolbar = QHBoxLayout()
        table_toolbar.addStretch()

        self.clear_btn = QPushButton("🗑️ Pulisci Tabella")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)

        group_layout.addLayout(table_toolbar)
        
        # Tabella con colonne: Numero OdA
        self.data_table = EditableDataTable([
            {"name": "Numero OdA", "type": "text"}
        ])
        self.data_table.data_changed.connect(self._save_data)
        group_layout.addWidget(self.data_table)
        
        self.content_layout.addWidget(group)
    
    def _open_settings(self):
        """Emette un segnale per aprire le impostazioni (gestito dalla main window)."""
        # Trova la main window e cambia pagina
        main_window = self.window()
        if hasattr(main_window, 'show_settings'):
            main_window.show_settings()
    
    def refresh_fornitori(self):
        """Ricarica l'elenco dei fornitori dalla configurazione."""
        config = config_manager.load_config()
        fornitori = config.get("fornitori", [])
        
        # Salva la selezione corrente
        current_text = self.fornitore_combo.currentText()
        
        # Aggiorna la lista
        self.fornitore_combo.clear()
        
        if fornitori:
            self.fornitore_combo.addItems(fornitori)
            
            # Ripristina la selezione se ancora presente
            index = self.fornitore_combo.findText(current_text)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)
            else:
                # Seleziona il primo elemento
                self.fornitore_combo.setCurrentIndex(0)
    
    def _browse_dest_path(self):
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella destinazione")
        if path:
            self.dest_path_edit.setText(path)

    def _load_saved_data(self):
        """Carica i dati salvati."""
        config = config_manager.load_config()
        
        # Carica fornitori
        self.refresh_fornitori()
        
        # Carica fornitore selezionato
        saved_fornitore = config.get("last_ts_fornitore", "")
        if saved_fornitore:
            index = self.fornitore_combo.findText(saved_fornitore)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)
        
        # Carica dati tabella
        saved_data = config.get("last_ts_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)
        
        # Carica la data salvata se presente
        saved_date = config.get("last_ts_date", "01.01.2025")
        try:
            parts = saved_date.split(".")
            if len(parts) == 3:
                day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                self.date_edit.setDate(QDate(year, month, day))
        except:
            pass

        # Carica path e flag
        self.dest_path_edit.setText(config.get("path_scarico_ts", ""))
        self.elabora_ts_check.setChecked(config.get("elabora_ts", False))
    
    def _clear_table(self):
        """Pulisce la tabella."""
        if QMessageBox.question(self, "Conferma", "Sei sicuro di voler cancellare tutte le righe?") == QMessageBox.StandardButton.Yes:
            self.data_table.set_data([])
            self._save_data()

    def _save_data(self):
        """Salva i dati correnti."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_ts_data", data)
        
        # Salva anche la data
        date_str = self.date_edit.date().toString("dd.MM.yyyy")
        config_manager.set_config_value("last_ts_date", date_str)
        
        # Salva il fornitore selezionato
        fornitore = self.fornitore_combo.currentText()
        if fornitore:
            config_manager.set_config_value("last_ts_fornitore", fornitore)

        # Salva path e flag
        config_manager.set_config_value("path_scarico_ts", self.dest_path_edit.text())
        config_manager.set_config_value("elabora_ts", self.elabora_ts_check.isChecked())

    def _ask_user_input(self, prompt: str, result_container: dict, event: threading.Event):
        """Callback per chiedere input all'utente (chiamato dal thread GUI)."""
        try:
            text, ok = QInputDialog.getText(self, "Conflitto File", prompt)
            if ok:
                result_container['value'] = text
            else:
                result_container['value'] = ""
        except Exception as e:
            print(f"Errore input dialog: {e}")
            result_container['value'] = ""
        finally:
            event.set()
    
    def _on_start(self):
        """Avvia il bot Scarico TS."""
        username, password = self.get_credentials()
        
        if not username or not password:
            QMessageBox.warning(
                self,
                "Credenziali mancanti",
                "Configura le credenziali ISAB nelle Impostazioni."
            )
            return
        
        data = self.data_table.get_data()
        if not data:
            QMessageBox.warning(
                self,
                "Dati mancanti",
                "Inserisci almeno una riga con i dati del Timesheet."
            )
            return
        
        fornitore = self.fornitore_combo.currentText()
        if not fornitore:
            QMessageBox.warning(
                self,
                "Fornitore mancante",
                "Seleziona un fornitore dal menu a tendina.\n\n"
                "Puoi gestire i fornitori nelle Impostazioni."
            )
            return
        
        # Salva i dati correnti
        self._save_data()
        
        # Ottieni la data selezionata
        data_da = self.date_edit.date().toString("dd.MM.yyyy")
        
        # Ottieni path specifico o default
        download_path = self.dest_path_edit.text()
        if not download_path:
            download_path = str(Path.home() / "Downloads")

        # Crea e avvia il worker
        from src.bots import create_bot
        
        config = config_manager.load_config()
        bot = create_bot(
            "scarico_ts",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=download_path,
            data_da=data_da,
            fornitore=fornitore,
            elabora_ts=self.elabora_ts_check.isChecked()
        )
        
        if not bot:
            QMessageBox.critical(self, "Errore", "Impossibile creare il bot.")
            return
        
        # Prepara i dati con la data e il fornitore
        bot_data = {
            "rows": data,
            "data_da": data_da,
            "fornitore": fornitore,
            "elabora_ts": self.elabora_ts_check.isChecked()
        }
        
        self.worker = BotWorker(bot, bot_data)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)
        self.worker.request_input_signal.connect(self._ask_user_input)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_indicator.set_status("running")
        
        self.log_widget.clear()
        self.log_widget.append(f"▶ Avvio bot Scarico TS")
        self.log_widget.append(f"  Fornitore: {fornitore}")
        self.log_widget.append(f"  Data: {data_da}")
        self.log_widget.append(f"  Elaborazione file: {'Sì' if self.elabora_ts_check.isChecked() else 'No'}")
        
        self.worker.start()
        self.bot_started.emit()


class DettagliOdAPanel(BaseBotPanel):
    """Pannello per il bot Dettagli OdA."""
    
    def __init__(self, parent=None):
        super().__init__(
            bot_name="📋 Dettagli OdA",
            bot_description="Accesso rapido ai dettagli degli Ordini d'Acquisto",
            parent=parent
        )
        self._setup_content()
        self._load_saved_data()
    
    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        # --- Sezione Parametri ---
        params_group = QGroupBox("⚙️ Parametri")
        params_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        params_layout = QVBoxLayout(params_group)

        # Riga 1: Fornitore (ComboBox)
        fornitore_layout = QHBoxLayout()
        fornitore_label = QLabel("Fornitore:")
        fornitore_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        fornitore_label.setMinimumWidth(80)
        fornitore_layout.addWidget(fornitore_label)

        self.fornitore_combo = QComboBox()
        self.fornitore_combo.setMinimumHeight(40)
        self.fornitore_combo.setEditable(False)
        self.fornitore_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 15px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #0d6efd;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ced4da;
                selection-background-color: #e7f1ff;
                selection-color: #0d6efd;
                font-size: 15px;
            }
        """)
        fornitore_layout.addWidget(self.fornitore_combo)

        # Pulsante per aprire impostazioni
        self.open_settings_btn = QPushButton("⚙️")
        self.open_settings_btn.setToolTip("Gestisci fornitori nelle Impostazioni")
        self.open_settings_btn.setFixedSize(35, 35)
        self.open_settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.open_settings_btn.clicked.connect(self._open_settings)
        fornitore_layout.addWidget(self.open_settings_btn)

        params_layout.addLayout(fornitore_layout)

        # Riga 2: Data Da e Data A
        date_layout = QHBoxLayout()

        # Data Da
        date_da_label = QLabel("Data Da:")
        date_da_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        date_layout.addWidget(date_da_label)

        self.date_da_edit = CalendarDateEdit()
        self.date_da_edit.setDate(QDate(2025, 1, 1))
        date_layout.addWidget(self.date_da_edit)

        date_layout.addSpacing(15)

        # Data A
        date_a_label = QLabel("Data A:")
        date_a_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        date_layout.addWidget(date_a_label)

        self.date_a_edit = CalendarDateEdit()
        self.date_a_edit.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_a_edit)

        date_layout.addStretch()
        params_layout.addLayout(date_layout)

        # Riga 3: Percorso destinazione
        dest_layout = QHBoxLayout()
        dest_label = QLabel("Destinazione:")
        dest_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        dest_label.setMinimumWidth(80)
        dest_layout.addWidget(dest_label)

        self.dest_path_edit = QLineEdit()
        self.dest_path_edit.setPlaceholderText("Download utente (default)")
        self.dest_path_edit.setReadOnly(True)
        dest_layout.addWidget(self.dest_path_edit)

        browse_btn = QPushButton("📂")
        browse_btn.setFixedSize(35, 35)
        browse_btn.clicked.connect(self._browse_dest_path)
        dest_layout.addWidget(browse_btn)

        params_layout.addLayout(dest_layout)

        self.content_layout.addWidget(params_group)

        # Form dati OdA
        group = QGroupBox("Dati Ordine d'Acquisto")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        group_layout = QVBoxLayout(group)
        
        # Istruzioni
        instructions = QLabel(
            "💡 Questo bot esegue il login, naviga a Dettagli OdA, imposta i filtri "
            "e si ferma per la consultazione manuale."
        )
        instructions.setStyleSheet("color: #6c757d; font-size: 14px; padding: 5px;")
        instructions.setWordWrap(True)
        group_layout.addWidget(instructions)

        # Toolbar per la tabella
        table_toolbar = QHBoxLayout()
        table_toolbar.addStretch()

        self.clear_btn = QPushButton("🗑️ Pulisci Tabella")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)

        group_layout.addLayout(table_toolbar)
        
        # Tabella con colonne: Numero OdA e Numero Contratto
        # Recupera default da config per le nuove righe
        config = config_manager.load_config()
        contracts = config.get("contracts", [])
        default_contract = config.get("default_contract", "")

        # Se non c'è un default ma ci sono contratti, usa il primo
        if not default_contract and contracts:
            default_contract = contracts[0]

        self.data_table = EditableDataTable([
            {"name": "Numero OdA", "type": "text"},
            {"name": "Numero Contratto", "type": "combo", "options": contracts, "default": default_contract}
        ])
        self.data_table.data_changed.connect(self._save_data)
        group_layout.addWidget(self.data_table)
        
        
        self.content_layout.addWidget(group)
    
    def _open_settings(self):
        """Emette un segnale per aprire le impostazioni."""
        main_window = self.window()
        if hasattr(main_window, 'show_settings'):
            main_window.show_settings()

    def _browse_dest_path(self):
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella destinazione")
        if path:
            self.dest_path_edit.setText(path)

    def refresh_fornitori(self):
        """Ricarica l'elenco dei fornitori e contratti."""
        config = config_manager.load_config()

        # 1. Aggiorna Fornitori
        fornitori = config.get("fornitori", [])
        current_text = self.fornitore_combo.currentText()
        self.fornitore_combo.clear()

        if fornitori:
            self.fornitore_combo.addItems(fornitori)
            index = self.fornitore_combo.findText(current_text)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)
            else:
                self.fornitore_combo.setCurrentIndex(0)

        # 2. Aggiorna Contratti nella tabella
        contracts = config.get("contracts", [])
        self.data_table.update_column_options("Numero Contratto", contracts)

    def _load_saved_data(self):
        """Carica i dati salvati."""
        config = config_manager.load_config()

        self.refresh_fornitori()

        saved_fornitore = config.get("last_oda_fornitore", "")
        if saved_fornitore:
            index = self.fornitore_combo.findText(saved_fornitore)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)

        # Carica date
        try:
            date_da = config.get("last_oda_date_da", "01.01.2025")
            d, m, y = map(int, date_da.split("."))
            self.date_da_edit.setDate(QDate(y, m, d))

            date_a = config.get("last_oda_date_a", QDate.currentDate().toString("dd.MM.yyyy"))
            d, m, y = map(int, date_a.split("."))
            self.date_a_edit.setDate(QDate(y, m, d))
        except:
            pass

        saved_data = config.get("last_oda_data", [])
        if saved_data:
            # Assicuriamo che i vecchi dati abbiano il contratto vuoto o default
            # e puliamo da chiavi obsolete
            cleaned_data = []
            default_contract = config.get("default_contract", "")
            contracts = config.get("contracts", [])
            if not default_contract and contracts:
                default_contract = contracts[0]

            for row in saved_data:
                cleaned_row = {
                    "numero_oda": row.get("numero_oda", ""),
                    "numero_contratto": row.get("numero_contratto", default_contract)
                }
                cleaned_data.append(cleaned_row)
            self.data_table.set_data(cleaned_data)

        # Carica path
        self.dest_path_edit.setText(config.get("path_dettagli_oda", ""))
    
    def _clear_table(self):
        """Pulisce la tabella."""
        if QMessageBox.question(self, "Conferma", "Sei sicuro di voler cancellare tutte le righe?") == QMessageBox.StandardButton.Yes:
            self.data_table.set_data([])
            self._save_data()

    def _save_data(self):
        """Salva i dati correnti."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_oda_data", data)

        config_manager.set_config_value("last_oda_fornitore", self.fornitore_combo.currentText())
        config_manager.set_config_value("last_oda_date_da", self.date_da_edit.date().toString("dd.MM.yyyy"))
        config_manager.set_config_value("last_oda_date_a", self.date_a_edit.date().toString("dd.MM.yyyy"))

        config_manager.set_config_value("path_dettagli_oda", self.dest_path_edit.text())
    
    def _on_start(self):
        """Avvia il bot Dettagli OdA."""
        username, password = self.get_credentials()
        
        if not username or not password:
            QMessageBox.warning(self, "Credenziali mancanti", "Configura le credenziali ISAB nelle Impostazioni.")
            return

        fornitore = self.fornitore_combo.currentText()
        if not fornitore:
            QMessageBox.warning(self, "Fornitore mancante", "Seleziona un fornitore.")
            return

        # Salva dati
        self._save_data()
        
        data = self.data_table.get_data()
        data_da = self.date_da_edit.date().toString("dd.MM.yyyy")
        data_a = self.date_a_edit.date().toString("dd.MM.yyyy")
        
        # Ottieni path specifico o default
        download_path = self.dest_path_edit.text()
        if not download_path:
            download_path = str(Path.home() / "Downloads")

        from src.bots import create_bot
        config = config_manager.load_config()

        bot = create_bot(
            "dettagli_oda",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=download_path,
            fornitore=fornitore,
            data_da=data_da,
            data_a=data_a
        )
        
        if not bot:
            QMessageBox.critical(self, "Errore", "Impossibile creare il bot.")
            return
        
        self.worker = BotWorker(bot, {
            "rows": data,
            "fornitore": fornitore,
            "data_da": data_da,
            "data_a": data_a
        })
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_indicator.set_status("running")
        
        self.log_widget.clear()
        self.log_widget.append("▶ Avvio bot Dettagli OdA...")
        self.log_widget.append(f"  Fornitore: {fornitore}")
        self.log_widget.append(f"  Periodo: {data_da} - {data_a}")
        
        self.worker.start()
        self.bot_started.emit()


class CaricoTSPanel(BaseBotPanel):
    """Pannello per il bot Carico TS."""
    
    def __init__(self, parent=None):
        super().__init__(
            bot_name="📤 Carico TS",
            bot_description="Upload automatico dei Timesheet sul portale ISAB",
            parent=parent
        )
        self._setup_content()
        self._load_saved_data()
    
    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        # Tabella dati
        group = QGroupBox("Dati Timesheet da Caricare")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        group_layout = QVBoxLayout(group)
        
        # Istruzioni
        instructions = QLabel(
            "💡 Tasto destro per aggiungere/rimuovere righe. "
            "Modifica i valori direttamente nelle celle."
        )
        instructions.setStyleSheet("color: #6c757d; font-size: 14px; padding: 5px;")
        instructions.setWordWrap(True)
        group_layout.addWidget(instructions)

        # Toolbar per la tabella
        table_toolbar = QHBoxLayout()
        table_toolbar.addStretch()

        self.clear_btn = QPushButton("🗑️ Pulisci Tabella")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)

        group_layout.addLayout(table_toolbar)
        
        # Tabella con tutte le colonne del database Carico TS
        self.data_table = EditableDataTable([
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
            {"name": "Codice Fiscale", "type": "text"},
            {"name": "Ingresso", "type": "text"},
            {"name": "Uscita", "type": "text"},
            {"name": "Tipo Prestazione", "type": "text"},
            {"name": "C", "type": "text"},
            {"name": "M", "type": "text"},
            {"name": "Str D", "type": "text"},
            {"name": "Str N", "type": "text"},
            {"name": "Str F D", "type": "text"},
            {"name": "Str F N", "type": "text"},
            {"name": "Sq", "type": "text"},
            {"name": "Nota D", "type": "text"},
            {"name": "Nota S", "type": "text"},
            {"name": "F S", "type": "text"},
            {"name": "G T", "type": "text"}
        ])
        self.data_table.data_changed.connect(self._save_data)
        group_layout.addWidget(self.data_table)
        
        self.content_layout.addWidget(group)
    
    def _load_saved_data(self):
        """Carica i dati salvati."""
        config = config_manager.load_config()
        saved_data = config.get("last_carico_ts_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)
    
    def _clear_table(self):
        """Pulisce la tabella."""
        if QMessageBox.question(self, "Conferma", "Sei sicuro di voler cancellare tutte le righe?") == QMessageBox.StandardButton.Yes:
            self.data_table.set_data([])
            self._save_data()

    def _save_data(self):
        """Salva i dati correnti."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_carico_ts_data", data)
    
    def _on_start(self):
        """Avvia il bot Carico TS."""
        username, password = self.get_credentials()
        
        if not username or not password:
            QMessageBox.warning(
                self,
                "Credenziali mancanti",
                "Configura le credenziali ISAB nelle Impostazioni."
            )
            return
        
        data = self.data_table.get_data()
        if not data:
            QMessageBox.warning(
                self,
                "Dati mancanti",
                "Inserisci almeno una riga con i dati del Timesheet da caricare."
            )
            return
        
        # Crea e avvia il worker
        from src.bots import create_bot
        
        config = config_manager.load_config()
        bot = create_bot(
            "carico_ts",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path()
        )
        
        if not bot:
            QMessageBox.critical(self, "Errore", "Impossibile creare il bot.")
            return
        
        self.worker = BotWorker(bot, {"rows": data})
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_indicator.set_status("running")
        
        self.log_widget.clear()
        self.log_widget.append("▶ Avvio bot Carico TS...")
        
        self.worker.start()
        self.bot_started.emit()


class TimbratureBotPanel(BaseBotPanel):
    """Pannello per il bot Timbrature (Controlli e Log)."""

    # Segnale per notificare che i dati sono stati aggiornati (e il DB deve ricaricare)
    data_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(
            bot_name="⏱️ Timbrature",
            bot_description="Scarica e gestisci le timbrature del personale",
            parent=parent
        )
        self._setup_content()
        self._load_saved_data()

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        # --- Sezione Parametri ---
        params_group = QGroupBox("⚙️ Parametri")
        params_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        params_layout = QVBoxLayout(params_group)

        # Riga 1: Fornitore (ComboBox)
        fornitore_layout = QHBoxLayout()
        fornitore_label = QLabel("Fornitore:")
        fornitore_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        fornitore_label.setMinimumWidth(80)
        fornitore_layout.addWidget(fornitore_label)

        self.fornitore_combo = QComboBox()
        self.fornitore_combo.setMinimumHeight(40)
        self.fornitore_combo.setEditable(False)
        self.fornitore_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 15px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #0d6efd;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ced4da;
                selection-background-color: #e7f1ff;
                selection-color: #0d6efd;
                font-size: 15px;
            }
        """)
        fornitore_layout.addWidget(self.fornitore_combo)

        # Pulsante per aprire impostazioni
        self.open_settings_btn = QPushButton("⚙️")
        self.open_settings_btn.setToolTip("Gestisci fornitori nelle Impostazioni")
        self.open_settings_btn.setFixedSize(35, 35)
        self.open_settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.open_settings_btn.clicked.connect(self._open_settings)
        fornitore_layout.addWidget(self.open_settings_btn)

        params_layout.addLayout(fornitore_layout)

        # Riga 2: Data Da e Data A
        date_layout = QHBoxLayout()

        # Data Da
        date_da_label = QLabel("Data Da:")
        date_da_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        date_layout.addWidget(date_da_label)

        self.date_da_edit = CalendarDateEdit()
        self.date_da_edit.setDate(QDate(2025, 1, 1))
        date_layout.addWidget(self.date_da_edit)

        date_layout.addSpacing(15)

        # Data A
        date_a_label = QLabel("Data A:")
        date_a_label.setStyleSheet("font-weight: normal; font-size: 15px;")
        date_layout.addWidget(date_a_label)

        self.date_a_edit = CalendarDateEdit()
        self.date_a_edit.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_a_edit)

        date_layout.addStretch()
        params_layout.addLayout(date_layout)

        self.content_layout.addWidget(params_group)

        # --- Sezione Scheduler (Autopilot) ---
        sched_group = QGroupBox("📅 Autopilot (Pianificatore)")
        sched_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        sched_layout = QHBoxLayout(sched_group)

        self.autopilot_check = QCheckBox("Abilita download automatico")
        self.autopilot_check.setStyleSheet("font-size: 15px;")
        sched_layout.addWidget(self.autopilot_check)

        sched_layout.addSpacing(20)

        lbl_time = QLabel("Alle ore:")
        lbl_time.setStyleSheet("font-size: 15px;")
        sched_layout.addWidget(lbl_time)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(9, 0))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setMinimumHeight(35)
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
        """)
        sched_layout.addWidget(self.time_edit)

        sched_layout.addStretch()
        self.content_layout.addWidget(sched_group)

    def _open_settings(self):
        main_window = self.window()
        if hasattr(main_window, 'show_settings'):
            main_window.show_settings()

    def refresh_fornitori(self):
        config = config_manager.load_config()
        fornitori = config.get("fornitori", [])

        current_text = self.fornitore_combo.currentText()
        self.fornitore_combo.clear()

        if fornitori:
            self.fornitore_combo.addItems(fornitori)
            index = self.fornitore_combo.findText(current_text)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)
            else:
                self.fornitore_combo.setCurrentIndex(0)

    def _load_saved_data(self):
        self.refresh_fornitori()

        config = config_manager.load_config()

        saved_fornitore = config.get("last_timbrature_fornitore", "")
        if saved_fornitore:
            index = self.fornitore_combo.findText(saved_fornitore)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)

        try:
            date_da = config.get("last_timbrature_date_da", "01.01.2025")
            d, m, y = map(int, date_da.split("."))
            self.date_da_edit.setDate(QDate(y, m, d))

            date_a = config.get("last_timbrature_date_a", QDate.currentDate().toString("dd.MM.yyyy"))
            d, m, y = map(int, date_a.split("."))
            self.date_a_edit.setDate(QDate(y, m, d))
        except:
            pass

    def _save_data(self):
        config_manager.set_config_value("last_timbrature_fornitore", self.fornitore_combo.currentText())
        config_manager.set_config_value("last_timbrature_date_da", self.date_da_edit.date().toString("dd.MM.yyyy"))
        config_manager.set_config_value("last_timbrature_date_a", self.date_a_edit.date().toString("dd.MM.yyyy"))

    def _on_start(self):
        username, password = self.get_credentials()

        if not username or not password:
            QMessageBox.warning(self, "Credenziali mancanti", "Configura le credenziali ISAB nelle Impostazioni.")
            return

        fornitore = self.fornitore_combo.currentText()
        if not fornitore:
            QMessageBox.warning(self, "Fornitore mancante", "Seleziona un fornitore.")
            return

        self._save_data()

        data_da = self.date_da_edit.date().toString("dd.MM.yyyy")
        data_a = self.date_a_edit.date().toString("dd.MM.yyyy")

        from src.bots import create_bot
        config = config_manager.load_config()

        bot = create_bot(
            "timbrature",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
            fornitore=fornitore,
            data_da=data_da,
            data_a=data_a
        )

        if not bot:
            QMessageBox.critical(self, "Errore", "Impossibile creare il bot.")
            return

        self.worker = BotWorker(bot, {
            "fornitore": fornitore,
            "data_da": data_da,
            "data_a": data_a
        })
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)

        # Emetti segnale di update se successo
        self.worker.finished_signal.connect(lambda s: self.data_updated.emit() if s else None)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_indicator.set_status("running")

        self.log_widget.clear()
        self.log_widget.append("▶ Avvio bot Timbrature...")
        self.log_widget.append(f"  Fornitore: {fornitore}")
        self.log_widget.append(f"  Periodo: {data_da} - {data_a}")

        self.worker.start()
        self.bot_started.emit()


class TimbratureDBPanel(QWidget):
    """Pannello per la visualizzazione del Database Timbrature Isab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = config_manager.CONFIG_DIR / "data" / "timbrature_Isab.db"
        self._setup_ui()
        self.refresh_data()

    def _setup_ui(self):
        """Configura l'interfaccia utente."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

        # --- Sezione Database ---
        db_group = QGroupBox("🗄️ Database Timbrature")
        db_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        db_layout = QVBoxLayout(db_group)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Filtra:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca per nome, cognome, data...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._filter_data)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        # Import Button
        import_btn = QPushButton("📥 Importa Excel")
        import_btn.setToolTip("Importa manualmente un file Excel di timbrature")
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        import_btn.clicked.connect(self._import_excel_manually)
        search_layout.addWidget(import_btn)

        # Refresh Button
        refresh_btn = QPushButton("🔄 Aggiorna")
        refresh_btn.setToolTip("Ricarica i dati dal database")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_data)
        search_layout.addWidget(refresh_btn)

        db_layout.addLayout(search_layout)

        # Table
        self.db_table = ExcelTableWidget()
        self.db_table.setColumnCount(7)
        self.db_table.setHorizontalHeaderLabels([
            "Data", "Ingresso", "Uscita", "Nome", "Cognome", "Presenza TS", "Sito Timbratura"
        ])

        header = self.db_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.db_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                gridline-color: #e9ecef;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
            }
        """)
        self.db_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        db_layout.addWidget(self.db_table)

        self.main_layout.addWidget(db_group)

    def refresh_data(self):
        """Metodo pubblico per ricaricare i dati."""
        self._load_db_data()

    def _load_db_data(self):
        """Carica i dati dal database nella tabella."""
        if not self.db_path.exists():
            return

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura FROM timbrature ORDER BY id DESC")
                rows = cursor.fetchall()

            self._update_table(rows)
        except Exception as e:
            print(f"Errore caricamento DB: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Errore Database", f"Impossibile caricare i dati:\n{e}")

    def _update_table(self, rows):
        """Aggiorna la tabella con i dati forniti."""
        self.db_table.setRowCount(0)
        for row_idx, row_data in enumerate(rows):
            self.db_table.insertRow(row_idx)

            # Format date (column 0) if necessary
            formatted_row = list(row_data)
            try:
                date_str = str(formatted_row[0])
                if date_str:
                    # Rimuovi l'eventuale parte oraria per pulizia
                    date_part = date_str.split(' ')[0] if ' ' in date_str else date_str

                    # Prova il parsing formato ISO standard (YYYY-MM-DD)
                    try:
                        dt = datetime.strptime(date_part, "%Y-%m-%d")
                        formatted_row[0] = dt.strftime("%d/%m/%Y")
                    except ValueError:
                        pass # Se non è YYYY-MM-DD, lascia com'è (potrebbe essere già DD/MM/YYYY)

            except Exception:
                # In caso di errore generico, mantieni il valore originale
                pass

            for col_idx, value in enumerate(formatted_row):
                self.db_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def _import_excel_manually(self):
        """Importa manualmente un file Excel nel database."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona File Excel Timbrature",
            str(Path.home() / "Downloads"),
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_path:
            return

        try:
            from src.bots.timbrature.bot import TimbratureBot

            # Callback per loggare (in questo caso useremo print o QMessageBox poiché non abbiamo log widget)
            def gui_log(msg):
                print(msg)

            # Usa il metodo statico del bot
            success = TimbratureBot.import_to_db_static(file_path, self.db_path, gui_log)

            if success:
                self._load_db_data() # Ricarica la tabella
                QMessageBox.information(self, "Successo", "Dati importati correttamente nel database.")
            else:
                QMessageBox.warning(self, "Errore", "Impossibile importare il file. Controlla la console per i dettagli.")

        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", f"Errore durante l'importazione:\n{e}")

    def _filter_data(self, text):
        """Filtra la tabella in base al testo usando SQL."""
        if not self.db_path.exists():
            return

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                query = "SELECT data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura FROM timbrature"
                params = []

                if text:
                    # Cerca corrispondenza di TUTTE le parole cercate in QUALSIASI colonna rilevante
                    search_terms = text.lower().split()
                    conditions = []

                    columns_to_search = ["data", "nome", "cognome", "sito_timbratura"]

                    for term in search_terms:
                        # Converti formato data italiano in formato DB (YYYY-MM-DD) per permettere la ricerca
                        search_term = term
                        if '/' in term:
                            try:
                                parts = term.split('/')

                                # Caso 1: Data completa DD/MM/YYYY -> YYYY-MM-DD
                                if len(parts) == 3:
                                    d, m, y = parts
                                    if len(d) <= 2 and len(m) <= 2 and len(y) == 4:
                                         search_term = f"{y}-{m.zfill(2)}-{d.zfill(2)}"

                                # Caso 2: Parziale MM/YYYY -> YYYY-MM
                                elif len(parts) == 2:
                                    p1, p2 = parts
                                    # Se il secondo pezzo è anno (4 cifre) -> MM/YYYY
                                    if len(p2) == 4:
                                        search_term = f"{p2}-{p1.zfill(2)}"
                                    # Se il secondo pezzo è mese/giorno (2 cifre) e primo anche -> DD/MM
                                    # Cerchiamo nel DB (YYYY-MM-DD) la sequenza -MM-DD
                                    elif len(p2) <= 2:
                                        # Attenzione: DD/MM (es. 17/12) diventa -12-17
                                        search_term = f"-{p2.zfill(2)}-{p1.zfill(2)}"
                            except Exception:
                                pass

                        term_conditions = []
                        for col in columns_to_search:
                            term_conditions.append(f"{col} LIKE ?")
                            params.append(f"%{search_term}%")
                        # Unisci le condizioni per questo termine con OR (il termine deve apparire in almeno una colonna)
                        conditions.append(f"({' OR '.join(term_conditions)})")

                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)

                query += " ORDER BY id DESC LIMIT 500" # Limita a 500 risultati per performance

                cursor.execute(query, params)
                rows = cursor.fetchall()

            self._update_table(rows)

        except Exception as e:
            print(f"Errore filtro: {e}")
            traceback.print_exc()
