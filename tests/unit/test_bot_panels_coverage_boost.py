from unittest.mock import ANY, patch

import pytest
from PyQt6.QtWidgets import QComboBox

from src.gui.panels import TimbratureDBPanel


@pytest.fixture
def timbrature_db_panel(qtbot, mocker):
    # Mock dependencies BEFORE creating the panel
    mocker.patch("src.gui.panels.TimbratureStorage")
    mocker.patch("src.gui.panels.config_manager.load_config", return_value={})
    mocker.patch("src.gui.panels.get_asset_path", return_value="")

    panel = TimbratureDBPanel()
    qtbot.addWidget(panel)
    return panel


def test_load_settings_data_filter(timbrature_db_panel, qtbot):
    panel = timbrature_db_panel
    # Mock storage return
    panel.storage.get_employees.return_value = [
        {"nome": "Mario", "cognome": "Rossi", "reparto": "R1", "cantiere": "C1"},
        {"nome": "Luca", "cognome": "Bianchi", "reparto": "", "cantiere": ""},
    ]

    # Filter OFF
    panel.filter_empty_cb.setChecked(False)
    panel._load_settings_data()
    assert panel.settings_table.rowCount() == 2

    # Filter ON
    panel.filter_empty_cb.setChecked(True)
    panel._load_settings_data()
    assert panel.settings_table.rowCount() == 1  # Luca Bianchi (empty)
    assert panel.settings_table.item(0, 0).text() == "Luca"


def test_employee_detail_update(timbrature_db_panel, qtbot):
    panel = timbrature_db_panel
    panel.storage.get_employees.return_value = [
        {"nome": "Mario", "cognome": "Rossi", "reparto": "", "cantiere": ""}
    ]

    # IMPORTANT: Pre-populate lists so setCurrentText works (Combo is not editable)
    panel.reparti = ["NUOVO_REPARTO"]

    panel._load_settings_data()

    # Get combo from table (Cell 0, 2 is Reparto)
    combo_rep = panel.settings_table.cellWidget(0, 2)
    assert isinstance(combo_rep, QComboBox)

    # Trigger change
    combo_rep.setCurrentText("NUOVO_REPARTO")

    # Verify call
    panel.storage.update_employee_details.assert_called_with(
        "Mario", "Rossi", reparto="NUOVO_REPARTO"
    )


def test_import_excel_manually_success(timbrature_db_panel, qtbot, mocker):
    panel = timbrature_db_panel
    mocker.patch(
        "PyQt6.QtWidgets.QFileDialog.getOpenFileName",
        return_value=("test.xlsx", "Excel"),
    )
    panel.storage.import_excel.return_value = True

    with (
        patch("src.gui.panels.AuditManager"),
        patch("src.gui.panels.ToastManager.instance") as mock_toast,
    ):
        panel._import_excel_manually()
        assert panel.storage.import_excel.called
        mock_toast.return_value.show.assert_called_with(ANY, "success")


def test_import_excel_manually_fail(timbrature_db_panel, qtbot, mocker):
    panel = timbrature_db_panel
    mocker.patch(
        "PyQt6.QtWidgets.QFileDialog.getOpenFileName",
        return_value=("test.xlsx", "Excel"),
    )
    panel.storage.import_excel.return_value = False

    with patch("src.gui.panels.ToastManager.instance") as mock_toast:
        panel._import_excel_manually()
        mock_toast.return_value.show.assert_called_with(ANY, "error")


def test_update_combo_boxes(timbrature_db_panel, qtbot):
    panel = timbrature_db_panel
    panel.lists = {"reparti": ["R1"], "cantieri": ["C1"]}
    panel._update_combo_boxes()

    assert panel.reparto_filter.count() == 2  # Tutti + R1
    assert panel.cantiere_filter.count() == 2  # Tutti + C1


@patch("src.gui.panels.QDialog.exec")
@patch("src.gui.panels.QInputDialog.getText")
def test_manage_list_add_item(mock_get_text, mock_exec, timbrature_db_panel, qtbot):
    panel = timbrature_db_panel
    panel.lists = {"reparti": []}
    mock_get_text.return_value = ("NEW_ITEM", True)
    panel._manage_list("reparti", "Titolo")
