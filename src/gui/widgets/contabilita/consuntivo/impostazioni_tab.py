"""
SyncroJob - Consuntivo Impostazioni Tab
Tab per la configurazione delle liste dinamiche (Tecnici, Stati).
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.gui.styles import COLORS


class ImpostazioniTab(QWidget):
    """Tab per configurare le liste dinamiche usate nei consuntivi."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        info = QLabel("⚙️ PERSONALIZZAZIONE LISTE")
        info.setStyleSheet(f"font-weight: 900; font-size: 16px; color: {COLORS['primary_dark']};")
        layout.addWidget(info)

        desc = QLabel("Modifica i nomi dei tecnici e gli stati dell'attività che appariranno nei menu a tendina.")
        desc.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
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
        container.setStyleSheet(f"background: white; border-radius: 12px; border: 1px solid {COLORS['border_light']};")
        lay = QVBoxLayout(container)
        lay.setContentsMargins(15, 15, 15, 15)

        lbl = QLabel(title.upper())
        lbl.setStyleSheet(f"font-weight: 800; font-size: 11px; color: {COLORS['text_muted']}; border: none;")
        lay.addWidget(lbl)

        lst = QListWidget()
        lst.setStyleSheet(f"border: 1px solid {COLORS['bg_alt']}; border-radius: 6px; padding: 5px; color: {COLORS['text_dark']};")
        lst.addItems(config_manager.get_config_value(config_key, []))
        lay.addWidget(lst)

        btns = QHBoxLayout()
        add_btn = QPushButton("+")
        rem_btn = QPushButton("-")
        for b in [add_btn, rem_btn]:
            b.setFixedSize(30, 30)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(f"background: {COLORS['bg_alt']}; font-weight: bold; border-radius: 4px; color: {COLORS['text_dark']};")
            btns.addWidget(b)

        def add() -> None:
            text, ok = QInputDialog.getText(self, title, "Nuovo valore:")
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
