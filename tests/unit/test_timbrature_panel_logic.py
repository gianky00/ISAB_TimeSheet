from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels.timbrature.panel import TimbratureDBPanel


@pytest.fixture
def panel(qtbot):
    # Mock dependencies BEFORE instantiation to avoid I/O
    with (
        patch("src.gui.panels.timbrature.panel.TimbratureStorage"),
        patch("src.gui.panels.timbrature.panel.config_manager.load_config", return_value={}),
        patch("src.gui.panels.timbrature.panel.get_asset_path", return_value=""),
        patch("src.gui.panels.timbrature.panel.config_manager.CONFIG_DIR", MagicMock()),
    ):
        widget = TimbratureDBPanel()
        qtbot.addWidget(widget)
        return widget


def test_initialization(panel):
    assert panel.storage is not None
    assert panel.settings_tab.settings_table.rowCount() == 0


def test_load_settings_data_filtering(panel):
    """Test logica di filtraggio dipendenti (vuoti vs tutti)."""
    # Mock data
    mock_employees = [
        {"nome": "Mario", "cognome": "Rossi", "reparto": "R1", "cantiere": "C1"},
        {"nome": "Luca", "cognome": "Bianchi", "reparto": "", "cantiere": ""},
    ]
    panel.storage.get_employees.return_value = mock_employees

    # 1. Filter Disabled (Show All)
    panel.settings_tab.filter_empty_cb.setChecked(False)
    panel.settings_tab.load_data()

    assert panel.settings_tab.settings_table.rowCount() == 2

    # 2. Filter Enabled (Show Only Empty)
    panel.settings_tab.filter_empty_cb.setChecked(True)
    panel.settings_tab.load_data()

    assert panel.settings_tab.settings_table.rowCount() == 1
    assert panel.settings_tab.settings_table.item(0, 0).text() == "Luca"


def test_update_employee_details(panel, qtbot):
    """Test che il cambio di combo chiami lo storage."""
    # Mock storage responses
    panel.storage.get_lists.return_value = {"reparti": ["R1", "R2"], "cantieri": []}
    mock_employees = [{"nome": "Mario", "cognome": "Rossi", "reparto": "", "cantiere": ""}]
    panel.storage.get_employees.return_value = mock_employees

    panel.settings_tab.load_data()

    # Get combo widget from cell (0, 2 is Reparto)
    combo = panel.settings_tab.settings_table.cellWidget(0, 2)
    assert combo.count() == 3  # "", "R1", "R2"

    # Change selection via index
    combo.setCurrentIndex(1)  # Select "R1"
    assert combo.currentText() == "R1"

    # Verify storage update called with wait
    qtbot.waitUntil(lambda: panel.storage.update_employee_details.called, timeout=5000)
    panel.storage.update_employee_details.assert_called_with("Mario", "Rossi", reparto="R1")


def test_import_excel_logic(panel):
    """Test logica importazione manuale."""
    with (
        patch(
            "PyQt6.QtWidgets.QFileDialog.getOpenFileName",
            return_value=("test.xlsx", "Excel"),
        ),
        patch("src.gui.panels.timbrature.panel.ToastManager.instance") as mock_toast,
    ):
        # Case 1: Success
        panel.storage.import_excel.return_value = True
        panel._import_excel_manually()

        mock_toast.return_value.show.assert_called_with("Dati importati correttamente.", "success")

        # Case 2: Failure
        panel.storage.import_excel.return_value = False
        panel._import_excel_manually()
        mock_toast.return_value.show.assert_called_with("Impossibile importare il file.", "error")
