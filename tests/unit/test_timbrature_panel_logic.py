from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtWidgets import QComboBox

from src.gui.panels import TimbratureDBPanel


@pytest.fixture
def panel(qtbot):
    # Mock dependencies BEFORE instantiation to avoid I/O
    with (
        patch("src.gui.panels.TimbratureStorage"),
        patch("src.gui.panels.config_manager.load_config", return_value={}),
        patch("src.gui.panels.get_asset_path", return_value=""),
        patch("src.gui.panels.config_manager.CONFIG_DIR", MagicMock()),
    ):
        widget = TimbratureDBPanel()
        qtbot.addWidget(widget)
        return widget


def test_initialization(panel):
    assert panel.storage is not None
    assert panel.settings_table.rowCount() == 0


def test_load_settings_data_filtering(panel):
    """Test logica di filtraggio dipendenti (vuoti vs tutti)."""
    # Mock data
    mock_employees = [
        {"nome": "Mario", "cognome": "Rossi", "reparto": "R1", "cantiere": "C1"},
        {"nome": "Luca", "cognome": "Bianchi", "reparto": "", "cantiere": ""},
    ]
    panel.storage.get_employees.return_value = mock_employees

    # 1. Filter Disabled (Show All)
    panel.filter_empty_cb.setChecked(False)
    panel._load_settings_data()

    assert panel.settings_table.rowCount() == 2

    # 2. Filter Enabled (Show Only Empty)
    panel.filter_empty_cb.setChecked(True)
    panel._load_settings_data()

    assert panel.settings_table.rowCount() == 1
    assert panel.settings_table.item(0, 0).text() == "Luca"


def test_update_employee_details(panel):
    """Test che il cambio di combo chiami lo storage."""
    mock_employees = [{"nome": "Mario", "cognome": "Rossi", "reparto": "", "cantiere": ""}]
    panel.storage.get_employees.return_value = mock_employees
    panel.reparti = ["R1", "R2"]

    panel._load_settings_data()

    # Get combo widget from cell (0, 2 is Reparto)
    combo = panel.settings_table.cellWidget(0, 2)
    assert isinstance(combo, QComboBox)

    # Change selection
    combo.setCurrentText("R1")

    # Verify storage update called
    panel.storage.update_employee_details.assert_called_with("Mario", "Rossi", reparto="R1")


def test_import_excel_logic(panel):
    """Test logica importazione manuale."""
    with (
        patch(
            "PyQt6.QtWidgets.QFileDialog.getOpenFileName",
            return_value=("test.xlsx", "Excel"),
        ),
        patch("src.gui.panels.ToastManager.instance") as mock_toast,
    ):
        # Case 1: Success
        panel.storage.import_excel.return_value = True
        panel._import_excel_manually()

        mock_toast.return_value.show.assert_called_with(
            "Dati importati correttamente nel database.", "success"
        )

        # Case 2: Failure
        panel.storage.import_excel.return_value = False
        panel._import_excel_manually()
        mock_toast.return_value.show.assert_called_with("Impossibile importare il file.", "error")


def test_manage_list_dialog(panel, mocker):
    """Test aggiunta elemento a lista (reparti/cantieri)."""
    # Mock input dialogs
    mocker.patch("PyQt6.QtWidgets.QDialog.exec", return_value=True)  # Accept dialog
    mocker.patch("PyQt6.QtWidgets.QInputDialog.getText", return_value=("NUOVO_REP", True))

    panel.lists = {"reparti": []}
