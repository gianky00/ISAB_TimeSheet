from collections.abc import Callable, Sequence
from typing import Any

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.dialogs.account_dialog import AccountDialog
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.dialogs.standard_input_dialog import StandardInputDialog
from src.gui.panels.settings.shared import (
    create_group_box,
    list_style,
    style_mini_button,
)
from src.utils.helpers import get_asset_path, get_colored_icon


class ListsPage(QWidget):
    """Pagina per la gestione delle liste dati (Account, Contratti, ecc.)."""

    settings_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self.main_content_layout = QVBoxLayout(content)
        self.main_content_layout.setSpacing(20)

        # RIGA 1: Accounts, Fornitori, Contratti (Tutto orizzontale)
        row1 = QHBoxLayout()
        self._setup_account_section(row1)
        self._setup_sw_account_section(row1)
        self._setup_fornitori_section(row1)
        self._setup_contract_section(row1)
        self.main_content_layout.addLayout(row1)

        # RIGA 2: REPARTI E CANTIERI (Affiancati)
        row2 = QHBoxLayout()
        self._setup_reparti_section(row2)
        self._setup_cantieri_section(row2)
        self.main_content_layout.addLayout(row2)

        self.main_content_layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    # --- SEZIONI UI ---

    def _setup_account_section(self, parent_layout: QHBoxLayout) -> None:
        group = create_group_box("Account ISAB")
        layout = QVBoxLayout(group)

        self.account_list = QListWidget()
        self.account_list.setMaximumHeight(150)  # Aumentato leggermente
        self.account_list.setStyleSheet(list_style())
        self.account_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.account_list.customContextMenuRequested.connect(self._show_account_menu)
        layout.addWidget(self.account_list)

        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, "#28a745", self._add_account, "Aggiungi")
        self._add_btn(btns, Icons.EDIT, "#0d6efd", self._edit_account, "Modifica")
        self._add_btn(btns, Icons.TRASH, "#dc3545", self._remove_account, "Rimuovi")
        self._add_btn(btns, Icons.STAR, "#ffc107", self._set_default_account, "Default")
        btns.addStretch()
        layout.addLayout(btns)
        parent_layout.addWidget(group)

    def _setup_sw_account_section(self, parent_layout: QHBoxLayout) -> None:
        group = create_group_box("Account SafeWork")
        layout = QVBoxLayout(group)

        self.sw_account_list = QListWidget()
        self.sw_account_list.setMaximumHeight(150)  # Aumentato leggermente
        self.sw_account_list.setStyleSheet(list_style())
        self.sw_account_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sw_account_list.customContextMenuRequested.connect(self._show_sw_account_menu)
        layout.addWidget(self.sw_account_list)

        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, "#28a745", self._add_sw_account, "Aggiungi")
        self._add_btn(btns, Icons.EDIT, "#0d6efd", self._edit_sw_account, "Modifica")
        self._add_btn(btns, Icons.TRASH, "#dc3545", self._remove_sw_account, "Rimuovi")
        self._add_btn(btns, Icons.STAR, "#ffc107", self._set_default_sw_account, "Default")
        btns.addStretch()
        layout.addLayout(btns)
        parent_layout.addWidget(group)

    def _setup_contract_section(self, parent_layout: QHBoxLayout) -> None:
        group = create_group_box("Contratti")
        layout = QVBoxLayout(group)
        self.contract_list = QListWidget()
        self.contract_list.setMaximumHeight(130)
        self.contract_list.setStyleSheet(list_style())
        self._setup_generic_list(
            self.contract_list,
            self._add_contract,
            self._edit_contract,
            self._remove_contract,
        )
        layout.addWidget(self.contract_list)

        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, "#28a745", self._add_contract)
        self._add_btn(btns, Icons.EDIT, "#0d6efd", self._edit_contract)
        self._add_btn(btns, Icons.TRASH, "#dc3545", self._remove_contract)
        btns.addStretch()
        layout.addLayout(btns)
        parent_layout.addWidget(group)

    def _setup_fornitori_section(self, parent_layout: QHBoxLayout) -> None:
        group = create_group_box("Fornitori")
        layout = QVBoxLayout(group)
        self.fornitori_list = QListWidget()
        self.fornitori_list.setMaximumHeight(130)
        self.fornitori_list.setStyleSheet(list_style())
        self._setup_generic_list(
            self.fornitori_list,
            self._add_fornitore,
            self._edit_fornitore,
            self._remove_fornitore,
        )
        layout.addWidget(self.fornitori_list)

        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, "#28a745", self._add_fornitore)
        self._add_btn(btns, Icons.EDIT, "#0d6efd", self._edit_fornitore)
        self._add_btn(btns, Icons.TRASH, "#dc3545", self._remove_fornitore)
        btns.addStretch()
        layout.addLayout(btns)
        parent_layout.addWidget(group)

    def _setup_reparti_section(self, parent_layout: QHBoxLayout) -> None:
        group = create_group_box("Reparti")
        layout = QVBoxLayout(group)
        self.reparti_list = QListWidget()
        self.reparti_list.setMaximumHeight(100)
        self.reparti_list.setStyleSheet(list_style())
        self._setup_generic_list(
            self.reparti_list,
            self._add_reparto,
            self._edit_reparto,
            self._remove_reparto,
        )
        layout.addWidget(self.reparti_list)

        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, "#28a745", self._add_reparto)
        self._add_btn(btns, Icons.EDIT, "#0d6efd", self._edit_reparto)
        self._add_btn(btns, Icons.TRASH, "#dc3545", self._remove_reparto)
        btns.addStretch()
        layout.addLayout(btns)
        parent_layout.addWidget(group)

    def _setup_cantieri_section(self, parent_layout: QHBoxLayout) -> None:
        group = create_group_box("Cantieri")
        layout = QVBoxLayout(group)
        self.cantieri_list = QListWidget()
        self.cantieri_list.setMaximumHeight(100)
        self.cantieri_list.setStyleSheet(list_style())
        self._setup_generic_list(
            self.cantieri_list,
            self._add_cantiere,
            self._edit_cantiere,
            self._remove_cantiere,
        )
        layout.addWidget(self.cantieri_list)

        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, "#28a745", self._add_cantiere)
        self._add_btn(btns, Icons.EDIT, "#0d6efd", self._edit_cantiere)
        self._add_btn(btns, Icons.TRASH, "#dc3545", self._remove_cantiere)
        btns.addStretch()
        layout.addLayout(btns)
        parent_layout.addWidget(group)

    # --- HELPERS ---

    def _add_btn(
        self, layout: QHBoxLayout, icon: str, color: str, callback: Callable[[], None], tooltip: str = ""
    ) -> None:
        btn = QPushButton()
        btn.setIcon(get_colored_icon(get_asset_path(icon), "#000000"))
        if tooltip:
            btn.setToolTip(tooltip)
        btn.clicked.connect(callback)
        style_mini_button(btn, color)
        layout.addWidget(btn)

    def _setup_generic_list(
        self,
        list_widget: QListWidget,
        add_cb: Callable[[], None],
        edit_cb: Callable[[], None],
        remove_cb: Callable[[], None],
    ) -> None:
        list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        list_widget.customContextMenuRequested.connect(
            lambda pos: self._show_generic_menu(pos, list_widget, add_cb, edit_cb, remove_cb)
        )

    # --- MENU CONTESTUALI ---

    def _show_account_menu(self, position: QPoint) -> None:
        self._show_acc_menu_impl(
            position,
            self.account_list,
            self._add_account,
            self._edit_account,
            self._remove_account,
            self._set_default_account,
        )

    def _show_sw_account_menu(self, position: QPoint) -> None:
        self._show_acc_menu_impl(
            position,
            self.sw_account_list,
            self._add_sw_account,
            self._edit_sw_account,
            self._remove_sw_account,
            self._set_default_sw_account,
        )

    def _show_acc_menu_impl(
        self,
        position: QPoint,
        list_widget: QListWidget,
        add_cb: Callable[[], None],
        edit_cb: Callable[[], None],
        remove_cb: Callable[[], None],
        def_cb: Callable[[], None],
    ) -> None:
        menu = QMenu()
        item = list_widget.itemAt(position)
        menu.addAction("Aggiungi", add_cb)
        if item:
            list_widget.setCurrentItem(item)
            menu.addSeparator()
            menu.addAction("Modifica", edit_cb)
            menu.addAction("Imposta Default", def_cb)
            menu.addAction("Rimuovi", remove_cb)
        viewport = list_widget.viewport()
        if viewport is not None:
            menu.exec(viewport.mapToGlobal(position))

    def _show_generic_menu(
        self,
        position: QPoint,
        list_widget: QListWidget,
        add_cb: Callable[[], None],
        edit_cb: Callable[[], None],
        remove_cb: Callable[[], None],
    ) -> None:
        menu = QMenu()
        item = list_widget.itemAt(position)
        menu.addAction("Aggiungi", add_cb)
        if item:
            list_widget.setCurrentItem(item)
            menu.addSeparator()
            menu.addAction("Modifica", edit_cb)
            menu.addAction("Rimuovi", remove_cb)
        viewport = list_widget.viewport()
        if viewport is not None:
            menu.exec(viewport.mapToGlobal(position))

    # --- LOGICA ACCOUNT ISAB ---

    def _get_accounts(self, list_widget: QListWidget) -> list[dict[str, Any]]:
        accounts = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item is not None:
                data = item.data(Qt.ItemDataRole.UserRole)
                if isinstance(data, dict):
                    accounts.append(data)
        return accounts

    def _render_accounts(self, list_widget: QListWidget, accounts: Sequence[dict[str, Any]]) -> None:
        list_widget.clear()
        for acc in accounts:
            label = str(acc["username"])
            if acc.get("type"):
                label += f" ({acc['type']})"
            label += " (Default)" if acc.get("default") else ""

            item = QListWidgetItem(label)
            if acc.get("default"):
                item.setIcon(get_colored_icon(get_asset_path(Icons.STAR), "#000000"))
            item.setData(Qt.ItemDataRole.UserRole, acc)
            list_widget.addItem(item)

    def _add_account(self) -> None:
        dlg = AccountDialog(self)
        if dlg.exec():
            u, p, _ = dlg.get_data()
            if u:
                accs = self._get_accounts(self.account_list)
                is_def = len(accs) == 0
                accs.append({"username": u, "password": p, "default": is_def})
                self._render_accounts(self.account_list, accs)
                self.settings_changed.emit()

    def _edit_account(self) -> None:
        row = self.account_list.currentRow()
        if row < 0:
            return

        # Ottieni tutti gli account
        accs = self._get_accounts(self.account_list)
        # Ottieni quello da modificare
        target_acc = accs[row]

        dlg = AccountDialog(self, target_acc["username"], target_acc["password"])
        if dlg.exec():
            u, p, _ = dlg.get_data()
            if u:
                target_acc["username"] = u
                target_acc["password"] = p
                self._render_accounts(self.account_list, accs)
                self.settings_changed.emit()

    def _remove_account(self) -> None:
        row = self.account_list.currentRow()
        if row >= 0 and ConfirmationDialog.confirm(self, "Conferma", "Rimuovere account?"):
            self.account_list.takeItem(row)
            accs = self._get_accounts(self.account_list)
            if accs and not any(a["default"] for a in accs):
                accs[0]["default"] = True
                self._render_accounts(self.account_list, accs)
            self.settings_changed.emit()

    def _set_default_account(self) -> None:
        row = self.account_list.currentRow()
        if row >= 0:
            accs = self._get_accounts(self.account_list)
            for i, a in enumerate(accs):
                a["default"] = i == row
            self._render_accounts(self.account_list, accs)
            self.settings_changed.emit()

    # --- LOGICA ACCOUNT SAFEWORK (Simile a ISAB ma su sw_account_list) ---
    # Per brevità potrei unificare ma per ora copio adattando
    def _add_sw_account(self) -> None:
        dlg = AccountDialog(self, show_type=True)
        dlg.setWindowTitle("Account SafeWork")
        if dlg.exec():
            u, p, t = dlg.get_data()
            if u:
                accs = self._get_accounts(self.sw_account_list)
                is_def = len(accs) == 0
                accs.append({"username": u, "password": p, "type": t, "default": is_def})
                self._render_accounts(self.sw_account_list, accs)
                self.settings_changed.emit()

    def _edit_sw_account(self) -> None:
        row = self.sw_account_list.currentRow()
        if row < 0:
            return

        accs = self._get_accounts(self.sw_account_list)
        target_acc = accs[row]

        dlg = AccountDialog(
            self,
            target_acc["username"],
            target_acc["password"],
            account_type=target_acc.get("type", ""),
            show_type=True,
        )
        if dlg.exec():
            u, p, t = dlg.get_data()
            if u:
                target_acc["username"] = u
                target_acc["password"] = p
                target_acc["type"] = t
                self._render_accounts(self.sw_account_list, accs)
                self.settings_changed.emit()

    def _remove_sw_account(self) -> None:
        row = self.sw_account_list.currentRow()
        if row >= 0 and ConfirmationDialog.confirm(self, "Conferma", "Rimuovere account?"):
            self.sw_account_list.takeItem(row)
            accs = self._get_accounts(self.sw_account_list)
            if accs and not any(a["default"] for a in accs):
                accs[0]["default"] = True
                self._render_accounts(self.sw_account_list, accs)
            self.settings_changed.emit()

    def _set_default_sw_account(self) -> None:
        row = self.sw_account_list.currentRow()
        if row >= 0:
            accs = self._get_accounts(self.sw_account_list)
            for i, a in enumerate(accs):
                a["default"] = i == row
            self._render_accounts(self.sw_account_list, accs)
            self.settings_changed.emit()

    # --- LOGICA LISTE SEMPLICI ---

    def _update_simple_list(self, list_widget: QListWidget, items: Sequence[str]) -> None:
        list_widget.clear()
        list_widget.addItems(items)

    def _get_simple_items(self, list_widget: QListWidget) -> list[str]:
        items = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item is not None:
                items.append(item.text())
        return items

    def _add_simple(self, list_widget: QListWidget, title: str) -> None:
        text, ok = StandardInputDialog.get_input(self, "Aggiungi", title)
        if ok and text:
            list_widget.addItem(text)
            self.settings_changed.emit()

    def _edit_simple(self, list_widget: QListWidget, title: str) -> None:
        item = list_widget.currentItem()
        if item:
            text, ok = StandardInputDialog.get_input(self, "Modifica", title, text=item.text())
            if ok and text:
                item.setText(text)
                self.settings_changed.emit()

    def _remove_simple(self, list_widget: QListWidget) -> None:
        row = list_widget.currentRow()
        if row >= 0 and ConfirmationDialog.confirm(self, "Conferma", "Rimuovere elemento?"):
            list_widget.takeItem(row)
            self.settings_changed.emit()

    # Wrapper specifici
    def _add_contract(self) -> None:
        self._add_simple(self.contract_list, "Contratto:")

    def _edit_contract(self) -> None:
        self._edit_simple(self.contract_list, "Contratto:")

    def _remove_contract(self) -> None:
        self._remove_simple(self.contract_list)

    def _add_fornitore(self) -> None:
        self._add_simple(self.fornitori_list, "Fornitore:")

    def _edit_fornitore(self) -> None:
        self._edit_simple(self.fornitori_list, "Fornitore:")

    def _remove_fornitore(self) -> None:
        self._remove_simple(self.fornitori_list)

    def _add_reparto(self) -> None:
        self._add_simple(self.reparti_list, "Reparto:")

    def _edit_reparto(self) -> None:
        self._edit_simple(self.reparti_list, "Reparto:")

    def _remove_reparto(self) -> None:
        self._remove_simple(self.reparti_list)

    def _add_cantiere(self) -> None:
        self._add_simple(self.cantieri_list, "Cantiere:")

    def _edit_cantiere(self) -> None:
        self._edit_simple(self.cantieri_list, "Cantiere:")

    def _remove_cantiere(self) -> None:
        self._remove_simple(self.cantieri_list)

    # --- LOAD & SAVE ---

    def load_from_config(self, config: dict[str, Any]) -> None:
        self._render_accounts(self.account_list, config.get("accounts", []))
        self._render_accounts(self.sw_account_list, config.get("safework_accounts", []))
        self._update_simple_list(self.contract_list, config.get("contracts", []))
        self._update_simple_list(self.fornitori_list, config.get("fornitori", []))
        self._update_simple_list(self.reparti_list, config.get("reparti_timbrature", []))
        self._update_simple_list(self.cantieri_list, config.get("cantieri_timbrature", []))

    def save_to_config(self, config_manager: Any) -> None:
        config_manager.set_config_value("accounts", self._get_accounts(self.account_list))
        config_manager.set_config_value("safework_accounts", self._get_accounts(self.sw_account_list))
        config_manager.set_config_value("contracts", self._get_simple_items(self.contract_list))
        config_manager.set_config_value("fornitori", self._get_simple_items(self.fornitori_list))
        config_manager.set_config_value("reparti_timbrature", self._get_simple_items(self.reparti_list))
        config_manager.set_config_value("cantieri_timbrature", self._get_simple_items(self.cantieri_list))
