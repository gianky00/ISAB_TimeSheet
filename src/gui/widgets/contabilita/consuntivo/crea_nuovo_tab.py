"""
SyncroJob - Consuntivo Crea Nuovo Tab
Tab per la generazione di un nuovo consuntivo da template Master.
"""

import os
import time
from datetime import UTC, datetime
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.contabilita.consuntivo.consuntivo_controller import ConsuntivoController
from src.core.contabilita.consuntivo.consuntivo_dto import ConsuntivoDataDTO
from src.core.preventivi_manager import GeneratoreWorker, MacroWorker
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.styles import COLORS
from src.gui.widgets.contabilita.consuntivo.log_widget import OperationLogWidget
from src.gui.widgets.contabilita.consuntivo.workers import ProgWorker
from src.gui.widgets.contabilita.consuntivo.workflow_widgets import WorkflowMapWidget, WorkflowStepButton
from src.gui.widgets.core_widgets import FilterComboBox, PrimaryButton, StandardInput, StandardTextEdit
from src.gui.widgets.modern_card import ModernContentCard


class CreaNuovoTab(QWidget):
    """Tab per la generazione di un nuovo consuntivo con tutti i campiùnecessari."""

    step_clicked = Signal(str)
    _prog_computed = Signal(str)

    def __init__(self, controller: ConsuntivoController, parent: QWidget | None = None) -> None:
        """Inizializza il tab con iniezione del controller."""
        super().__init__(parent)
        self.controller = controller
        self.worker: GeneratoreWorker | None = None
        self.macro_worker: MacroWorker | None = None
        self.prog_worker: ProgWorker | None = None
        self.last_generated_file: str | None = None
        self._last_prog_check = 0.0
        self._cached_prog = ""
        self._prog_computed.connect(self._on_prog_computed)
        self._setup_ui()

    def _on_prog_computed(self, prog: str) -> None:
        self.progressivo_edit.setText(prog)

    def _setup_ui(self) -> None:  # noqa: PLR0915
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 12, 20, 16)
        layout.setSpacing(14)

        # --- CARD 1: SETUP E PERCORSI ---
        card1, card1_lay = self._create_card("IMPOSTAZIONI E DESTINAZIONE")
        config_row = QHBoxLayout()
        config_row.setSpacing(20)

        self.anno_combo = FilterComboBox()
        self.anno_combo.addItems([str(y) for y in range(datetime.now(UTC).year, 2024, -1)])
        self.anno_combo.currentIndexChanged.connect(lambda: self._update_dynamic_path(force=True))
        config_row.addLayout(self._create_input_group("ANNO", self.anno_combo, width=100))

        self.progressivo_edit = StandardInput()
        self.progressivo_edit.setStyleSheet(f"color: {COLORS['teal_accent']}; font-weight: bold;")
        config_row.addLayout(self._create_input_group("PROGRESSIVO", self.progressivo_edit, width=120))

        self.dest_path_edit = StandardInput()
        self.dest_path_edit.setReadOnly(True)
        self.dest_path_edit.setStyleSheet(
            f"background-color: {COLORS['bg_light']}; color: {COLORS['text_muted']};"
        )
        config_row.addLayout(self._create_input_group("PERCORSO DI RETE (AUTOMATICO)", self.dest_path_edit))

        card1_lay.addLayout(config_row)
        layout.addWidget(card1)

        # --- CARD 2: DATI IDENTIFICATIVI ---
        card2, id_layout = self._create_card("DETTAGLI INTERVENTO E CLASSIFICAZIONE")

        row1 = QHBoxLayout()
        row1.setSpacing(15)
        self.data_edit = StandardInput()
        self.data_edit.setText(datetime.now(UTC).strftime("%d/%m/%Y"))
        row1.addLayout(self._create_input_group("DATA (A5)", self.data_edit, width=120))

        self.tcl_combo = FilterComboBox()
        # Carica dinamico da controller (CORE)
        opts = self.controller.get_config_options()
        self.tcl_combo.addItems(opts["tcl"])
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

        self.stato_combo = FilterComboBox()
        self.stato_combo.addItems(opts["stati"])
        row2.addLayout(self._create_input_group("STATO Attività(D11)", self.stato_combo, width=220))

        self.tipo_prev_combo = FilterComboBox()
        self.tipo_prev_combo.addItems(opts["tipologie"])
        row2.addLayout(
            self._create_input_group("TIPOLOGIA PREVENTIVO (D13)", self.tipo_prev_combo, width=220)
        )

        self.tipo_econ_combo = FilterComboBox()
        self.tipo_econ_combo.addItems(opts["economie"])
        row2.addLayout(self._create_input_group("TIPOLOGIA ECONOMIA (E13)", self.tipo_econ_combo, width=220))
        row2.addStretch()
        id_layout.addLayout(row2)
        layout.addWidget(card2)

        # --- CARD 3: DESCRIZIONI ---
        card3, desc_layout = self._create_card("DESCRIZIONE DELLE Attività")

        desc_row = QHBoxLayout()
        desc_row.setSpacing(20)

        self.desc_lavoro_edit = StandardTextEdit()
        self.desc_lavoro_edit.setPlaceholderText("Es. Smontaggio valvola...")
        self.desc_lavoro_edit.setMinimumHeight(80)
        self.desc_lavoro_edit.setMaximumHeight(110)
        desc_row.addLayout(self._create_input_group("DESCRIZIONE LAVORO (A11:A21)", self.desc_lavoro_edit))

        self.desc_relazione_edit = StandardTextEdit()
        self.desc_relazione_edit.setPlaceholderText("Inserisci eventuali note (A32)...")
        self.desc_relazione_edit.setMinimumHeight(80)
        self.desc_relazione_edit.setMaximumHeight(110)
        desc_row.addLayout(self._create_input_group("DESCRIZIONE RELAZIONE (A32)", self.desc_relazione_edit))

        desc_layout.addLayout(desc_row)
        layout.addWidget(card3)

        # --- MAPPA WORKFLOW ---
        self.workflow_map = WorkflowMapWidget()
        self.workflow_map.step_clicked.connect(self._on_workflow_step)
        layout.addWidget(self.workflow_map)

        # --- BOTTONE GENERA ---
        self.btn_generate = PrimaryButton("GENERA CONSUNTIVO EXCEL")
        self.btn_generate.setMinimumHeight(55)
        self.btn_generate.clicked.connect(self._on_generate)
        layout.addWidget(self.btn_generate, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- LOG ---
        self.log_widget = OperationLogWidget()
        self.log_widget.setMinimumHeight(160)
        layout.addWidget(self.log_widget)

        layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Init
        self._update_dynamic_path()

    def _create_card(self, title_text: str) -> tuple[ModernContentCard, QVBoxLayout]:
        card = ModernContentCard()
        lay = card.content_layout
        lay.setContentsMargins(20, 15, 20, 20)
        lay.setSpacing(15)
        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet(
            f"font-weight: 800; font-size: 13px; letter-spacing: 0.5px; "
            f"color: {COLORS['primary_dark']}; border: none;"
        )
        lay.addWidget(title_lbl)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(
            f"background-color: {COLORS['bg_alt']}; border: none; min-height: 1px; max-height: 1px;"
        )
        lay.addWidget(line)
        return card, lay

    def _create_input_group(self, label_text: str, widget: QWidget, width: int = 0) -> QVBoxLayout:
        lay = QVBoxLayout()
        lay.setSpacing(4)
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {COLORS['text_muted']}; border: none;")
        lay.addWidget(lbl)
        if width > 0:
            widget.setFixedWidth(width)
        if isinstance(widget, StandardInput):
            widget.setMinimumHeight(36)
            widget.setMaximumHeight(36)
        lay.addWidget(widget)
        return lay

    def _update_dynamic_path(self, force: bool = False) -> None:
        """Aggiorna il percorso e calcola il progressivo in background."""
        now = time.time()
        year = self.anno_combo.currentText()
        dynamic_path = self.controller.get_dynamic_path(year)

        self.dest_path_edit.setText(dynamic_path)
        self.dest_path_edit.setToolTip(dynamic_path)

        if not force and (now - self._last_prog_check < 60) and self._cached_prog:  # noqa: PLR2004
            self.progressivo_edit.setText(self._cached_prog)
            return

        self._last_prog_check = now

        if self.prog_worker and self.prog_worker.isRunning():
            self.prog_worker.terminate()
            self.prog_worker.wait()

        self.prog_worker = ProgWorker(self.controller, year)
        self.prog_worker.finished.connect(self._on_worker_prog_ready)
        self.prog_worker.start()

    def _on_worker_prog_ready(self, prog: str) -> None:
        """Slot per l'aggiornamento UI dal worker."""
        self._cached_prog = prog
        self.progressivo_edit.setText(prog)

    def _on_generate(self) -> None:
        master_path = self.controller.get_master_path()

        if not master_path or not Path(master_path).exists():
            ConfirmationDialog.show_error(
                self,
                "Configurazione Errata",
                "Il file Master non  stato configurato nelle Impostazioni.",
            )
            return

        dto = ConsuntivoDataDTO(
            progressivo=self.progressivo_edit.text(),
            anno_short=self.anno_combo.currentText()[-2:],
            data=self.data_edit.text(),
            tcl=self.tcl_combo.currentText(),
            odc=self.odc_edit.text(),
            avviso=self.avviso_edit.text(),
            ordine=self.ordine_edit.text(),
            stato_attivita=self.stato_combo.currentText(),
            tipologia_preventivo=self.tipo_prev_combo.currentText(),
            tipologia_economia=self.tipo_econ_combo.currentText(),
            descrizione_lavoro=self.desc_lavoro_edit.toPlainText(),
            descrizione_relazione=self.desc_relazione_edit.toPlainText(),
        )

        self.setEnabled(False)
        self.btn_generate.setText("GENERAZIONE IN CORSO...")
        self.log_widget.append_log("Generazione file in corso...", "step")

        self.worker = GeneratoreWorker(master_path, dto.to_dict(), self.dest_path_edit.text())
        self.worker.finished_signal.connect(self._on_generate_finished)
        self.worker.start()

    def _on_generate_finished(self, success: bool, result: str) -> None:
        self.setEnabled(True)
        self.btn_generate.setText("GENERA CONSUNTIVO EXCEL")

        if success:
            self.last_generated_file = result
            self._last_prog_check = 0  # Forza ricalcolo al prossimo passaggio
            self.log_widget.append_log(f"File generato: {result}", "success")
            ConfirmationDialog.show_info(
                self,
                "File Generato",
                f"Il file Excel  pronto:\n\n{result}\n\nPuoi ora lanciare le Macro dalla mappa workflow.",
            )
        else:
            self.log_widget.append_log(f"Errore: {result}", "error")
            ConfirmationDialog.show_error(self, "Errore Generazione", result)

    def _on_workflow_step(self, step_id: str) -> None:
        macros = self.workflow_map.get_macros_for_step(step_id)
        if not macros:
            return

        if not self.last_generated_file or not Path(self.last_generated_file).exists():
            ConfirmationDialog.show_error(
                self,
                "Errore",
                "Nessun file generato. Genera prima il consuntivo Excel.",
            )
            return

        self.workflow_map.set_step_state(step_id, WorkflowStepButton.State.ACTIVE)
        self.log_widget.append_log(
            f"[SYNC] Esecuzione: {', '.join(macros)} su {os.path.basename(self.last_generated_file)}",
            "step",
        )

        self.setEnabled(False)
        self.macro_worker = MacroWorker(self.last_generated_file, macros)
        self.macro_worker.finished_signal.connect(lambda ok, msg: self._on_macro_finished(ok, msg, step_id))
        self.macro_worker.start()

    def _on_macro_finished(self, success: bool, result: str, step_id: str) -> None:
        self.setEnabled(True)
        if success:
            self.workflow_map.set_step_state(step_id, WorkflowStepButton.State.COMPLETED)
            self.log_widget.append_log(f"✅ {result}", "success")
            ConfirmationDialog.show_info(self, "Macro Eseguite", result)
        else:
            self.workflow_map.set_step_state(step_id, WorkflowStepButton.State.ERROR)
            self.log_widget.append_log(f"❌ {result}", "error")
            ConfirmationDialog.show_error(self, "Errore Macro", result)
