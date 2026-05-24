"""Unit tests for BugReportDialog."""

import pytest
from PySide6.QtWidgets import QFileDialog, QMessageBox

from src.gui.dialogs.bug_report_dialog import BugReportDialog, ReportWorker


@pytest.fixture
def mock_bug_reporter(mocker):
    """Fixture per mockare BugReporter."""
    return mocker.patch("src.gui.dialogs.bug_report_dialog.BugReporter")


class TestBugReportDialog:
    """Test suite per BugReportDialog."""

    def test_initialization(self, qtbot, mock_bug_reporter):
        """Verifica lbl'inizializzazione del dialog."""
        dialog = BugReportDialog()
        qtbot.addWidget(dialog)

        assert dialog.windowTitle() == "Segnala un Problema"
        assert dialog.btn_send.text() == "Genera e Invia"
        assert dialog.chk_include_logs.isChecked()

    def test_description_validation(self, qtbot, mocker):
        """Verifica la validazione della descrizione troppo breve."""
        dialog = BugReportDialog()
        qtbot.addWidget(dialog)

        mock_warn = mocker.patch.object(QMessageBox, "warning")

        dialog.txt_description.setText("Short")
        dialog.start_generation()

        assert mock_warn.called
        assert dialog.btn_send.isEnabled()  # Rimane abilitato se fallisce validazione

    def test_start_generation_ui_state(self, qtbot, mock_bug_reporter, mocker):
        """Verifica lo stato della UI durante la generazione."""
        dialog = BugReportDialog()
        qtbot.addWidget(dialog)
        dialog.show()  # Necessario per isVisible()

        # Evitiamo lbl'avvio reale del thread
        mocker.patch.object(ReportWorker, "start")

        dialog.txt_description.setText("Questa descrizione è lunga abbastanza per passare il controllo.")
        dialog.start_generation()

        assert not dialog.btn_send.isEnabled()
        assert not dialog.txt_description.isEnabled()
        assert dialog.progress.isVisible()

    def test_report_generated_success_with_outlook(self, qtbot, mocker):
        """Verifica il comportamento al termine della generazione con Outlook disponibile."""
        dialog = BugReportDialog()
        qtbot.addWidget(dialog)
        dialog.show()  # Necessario per isVisible()

        # Mock methods to avoid real logic
        mocker.patch.object(dialog, "open_outlook", return_value=True)
        mock_accept = mocker.patch.object(dialog, "accept")

        # Simula il testo della descrizione
        dialog.txt_description.setText("Valid description")

        dialog.on_report_generated(True, "OK", "test.zip", ["file1.log", "file2.json"])

        assert dialog.preview_group.isVisible()
        assert "file1.log" in dialog.preview_content.text()
        assert mock_accept.called

    def test_report_generated_success_no_outlook(self, qtbot, mocker):
        """Verifica il fallback al salvataggio manuale se Outlook fallisce."""
        dialog = BugReportDialog()
        qtbot.addWidget(dialog)

        mocker.patch.object(dialog, "open_outlook", return_value=False)
        mock_save = mocker.patch.object(dialog, "save_manually")
        mocker.patch.object(QMessageBox, "warning")

        dialog.on_report_generated(True, "OK", "test.zip", [])

        assert mock_save.called

    def test_save_manually(self, qtbot, mocker):
        """Verifica il salvataggio manuale tramite file dialog."""
        dialog = BugReportDialog()
        qtbot.addWidget(dialog)

        mocker.patch.object(QFileDialog, "getSaveFileName", return_value=("/path/to/dest.zip", "ZIP"))
        mock_copy = mocker.patch("shutil.copy2")
        mock_info = mocker.patch.object(QMessageBox, "information")

        dialog.save_manually("temp.zip")

        assert mock_copy.called
        assert mock_info.called

    def test_update_size_estimate(self, qtbot, mock_bug_reporter):
        """Verifica lbl'aggiornamento della label dimensione."""
        mock_bug_reporter.get_estimated_size.return_value = "1.5 MB"

        dialog = BugReportDialog()
        qtbot.addWidget(dialog)

        dialog._update_size_estimate()
        assert "1.5 MB" in dialog.lbl_size.text()

    def test_outlook_automation_mock(self, qtbot, mocker):
        """Verifica la logica di automazione Outlook (mocking win32com)."""
        mock_dispatch = mocker.patch("win32com.client.Dispatch")
        mock_outlook = mocker.MagicMock()
        mock_dispatch.return_value = mock_outlook

        dialog = BugReportDialog()
        qtbot.addWidget(dialog)

        # Mock license info to avoid real decryption
        mocker.patch.object(dialog, "_get_client_info", return_value="TEST CLIENT")

        # Setup metadata mock with ALL required keys
        mocker.patch.object(
            dialog,
            "_prepare_ticket_metadata",
            return_value={
                "ticket_id": "TKT-1234",
                "version": "1.0",
                "user": "TEST_USER",
                "subject_suffix": "test_suffix",
                "full_ticket_file": "test_file",
            },
        )

        res = dialog.open_outlook("dummy.zip", "Description")

        assert res is True
        assert mock_outlook.CreateItem.called
