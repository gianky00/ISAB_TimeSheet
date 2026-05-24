"""Unit tests for UpdaterDialog."""

from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QMessageBox

from src.gui.dialogs.updater_dialog import (
    UpdateProgressDialog,
    handle_update_result,
    perform_auto_update,
    show_install_prompt,
)


class TestUpdateProgressDialog:
    """Test suite per UpdateProgressDialog."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione del dialog."""
        # Mock DownloadWorker all'interno del costruttore
        with patch("src.gui.dialogs.updater_dialog.DownloadWorker"):
            dialog = UpdateProgressDialog("http://test.com/setup.exe")
            qtbot.addWidget(dialog)

            assert dialog.windowTitle() == "Aggiornamento SyncroJob"
            assert "Avvio download" in dialog.lbl_status.text()
            assert dialog.pb is not None

    def test_update_progress(self, qtbot, mocker):
        """Verifica lbl'aggiornamento della barra e delle label."""
        with patch("src.gui.dialogs.updater_dialog.DownloadWorker"):
            dialog = UpdateProgressDialog("http://test.com/setup.exe")
            qtbot.addWidget(dialog)

            # Simuliamo 5MB su 10MB scaricati a 1MB/s, 5s rimanenti
            dialog.update_progress(5 * 1024 * 1024, 10 * 1024 * 1024, 1024 * 1024, 5.0)

            assert "5.0 / 10.0 MB" in dialog.lbl_details.text()
            assert "1.00 MB/s" in dialog.lbl_details.text()
            assert "5s" in dialog.lbl_details.text()

            # Verifica animazione
            assert dialog.animation.endValue() == 50

    def test_on_retrying_feedback(self, qtbot):
        """Verifica feedback visivo su retry."""
        with patch("src.gui.dialogs.updater_dialog.DownloadWorker"):
            dialog = UpdateProgressDialog("url")
            qtbot.addWidget(dialog)

            dialog.on_retrying(3)
            assert "Tentativo #3" in dialog.lbl_retry.text()

    def test_on_finished_trigger(self, qtbot, mocker):
        """Verifica che la fine download apra il prompt di installazione."""
        with patch("src.gui.dialogs.updater_dialog.DownloadWorker"):
            dialog = UpdateProgressDialog("url")
            qtbot.addWidget(dialog)

            mock_prompt = mocker.patch("src.gui.dialogs.updater_dialog.show_install_prompt")

            dialog.on_finished("/path/to/setup.exe")

            assert mock_prompt.called
            assert mock_prompt.call_args[0][0] == "/path/to/setup.exe"

    def test_on_error_dialog(self, qtbot, mocker):
        """Verifica visualizzazione errore critico."""
        with patch("src.gui.dialogs.updater_dialog.DownloadWorker"):
            dialog = UpdateProgressDialog("url")
            qtbot.addWidget(dialog)

            mock_crit = mocker.patch.object(QMessageBox, "critical")

            dialog.on_error("Disk Full")

            assert mock_crit.called
            assert "Disk Full" in mock_crit.call_args[0][2]


class TestUpdaterFunctions:
    """Test per le funzioni helper dell'updater."""

    def test_show_install_prompt_now(self, mocker):
        """Verifica scelta 'Installa Ora'."""
        mock_msg = mocker.patch("src.gui.dialogs.updater_dialog.QMessageBox")
        instance = mock_msg.return_value

        # Simuliamo click su "Installa Ora"
        btn_now = MagicMock()
        instance.addButton.return_value = btn_now
        instance.clickedButton.return_value = btn_now

        mock_run = mocker.patch("src.gui.dialogs.updater_dialog.run_installer_and_exit")

        show_install_prompt("/path/exe")

        assert mock_run.called

    def test_handle_update_result_new_version(self, mocker):
        """Verifica gestione nuova versione disponibile."""
        mock_quest = mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.Yes)
        mock_perf = mocker.patch("src.gui.dialogs.updater_dialog.perform_auto_update")

        data = {"version": "2.0.0", "changelog": "New stuff", "url": "http://new", "is_complete": False}

        handle_update_result(data)

        assert mock_quest.called
        assert mock_perf.called
        assert mock_perf.call_args[0][0] == "http://new"

    def test_perform_auto_update_no_banner(self, mocker, qtbot):
        """Verifica avvio dialog se non c'è il banner in MainWindow."""
        mocker.patch("src.gui.dialogs.updater_dialog.DownloadWorker")
        mock_dialog_cls = mocker.patch("src.gui.dialogs.updater_dialog.UpdateProgressDialog")

        perform_auto_update("http://url")

        assert mock_dialog_cls.called
