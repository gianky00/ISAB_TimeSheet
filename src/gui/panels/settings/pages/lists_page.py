from collections.abc import Callable, Sequence
from typing import Any

from src.gui.widgets.core_widgets import (PrimaryButton, SecondaryButton, DangerButton, GhostButton, IconButton, SearchInput, StandardInput, StandardTextEdit, FilterComboBox, StandardCheckBox, StandardSpinBox, StandardTable, StandardListWidget, StandardTreeWidget, StandardGroupBox, StandardProgressBar)
from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
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
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class ListsPage(QWidget):
    """
    Pagina per la gestione delle liste dati (Account, Contratti, ecc.).
    Fornisce sezioni modulari per l'anagrafica operativa utilizzate in ConfigTab.
    """

    settings_changed = pyqtSignal()
    """Segnale emesso quando una lista viene modificata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza la pagina delle liste.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Inizializza le sezioni come widget indipendenti per l'iniezione nel layout a card."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Inizializziamo le sezioni come widget indipendenti
        self.account_section = self._create_account_section()
        self.sw_account_section = self._create_sw_account_section()
        self.fornitori_section = self._create_fornitori_section()
        self.contract_section = self._create_contract_section()
        self.reparti_section = self._create_reparti_section()
        self.cantieri_section = self._create_cantieri_section()

    def _create_account_section(self) -> QWidget:
        """Crea la sezione per la gestione degli account Portale Fornitori ISAB."""
        group = create_group_box("Account ISAB")
        layout = QVBoxLayout(group)
        self.account_list = StandardListWidget()
        self.account_list.setMinimumHeight(120)
        self.account_list.setStyleSheet(list_style())
        self.account_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.account_list.customContextMenuRequested.connect(self._show_account_menu)
        layout.addWidget(self.account_list)
        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, COLORS["success_green"], self._add_account, "Aggiungi")
        self._add_btn(btns, Icons.EDIT, COLORS["primary_blue"], self._edit_account, "Modifica")
        self._add_btn(btns, Icons.TRASH, COLORS["error_red"], self._remove_account, "Rimuovi")
        self._add_btn(btns, Icons.STAR, COLORS["warning_yellow"], self._set_default_account, "Default")
        btns.addStretch()
        layout.addLayout(btns)
        return group

    def _create_sw_account_section(self) -> QWidget:
        """Crea la sezione per la gestione degli account SafeWork."""
        group = create_group_box("Account SafeWork")
        layout = QVBoxLayout(group)
        self.sw_account_list = StandardListWidget()
        self.sw_account_list.setMinimumHeight(120)
        self.sw_account_list.setStyleSheet(list_style())
        self.sw_account_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sw_account_list.customContextMenuRequested.connect(self._show_sw_account_menu)
        layout.addWidget(self.sw_account_list)
        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, COLORS["success_green"], self._add_sw_account, "Aggiungi")
        self._add_btn(btns, Icons.EDIT, COLORS["primary_blue"], self._edit_sw_account, "Modifica")
        self._add_btn(btns, Icons.TRASH, COLORS["error_red"], self._remove_sw_account, "Rimuovi")
        self._add_btn(btns, Icons.STAR, COLORS["warning_yellow"], self._set_default_sw_account, "Default")
        btns.addStretch()
        layout.addLayout(btns)
        return group

    def _create_contract_section(self) -> QWidget:
        """Crea la sezione per la gestione dei numeri di contratto."""
        group = create_group_box("Contratti")
        layout = QVBoxLayout(group)
        self.contract_list = StandardListWidget()
        self.contract_list.setMinimumHeight(100)
        self.contract_list.setStyleSheet(list_style())
        self._setup_generic_list(self.contract_list, self._add_contract, self._edit_contract, self._remove_contract)
        layout.addWidget(self.contract_list)
        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, COLORS["success_green"], self._add_contract)
        self._add_btn(btns, Icons.EDIT, COLORS["primary_blue"], self._edit_contract)
        self._add_btn(btns, Icons.TRASH, COLORS["error_red"], self._remove_contract)
        btns.addStretch()
        layout.addLayout(btns)
        return group

    def _create_fornitori_section(self) -> QWidget:
        """Crea la sezione per la gestione della lista fornitori."""
        group = create_group_box("Fornitori")
        layout = QVBoxLayout(group)
        self.fornitori_list = StandardListWidget()
        self.fornitori_list.setMinimumHeight(100)
        self.fornitori_list.setStyleSheet(list_style())
        self._setup_generic_list(self.fornitori_list, self._add_fornitore, self._edit_fornitore, self._remove_fornitore)
        layout.addWidget(self.fornitori_list)
        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, COLORS["success_green"], self._add_fornitore)
        self._add_btn(btns, Icons.EDIT, COLORS["primary_blue"], self._edit_fornitore)
        self._add_btn(btns, Icons.TRASH, COLORS["error_red"], self._remove_fornitore)
        btns.addStretch()
        layout.addLayout(btns)
        return group

    def _create_reparti_section(self) -> QWidget:
        """Crea la sezione per i reparti aziendali."""
        group = create_group_box("Reparti")
        layout = QVBoxLayout(group)
        self.reparti_list = StandardListWidget()
        self.reparti_list.setMinimumHeight(80)
        self.reparti_list.setStyleSheet(list_style())
        self._setup_generic_list(self.reparti_list, self._add_reparto, self._edit_reparto, self._remove_reparto)
        layout.addWidget(self.reparti_list)
        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, COLORS["success_green"], self._add_reparto)
        self._add_btn(btns, Icons.EDIT, COLORS["primary_blue"], self._edit_reparto)
        self._add_btn(btns, Icons.TRASH, COLORS["error_red"], self._remove_reparto)
        btns.addStretch()
        layout.addLayout(btns)
        return group

    def _create_cantieri_section(self) -> QWidget:
        """Crea la sezione per la gestione dei nomi cantiere."""
        group = create_group_box("Cantieri")
        layout = QVBoxLayout(group)
        self.cantieri_list = StandardListWidget()
        self.cantieri_list.setMinimumHeight(80)
        self.cantieri_list.setStyleSheet(list_style())
        self._setup_generic_list(self.cantieri_list, self._add_cantiere, self._edit_cantiere, self._remove_cantiere)
        layout.addWidget(self.cantieri_list)
        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, COLORS["success_green"], self._add_cantiere)
        self._add_btn(btns, Icons.EDIT, COLORS["primary_blue"], self._edit_cantiere)
        self._add_btn(btns, Icons.TRASH, COLORS["error_red"], self._remove_cantiere)
        btns.addStretch()
        layout.addLayout(btns)
        return group

    def _add_btn(
        self, layout: QHBoxLayout, icon: str, color: str, callback: Callable[[], None], tooltip: str = ""
    ) -> None:
        """Aggiunge un pulsante stilizzato al layout specificato."""
        btn = IconButton()
        btn.setIcon(get_colored_icon(get_asset_path(icon), COLORS["text_dark"]))
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
        """Configura il menu contestuale per una QListWidget generica."""
        list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        list_widget.customContextMenuRequested.connect(
            lambda pos: self._show_generic_menu(pos, list_widget, add_cb, edit_cb, remove_cb)
        )

    def _show_account_menu(self, position: QPoint) -> None:
        """Mostra il menu contestuale per gli account ISAB."""
        self._show_acc_menu_impl(
            position,
            self.account_list,
            self._add_account,
            self._edit_account,
            self._remove_account,
            self._set_default_account,
        )

    def _show_sw_account_menu(self, position: QPoint) -> None:
        """Mostra il menu contestuale per gli account SafeWork."""
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
        """Implementazione core del menu contestuale degli account."""
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
        """Implementazione core del menu contestuale generico."""
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

    def _get_accounts(self, list_widget: QListWidget) -> list[dict[str, Any]]:
        """Estrae i dati degli account dalla QListWidget."""
        accounts = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item is not None:
                data = item.data(Qt.ItemDataRole.UserRole)
                if isinstance(data, dict):
                    accounts.append(data)
        return accounts

    def _render_accounts(self, list_widget: QListWidget, accounts: Sequence[dict[str, Any]]) -> None:
        """Renderizza graficamente la lista degli account."""
        list_widget.clear()
        for acc in accounts:
            label = str(acc["username"])
            if acc.get("type"):
                label += f" ({acc['type']})"
            label += " (Default)" if acc.get("default") else ""

            item = QListWidgetItem(label)
            if acc.get("default"):
                item.setIcon(get_colored_icon(get_asset_path(Icons.STAR), COLORS["text_dark"]))
            item.setData(Qt.ItemDataRole.UserRole, acc)
            list_widget.addItem(item)

    def _add_account(self) -> None:
        """Apre il dialogo per aggiungere un nuovo account ISAB."""
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
        """Modifica l'account ISAB selezionato."""
        row = self.account_list.currentRow()
        if row < 0:
            return
        accs = self._get_accounts(self.account_list)
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
        """Rimuove l'account ISAB selezionato previa conferma."""
        row = self.account_list.currentRow()
        if row >= 0 and ConfirmationDialog.confirm(self, "Conferma", "Rimuovere account?"):
            self.account_list.takeItem(row)
            accs = self._get_accounts(self.account_list)
            if accs and not any(a["default"] for a in accs):
                accs[0]["default"] = True
                self._render_accounts(self.account_list, accs)
            self.settings_changed.emit()

    def _set_default_account(self) -> None:
        """Imposta l'account ISAB selezionato come predefinito."""
        row = self.account_list.currentRow()
        if row >= 0:
            accs = self._get_accounts(self.account_list)
            for i, a in enumerate(accs):
                a["default"] = i == row
            self._render_accounts(self.account_list, accs)
            self.settings_changed.emit()

    def _add_sw_account(self) -> None:
        """Aggiunge un nuovo account SafeWork."""
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
        """Modifica l'account SafeWork selezionato."""
        row = self.sw_account_list.currentRow()
        if row < 0:
            return
        accs = self._get_accounts(self.sw_account_list)
        target_acc = accs[row]
        dlg = AccountDialog(self, target_acc["username"], target_acc["password"], account_type=target_acc.get("type", ""), show_type=True)
        if dlg.exec():
            u, p, t = dlg.get_data()
            if u:
                target_acc["username"] = u
                target_acc["password"] = p
                target_acc["type"] = t
                self._render_accounts(self.sw_account_list, accs)
                self.settings_changed.emit()

    def _remove_sw_account(self) -> None:
        """Rimuove l'account SafeWork selezionato."""
        row = self.sw_account_list.currentRow()
        if row >= 0 and ConfirmationDialog.confirm(self, "Conferma", "Rimuovere account?"):
            self.sw_account_list.takeItem(row)
            accs = self._get_accounts(self.sw_account_list)
            if accs and not any(a["default"] for a in accs):
                accs[0]["default"] = True
                self._render_accounts(self.sw_account_list, accs)
            self.settings_changed.emit()

    def _set_default_sw_account(self) -> None:
        """Imposta l'account SafeWork selezionato come predefinito."""
        row = self.sw_account_list.currentRow()
        if row >= 0:
            accs = self._get_accounts(self.sw_account_list)
            for i, a in enumerate(accs):
                a["default"] = i == row
            self._render_accounts(self.sw_account_list, accs)
            self.settings_changed.emit()

    def _update_simple_list(self, list_widget: QListWidget, items: Sequence[str]) -> None:
        """Aggiorna una QListWidget con una lista di stringhe."""
        list_widget.clear()
        list_widget.addItems(items)

    def _get_simple_items(self, list_widget: QListWidget) -> list[str]:
        """Estrae i testi da una QListWidget."""
        items = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item is not None:
                items.append(item.text())
        return items

    def _add_simple(self, list_widget: QListWidget, title: str) -> None:
        """Aggiunge un elemento testuale a una lista tramite input dialog."""
        text, ok = StandardInputDialog.get_input(self, "Aggiungi", title)
        if ok and text:
            list_widget.addItem(text)
            self.settings_changed.emit()

    def _edit_simple(self, list_widget: QListWidget, title: str) -> None:
        """Modifica l'elemento testuale selezionato."""
        item = list_widget.currentItem()
        if item:
            text, ok = StandardInputDialog.get_input(self, "Modifica", title, text=item.text())
            if ok and text:
                item.setText(text)
                self.settings_changed.emit()

    def _remove_simple(self, list_widget: QListWidget) -> None:
        """Rimuove l'elemento selezionato."""
        row = list_widget.currentRow()
        if row >= 0 and ConfirmationDialog.confirm(self, "Conferma", "Rimuovere elemento?"):
            list_widget.takeItem(row)
            self.settings_changed.emit()

    def _add_contract(self) -> None:
        """Wrapper per aggiungere un contratto."""
        self._add_simple(self.contract_list, "Contratto:")

    def _edit_contract(self) -> None:
        """Wrapper per modificare un contratto."""
        self._edit_simple(self.contract_list, "Contratto:")

    def _remove_contract(self) -> None:
        """Wrapper per rimuovere un contratto."""
        self._remove_simple(self.contract_list)

    def _add_fornitore(self) -> None:
        """Wrapper per aggiungere un fornitore."""
        self._add_simple(self.fornitori_list, "Fornitore:")

    def _edit_fornitore(self) -> None:
        """Wrapper per modificare un fornitore."""
        self._edit_simple(self.fornitori_list, "Fornitore:")

    def _remove_fornitore(self) -> None:
        """Wrapper per rimuovere un fornitore."""
        self._remove_simple(self.fornitori_list)

    def _add_reparto(self) -> None:
        """Wrapper per aggiungere un reparto."""
        self._add_simple(self.reparti_list, "Reparto:")

    def _edit_reparto(self) -> None:
        """Wrapper per modificare un reparto."""
        self._edit_simple(self.reparti_list, "Reparto:")

    def _remove_reparto(self) -> None:
        """Wrapper per rimuovere un reparto."""
        self._remove_simple(self.reparti_list)

    def _add_cantiere(self) -> None:
        """Wrapper per aggiungere un cantiere."""
        self._add_simple(self.cantieri_list, "Cantiere:")

    def _edit_cantiere(self) -> None:
        """Wrapper per modificare un cantiere."""
        self._edit_simple(self.cantieri_list, "Cantiere:")

    def _remove_cantiere(self) -> None:
        """Wrapper per rimuovere un cantiere."""
        self._remove_simple(self.cantieri_list)

    def load_from_config(self, config: dict[str, Any]) -> None:
        """Carica tutte le liste (account, contratti, fornitori, ecc.) dalla configurazione."""
        self._render_accounts(self.account_list, config.get("accounts", []))
        self._render_accounts(self.sw_account_list, config.get("safework_accounts", []))
        self._update_simple_list(self.contract_list, config.get("contracts", []))
        self._update_simple_list(self.fornitori_list, config.get("fornitori", []))
        self._update_simple_list(self.reparti_list, config.get("reparti_timbrature", []))
        self._update_simple_list(self.cantieri_list, config.get("cantieri_timbrature", []))

    def save_to_config(self, config_manager: Any) -> None:
        """Salva lo stato corrente delle liste nella configurazione globale."""
        config_manager.set_config_value("accounts", self._get_accounts(self.account_list))
        config_manager.set_config_value("safework_accounts", self._get_accounts(self.sw_account_list))
        config_manager.set_config_value("contracts", self._get_simple_items(self.contract_list))
        config_manager.set_config_value("fornitori", self._get_simple_items(self.fornitori_list))
        config_manager.set_config_value("reparti_timbrature", self._get_simple_items(self.reparti_list))
        config_manager.set_config_value("cantieri_timbrature", self._get_simple_items(self.cantieri_list))
