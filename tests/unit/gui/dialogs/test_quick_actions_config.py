"""Unit tests for QuickActionsConfigDialog."""

import pytest
from PySide6.QtCore import Qt

from src.gui.dialogs.quick_actions_config import QuickActionsConfigDialog


@pytest.fixture
def mock_config(mocker):
    """Mock della configurazione azioni rapide."""
    mocker.patch("src.gui.dialogs.quick_actions_config.get_config_value", return_value=["nav_scarico_ts"])
    mocker.patch("src.gui.dialogs.quick_actions_config.set_config_value")


class TestQuickActionsConfigDialog:
    """Test suite per QuickActionsConfigDialog."""

    def test_initialization(self, qtbot, mock_config):
        """Verifica lbl'inizializzazione del tree."""
        dialog = QuickActionsConfigDialog()
        qtbot.addWidget(dialog)

        assert dialog.windowTitle() == "Configura Azioni Rapide"
        assert dialog.tree.topLevelItemCount() > 0

        # Verifica che il pre-selezionato sia checked
        # Troviamo la foglia con chiave 'nav_scarico_ts'
        from PySide6.QtWidgets import QTreeWidgetItemIterator

        it = QTreeWidgetItemIterator(dialog.tree)
        found = False
        while it.value():
            item = it.value()
            if item.data(0, Qt.ItemDataRole.UserRole) == "nav_scarico_ts":
                assert item.checkState(0) == Qt.CheckState.Checked
                found = True
                break
            it += 1
        assert found

    def test_get_selected_actions(self, qtbot, mock_config):
        """Verifica il recupero delle chiavi selezionate."""
        dialog = QuickActionsConfigDialog()
        qtbot.addWidget(dialog)

        # Selezioniamo manualmente una foglia
        from PySide6.QtWidgets import QTreeWidgetItemIterator

        it = QTreeWidgetItemIterator(dialog.tree)
        while it.value():
            item = it.value()
            if item.data(0, Qt.ItemDataRole.UserRole) == "pf_timbrature":
                item.setCheckState(0, Qt.CheckState.Checked)
                break
            it += 1

        selected = dialog.get_selected_actions()
        assert "nav_scarico_ts" in selected
        assert "pf_timbrature" in selected

    def test_accept_saves_config(self, qtbot, mock_config, mocker):
        """Verifica che accept() chiami set_config_value."""
        mock_set = mocker.patch("src.gui.dialogs.quick_actions_config.set_config_value")

        dialog = QuickActionsConfigDialog()
        qtbot.addWidget(dialog)

        # Mocking get_selected_actions
        mocker.patch.object(dialog, "get_selected_actions", return_value=["A", "B"])

        dialog.accept()
        mock_set.assert_called_with("quick_actions", ["A", "B"])
