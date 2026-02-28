"""
SyncroJob - Scarico PDL Panel (Refactored)
Pannello coordinato per lo scarico massivo e la stampa dei PDL da SafeWork.
Modularizzato per una migliore manutenibilità.
"""

import logging
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from src.core import config_manager
from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel
from src.gui.styles import COLORS, COMBOBOX_STYLE, LABEL_MUTED, LINEEDIT_STYLE
from src.gui.widgets import EditableDataTable
from src.gui.widgets.core_widgets import (
    FilterComboBox,
    IconButton,
    StandardCheckBox,
    StandardInput,
)
from src.gui.widgets.safework.status_list import StatusListWidget
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.printing import get_installed_printers

logger = logging.getLogger(__name__)


class ScaricoPDLPanel(BaseBotPanel):
    """Orchestratore per lo scarico PDL con gestione parametri e stati riga."""

    def __init__(self, parent=None):
        super().__init__(
            bot_id="scarico_pdl",
            bot_name="Scarico PDL",
            bot_description="Scarica e stampa i Permessi di Lavoro da SafeWork.",
            parent=parent,
        )
        self._setup_content()
        QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self):
        from src.bots.safework.pdl.bot import SafeWorkPDLBot

        return SafeWorkPDLBot

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            logger.error(f"Error loading data: {e}")

    def _setup_content(self):
        # 1. Parametri
        self.params_container = QFrame()
        self.params_container.setObjectName("filterBar")
        self.params_container.setStyleSheet(
            f"QFrame#filterBar {{ background: {COLORS['bg_white']}; border: 1px solid {COLORS['border_light']}; border-radius: 12px; }}"
        )
        params_lay = QHBoxLayout(self.params_container)
        params_lay.setContentsMargins(15, 10, 15, 10)
        params_lay.setSpacing(20)

        # Stampa
        v_print = QVBoxLayout()
        v_print.setSpacing(4)
        lbl_p = QLabel("OPZIONI STAMPA")
        lbl_p.setStyleSheet(LABEL_MUTED)
        v_print.addWidget(lbl_p)
        h_p = QHBoxLayout()
        h_p.setSpacing(10)
        self.check_stampa = StandardCheckBox("Attiva Stampa")
        self.combo_stampanti = FilterComboBox()
        self.combo_stampanti.addItems(get_installed_printers())
        self.combo_stampanti.setStyleSheet(COMBOBOX_STYLE)
        for w in (self.check_stampa, self.combo_stampanti):
            h_p.addWidget(w)
        v_print.addLayout(h_p)
        params_lay.addLayout(v_print)

        # Destinazione
        v_dest = QVBoxLayout()
        v_dest.setSpacing(4)
        lbl_d = QLabel("CARTELLA DESTINAZIONE")
        lbl_d.setStyleSheet(LABEL_MUTED)
        v_dest.addWidget(lbl_d)
        h_d = QHBoxLayout()
        h_d.setSpacing(5)
        self.edit_dest = StandardInput()
        self.edit_dest.setPlaceholderText("Seleziona cartella...")
        self.edit_dest.setStyleSheet(LINEEDIT_STYLE)
        self.btn_browse = IconButton()
        self.btn_browse.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), COLORS["text_dark"]))
        self.btn_browse.setToolTip("Sfoglia...")
        self.btn_browse.clicked.connect(self._on_browse_clicked)
        h_d.addWidget(self.edit_dest)
        h_d.addWidget(self.btn_browse)
        v_dest.addLayout(h_d)
        params_lay.addLayout(v_dest)

        params_lay.addStretch()
        lay = self.layout()
        if isinstance(lay, QVBoxLayout):
            lay.insertWidget(1, self.params_container)

        # 2. Tabella e Stati
        content_lay = QHBoxLayout()
        content_lay.setSpacing(10)
        cols = [
            {"name": "N° PDL", "type": "text", "default": ""},
            {"name": "Note / Esito", "type": "text", "default": ""},
        ]
        self.data_table = EditableDataTable(cols)
        self.data_table.data_changed.connect(self._update_status_list)

        v_status = QVBoxLayout()
        v_status.setContentsMargins(0, 35, 0, 0)
        self.status_list = StatusListWidget()
        self.status_list.setFixedWidth(40)
        v_status.addWidget(self.status_list)
        v_status.addStretch()

        content_lay.addLayout(v_status)
        content_lay.addWidget(self.data_table)

        lay2 = self.layout()
        if isinstance(lay2, QVBoxLayout):
            lay2.insertLayout(2, content_lay)

    def _update_status_list(self):
        count = self.data_table.table.rowCount()
        self.status_list.initialize_rows(count, self.data_table.table.rowHeight(0) or 30)

    def _on_browse_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "Seleziona Cartella Destinazione")
        if path:
            self.edit_dest.setText(path)

    def _load_saved_data(self):
        config = config_manager.load_config()
        data = config.get("last_pdl_data", [])
        if data:
            self.data_table.set_data(data)

        p_cfg = config.get("last_pdl_params", {})
        self.check_stampa.setChecked(p_cfg.get("stampa", False))
        if p_cfg.get("stampante"):
            self.combo_stampanti.setCurrentText(p_cfg["stampante"])
        self.edit_dest.setText(p_cfg.get("destinazione", str(Path.home() / "Downloads")))
        self._update_status_list()

    def _get_bot_data(self):
        items = self.data_table.get_data()
        if not items:
            ConfirmationDialog.show_warning(
                self, "Tabella Vuota", "Inserisci almeno un numero PDL da processare."
            )
            return None

        # Salvataggio persistente
        config_manager.set_config_value("last_pdl_data", items)
        config_manager.set_config_value(
            "last_pdl_params",
            {
                "stampa": self.check_stampa.isChecked(),
                "stampante": self.combo_stampanti.currentText(),
                "destinazione": self.edit_dest.text(),
            },
        )

        return [
            {
                "pdl_number": it["n°_pdl"],
                "stampa": self.check_stampa.isChecked(),
                "stampante": self.combo_stampanti.currentText(),
                "output_dir": self.edit_dest.text(),
            }
            for it in items
        ]

    def _on_bot_finished(self, success: bool):
        super()._on_bot_finished(success)
        if success:
            ToastManager.instance().show("Processo PDL Completato!", "success")

    def on_step_completed(self, step_idx: int, success: bool, message: str):
        self.status_list.update_status(step_idx, success)
        if not success:
            logger.error(f"Errore riga {step_idx}: {message}")
