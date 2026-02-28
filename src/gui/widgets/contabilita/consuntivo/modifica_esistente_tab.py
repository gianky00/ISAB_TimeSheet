"""
SyncroJob - Consuntivo Modifica Esistente Tab
Tab intelligente per la scansione, auto-fill e manipolazione di file esistenti.
"""

import os
from contextlib import suppress
from datetime import datetime
from typing import cast

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.preventivi_manager import MacroWorker
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.styles import COLORS
from src.gui.widgets.contabilita.consuntivo.log_widget import OperationLogWidget
from src.gui.widgets.contabilita.consuntivo.workflow_widgets import WorkflowMapWidget, WorkflowStepButton
from src.gui.widgets.modern_card import ModernContentCard


class ModificaEsistenteTab(QWidget):
    """Tab intelligente: scansiona la directory preventivi, elenca i file .xlsm,
    e auto-compila i campi leggendo le informazioni dal file selezionato."""

    step_clicked = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.macro_worker: MacroWorker | None = None
        self.loaded_file: str | None = None
        self._setup_ui()
        QTimer.singleShot(500, self._scan_directory)

    def _setup_ui(self) -> None:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 12, 20, 16)
        layout.setSpacing(14)

        # --- CARD: SELEZIONE FILE ---
        file_card = ModernContentCard()
        file_lay = file_card.content_layout
        file_lay.setContentsMargins(20, 15, 20, 20)
        file_lay.setSpacing(12)

        file_title = QLabel("📂 SELEZIONE CONSUNTIVO")
        file_title.setStyleSheet(
            f"font-weight: 800; font-size: 13px; letter-spacing: 0.5px; "
            f"color: {COLORS['primary_dark']}; border: none;"
        )
        file_lay.addWidget(file_title)

        top_row = QHBoxLayout()
        top_row.setSpacing(15)
        anno_lbl = QLabel("ANNO")
        anno_lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {COLORS['text_muted']}; border: none;")
        top_row.addWidget(anno_lbl)
        self.anno_combo = QComboBox()
        self.anno_combo.addItems([str(y) for y in range(datetime.now().year, 2024, -1)])
        self.anno_combo.setFixedWidth(100)
        self.anno_combo.currentIndexChanged.connect(self._scan_directory)
        top_row.addWidget(self.anno_combo)
        self._dir_label = QLabel("")
        self._dir_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; border: none;")
        top_row.addWidget(self._dir_label, 1)
        scan_btn = QPushButton("🔄 Aggiorna")
        scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        scan_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['teal_accent']}; color: white; border: none;
                border-radius: 6px; padding: 6px 16px; font-weight: 600; font-size: 12px;
            }}
            QPushButton:hover {{ background: #2b9e95; }}
        """)
        scan_btn.clicked.connect(self._scan_directory)
        top_row.addWidget(scan_btn)
        file_lay.addLayout(top_row)

        file_sel_row = QHBoxLayout()
        file_sel_row.setSpacing(10)
        file_lbl = QLabel("FILE")
        file_lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {COLORS['text_muted']}; border: none;")
        file_sel_row.addWidget(file_lbl)
        self.file_combo = QComboBox()
        self.file_combo.setMinimumHeight(38)
        self.file_combo.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {COLORS['border_light']}; border-radius: 8px;
                padding: 6px 12px; background: {COLORS['bg_white']};
                color: {COLORS['text_dark']}; font-size: 13px; font-weight: 600;
            }}
            QComboBox:focus {{ border: 2px solid {COLORS['teal_accent']}; }}
            QComboBox::drop-down {{ width: 30px; border-left: 1px solid {COLORS['border_light']}; }}
        """)
        self.file_combo.currentIndexChanged.connect(self._on_file_selected)
        file_sel_row.addWidget(self.file_combo, 1)
        self._file_count_label = QLabel("0 file trovati")
        self._file_count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; border: none;")
        file_sel_row.addWidget(self._file_count_label)
        file_lay.addLayout(file_sel_row)
        layout.addWidget(file_card)

        # --- CARD: DATI ESTRATTI ---
        data_card = ModernContentCard()
        data_lay = data_card.content_layout
        data_lay.setContentsMargins(20, 15, 20, 20)
        data_lay.setSpacing(12)
        data_title = QLabel("📋 DATI ESTRATTI DAL FILE")
        data_title.setStyleSheet(
            f"font-weight: 800; font-size: 13px; letter-spacing: 0.5px; "
            f"color: {COLORS['primary_dark']}; border: none;"
        )
        data_lay.addWidget(data_title)
        self._status_label = QLabel("Seleziona un file per visualizzare i dati.")
        self._status_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px; border: none;")
        data_lay.addWidget(self._status_label)

        grid = QGridLayout()
        grid.setSpacing(10)
        self._fields: dict[str, QLineEdit] = {}
        field_defs = [
            ("Data (A5)", "data", 0, 0), ("TCL (A7)", "tcl", 0, 1),
            ("ODC (B5)", "odc", 0, 2), ("Avviso (C7)", "avviso", 0, 3),
            ("Ordine (C5)", "ordine", 1, 0), ("Stato (D11)", "stato", 1, 1),
            ("Tipo Prev. (D13)", "tipo_prev", 1, 2), ("Tipo Econ. (E13)", "tipo_econ", 1, 3),
            ("Progressivo", "progressivo", 2, 0),
        ]
        for label, key, row, col in field_defs:
            lbl = QLabel(label)
            lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {COLORS['text_muted']}; border: none;")
            inp = QLineEdit()
            inp.setStyleSheet(
                f"background-color: {COLORS['bg_white']}; color: {COLORS['text_dark']}; "
                f"border: 1px solid {COLORS['border_light']}; border-radius: 6px; "
                f"padding: 6px 10px; font-size: 13px;"
            )
            inp.setMinimumHeight(32)
            self._fields[key] = inp
            v = QVBoxLayout()
            v.setSpacing(2)
            v.addWidget(lbl)
            v.addWidget(inp)
            grid.addLayout(v, row, col)
        data_lay.addLayout(grid)

        desc_lbl = QLabel("Descrizione Lavoro (A11:A21)")
        desc_lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {COLORS['text_muted']}; border: none;")
        data_lay.addWidget(desc_lbl)
        self._desc_lavoro_display = QTextEdit()
        self._desc_lavoro_display.setMaximumHeight(80)
        self._desc_lavoro_display.setStyleSheet(
            f"background-color: #f0f9f8; color: {COLORS['text_dark']}; "
            f"border: 1px solid {COLORS['border_light']}; border-radius: 6px; "
            f"padding: 6px; font-size: 12px;"
        )
        data_lay.addWidget(self._desc_lavoro_display)

        # Bottone salva modifiche
        self._save_btn = QPushButton("💾 Salva Modifiche nel File Excel")
        self._save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save_btn.setMinimumHeight(42)
        self._save_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self._save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['teal_accent']}; color: white;
                border: none; border-radius: 8px; font-weight: 600;
            }}
            QPushButton:hover {{ background-color: #2b9e95; }}
            QPushButton:disabled {{ background-color: {COLORS['border_light']}; color: {COLORS['text_muted']}; }}
        """)
        self._save_btn.clicked.connect(self._save_to_file)
        data_lay.addWidget(self._save_btn)

        layout.addWidget(data_card)

        # Workflow
        self.workflow_map = WorkflowMapWidget()
        self.workflow_map.step_clicked.connect(self._on_workflow_step)
        layout.addWidget(self.workflow_map)

        # Log
        self.log_widget = OperationLogWidget()
        self.log_widget.setMinimumHeight(160)
        layout.addWidget(self.log_widget)

        layout.addStretch()
        scroll.setWidget(content)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _get_dynamic_dir(self) -> str:
        year = self.anno_combo.currentText()
        base = config_manager.get_config_value("base_network_path_preventivi", r"\\192.168.11.251\Database_Tecnico_SMI\Contabilita' strumentale")
        return os.path.join(base, year, "CONSUNTIVI", year)

    def _scan_directory(self) -> None:
        directory = self._get_dynamic_dir()
        self._dir_label.setText(directory)
        self._dir_label.setToolTip(directory)
        self.file_combo.blockSignals(True)
        self.file_combo.clear()
        try:
            if os.path.isdir(directory):
                files = sorted(
                    [f for f in os.listdir(directory) if f.lower().endswith(".xlsm")],
                    reverse=True,
                )
                for f in files:
                    full = os.path.join(directory, f)
                    try:
                        size_kb = os.path.getsize(full) / 1024
                        self.file_combo.addItem(f"{f}  ({size_kb:.0f} KB)", full)
                    except OSError:
                        self.file_combo.addItem(f, full)
                count = len(files)
                self._file_count_label.setText(f"{count} file trovati")
                color = "#2E7D32" if count > 0 else COLORS["text_muted"]
                self._file_count_label.setStyleSheet(
                    f"color: {color}; font-size: 11px; font-weight: 600; border: none;"
                )
                self.log_widget.append_log(f"📂 Scansione: {count} file in {directory}", "info")
            else:
                self._file_count_label.setText("Directory non raggiungibile")
                self._file_count_label.setStyleSheet(
                    f"color: {COLORS['error_red']}; font-size: 11px; border: none;"
                )
                self.log_widget.append_log(f"⚠️ Directory non trovata: {directory}", "warning")
        except Exception as e:
            self._file_count_label.setText("Errore scansione")
            self.log_widget.append_log(f"❌ Errore scansione: {e}", "error")
        self.file_combo.blockSignals(False)
        if self.file_combo.count() > 0:
            self._on_file_selected(0)

    def _on_file_selected(self, index: int) -> None:
        if index < 0 or self.file_combo.count() == 0:
            return
        file_path = self.file_combo.itemData(index)
        if not file_path or not os.path.exists(file_path):
            self._status_label.setText("⚠️ File non trovato.")
            return
        self.loaded_file = file_path
        self.log_widget.append_log(f"📄 Lettura: {os.path.basename(file_path)}", "step")
        self._auto_fill_from_file(file_path)

    def _auto_fill_from_file(self, file_path: str) -> None:
        try:
            import openpyxl
            wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
            sheet = None
            for name in ["inserimento dati", "Inserimento Dati", "inserimento_dati"]:
                if name in wb.sheetnames:
                    sheet = wb[name]
                    break
            if sheet is None and wb.sheetnames:
                sheet = wb[wb.sheetnames[0]]
            if sheet is None:
                self._status_label.setText("⚠️ Nessun foglio trovato.")
                wb.close()
                return

            def cv(addr: str) -> str:
                try:
                    v = sheet[addr].value
                    if v is None:
                        return ""
                    if hasattr(v, 'strftime'):
                        return cast("str", v.strftime("%d/%m/%Y"))
                    return str(v).strip()
                except Exception:
                    return ""

            self._fields["data"].setText(cv("A5"))
            self._fields["tcl"].setText(cv("A7"))
            self._fields["odc"].setText(cv("B5"))
            self._fields["avviso"].setText(cv("C7"))
            self._fields["ordine"].setText(cv("C5"))
            self._fields["stato"].setText(cv("D11"))
            self._fields["tipo_prev"].setText(cv("D13"))
            self._fields["tipo_econ"].setText(cv("E13"))

            prog = ""
            if "rif.VBA" in wb.sheetnames:
                with suppress(Exception):
                    prog_val = wb["rif.VBA"]["A4"].value
                    if prog_val:
                        prog = str(prog_val).strip()
            self._fields["progressivo"].setText(prog)

            lines = [cv(f"A{r}") for r in range(11, 22) if cv(f"A{r}")]
            self._desc_lavoro_display.setPlainText("\n".join(lines))
            wb.close()

            n = sum(1 for f in self._fields.values() if f.text())
            self._status_label.setText(f"✅ {n} campi compilati automaticamente")
            self._status_label.setStyleSheet("color: #2E7D32; font-size: 12px; font-weight: 600; border: none;")
            self.log_widget.append_log(f"✅ Auto-fill completato: {n} campi", "success")
        except ImportError:
            self._status_label.setText("⚠️ openpyxl non disponibile")
            self.log_widget.append_log("⚠️ openpyxl non installato", "warning")
        except Exception as e:
            self._status_label.setText(f"❌ Errore lettura: {e}")
            self.log_widget.append_log(f"❌ Errore: {e}", "error")

    def _save_to_file(self) -> None:
        """Salva i valori dei campi editati nel file Excel."""
        if not self.loaded_file or not os.path.exists(self.loaded_file):
            ConfirmationDialog.show_error(self, "Errore", "Nessun file selezionato.")
            return

        try:
            import openpyxl
            wb = openpyxl.load_workbook(self.loaded_file, keep_vba=True)

            sheet = None
            for name in ["inserimento dati", "Inserimento Dati", "inserimento_dati"]:
                if name in wb.sheetnames:
                    sheet = wb[name]
                    break
            if sheet is None and wb.sheetnames:
                sheet = wb[wb.sheetnames[0]]
            if sheet is None:
                ConfirmationDialog.show_error(self, "Errore", "Foglio non trovato.")
                wb.close()
                return

            cell_map = {
                "data": "A5", "tcl": "A7", "odc": "B5", "avviso": "C7",
                "ordine": "C5", "stato": "D11", "tipo_prev": "D13", "tipo_econ": "E13",
            }

            for key, addr in cell_map.items():
                val = self._fields[key].text().strip()
                if val:
                    sheet[addr] = val

            # Descrizione lavoro (A11:A21)
            desc_lines = self._desc_lavoro_display.toPlainText().split("\n")
            for i in range(11, 22):
                idx = i - 11
                if idx < len(desc_lines):
                    sheet[f"A{i}"] = desc_lines[idx]
                else:
                    sheet[f"A{i}"] = ""

            wb.save(self.loaded_file)
            wb.close()

            self.log_widget.append_log("💾 Modifiche salvate con successo!", "success")
            self._status_label.setText("✅ Modifiche salvate nel file Excel")
            self._status_label.setStyleSheet("color: #2E7D32; font-size: 12px; font-weight: 600; border: none;")
            ConfirmationDialog.show_info(
                self, "Salvato", f"Le modifiche sono state salvate in:\n{os.path.basename(self.loaded_file)}"
            )
        except ImportError:
            ConfirmationDialog.show_error(self, "Errore", "openpyxl non disponibile.")
        except Exception as e:
            self.log_widget.append_log(f"❌ Errore salvataggio: {e}", "error")
            ConfirmationDialog.show_error(self, "Errore Salvataggio", str(e))

    def _on_workflow_step(self, step_id: str) -> None:
        macros = self.workflow_map.get_macros_for_step(step_id)
        if not macros:
            return
        if not self.loaded_file or not os.path.exists(self.loaded_file):
            ConfirmationDialog.show_error(self, "Errore", "Nessun file selezionato.")
            return
        self.workflow_map.set_step_state(step_id, WorkflowStepButton.State.ACTIVE)
        self.log_widget.append_log(
            f"🔄 {', '.join(macros)} su {os.path.basename(self.loaded_file)}", "step",
        )
        self.setEnabled(False)
        self.macro_worker = MacroWorker(self.loaded_file, macros)
        self.macro_worker.finished_signal.connect(
            lambda ok, msg: self._on_macro_finished(ok, msg, step_id)
        )
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
