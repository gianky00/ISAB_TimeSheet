import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QPushButton, QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import PrimaryButton, StandardInput
from src.core.preventivi_manager import PreventiviGeneratorManager, MacroWorker
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog

class MappaInterattiva(QFrame):
    """
    Rappresentazione visuale dei pulsanti Macro 1-5 ispirata alla mappa VBA.
    Usa un layout a griglia/flowchart per simulare il flusso.
    """
    macro_requested = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {COLORS['bg_light']}; border-radius: 12px; border: 1px dashed {COLORS['border_light']};")
        self.setMinimumHeight(350)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Riga Superiore (1-5)
        top_row = QHBoxLayout()
        top_row.setSpacing(15)
        
        self.btn1 = self._create_node("1", "CARICA\nDATI", ["CaricaDatiMultiplo"])
        self.btn2 = self._create_node("2", "ELABORA\nDATI", ["elaboraDati"])
        self.btn3 = self._create_node("3", "COMPILA\nCONSUNTIVO", ["EseguiTuttiSmista"])
        self.btn4 = self._create_node("4", "VERIFICA", ["VerificaConsuntivo"])
        self.btn5 = self._create_node("5", "STAMPA", ["verificaEstampaFogli"])
        
        for b in [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5]:
            top_row.addWidget(b)
        layout.addLayout(top_row)

        # Riga Centrale (Connettori)
        conn_row = QHBoxLayout()
        arrow_lbl = QLabel("▼")
        arrow_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow_lbl.setStyleSheet(f"color: {COLORS['border_light']}; font-size: 24px; border: none;")
        conn_row.addWidget(arrow_lbl)
        layout.addLayout(conn_row)

        # Riga Inferiore (Azioni Composte)
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)
        
        self.btn_sviluppa = self._create_node("🚀", "SVILUPPA\n(1 -> 4)", 
                                              ["CaricaDatiMultiplo", "elaboraDati", "EseguiTuttiSmista", "VerificaConsuntivo"], 
                                              is_primary=True)
        self.btn_tutto = self._create_node("✅", "ESEGUI\nTUTTO", 
                                           ["CaricaDatiMultiplo", "elaboraDati", "EseguiTuttiSmista", "VerificaConsuntivo", "verificaEstampaFogli"], 
                                           is_primary=True)
        
        bottom_row.addStretch()
        bottom_row.addWidget(self.btn_sviluppa)
        bottom_row.addWidget(self.btn_tutto)
        bottom_row.addStretch()
        layout.addLayout(bottom_row)

        self.nodes = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn_sviluppa, self.btn_tutto]
        self.set_active(False)

    def _create_node(self, num: str, text: str, macros: list, is_primary: bool = False):
        container = QFrame()
        bg = "#27ae60" if is_primary else "#2ecc71"
        container.setFixedSize(140, 100)
        container.setCursor(Qt.CursorShape.PointingHandCursor)
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border: 2px solid white;
                border-radius: 8px;
            }}
            QFrame:hover {{ background-color: #27ae60; border: 2px solid {COLORS['teal_accent']}; }}
        """)
        
        l = QVBoxLayout(container)
        l.setContentsMargins(5, 5, 5, 5)
        l.setSpacing(2)
        
        n_lbl = QLabel(num)
        n_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        n_lbl.setStyleSheet("color: rgba(255,255,255,0.7); font-weight: 800; font-size: 10px; border: none;")
        l.addWidget(n_lbl)
        
        t_lbl = QLabel(text)
        t_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t_lbl.setWordWrap(True)
        t_lbl.setStyleSheet("color: white; font-weight: 900; font-size: 12px; border: none; line-height: 14px;")
        l.addWidget(t_lbl)
        
        # Rendiamo il container cliccabile
        container.mousePressEvent = lambda e: self.macro_requested.emit(macros)
        return container

    def set_active(self, active: bool):
        self.setEnabled(active)
        opacity = "1.0" if active else "0.4"
        self.setStyleSheet(f"background-color: {COLORS['bg_light']}; border-radius: 12px; border: 1px dashed {COLORS['border_light']}; opacity: {opacity};")

class TabGestioneEsistente(QWidget):
    """Tab per caricare un file esistente e manipolarlo via macro."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None
        self.macro_worker = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Selettore File
        file_card = QFrame()
        file_card.setStyleSheet(f"background-color: {COLORS['bg_white']}; border-radius: 8px; border: 1px solid {COLORS['border_light']};")
        file_lay = QHBoxLayout(file_card)
        
        self.path_edit = StandardInput()
        self.path_edit.setPlaceholderText("Seleziona un file Consuntivo esistente (.xlsm)...")
        self.path_edit.setReadOnly(True)
        file_lay.addWidget(self.path_edit)
        
        btn_browse = QPushButton("SFOGLIA")
        btn_browse.setStyleSheet(f"background-color: {COLORS['bg_alt']}; padding: 8px 15px; font-weight: bold;")
        btn_browse.clicked.connect(self._browse_file)
        file_lay.addWidget(btn_browse)
        layout.addWidget(file_card)

        # Mappa Interattiva
        lbl_mappa = QLabel("MAPPA INTERATTIVA AUTOMAZIONI")
        lbl_mappa.setStyleSheet(f"font-weight: 800; font-size: 12px; color: {COLORS['text_muted']};")
        layout.addWidget(lbl_mappa)
        
        self.mappa = MappaInterattiva()
        self.mappa.macro_requested.connect(self._run_macros)
        layout.addWidget(self.mappa)

        layout.addStretch()

    def _browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleziona Consuntivo", "", "Excel Macro-Enabled (*.xlsm)")
        if file:
            self.current_file = file
            self.path_edit.setText(file)
            self.mappa.set_active(True)

    def _run_macros(self, macros: list):
        if not self.current_file: return
        self.setEnabled(False)
        self.macro_worker = MacroWorker(self.current_file, macros)
        self.macro_worker.finished_signal.connect(self._on_macro_finished)
        self.macro_worker.start()

    def _on_macro_finished(self, success: bool, msg: str):
        self.setEnabled(True)
        if success:
            ConfirmationDialog.show_info(self, "Completato", msg)
        else:
            ConfirmationDialog.show_error(self, "Errore Macro", msg)
