"""Unit tests for CaricoTSPanel."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt

from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.carico_ts import CaricoTSPanel


@pytest.fixture
def mock_config(mocker):
    """Fixture per mockare config_manager."""
    mock_load = mocker.patch("src.core.config_manager.load_config")
    # Colonne corrette per CaricoTSBot: numero_oda, posizione_oda
    mock_load.return_value = {
        "last_carico_ts_data": [{"numero_oda": "123", "posizione_oda": "10"}],
        "browser_headless": True,
        "browser_timeout": 30,
    }
    mocker.patch("src.core.config_manager.set_config_value")
    return mock_load


@pytest.fixture
def panel(qtbot, mock_config, mocker):
    """Istanza di CaricoTSPanel per i test."""
    mocker.patch("src.gui.panels.base.BaseBotPanel.get_credentials", return_value=("user", "pass"))
    mocker.patch("PySide6.QtCore.QTimer.singleShot")
    mocker.patch("src.gui.styles.ui_effects.UIEffectsManager.apply_shadow")
    mocker.patch("src.gui.styles.ui_effects.UIEffectsManager.animate_fade")

    p = CaricoTSPanel()
    qtbot.addWidget(p)
    return p


class TestCaricoTSPanel:
    """Test suite per CaricoTSPanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione del pannello."""
        assert panel.bot_id == "carico_ts"
        assert panel.data_table is not None
        assert panel.clear_btn is not None

    def test_load_saved_data(self, qtbot, panel, mock_config):
        """Verifica il caricamento dei dati salvati."""
        panel._load_saved_data()

        # EditableDataTable mantiene initial_rows (default 20)
        assert panel.data_table.table.rowCount() == 20
        assert panel.data_table.table.item(0, 0).text() == "123"

    def test_clear_table_confirmed(self, qtbot, panel, mocker):
        """Verifica la pulizia della tabella su conferma."""
        panel.data_table.set_data([{"numero_oda": "X"}])
        mocker.patch.object(ConfirmationDialog, "confirm", return_value=True)

        qtbot.mouseClick(panel.clear_btn, Qt.MouseButton.LeftButton)

        assert panel.data_table.table.rowCount() == 20
        assert panel.data_table.table.item(0, 0).text() == ""

    def test_start_bot_trigger(self, qtbot, panel, mocker):
        """Verifica il trigger di avvio del bot tramite BotWorker."""
        panel.data_table.set_data([{"numero_oda": "123", "posizione_oda": "10"}])

        mock_worker_cls = mocker.patch("src.gui.panels.carico_ts.BotWorker")
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker

        mocker.patch.object(panel, "window", return_value=MagicMock())

        # Assicuriamoci che validate_ready passi
        mocker.patch.object(panel, "get_credentials", return_value=("user", "pass"))

        qtbot.mouseClick(panel.start_btn, Qt.MouseButton.LeftButton)

        assert mock_worker_cls.called
        assert mock_worker.start.called
        assert not panel.start_btn.isEnabled()

    def test_validate_ready(self, panel, mocker):
        """Verifica la validazione dell'input."""
        # Caso: No credenziali
        mocker.patch.object(panel, "get_credentials", return_value=("", ""))
        ready, msg = panel.validate_ready()
        assert ready is False
        assert "Credenziali" in msg

        # Caso: No dati
        mocker.patch.object(panel, "get_credentials", return_value=("u", "p"))
        panel.data_table.set_data([])
        ready, msg = panel.validate_ready()
        assert ready is False
        assert "Nessun dato" in msg

        panel.data_table.set_data([{"numero_oda": "1"}])
        ready, msg = panel.validate_ready()
        assert ready is True

    def test_save_data_on_change(self, qtbot, panel, mocker):
        """Verifica che la modifica della tabella triggeri il salvataggio."""
        mock_set_cfg = mocker.patch("src.core.config_manager.set_config_value")

        # Simuliamo modifica dati
        panel.data_table.set_data([{"numero_oda": "val"}])

        assert mock_set_cfg.called
        assert mock_set_cfg.call_args[0][0] == "last_carico_ts_data"
