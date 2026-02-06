from unittest.mock import ANY, patch

import pytest
from PyQt6.QtWidgets import QComboBox

from src.gui.panels import TimbratureDBPanel


@pytest.fixture
def timbrature_db_panel(qtbot, mocker):
    # Mock dependencies BEFORE creating the panel
    mock_storage_class = mocker.patch(
        "src.gui.panels.timbrature.panel.TimbratureStorage"
    )
    mock_storage_instance = mock_storage_class.return_value
    mock_storage_instance.get_lists.return_value = {"reparti": [], "cantieri": []}

    mocker.patch(
        "src.gui.panels.timbrature.panel.config_manager.load_config", return_value={}
    )
    mocker.patch("src.gui.panels.timbrature.panel.get_asset_path", return_value="")

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
    panel.settings_tab.filter_empty_cb.setChecked(False)
    panel.settings_tab.load_data()
    assert panel.settings_tab.settings_table.rowCount() == 2

    # Filter ON
    panel.settings_tab.filter_empty_cb.setChecked(True)
    panel.settings_tab.load_data()
    assert panel.settings_tab.settings_table.rowCount() == 1  # Luca Bianchi (empty)
    assert panel.settings_tab.settings_table.item(0, 0).text() == "Luca"


def test_employee_detail_update(timbrature_db_panel, qtbot):
    panel = timbrature_db_panel
    panel.storage.get_employees.return_value = [
        {"nome": "Mario", "cognome": "Rossi", "reparto": "", "cantiere": ""}
    ]
    # Mock lists in storage so load_data finds them
    panel.storage.get_lists.return_value = {
        "reparti": ["NUOVO_REPARTO"],
        "cantieri": [],
    }

    panel.settings_tab.load_data()

    # Get combo from table (Cell 0, 2 is Reparto)
    combo_rep = panel.settings_tab.settings_table.cellWidget(0, 2)
    assert isinstance(combo_rep, QComboBox)

    # Trigger change
    with qtbot.waitSignal(combo_rep.currentTextChanged, timeout=1000):
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
        patch("src.core.audit_manager.AuditManager"),
        patch("src.gui.widgets.toast.ToastManager.instance") as mock_toast,
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

    with patch("src.gui.widgets.toast.ToastManager.instance") as mock_toast:
        panel._import_excel_manually()
        mock_toast.return_value.show.assert_called_with(ANY, "error")


def test_update_combo_boxes(timbrature_db_panel, qtbot):
    panel = timbrature_db_panel
    panel.storage.get_lists.return_value = {"reparti": ["R1"], "cantieri": ["C1"]}
    panel._update_filter_combos()

    assert panel.reparto_filter.count() == 2  # Tutti + R1
    assert panel.cantiere_filter.count() == 2  # Tutti + C1


@patch("PyQt6.QtWidgets.QDialog.exec")
@patch("PyQt6.QtWidgets.QInputDialog.getText")
def test_manage_list_add_item(mock_get_text, mock_exec, timbrature_db_panel, qtbot):
    # Nota: _manage_list è stato rimosso in favore delle impostazioni generali.
    # Questo test è obsoleto per TimbratureDBPanel ma lo manteniamo come stub se necessario.
    pass
