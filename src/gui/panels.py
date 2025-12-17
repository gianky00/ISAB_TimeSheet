"""
Bot TS - Bot Panels
Pannelli specifici per ogni bot.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QFrame, QMessageBox, QSizePolicy, QFileDialog,
    QDateEdit, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QDate

from src.gui.widgets import EditableDataTable, LogWidget, StatusIndicator
from src.core import config_manager


class BotWorker(QThread):
    """Thread worker per eseguire i bot in background."""
    
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    
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
            
            result = self.bot.execute(self.data)
            self.finished_signal.emit(result)
        except Exception as e:
            self.log_signal.emit(f"[ERRORE] {e}")
            self.finished_signal.emit(False)
    
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
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)
        
        desc = QLabel(self.bot_description)
        desc.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 12px;")
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
        pass
    
    def _on_stop(self):
        """Gestisce lo stop del bot."""
        if self.worker:
            self.worker.stop()
            self.log_widget.append("[AVVISO] Stop richiesto...")
    
    def _on_worker_finished(self, success: bool):
        """Gestisce il completamento del worker."""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            self.status_indicator.set_status("completed")
            self.log_widget.append("✓ Operazione completata con successo!")
        else:
            self.status_indicator.set_status("error")
        
        self.bot_finished.emit(success)
        self.worker = None
    
    def _on_log(self, message: str):
        """Aggiunge un messaggio al log."""
        self.log_widget.append(message)
    
    def _on_status(self, status: str):
        """Aggiorna lo stato."""
        self.status_indicator.set_status(status)
    
    def get_credentials(self) -> tuple:
        """Ottiene le credenziali dalla configurazione."""
        config = config_manager.load_config()
        username = config.get("isab_username", "")
        password = config.get("isab_password", "")
        return username, password


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
        fornitore_label.setStyleSheet("font-weight: normal;")
        fornitore_label.setMinimumWidth(80)
        fornitore_layout.addWidget(fornitore_label)
        
        self.fornitore_combo = QComboBox()
        self.fornitore_combo.setMinimumHeight(35)
        self.fornitore_combo.setEditable(False)
        self.fornitore_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
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
        date_label.setStyleSheet("font-weight: normal;")
        date_label.setMinimumWidth(80)
        date_layout.addWidget(date_label)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        # Default: 01.01.2025
        self.date_edit.setDate(QDate(2025, 1, 1))
        self.date_edit.setMinimumWidth(150)
        self.date_edit.setMinimumHeight(35)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
                background-color: white;
            }
            QDateEdit:focus {
                border-color: #0d6efd;
            }
            QDateEdit::drop-down {
                border: none;
                width: 30px;
            }
        """)
        date_layout.addWidget(self.date_edit)
        
        date_hint = QLabel("(Formato: gg.mm.aaaa)")
        date_hint.setStyleSheet("color: #6c757d; font-size: 11px; font-weight: normal;")
        date_layout.addWidget(date_hint)
        
        date_layout.addStretch()
        
        params_layout.addLayout(date_layout)
        
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
        instructions.setStyleSheet("color: #6c757d; font-size: 11px; padding: 5px;")
        instructions.setWordWrap(True)
        group_layout.addWidget(instructions)
        
        # Tabella con colonne: Numero OdA, Posizione OdA
        self.data_table = EditableDataTable([
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"}
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
        
        # Crea e avvia il worker
        from src.bots import create_bot
        
        config = config_manager.load_config()
        bot = create_bot(
            "scarico_ts",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
            data_da=data_da,
            fornitore=fornitore
        )
        
        if not bot:
            QMessageBox.critical(self, "Errore", "Impossibile creare il bot.")
            return
        
        # Prepara i dati con la data e il fornitore
        bot_data = {
            "rows": data,
            "data_da": data_da,
            "fornitore": fornitore
        }
        
        self.worker = BotWorker(bot, bot_data)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_indicator.set_status("running")
        
        self.log_widget.clear()
        self.log_widget.append(f"▶ Avvio bot Scarico TS")
        self.log_widget.append(f"  Fornitore: {fornitore}")
        self.log_widget.append(f"  Data: {data_da}")
        
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
        fornitore_label.setStyleSheet("font-weight: normal;")
        fornitore_label.setMinimumWidth(80)
        fornitore_layout.addWidget(fornitore_label)

        self.fornitore_combo = QComboBox()
        self.fornitore_combo.setMinimumHeight(35)
        self.fornitore_combo.setEditable(False)
        self.fornitore_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
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
        date_da_label.setStyleSheet("font-weight: normal;")
        date_layout.addWidget(date_da_label)

        self.date_da_edit = QDateEdit()
        self.date_da_edit.setCalendarPopup(True)
        self.date_da_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_da_edit.setDate(QDate(2025, 1, 1))
        self.date_da_edit.setMinimumHeight(35)
        self.date_da_edit.setStyleSheet(self._get_date_style())
        date_layout.addWidget(self.date_da_edit)

        date_layout.addSpacing(15)

        # Data A
        date_a_label = QLabel("Data A:")
        date_a_label.setStyleSheet("font-weight: normal;")
        date_layout.addWidget(date_a_label)

        self.date_a_edit = QDateEdit()
        self.date_a_edit.setCalendarPopup(True)
        self.date_a_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_a_edit.setDate(QDate.currentDate())
        self.date_a_edit.setMinimumHeight(35)
        self.date_a_edit.setStyleSheet(self._get_date_style())
        date_layout.addWidget(self.date_a_edit)

        date_layout.addStretch()
        params_layout.addLayout(date_layout)

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
        instructions.setStyleSheet("color: #6c757d; font-size: 11px; padding: 5px;")
        instructions.setWordWrap(True)
        group_layout.addWidget(instructions)
        
        # Tabella con colonne: Numero OdA, Posizione OdA
        self.data_table = EditableDataTable([
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"}
        ])
        self.data_table.data_changed.connect(self._save_data)
        group_layout.addWidget(self.data_table)
        
        # Note
        note = QLabel(
            "⚠️ Il browser rimarrà aperto. Chiudilo manualmente quando hai finito."
        )
        note.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                color: #856404;
                padding: 10px;
                border: 1px solid #ffeeba;
                border-radius: 4px;
            }
        """)
        note.setWordWrap(True)
        group_layout.addWidget(note)
        
        self.content_layout.addWidget(group)
    
    def _get_date_style(self):
        return """
            QDateEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
                background-color: white;
            }
            QDateEdit:focus {
                border-color: #0d6efd;
            }
            QDateEdit::drop-down {
                border: none;
                width: 30px;
            }
        """

    def _open_settings(self):
        """Emette un segnale per aprire le impostazioni."""
        main_window = self.window()
        if hasattr(main_window, 'show_settings'):
            main_window.show_settings()

    def refresh_fornitori(self):
        """Ricarica l'elenco dei fornitori."""
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
            self.data_table.set_data(saved_data)
    
    def _save_data(self):
        """Salva i dati correnti."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_oda_data", data)

        config_manager.set_config_value("last_oda_fornitore", self.fornitore_combo.currentText())
        config_manager.set_config_value("last_oda_date_da", self.date_da_edit.date().toString("dd.MM.yyyy"))
        config_manager.set_config_value("last_oda_date_a", self.date_a_edit.date().toString("dd.MM.yyyy"))
    
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
        
        from src.bots import create_bot
        config = config_manager.load_config()

        bot = create_bot(
            "dettagli_oda",
            username=username,
            password=password,
            headless=False,
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
        instructions.setStyleSheet("color: #6c757d; font-size: 11px; padding: 5px;")
        instructions.setWordWrap(True)
        group_layout.addWidget(instructions)
        
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
