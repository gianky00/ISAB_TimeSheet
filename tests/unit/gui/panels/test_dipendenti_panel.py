from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QDialog

from src.gui.panels.dipendenti_manager_panel import DipendentiManagerPanel, EmployeeEditorDialog


class TestDipendentiPanel:
    @pytest.fixture
    def panel(self, qtbot):
        with (
            patch(
                "src.gui.panels.dipendenti_manager_panel.employee_manager.get_all_employees", return_value=[]
            ),
            patch("src.core.sync_tracker.SyncTracker.get_formatted_status", return_value="N/D"),
        ):
            p = DipendentiManagerPanel()
            qtbot.addWidget(p)
            p.show()
            return p

    def test_initialization(self, panel):
        assert panel.lbl_count.text() == "0 Dipendenti"
        assert panel.table.columnCount() == 6

    def test_refresh_data_with_items(self, panel, qtbot):
        mock_employees = [
            {
                "id_risorsa": 1,
                "cognome": "Rossi",
                "nome": "Mario",
                "badge": "B1",
                "codice_fiscale": "CF1",
                "data_assunzione": "01/01/2020",
            },
            {
                "id_risorsa": 2,
                "cognome": "Bianchi",
                "nome": "Luigi",
                "badge": "B2",
                "codice_fiscale": "CF2",
                "data_assunzione": "01/01/2021",
            },
        ]
        with patch("src.core.employees.employee_manager.get_all_employees", return_value=mock_employees):
            panel.refresh_data()
            assert panel.table.rowCount() == 2
            assert "2 Dipendenti" in panel.lbl_count.text()
            assert panel.table.item(0, 1).text() == "Rossi"

    def test_filter_table(self, panel):
        from PySide6.QtWidgets import QTableWidgetItem

        # Setup table
        panel.table.setRowCount(2)
        panel.table.setItem(0, 1, QTableWidgetItem("Rossi"))
        panel.table.setItem(1, 1, QTableWidgetItem("Bianchi"))

        # Filter "Rossi"
        panel._filter_table("rossi")
        assert not panel.table.isRowHidden(0)
        assert panel.table.isRowHidden(1)

        # Reset
        panel._filter_table("")
        assert not panel.table.isRowHidden(1)

    @patch("src.gui.panels.dipendenti_manager_panel.QFileDialog.getOpenFileName")
    @patch("src.core.employees.employee_manager.import_from_csv")
    def test_sync_from_csv(self, mock_import, mock_file, panel):
        mock_file.return_value = ("/fake/file.csv", "")
        mock_import.return_value = 5

        with patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_info") as mock_info:
            panel._sync_from_csv()
            assert mock_import.called
            assert mock_info.called
            assert "5" in mock_info.call_args[0][2]

    @patch("src.gui.panels.dipendenti_manager_panel.EmployeeEditorDialog.exec")
    @patch("src.gui.panels.dipendenti_manager_panel.EmployeeEditorDialog.get_data")
    @patch("src.core.employees.employee_manager.add_employee")
    def test_add_employee_success(self, mock_add, mock_data, mock_exec, panel):
        mock_exec.return_value = QDialog.DialogCode.Accepted
        mock_data.return_value = {"badge": "B3"}
        mock_add.return_value = True

        panel._add_employee()
        assert mock_add.called

    @patch("src.gui.panels.dipendenti_manager_panel.ConfirmationDialog.show_warning")
    @patch("src.gui.panels.dipendenti_manager_panel.EmployeeEditorDialog.exec")
    @patch("src.gui.panels.dipendenti_manager_panel.EmployeeEditorDialog.get_data")
    @patch("src.core.employees.employee_manager.add_employee")
    def test_add_employee_fail(self, mock_add, mock_data, mock_exec, mock_warn, panel):
        mock_exec.return_value = QDialog.DialogCode.Accepted
        mock_data.return_value = {"badge": "B3"}
        mock_add.return_value = False

        panel._add_employee()
        assert mock_add.called
        assert mock_warn.called

    @patch("src.gui.panels.dipendenti_manager_panel.EmployeeEditorDialog.exec")
    @patch("src.gui.panels.dipendenti_manager_panel.EmployeeEditorDialog.get_data")
    @patch("src.core.employees.employee_manager.update_employee")
    def test_edit_selected_success(self, mock_update, mock_data, mock_exec, panel):
        # Setup selection
        from PySide6.QtWidgets import QTableWidgetItem

        panel.table.setRowCount(1)
        panel.table.setItem(0, 0, QTableWidgetItem("1"))
        panel.table.selectRow(0)

        mock_exec.return_value = QDialog.DialogCode.Accepted
        mock_data.return_value = {"badge": "B1-mod"}
        mock_update.return_value = True

        panel._edit_selected()
        assert mock_update.called


class TestEmployeeEditorDialog:
    def test_editor_dialog_get_data(self, qtbot):
        dlg = EmployeeEditorDialog()
        qtbot.addWidget(dlg)

        dlg.inputs["cognome"].setText("Verdi")
        dlg.inputs["nome"].setText("G")

        data = dlg.get_data()
        assert data["cognome"] == "VERDI"
        assert data["nome"] == "G"
