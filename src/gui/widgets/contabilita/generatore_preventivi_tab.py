import os
from datetime import datetime
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QFrame,
    QSizePolicy,
    QPushButton,
    QScrollArea
)

from src.core import config_manager
from src.core.preventivi_manager import PreventiviGeneratorManager
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import PrimaryButton, StandardInput
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog


class GeneratoreWorker(QThread):
    """Esegue la generazione del file Excel in background."""
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, master_path: str, data: dict, dest_path: str):
        super().__init__()
        self.master_path = master_path
        self.data = data
        self.dest_path = dest_path

    def run(self):
        try:
            manager = PreventiviGeneratorManager(self.master_path)
            success, result = manager.generate_preventivo(self.data, self.dest_path)
            self.finished_signal.emit(success, result)
        except Exception as e:
            self.finished_signal.emit(False, f"Errore critico thread: {e}")


class MacroWorker(QThread):
    """Esegue una o più Macro VBA sul file generato in un thread separato."""
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, file_path: str, macros: list[str]):
        super().__init__()
        self.file_path = file_path
        self.macros = macros

    def run(self):
        try:
            import pythoncom
            pythoncom.CoInitialize() # Necessario per usare COM in un thread secondario
            import win32com.client
            
            excel_app = win32com.client.Dispatch("Excel.Application")
            excel_app.Visible = True # Importante affinché i MsgBox di VBA non blocchino tutto in background
            
            wb = excel_app.Workbooks.Open(self.file_path, UpdateLinks=0)
            
            for macro in self.macros:
                # Esecuzione della macro specificando il nome del file
                excel_app.Run(f"'{wb.Name}'!{macro}")
            
            wb.Save()
            self.finished_signal.emit(True, f"Macro completate con successo.")
        except Exception as e:
            self.finished_signal.emit(False, f"Errore durante l'esecuzione della macro:\n{e}")
        finally:
            try:
                import pythoncom
                pythoncom.CoUninitialize()
            except:
                pass


class GeneratorePreventiviTab(QWidget):
    """Sottoscheda dedicata alla generazione di preventivi e all'esecuzione di macro VBA."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.macro_worker = None
        self.last_generated_file = None
        self._macro_buttons = []
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {COLORS['border_light']};
                border-radius: 6px;
                padding: 5px 10px;
                background-color: {COLORS['bg_white']};
                color: {COLORS['text_dark']};
                min-height: 36px;
                font-size: 13px;
            }}
            QComboBox:focus {{ border: 2px solid {COLORS['teal_accent']}; }}
            QComboBox::drop-down {{ width: 25px; border-left: 1px solid {COLORS['border_light']}; }}
            QTextEdit {{
                border: 1px solid {COLORS['border_light']};
                border-radius: 6px;
                padding: 10px;
                background-color: {COLORS['bg_white']};
                color: {COLORS['text_dark']};
                font-size: 13px;
            }}
            QTextEdit:focus {{ border: 2px solid {COLORS['teal_accent']}; }}
        """)

        # --- HEADER ---
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        header_layout.setSpacing(4)
        
        title = QLabel("Generatore Consuntivi Strumentale")
        title.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {COLORS['primary_dark']};")
        subtitle = QLabel("Compilazione rapida ed esecuzione sequenziale Macro VBA.")
        subtitle.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_widget)

        # --- SCROLL AREA (Aggiunta per contenere tutte le card) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(15)

        # --- CARD 1: SETUP E PERCORSI ---
        config_card, config_lay = self._create_card("IMPOSTAZIONI E DESTINAZIONE")
        config_row = QHBoxLayout()
        config_row.setSpacing(20)

        self.anno_combo = QComboBox()
        self.anno_combo.addItems([str(y) for y in range(datetime.now().year, 2020, -1)])
        self.anno_combo.currentIndexChanged.connect(self._update_dynamic_path)
        config_row.addLayout(self._create_input_group("ANNO", self.anno_combo, width=100))

        self.progressivo_edit = StandardInput()
        self.progressivo_edit.setStyleSheet(f"color: {COLORS['teal_accent']}; font-weight: bold;")
        config_row.addLayout(self._create_input_group("PROGRESSIVO", self.progressivo_edit, width=120))

        self.dest_path_edit = StandardInput()
        self.dest_path_edit.setReadOnly(True)
        self.dest_path_edit.setStyleSheet(f"background-color: {COLORS['bg_light']}; color: {COLORS['text_muted']};")
        config_row.addLayout(self._create_input_group("PERCORSO DI RETE (AUTOMATICO)", self.dest_path_edit))

        config_lay.addLayout(config_row)
        scroll_layout.addWidget(config_card)

        # --- CARD 2: DATI IDENTIFICATIVI ---
        id_card, id_layout = self._create_card("DETTAGLI INTERVENTO E CLASSIFICAZIONE")
        
        row1 = QHBoxLayout()
        row1.setSpacing(15)
        
        self.data_edit = StandardInput()
        self.data_edit.setText(datetime.now().strftime("%d/%m/%Y"))
        row1.addLayout(self._create_input_group("DATA (A5)", self.data_edit, width=120))
        
        self.tcl_combo = QComboBox()
        self.tcl_combo.addItems(["MESSINA I.", "AGUSTA D.", "CALDARELLA F.", "PREZZAVENTO M.", "BOSCO F.", "RUGGIERI F.", "BARBAGALLO G."])
        row1.addLayout(self._create_input_group("TCL (A7)", self.tcl_combo, width=180))
        
        self.odc_edit = StandardInput()
        row1.addLayout(self._create_input_group("ODC (B5)", self.odc_edit, width=140))
        
        self.avviso_edit = StandardInput()
        row1.addLayout(self._create_input_group("AVVISO (C7)", self.avviso_edit, width=140))
        
        self.ordine_edit = StandardInput()
        row1.addLayout(self._create_input_group("ORDINE (C5)", self.ordine_edit, width=140))
        row1.addStretch()
        id_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(15)

        self.stato_combo = QComboBox()
        self.stato_combo.addItems(["ATTIVITA' DA COMPLETARE", "IN ATTESA TCL", "RICHIESTA ODC MIDOLO", "CONTABILIZZATA"])
        row2.addLayout(self._create_input_group("STATO ATTIVITÀ (D11)", self.stato_combo, width=220))

        self.tipo_prev_combo = QComboBox()
        self.tipo_prev_combo.addItems(["MISURA", "SQUADRA", "CHIAMATA", "FORNITURA", "PREVENTIVO"])
        row2.addLayout(self._create_input_group("TIPOLOGIA PREVENTIVO (D13)", self.tipo_prev_combo, width=220))

        self.tipo_econ_combo = QComboBox()
        self.tipo_econ_combo.addItems(["SQUADRA GIORNALIERA", "SQUADRA SETTIMANALE", "CONSTATAZIONE PURA"])
        row2.addLayout(self._create_input_group("TIPOLOGIA ECONOMIA (E13)", self.tipo_econ_combo, width=220))
        row2.addStretch()
        id_layout.addLayout(row2)
        
        scroll_layout.addWidget(id_card)

        # --- CARD 3: DESCRIZIONI ---
        desc_card, desc_layout = self._create_card("DESCRIZIONE DELLE ATTIVITÀ")
        
        row3 = QHBoxLayout()
        row3.setSpacing(20)
        
        self.desc_lavoro_edit = QTextEdit()
        self.desc_lavoro_edit.setPlaceholderText("Es. Smontaggio valvola...")
        self.desc_lavoro_edit.setMinimumHeight(80)
        self.desc_lavoro_edit.setMaximumHeight(110)
        row3.addLayout(self._create_input_group("DESCRIZIONE LAVORO (A11:A21)", self.desc_lavoro_edit))
        
        self.desc_relazione_edit = QTextEdit()
        self.desc_relazione_edit.setPlaceholderText("Inserisci eventuali note (A32)...")
        self.desc_relazione_edit.setMinimumHeight(80)
        self.desc_relazione_edit.setMaximumHeight(110)
        row3.addLayout(self._create_input_group("DESCRIZIONE RELAZIONE (A32)", self.desc_relazione_edit))
        
        desc_layout.addLayout(row3)
        scroll_layout.addWidget(desc_card)

        # --- CARD 4: MACRO AUTOMAZIONI ---
        macro_card, macro_layout = self._create_card("ESECUZIONE MACRO (ATTIVE DOPO LA GENERAZIONE)")
        
        # Singole Macro
        m_row1 = QHBoxLayout()
        m_row1.setSpacing(10)
        self._create_macro_btn("1. Carica Dati", ["CaricaDatiMultiplo"], m_row1)
        self._create_macro_btn("2. Elabora", ["elaboraDati"], m_row1)
        self._create_macro_btn("3. COMPILA CONSUNTIVO", ["EseguiTuttiSmista"], m_row1)
        self._create_macro_btn("4. Verifica", ["VerificaConsuntivo"], m_row1)
        self._create_macro_btn("5. Stampa", ["verificaEstampaFogli"], m_row1)
        macro_layout.addLayout(m_row1)

        # Azioni composte / Extra
        m_row2 = QHBoxLayout()
        m_row2.setSpacing(10)
        
        self._create_macro_btn("🚀 Esegui 1 -> 4", ["CaricaDatiMultiplo", "elaboraDati", "EseguiTuttiSmista", "VerificaConsuntivo"], m_row2, is_primary=True)
        self._create_macro_btn("🚀 Esegui 1 -> 5", ["CaricaDatiMultiplo", "elaboraDati", "EseguiTuttiSmista", "VerificaConsuntivo", "verificaEstampaFogli"], m_row2, is_primary=True)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setStyleSheet(f"color: {COLORS['border_light']};")
        m_row2.addWidget(line)

        self._create_macro_btn("Email Generica", ["InviaEmailGenerico"], m_row2)
        self._create_macro_btn("Email Chiamata", ["InviaEmailConsuntivoChiamata"], m_row2)
        self._create_macro_btn("Relazione Tecnica", ["CreaEConvertiRelazioneTecnica"], m_row2)
        macro_layout.addLayout(m_row2)

        scroll_layout.addWidget(macro_card)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # --- FOOTER / BUTTON ---
        self.btn_generate = PrimaryButton("1. INIZIA: GENERA CONSUNTIVO EXCEL")
        self.btn_generate.setMinimumHeight(55)
        self.btn_generate.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['teal_accent']};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{ background-color: #2b9e95; }}
            QPushButton:disabled {{ background-color: {COLORS['border_light']}; color: {COLORS['text_muted']}; }}
        """)
        self.btn_generate.clicked.connect(self._on_generate)
        main_layout.addWidget(self.btn_generate)

        # Inizializzazione dinamica
        self._update_dynamic_path()

    def _create_card(self, title_text: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setStyleSheet(f"QFrame {{ background-color: {COLORS['bg_white']}; border-radius: 10px; border: 1px solid {COLORS['border_light']}; }}")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 20)
        layout.setSpacing(15)
        
        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet(f"font-weight: 800; font-size: 12px; letter-spacing: 0.5px; color: {COLORS['primary_dark']}; border: none;")
        layout.addWidget(title_lbl)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background-color: {COLORS['bg_alt']}; border: none; min-height: 1px; max-height: 1px;")
        layout.addWidget(line)
        return card, layout

    def _create_input_group(self, label_text: str, widget: QWidget, width: int = 0) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(4)
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {COLORS['text_muted']}; border: none;")
        layout.addWidget(lbl)
        if width > 0:
            widget.setFixedWidth(width)
        if isinstance(widget, StandardInput):
            widget.setMinimumHeight(36)
            widget.setMaximumHeight(36)
        layout.addWidget(widget)
        return layout

    def _create_macro_btn(self, text: str, macros: list, parent_layout: QHBoxLayout, is_primary: bool = False):
        btn = QPushButton(text)
        btn.setMinimumHeight(38)
        
        bg_color = COLORS['teal_accent'] if is_primary else COLORS['bg_light']
        text_color = "white" if is_primary else COLORS['primary_dark']
        border = "none" if is_primary else f"1px solid {COLORS['border_light']}"
        hover_bg = "#2b9e95" if is_primary else COLORS['bg_alt']
        
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: {border};
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 15px;
            }}
            QPushButton:hover {{ background-color: {hover_bg}; }}
            QPushButton:disabled {{ background-color: {COLORS['bg_white']}; color: {COLORS['border_light']}; border: 1px solid {COLORS['bg_alt']}; }}
        """)
        
        btn.clicked.connect(lambda: self._run_macros(macros))
        btn.setEnabled(False) # Disabilitato di default
        self._macro_buttons.append(btn)
        parent_layout.addWidget(btn)
        return btn

    def _update_dynamic_path(self):
        year = self.anno_combo.currentText()
        base_network = r"\\192.168.11.251\Database_Tecnico_SMI\Contabilita' strumentale"
        dynamic_path = os.path.join(base_network, year, "CONSUNTIVI", year)
        self.dest_path_edit.setText(dynamic_path)
        self.dest_path_edit.setToolTip(dynamic_path)
        
        try:
            manager = PreventiviGeneratorManager("")
            next_prog = manager.get_next_progressive(dynamic_path)
            self.progressivo_edit.setText(next_prog)
        except Exception:
            self.progressivo_edit.setText("001")

    def _on_generate(self):
        config = config_manager.load_config()
        master_path = config.get("master_preventivi_path", "")
        
        if not master_path or not os.path.exists(master_path):
            ConfirmationDialog.show_error(self, "Configurazione Errata", "Il file Master non è stato configurato nelle Impostazioni.")
            return

        data = {
            "progressivo": self.progressivo_edit.text(),
            "anno_short": self.anno_combo.currentText()[-2:],
            "data": self.data_edit.text(),
            "tcl": self.tcl_combo.currentText(),
            "odc": self.odc_edit.text(),
            "avviso": self.avviso_edit.text(),
            "ordine": self.ordine_edit.text(),
            "stato_attivita": self.stato_combo.currentText(),
            "tipologia_preventivo": self.tipo_prev_combo.currentText(),
            "tipologia_economia": self.tipo_econ_combo.currentText(),
            "descrizione_lavoro": self.desc_lavoro_edit.toPlainText(),
            "descrizione_relazione": self.desc_relazione_edit.toPlainText()
        }

        self.setEnabled(False)
        self.btn_generate.setText("GENERAZIONE IN CORSO...")
        
        self.worker = GeneratoreWorker(master_path, data, self.dest_path_edit.text())
        self.worker.finished_signal.connect(self._on_generate_finished)
        self.worker.start()

    def _on_generate_finished(self, success: bool, result: str):
        self.setEnabled(True)
        self.btn_generate.setText("1. INIZIA: GENERA CONSUNTIVO EXCEL")
        
        if success:
            self.last_generated_file = result
            # Abilita tutti i pulsanti delle macro
            for btn in self._macro_buttons:
                btn.setEnabled(True)
            ConfirmationDialog.show_info(self, "File Generato", f"Il file Excel è pronto:\n\n{result}\n\nPuoi ora lanciare le Macro dai pulsanti appositi.")
        else:
            ConfirmationDialog.show_error(self, "Errore Generazione", result)

    def _run_macros(self, macros: list[str]):
        if not self.last_generated_file or not os.path.exists(self.last_generated_file):
            ConfirmationDialog.show_error(self, "Errore", "Nessun file generato o file non trovato.")
            return
            
        self.setEnabled(False)
        self.macro_worker = MacroWorker(self.last_generated_file, macros)
        self.macro_worker.finished_signal.connect(self._on_macro_finished)
        self.macro_worker.start()

    def _on_macro_finished(self, success: bool, result: str):
        self.setEnabled(True)
        if success:
            ConfirmationDialog.show_info(self, "Macro Eseguite", result)
        else:
            ConfirmationDialog.show_error(self, "Errore Macro", result)
