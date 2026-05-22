from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    FilterComboBox,
    StandardCheckBox,
    StandardTable,
)
from src.gui.widgets.modern_button import ModernButton


class TimbratureSettingsTab(QWidget):
    """
    Tab per la gestione delle impostazioni (Dipendenti, Reparti, Cantieri).
    """

    settings_changed = Signal()  # Emesso quando cambiano le liste o i dati

    def __init__(self, storage: Any, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.storage = storage
        self.lists = self.storage.get_lists()
        self.reparti: list[str] = self.lists.get("reparti", [])
        self.cantieri: list[str] = self.lists.get("cantieri", [])
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Header Controls
        header_layout = QHBoxLayout()
        info = QLabel("Gestione Dipendenti")
        info.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(info)
        header_layout.addStretch()

        # Open Settings Button
        open_settings_btn = ModernButton(
            "Gestisci Liste",
            variant=ModernButton.Variant.SECONDARY,
            size=ModernButton.Size.SMALL,
        )
        open_settings_btn.setToolTip("Gestisci reparti e cantieri nelle Impostazioni")
        open_settings_btn.clicked.connect(self._open_settings_request)
        header_layout.addWidget(open_settings_btn)
        layout.addLayout(header_layout)

        sub = QLabel("Assegna Reparto e Cantiere ai dipendenti. Modifiche salvate automaticamente.")
        sub.setStyleSheet(f"color: {COLORS['text_muted']}; margin-bottom: 5px;")
        layout.addWidget(sub)

        # Filters
        filter_layout = QHBoxLayout()
        self.filter_empty_cb = StandardCheckBox("Mostra solo dati mancanti (Vuoti)")
        config = config_manager.load_config()
        self.filter_empty_cb.setChecked(bool(config.get("timbrature_filter_empty_only", False)))
        self.filter_empty_cb.stateChanged.connect(lambda _: self._on_filter_empty_changed())
        filter_layout.addWidget(self.filter_empty_cb)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Table
        self.settings_table = StandardTable()
        self.settings_table.setStyleSheet(f"""
      QTableWidget {{
        gridline-color: {COLORS["bg_alt"]};
        selection-background-color: {COLORS["table_selection_bg"]};
        selection-color: {COLORS["text_dark"]};
        background-color: {COLORS["bg_white"]};
      }}
      QHeaderView::section {{
        background-color: {COLORS["bg_light"]};
        color: {COLORS["text_dark"]};
        padding: 8px;
        font-weight: bold;
        border: none;
        border-bottom: 1px solid {COLORS["border_light"]};
      }}
    """)
        v_header = self.settings_table.verticalHeader()
        if v_header is not None:
            v_header.setVisible(False)
        self.settings_table.setColumnCount(4)
        self.settings_table.setHorizontalHeaderLabels(["Nome", "Cognome", "Reparto", "Cantiere"])
        h_header = self.settings_table.horizontalHeader()
        if h_header is not None:
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.settings_table)

    def load_data(self) -> None:
        """Carica i dati dei dipendenti nella tabella."""
        employees = self.storage.get_employees()
        show_empty_only = self.filter_empty_cb.isChecked()

        # Reload cache lists
        self.lists = self.storage.get_lists()
        self.reparti = self.lists.get("reparti", [])
        self.cantieri = self.lists.get("cantieri", [])

        self.settings_table.blockSignals(True)
        self.settings_table.setRowCount(0)

        filtered_employees = []
        for emp in employees:
            if show_empty_only and emp["reparto"] and emp["cantiere"]:
                continue
            filtered_employees.append(emp)

        for i, emp in enumerate(filtered_employees):
            self.settings_table.insertRow(i)
            self._create_row(i, emp)

        self.settings_table.blockSignals(False)

    def _create_row(self, row_idx: int, emp: dict[str, Any]) -> None:
        # Nome/Cognome Readonly
        item_nome = QTableWidgetItem(str(emp["nome"]))
        item_nome.setFlags(item_nome.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.settings_table.setItem(row_idx, 0, item_nome)

        item_cognome = QTableWidgetItem(str(emp["cognome"]))
        item_cognome.setFlags(item_cognome.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.settings_table.setItem(row_idx, 1, item_cognome)

        # Combos
        combo_rep = FilterComboBox()
        combo_rep.addItems(["", *self.reparti])
        combo_rep.setCurrentText(str(emp["reparto"]))
        combo_rep.setStyleSheet("QComboBox { border: none; background: transparent; }")

        combo_cant = FilterComboBox()
        combo_cant.addItems(["", *self.cantieri])
        combo_cant.setCurrentText(str(emp["cantiere"]))
        combo_cant.setStyleSheet("QComboBox { border: none; background: transparent; }")

        # Connect signals
        nome, cognome = emp["nome"], emp["cognome"]
        combo_rep.currentTextChanged.connect(
            lambda text, n=nome, c=cognome: self._update_details(n, c, reparto=text)
        )
        combo_cant.currentTextChanged.connect(
            lambda text, n=nome, c=cognome: self._update_details(n, c, cantiere=text)
        )

        self.settings_table.setCellWidget(row_idx, 2, combo_rep)
        self.settings_table.setCellWidget(row_idx, 3, combo_cant)

    def _update_details(
        self, nome: str, cognome: str, reparto: str | None = None, cantiere: str | None = None
    ) -> None:
        kwargs: dict[str, Any] = {}
        if reparto is not None:
            kwargs["reparto"] = reparto
        if cantiere is not None:
            kwargs["cantiere"] = cantiere

        self.storage.update_employee_details(nome, cognome, **kwargs)
        self.settings_changed.emit()

    def _on_filter_empty_changed(self) -> None:
        config_manager.set_config_value("timbrature_filter_empty_only", self.filter_empty_cb.isChecked())
        self.load_data()

    def _open_settings_request(self) -> None:
        """Richiede l'apertura delle impostazioni generali alla main window."""
        # This needs to be handled by the parent
        main_window = self.window()
        if hasattr(main_window, "show_settings"):
            main_window.show_settings()
