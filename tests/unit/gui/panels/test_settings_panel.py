"""Unit tests for SettingsPanel."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from src.gui.panels.settings.main_panel import ConfigSaveWorker, SettingsPanel


class MockTabWidget(QWidget):
    """Sottoclasse di QWidget che include i segnali attesi dai tab delle impostazioni."""

    settings_changed = Signal()

    def load_from_config(self, cfg):
        pass

    def save_to_config(self, cfg):
        pass

    def refresh(self):
        pass


@pytest.fixture
def mock_tabs(mocker):
    """Mock dei tab interni per isolare SettingsPanel."""
    m_config = MockTabWidget()
    m_backup = MockTabWidget()
    m_roi = MockTabWidget()
    m_telegram = MockTabWidget()

    mocker.patch("src.gui.panels.settings.main_panel.ConfigTab", return_value=m_config)
    mocker.patch("src.gui.panels.settings.main_panel.BackupTab", return_value=m_backup)
    mocker.patch("src.gui.panels.settings.main_panel.ROITab", return_value=m_roi)
    mocker.patch("src.gui.panels.settings.main_panel.TelegramTab", return_value=m_telegram)

    return {"config": m_config, "backup": m_backup, "roi": m_roi, "telegram": m_telegram}


@pytest.fixture
def mock_config(mocker):
    """Mock config_manager."""
    mocker.patch("src.core.config_manager.load_config", return_value={"theme": "dark"})
    mocker.patch("src.core.config_manager.save_config")
    mocker.patch("src.core.config_manager.reset_to_defaults")


@pytest.fixture
def panel(qtbot, mock_tabs, mock_config):
    p = SettingsPanel()
    qtbot.addWidget(p)
    return p


class TestSettingsPanel:
    """Test suite per SettingsPanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione del pannello e dei tab."""
        assert panel.tabs.count() == 4

    def test_load_settings(self, panel, mocker, mock_tabs):
        """Verifica che load_settings chiami i metodi di caricamento sui tab."""
        mock_load_config = mocker.patch.object(mock_tabs["config"], "load_from_config")
        mock_load_roi = mocker.patch.object(mock_tabs["roi"], "load_from_config")

        panel.load_settings()

        assert mock_load_config.called
        assert mock_load_roi.called

    def test_save_settings_debounce(self, qtbot, panel):
        """Verifica che il salvataggio sia ritardato dal timer (debounce)."""
        panel._is_loading = False
        panel.save_settings()
        assert panel._save_timer.isActive()

    def test_execute_async_save(self, qtbot, panel, mocker, mock_tabs):
        """Verifica lbl'avvio del worker di salvataggio."""
        mock_worker_cls = mocker.patch("src.gui.panels.settings.main_panel.ConfigSaveWorker")
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker

        mock_save_config = mocker.patch.object(mock_tabs["config"], "save_to_config")

        panel._execute_async_save()

        assert mock_worker_cls.called
        assert mock_worker.start.called
        assert mock_save_config.called

    def test_reset_to_defaults(self, qtbot, panel, mocker):
        """Verifica il reset con conferma."""
        from src.gui.dialogs.confirmation_dialog import ConfirmationDialog

        mocker.patch.object(ConfirmationDialog, "confirm", return_value=True)
        mock_reset = mocker.patch("src.core.config_manager.reset_to_defaults")

        qtbot.mouseClick(panel.btn_reset, Qt.MouseButton.LeftButton)
        assert mock_reset.called

    def test_export_config(self, qtbot, panel, mocker):
        """Verifica lbl'esportazione file."""
        mocker.patch(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName", return_value=("/mock/backup.json", "JSON")
        )
        mock_shutil = mocker.patch("shutil.copy")
        mocker.patch("src.core.config_manager.CONFIG_FILE", "/path/to/cfg")

        qtbot.mouseClick(panel.btn_export, Qt.MouseButton.LeftButton)
        assert mock_shutil.called


class TestConfigSaveWorker:
    """Test suite per ConfigSaveWorker."""

    def test_run_success(self, qtbot, mocker):
        mocker.patch("src.core.config_manager.save_config")
        worker = ConfigSaveWorker({"test": 1})

        with qtbot.waitSignal(worker.finished) as blocker:
            worker.run()

        assert blocker.args == [True, ""]

    def test_run_failure(self, qtbot, mocker):
        mocker.patch("src.core.config_manager.save_config", side_effect=Exception("Disk Full"))
        worker = ConfigSaveWorker({})

        with qtbot.waitSignal(worker.finished) as blocker:
            worker.run()

        assert blocker.args == [False, "Disk Full"]
