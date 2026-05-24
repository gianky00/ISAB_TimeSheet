"""Unit tests for PrenotaBPPanel."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt

from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.prenota_bp import PrenotaBPPanel


@pytest.fixture
def mock_config(mocker):
    """Fixture per mockare config_manager."""
    mock = mocker.patch("src.core.config_manager.load_config")
    # Configurazione con fornitore atteso
    mock.return_value = {
        "fornitori": ["COEMI", "ALTRO"],
        "last_login_date": "20/05/2026",
        "isab_accounts": [{"username": "u", "password": "p", "is_default": True}],
    }
    return mock


@pytest.fixture
def mock_service(mocker):
    """Fixture per mockare PrenotaBPService."""
    mock_cls = mocker.patch("src.core.bots.services.PrenotaBPService")
    instance = MagicMock()

    instance.load_config.return_value = {
        "societa": "ISAB",
        "fornitore": "COEMI",
        "data_da": "01.05.2026",
        "data_a": "31.05.2026",
        "data": [{"numero_bp": "BP123"}],
    }

    instance.prepare_payload.return_value = ({"param1": "val1"}, {"rows": []})
    mock_cls.return_value = instance
    return instance


@pytest.fixture
def panel(qtbot, mock_config, mock_service, mocker):
    """Istanza di PrenotaBPPanel per i test."""
    mocker.patch("src.gui.panels.base.BaseBotPanel.get_credentials", return_value=("user", "pass"))
    mocker.patch("PySide6.QtCore.QTimer.singleShot")
    mocker.patch("src.gui.styles.ui_effects.UIEffectsManager.apply_shadow")
    mocker.patch("src.gui.styles.ui_effects.UIEffectsManager.animate_fade")

    p = PrenotaBPPanel()
    qtbot.addWidget(p)
    return p


class TestPrenotaBPPanel:
    """Test suite per PrenotaBPPanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione del pannello."""
        assert panel.bot_id == "prenota_bp"
        assert panel.params_widget is not None
        assert panel.data_table is not None

    def test_load_saved_data(self, qtbot, panel, mock_service):
        """Verifica il caricamento dei dati salvati."""
        panel._load_saved_data()

        assert panel.params_widget.get_societa() == "ISAB"
        assert panel.params_widget.get_fornitore() == "COEMI"
        # EditableDataTable mantiene initial_rows (default 20)
        assert panel.data_table.table.rowCount() == 20
        assert panel.data_table.table.item(0, 0).text() == "BP123"

    def test_clear_table_confirmed(self, qtbot, panel, mocker):
        """Verifica la pulizia della tabella su conferma."""
        # Aggiungiamo un dato reale
        panel.data_table.set_data([{"numero_bp": "X"}])
        mocker.patch.object(ConfirmationDialog, "confirm", return_value=True)

        qtbot.mouseClick(panel.clear_btn, Qt.MouseButton.LeftButton)

        # Dopo clear(), ripristina le 20 righe vuote
        assert panel.data_table.table.rowCount() == 20
        assert panel.data_table.table.item(0, 0).text() == ""

    def test_on_step_completed_success(self, qtbot, panel):
        """Verifica lbl'aggiornamento visivo al completamento di una riga."""
        panel.data_table.set_data([{"numero_bp": "BP1"}])
        panel._update_status_list(force=True)

        panel.on_step_completed(0, True, "OK")

        # Cerchiamo la colonna ESITO
        col_idx = -1
        for i, col in enumerate(panel.data_table.columns):
            if col["name"] == "esito":
                col_idx = i
                break

        assert panel.data_table.table.item(0, col_idx).text() == "Completato"

    def test_start_bot_trigger(self, qtbot, panel, mocker, mock_service):
        """Verifica il trigger di avvio del bot tramite controller."""
        panel.params_widget.set_societa("ISAB")
        panel.params_widget.set_fornitore("COEMI")
        panel.data_table.set_data([{"numero_bp": "BP1"}])

        mocker.patch.object(panel, "validate_ready", return_value=(True, ""))
        mock_ctrl_start = mocker.patch.object(panel.bot_controller, "start", return_value=True)
        mocker.patch.object(panel, "window", return_value=MagicMock())

        qtbot.mouseClick(panel.start_btn, Qt.MouseButton.LeftButton)

        assert mock_ctrl_start.called
        assert not panel.start_btn.isEnabled()

    def test_stop_bot_trigger(self, qtbot, panel, mocker):
        """Verifica il trigger di stop."""
        mock_ctrl_stop = mocker.patch.object(panel.bot_controller, "stop")

        panel.start_btn.setEnabled(False)
        panel.stop_btn.setEnabled(True)

        qtbot.mouseClick(panel.stop_btn, Qt.MouseButton.LeftButton)

        assert mock_ctrl_stop.called

        # Simuliamo il segnale di fine dal controller per riabilitare i bottoni
        panel._on_worker_finished(True)
        assert panel.start_btn.isEnabled()
