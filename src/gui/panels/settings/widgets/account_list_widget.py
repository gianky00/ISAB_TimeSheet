"""
SyncroJob - Account List Widget
Widget specializzato per la gestione degli account (ISAB, SafeWork) con supporto a password e default.
"""

from collections.abc import Sequence
from typing import Any

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QListWidgetItem,
    QMenu,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.dialogs.account_dialog import AccountDialog
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.settings.shared import (
    create_group_box,
    list_style,
    style_mini_button,
)
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    IconButton,
    StandardListWidget,
)
from src.utils.helpers import get_asset_path, get_colored_icon


class AccountListWidget(QWidget):
    """Gestisce una lista di account con icone di default e dialoghi cifrati."""

    changed = pyqtSignal()

    def __init__(self, title: str, show_type: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.title = title
        self.show_type = show_type
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.group = create_group_box(self.title)
        layout = QVBoxLayout(self.group)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.group)

        self.list_widget = StandardListWidget()
        self.list_widget.setMinimumHeight(120)
        self.list_widget.setStyleSheet(list_style())
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_menu)
        layout.addWidget(self.list_widget)

        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, COLORS["success_green"], self.add_account, "Aggiungi")
        self._add_btn(btns, Icons.EDIT, COLORS["primary_blue"], self.edit_account, "Modifica")
        self._add_btn(btns, Icons.TRASH, COLORS["error_red"], self.remove_account, "Rimuovi")
        self._add_btn(btns, Icons.STAR, COLORS["warning_yellow"], self.set_default, "Imposta Default")
        btns.addStretch()
        layout.addLayout(btns)

    def _add_btn(self, layout: QHBoxLayout, icon: str, color: str, callback: Any, tooltip: str) -> None:
        btn = IconButton()
        btn.setIcon(get_colored_icon(get_asset_path(icon), COLORS["text_dark"]))
        btn.setToolTip(tooltip)
        btn.clicked.connect(callback)
        style_mini_button(btn, color)
        layout.addWidget(btn)

    def _show_menu(self, pos: QPoint) -> None:
        menu = QMenu()
        item = self.list_widget.itemAt(pos)
        menu.addAction("Aggiungi", self.add_account)
        if item:
            self.list_widget.setCurrentItem(item)
            menu.addSeparator()
            menu.addAction("Modifica", self.edit_account)
            menu.addAction("Imposta Default", self.set_default)
            menu.addAction("Rimuovi", self.remove_account)

        viewport = self.list_widget.viewport()
        if viewport:
            menu.exec(viewport.mapToGlobal(pos))

    def add_account(self) -> None:
        dlg = AccountDialog(self, show_type=self.show_type)
        if dlg.exec():
            u, p, t = dlg.get_data()
            if u:
                accs = self.get_accounts()
                is_def = len(accs) == 0
                accs.append({"username": u, "password": p, "type": t, "default": is_def})
                self.set_accounts(accs)
                self.changed.emit()

    def edit_account(self) -> None:
        row = self.list_widget.currentRow()
        if row < 0:
            return
        accs = self.get_accounts()
        target = accs[row]
        dlg = AccountDialog(
            self,
            target["username"],
            target["password"],
            account_type=target.get("type", ""),
            show_type=self.show_type,
        )
        if dlg.exec():
            u, p, t = dlg.get_data()
            if u:
                target["username"] = u
                target["password"] = p
                target["type"] = t
                self.set_accounts(accs)
                self.changed.emit()

    def remove_account(self) -> None:
        row = self.list_widget.currentRow()
        if row >= 0 and ConfirmationDialog.confirm(self, "Conferma", "Rimuovere account?"):
            self.list_widget.takeItem(row)
            accs = self.get_accounts()
            if accs and not any(a.get("default") for a in accs):
                accs[0]["default"] = True
                self.set_accounts(accs)
            self.changed.emit()

    def set_default(self) -> None:
        row = self.list_widget.currentRow()
        if row >= 0:
            accs = self.get_accounts()
            for i, a in enumerate(accs):
                a["default"] = i == row
            self.set_accounts(accs)
            self.changed.emit()

    def get_accounts(self) -> list[dict[str, Any]]:
        accounts = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item:
                data = item.data(Qt.ItemDataRole.UserRole)
                if isinstance(data, dict):
                    accounts.append(data)
        return accounts

    def set_accounts(self, accounts: Sequence[dict[str, Any]]) -> None:
        self.list_widget.clear()
        for acc in accounts:
            label = str(acc["username"])
            if acc.get("type"):
                label += f" ({acc['type']})"
            if acc.get("default"):
                label += " (Default)"

            item = QListWidgetItem(label)
            if acc.get("default"):
                item.setIcon(get_colored_icon(get_asset_path(Icons.STAR), COLORS["text_dark"]))
            item.setData(Qt.ItemDataRole.UserRole, acc)
            self.list_widget.addItem(item)
