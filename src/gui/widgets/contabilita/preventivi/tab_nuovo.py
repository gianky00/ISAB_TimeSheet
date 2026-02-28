import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextEdit, QScrollArea, QFrame
)
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import PrimaryButton, StandardInput
from src.gui.widgets.contabilita.preventivi.base_form import FormUtils
from src.core.preventivi_manager import PreventiviGeneratorManager, GeneratoreWorker
from src.core import config_manager
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog

class TabNuovoPreventivo(QWidget):
    """Form per la creazione di un nuovo preventivo da template Master."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)

        # 1. SETUP CARD
        config_card, config_lay = FormUtils.create_card("IMPOSTAZIONI E DESTINAZIONE")
        config_row = QHBoxLayout()
        self.anno_combo = QComboBox()
        self.anno_combo.addItems([str(y) for y in range(datetime.now().year, 2020, -1)])
        self.anno_combo.currentIndexChanged.connect(self._update_dynamic_path)
        config_row.addLayout(FormUtils.create_input_group("ANNO", self.anno_combo, width=100))

        self.progressivo_edit = StandardInput()
        config_row.addLayout(FormUtils.create_input_group("PROGRESSIVO", self.progressivo_edit, width=120))

        self.dest_path_edit = StandardInput()
        self.dest_path_edit.setReadOnly(True)
        self.dest_path_edit.setStyleSheet(f"background-color: {COLORS['bg_light']}; color: {COLORS['text_muted']};")
        config_row.addLayout(FormUtils.create_input_group("PERCORSO DI RETE (AUTOMATICO)", self.dest_path_edit))
        config_lay.addLayout(config_row)
        scroll_layout.addWidget(config_card)

        # 2. IDENTIFICATIVI CARD
        id_card, id_lay = FormUtils.create_card("DETTAGLI INTERVENTO E CLASSIFICAZIONE")
        r1 = QHBoxLayout()
        self.data_edit = StandardInput()
        self.data_edit.setText(datetime.now().strftime("%d/%m/%Y"))
        r1.addLayout(FormUtils.create_input_group("DATA (A5)", self.data_edit, width=120))
        self.tcl_combo = QComboBox()
        self.tcl_combo.addItems(["MESSINA I.", "AGUSTA D.", "CALDARELLA F.", "PREZZAVENTO M.", "BOSCO F.", "RUGGIERI F.", "BARBAGALLO G."])
        r1.addLayout(FormUtils.create_input_group("TCL (A7)", self.tcl_combo, width=180))
        self.odc_edit = StandardInput()
        r1.addLayout(FormUtils.create_input_group("ODC (B5)", self.odc_edit, width=140))
        self.avviso_edit = StandardInput()
        r1.addLayout(FormUtils.create_input_group("AVVISO (C7)", self.avviso_edit, width=140))
        self.ordine_edit = StandardInput()
        r1.addLayout(FormUtils.create_input_group("ORDINE (C5)", self.ordine_edit, width=140))
        id_lay.addLayout(r1)

        r2 = QHBoxLayout()
        self.stato_combo = QComboBox()
        self.stato_combo.addItems(["ATTIVITA' DA COMPLETARE", "IN ATTESA TCL", "RICHIESTA ODC MIDOLO", "CONTABILIZZATA"])
        r2.addLayout(FormUtils.create_input_group("STATO ATTIVITÀ (D11)", self.stato_combo, width=220))
        self.tipo_prev_combo = QComboBox()
        self.tipo_prev_combo.addItems(["MISURA", "SQUADRA", "CHIAMATA", "FORNITURA", "PREVENTIVO"])
        r2.addLayout(FormUtils.create_input_group("TIPOLOGIA PREVENTIVO (D13)", self.tipo_prev_combo, width=220))
        self.tipo_econ_combo = QComboBox()
        self.tipo_econ_combo.addItems(["SQUADRA GIORNALIERA", "SQUADRA SETTIMANALE", "CONSTATAZIONE PURA"])
        r2.addLayout(FormUtils.create_input_group("TIPOLOGIA ECONOMIA (E13)", self.tipo_econ_combo, width=220))
        id_lay.addLayout(r2)
        scroll_layout.addWidget(id_card)

        # 3. DESCRIZIONI CARD
        desc_card, desc_lay = FormUtils.create_card("DESCRIZIONE DELLE ATTIVITÀ")
        r3 = QHBoxLayout()
        self.desc_lavoro_edit = QTextEdit()
        self.desc_lavoro_edit.setMinimumHeight(100)
        r3.addLayout(FormUtils.create_input_group("DESCRIZIONE LAVORO (A11:A21)", self.desc_lavoro_edit))
        self.desc_relazione_edit = QTextEdit()
        self.desc_relazione_edit.setMinimumHeight(100)
        r3.addLayout(FormUtils.create_input_group("DESCRIZIONE RELAZIONE (A32)", self.desc_relazione_edit))
        desc_lay.addLayout(r3)
        scroll_layout.addWidget(desc_card)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # GENERATE BUTTON
        self.btn_generate = PrimaryButton("GENERA CONSUNTIVO EXCEL")
        self.btn_generate.clicked.connect(self._on_generate)
        main_layout.addWidget(self.btn_generate)

        self._update_dynamic_path()

    def _update_dynamic_path(self):
        year = self.anno_combo.currentText()
        base = r"\\192.168.11.251\Database_Tecnico_SMI\Contabilita' strumentale"
        path = os.path.join(base, year, "CONSUNTIVI", year)
        self.dest_path_edit.setText(path)
        try:
            mgr = PreventiviGeneratorManager()
            self.progressivo_edit.setText(mgr.get_next_progressive(path))
        except: pass

    def _on_generate(self):
        config = config_manager.load_config()
        master = config.get("master_preventivi_path", "")
        if not os.path.exists(master):
            ConfirmationDialog.show_error(self, "Configurazione", "Master non trovato nelle impostazioni.")
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
        self.worker = GeneratoreWorker(master, data, self.dest_path_edit.text())
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.start()

    def _on_finished(self, success: bool, res: str):
        self.setEnabled(True)
        if success:
            ConfirmationDialog.show_info(self, "Successo", f"File creato: {res}")
            # Potremmo emettere un segnale per passare al Tab Gestione
        else:
            ConfirmationDialog.show_error(self, "Errore", res)
