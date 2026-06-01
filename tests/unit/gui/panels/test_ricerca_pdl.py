from unittest.mock import MagicMock

import pytest

from src.gui.panels.ricerca_pdl import RicercaPDLPanel


@pytest.fixture
def panel(qtbot, mocker):
    """Istanza di RicercaPDLPanel con mocking dei controller."""
    # Mock BotExecutionController per evitare thread reali
    mocker.patch("src.gui.controllers.bot_execution_controller.BotExecutionController")
    # Mock config_manager per evitare scritture su disco
    mocker.patch("src.core.config_manager.load_config", return_value={})
    mocker.patch("src.core.config_manager.set_config_value")

    p = RicercaPDLPanel()
    qtbot.addWidget(p)
    return p


class TestRicercaPDLPanel:
    """Test suite per RicercaPDLPanel."""

    def test_initialization(self, panel):
        """Verifica l'inizializzazione corretta dei componenti."""
        assert panel.bot_id == "ricerca_pdl"
        assert panel.sync_module_id == "pdl"
        assert panel.exclude_closed_check is not None
        assert panel.site_combo is not None
        assert panel.exclude_closed_check.isChecked() is True

    def test_load_saved_data(self, qtbot, mocker):
        """Verifica il caricamento dei dati dalla configurazione."""
        mock_config = {"pdl_search_exclude_closed": False, "pdl_search_site": "ISAB Nord"}
        mocker.patch("src.core.config_manager.load_config", return_value=mock_config)
        mocker.patch("src.gui.controllers.bot_execution_controller.BotExecutionController")

        p = RicercaPDLPanel()
        qtbot.addWidget(p)

        # Chiamata manuale perché showEvent è asincrono via timer
        p._load_saved_data()

        assert p.exclude_closed_check.isChecked() is False
        assert p.site_combo.currentText() == "ISAB Nord"

    def test_save_data(self, panel, mocker):
        """Verifica il salvataggio dei dati in configurazione."""
        mock_set = mocker.patch("src.core.config_manager.set_config_value")

        panel.exclude_closed_check.setChecked(True)
        panel.site_combo.setCurrentText("ISAB Sud")

        panel._save_data()

        # Verifica chiamate multiple per i due parametri
        mock_set.assert_any_call("pdl_search_exclude_closed", True)
        mock_set.assert_any_call("pdl_search_site", "ISAB Sud")

    def test_get_safework_credentials(self, panel, mocker):
        """Verifica il recupero delle credenziali."""
        mock_config = {
            "safework_accounts": [
                {"username": "user1", "password": "p1", "type": "ISAB", "default": False},
                {"username": "user2", "password": "p2", "type": "Esecutore", "default": True},
            ]
        }
        mocker.patch("src.core.config_manager.load_config", return_value=mock_config)

        user, pwd, acc_type = panel.get_safework_credentials()
        assert user == "user2"
        assert pwd == "p2"
        assert acc_type == "Esecutore"

    def test_validate_and_switch_account_isab_to_esecutore(self, panel, mocker):
        """Verifica lo switch dell'account da ISAB a Esecutore."""
        mock_config = {
            "safework_accounts": [{"username": "exec_user", "password": "p_exec", "type": "Esecutore"}]
        }
        mocker.patch("src.core.config_manager.load_config", return_value=mock_config)
        mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.confirm", return_value=True)
        mocker.patch("src.core.config_manager.set_default_account", return_value=True)

        u, _p, t, ok = panel._validate_and_switch_account("isab_user", "p_isab", "ISAB")

        assert ok is True
        assert u == "exec_user"
        assert t == "Esecutore"

    def test_on_start_bot_logic(self, panel, mocker):
        """Verifica la logica di avvio del bot."""
        # Mock credenziali
        mocker.patch.object(panel, "get_safework_credentials", return_value=("user", "pass", "Esecutore"))
        # Mock switch (già Esecutore)
        mocker.patch.object(
            panel, "_validate_and_switch_account", return_value=("user", "pass", "Esecutore", True)
        )

        mock_start = mocker.patch.object(panel.bot_controller, "start", return_value=True)

        panel._on_start()

        assert mock_start.called
        assert panel.bot_controller.start.call_args[0][0]["username"] == "user"

    def test_on_worker_finished_emits_updated(self, panel):
        """Verifica l'emissione del segnale al termine con successo."""
        mock_slot = MagicMock()
        panel.data_updated.connect(mock_slot)
        panel._on_worker_finished(True)
        assert mock_slot.called
