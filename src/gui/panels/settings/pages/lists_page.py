"""
SyncroJob - Lists Settings Page
Pagina per la gestione delle anagrafiche operative (Account, Contratti, Fornitori, ecc.).
Refactored V9.5: Modular architecture with specialized CRUD widgets.
"""

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from src.gui.panels.settings.widgets.account_list_widget import AccountListWidget
from src.gui.panels.settings.widgets.editable_list_widget import EditableListWidget


class ListsPage(QWidget):
    """
    Pagina per la gestione delle liste dati.
    Fornisce sezioni modulari per l'anagrafica operativa.
    """

    settings_changed = pyqtSignal()
    """Segnale emesso quando una lista viene modificata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Inizializza le sezioni modulari."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # 1. Sezione Account
        self.account_section = AccountListWidget("Account Portale Fornitori ISAB", show_type=False)
        self.account_section.changed.connect(self.settings_changed.emit)
        self.main_layout.addWidget(self.account_section)

        self.sw_account_section = AccountListWidget("Account SafeWork", show_type=True)
        self.sw_account_section.changed.connect(self.settings_changed.emit)
        self.main_layout.addWidget(self.sw_account_section)

        # 2. Sezioni Liste Semplici
        self.fornitori_section = EditableListWidget("Lista Fornitori", "Fornitore:")
        self.fornitori_section.changed.connect(self.settings_changed.emit)
        self.main_layout.addWidget(self.fornitori_section)

        self.contract_section = EditableListWidget("Numeri di Contratto", "Contratto:")
        self.contract_section.changed.connect(self.settings_changed.emit)
        self.main_layout.addWidget(self.contract_section)

        self.reparti_section = EditableListWidget("Reparti Aziendali", "Reparto:")
        self.reparti_section.changed.connect(self.settings_changed.emit)
        self.main_layout.addWidget(self.reparti_section)

        self.cantieri_section = EditableListWidget("Nomi Cantiere", "Cantiere:")
        self.cantieri_section.changed.connect(self.settings_changed.emit)
        self.main_layout.addWidget(self.cantieri_section)

    def load_from_config(self, config: dict[str, Any]) -> None:
        """Carica i dati dalla configurazione nei widget corrispondenti."""
        self.account_section.set_accounts(config.get("accounts", []))
        self.sw_account_section.set_accounts(config.get("safework_accounts", []))
        self.contract_section.set_items(config.get("contracts", []))
        self.fornitori_section.set_items(config.get("fornitori", []))
        self.reparti_section.set_items(config.get("reparti_timbrature", []))
        self.cantieri_section.set_items(config.get("cantieri_timbrature", []))

    def save_to_config(self, config_manager: Any) -> None:
        """Persiste lo stato dei widget nella configurazione globale."""
        config_manager.set_config_value("accounts", self.account_section.get_accounts())
        config_manager.set_config_value("safework_accounts", self.sw_account_section.get_accounts())
        config_manager.set_config_value("contracts", self.contract_section.get_items())
        config_manager.set_config_value("fornitori", self.fornitori_section.get_items())
        config_manager.set_config_value("reparti_timbrature", self.reparti_section.get_items())
        config_manager.set_config_value("cantieri_timbrature", self.cantieri_section.get_items())
