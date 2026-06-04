"""Unit tests for ScaricoPDLPanel."""

from unittest.mock import MagicMock, patch

import pytest

# Mock SafeWorkPDLBot BEFORE importing ScaricoPDLPanel
mock_bot_module = MagicMock()
mock_bot_class = MagicMock()
mock_bot_class.STEPS = ["start", "search"]
mock_bot_class.get_columns.return_value = [{"name": "numero_pdl", "label": "Numero PDL", "type": "text"}]
mock_bot_module.SafeWorkPDLBot = mock_bot_class

with patch.dict("sys.modules", {"src.infrastructure.bots.safework.pdl.bot": mock_bot_module}):
    from src.gui.panels.scarico_pdl import ScaricoPDLPanel


@pytest.fixture
def mock_service(mocker):
    """Fixture per mockare ScaricoPDLService."""
    mock_cls = mocker.patch("src.application.services.bots.services.ScaricoPDLService")
    instance = MagicMock()
    instance.load_config.return_value = {
        "stampa": False,
        "stampante": "",
        "dest_path": "/mock/pdl",
        "data": [{"numero_pdl": "PDL-2026-001"}],
    }
    instance.prepare_payload.return_value = ({"p": 1}, {"d": 1})
    mock_cls.return_value = instance
    return instance


@pytest.fixture
def panel(qtbot, mock_service, mocker):
    """Istanza di ScaricoPDLPanel per i test."""
    mocker.patch("PySide6.QtCore.QTimer.singleShot")
    mocker.patch("src.gui.styles.ui_effects.UIEffectsManager.apply_shadow")
    mocker.patch("src.gui.styles.ui_effects.UIEffectsManager.animate_fade")
    mocker.patch("src.infrastructure.utils.printing.get_installed_printers", return_value=["Printer1", "Printer2"])
    mocker.patch(
        "src.application.services.config_manager.get_default_account", return_value={"username": "u", "password": "p"}
    )

    p = ScaricoPDLPanel()
    p.get_safework_credentials = MagicMock(return_value=("sw_user", "sw_pass", "Esecutore"))

    qtbot.addWidget(p)
    return p


class TestScaricoPDLPanel:
    """Test suite per ScaricoPDLPanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione del pannello."""
        assert panel.bot_id == "scarico_pdl"

    def test_load_saved_data(self, qtbot, panel, mock_service):
        """Verifica il caricamento dei dati salvati."""
        panel.data_table.clear()
        panel._load_saved_data()

        data = panel.data_table.get_data()
        assert len(data) >= 1
        assert data[0]["numero_pdl"] == "PDL-2026-001"

    def test_on_step_completed(self, qtbot, panel):
        """Verifica lbl'aggiornamento visivo della riga."""
        panel.data_table.set_data([{"numero_pdl": "P1"}])
        panel._update_status_list(force=True)

        panel.on_step_completed(0, True, "OK")

        data = panel.data_table.get_data()
        assert "Completato" in data[0]["esito"]

    def test_validate_ready(self, panel):
        """Verifica la validazione."""
        panel.data_table.clear()
        ready, _msg = panel.validate_ready()
        assert ready is False

        panel.data_table.set_data([{"numero_pdl": "123"}])
        ready, _msg = panel.validate_ready()
        assert ready is True

    def test_on_browse_clicked(self, panel, mocker):
        """Verifica la selezione cartella tramite dialogo."""
        mocker.patch("PySide6.QtWidgets.QFileDialog.getExistingDirectory", return_value="/new/path")
        panel._on_browse_clicked()
        assert panel.edit_dest.text() == "/new/path"
