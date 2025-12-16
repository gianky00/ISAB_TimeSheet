"""
Bot TS - Bot Panels
Pannelli specifici per ogni bot.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QFrame, QMessageBox, QSizePolicy, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread

from .widgets import EditableDataTable, LogWidget, StatusIndicator
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
        # Tabella dati
        group = QGroupBox("Dati Timesheet")
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
    
    def _load_saved_data(self):
        """Carica i dati salvati."""
        config = config_manager.load_config()
        saved_data = config.get("last_ts_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)
    
    def _save_data(self):
        """Salva i dati correnti."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_ts_data", data)
    
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
        
        # Crea e avvia il worker
        from src.bots import create_bot
        
        config = config_manager.load_config()
        bot = create_bot(
            "scarico_ts",
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
        self.log_widget.append("▶ Avvio bot Scarico TS...")
        
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
            "💡 Questo bot esegue il login e si ferma, lasciando il browser aperto "
            "per la navigazione manuale. I dati OdA sono opzionali."
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
            "⚠️ Il browser rimarrà aperto dopo il login. Chiudilo manualmente quando hai finito."
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
    
    def _load_saved_data(self):
        """Carica i dati salvati."""
        config = config_manager.load_config()
        saved_data = config.get("last_oda_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)
    
    def _save_data(self):
        """Salva i dati correnti."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_oda_data", data)
    
    def _on_start(self):
        """Avvia il bot Dettagli OdA."""
        username, password = self.get_credentials()
        
        if not username or not password:
            QMessageBox.warning(
                self,
                "Credenziali mancanti",
                "Configura le credenziali ISAB nelle Impostazioni."
            )
            return
        
        # Ottieni i dati (opzionali)
        data = self.data_table.get_data()
        
        # Crea e avvia il worker
        from src.bots import create_bot
        
        config = config_manager.load_config()
        bot = create_bot(
            "dettagli_oda",
            username=username,
            password=password,
            headless=False,  # Sempre visibile per questo bot
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
        self.log_widget.append("▶ Avvio bot Dettagli OdA...")
        
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
