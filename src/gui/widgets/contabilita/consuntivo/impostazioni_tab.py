"""SyncroJob - Consuntivo Impostazioni Tab.

Tab per la configurazione delle liste dinamiche (Tecnici, Stati).
"""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QVBoxLayout,
    QWidget,
)

from src.application.services import config_manager
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import SecondaryButton, StandardListWidget


class ImpostazioniTab(QWidget):
    """Tab per configurare le liste dinamiche usate nei consuntivi.

    Inizializza la classe.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        info = QLabel("PERSONALIZZAZIONE LISTE")
        info.setStyleSheet(
            f"font-weight: 900; font-size: 16px; color: {COLORS['primary_dark']}; border: none;"
        )
        layout.addWidget(info)

        desc = QLabel(
            "Modifica i nomi dei tecnici e gli stati dell'attivitàche appariranno nei menu a tendina."
        )
        desc.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px; border: none;")
        layout.addWidget(desc)

        lists_row = QHBoxLayout()
        lists_row.setSpacing(30)

        self.tcl_editor = self._create_list_editor("Tecnici (TCL)", "preventivi_tcl")
        self.stati_editor = self._create_list_editor("Stati Attività", "preventivi_stati")

        lists_row.addWidget(self.tcl_editor)
        lists_row.addWidget(self.stati_editor)
        layout.addLayout(lists_row)
        layout.addStretch()

    def _create_list_editor(self, title: str, config_key: str) -> QFrame:
        container = QFrame()
        container.setObjectName("listContainer")
        container.setStyleSheet(f"""
      QFrame#listContainer {{
        background: {COLORS["bg_white"]};
        border-radius: 12px;
        border: 1px solid {COLORS["border_light"]};
      }}
    """)

        lay = QVBoxLayout(container)
        lay.setContentsMargins(15, 15, 15, 15)
        lay.setSpacing(10)

        lbl = QLabel(title.upper())
        lbl.setStyleSheet(f"font-weight: 800; font-size: 11px; color: {COLORS['text_muted']}; border: none;")
        lay.addWidget(lbl)

        lst = StandardListWidget()
        lst.addItems(config_manager.get_config_value(config_key, []))
        lay.addWidget(lst)

        btns = QHBoxLayout()
        btns.setSpacing(10)
        add_btn = SecondaryButton("Aggiungi")
        add_btn.setMinimumHeight(32)
        rem_btn = SecondaryButton("Rimuovi")
        rem_btn.setMinimumHeight(32)

        for b in (add_btn, rem_btn):
            btns.addWidget(b)

        def add() -> None:
            from src.gui.dialogs.standard_input_dialog import StandardInputDialog

            text, ok = StandardInputDialog.get_input(self, title, "Nuovo valore:")
            if ok and text.strip():
                lst.addItem(text.strip())
                self._save(lst, config_key)

        def rem() -> None:
            for it in lst.selectedItems():
                lst.takeItem(lst.row(it))
            self._save(lst, config_key)

        add_btn.clicked.connect(add)
        rem_btn.clicked.connect(rem)
        lay.addLayout(btns)
        return container

    def _save(self, lst: QListWidget, key: str) -> None:
        items = []
        for i in range(lst.count()):
            item = lst.item(i)
            if item:
                items.append(item.text())
        config_manager.set_config_value(key, items)
