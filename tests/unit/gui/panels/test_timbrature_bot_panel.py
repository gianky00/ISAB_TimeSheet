"""Unit tests for TimbratureBotPanel."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QInputDialog

from src.gui.panels.timbrature_bot import TimbratureBotPanel


@pytest.fixture
def mock_config(mocker):
    """Fixture per mockare config_manager."""
    mock_load = mocker.patch("src.application.services.config_manager.load_config")
    mock_load.return_value = {
        "fornitori": ["COEMI", "ALTRO"],
        "last_timbrature_societa": "ISAB",
        "last_timbrature_fornitore": "COEMI",
    }
    mocker.patch("src.application.services.config_manager.set_config_value")
    mocker.patch(
        "src.application.services.config_manager.get_default_account",
        return_value={"username": "u", "password": "p"},
    )
    mocker.patch("src.application.services.config_manager.get_download_path", return_value="/mock/downloads")
    return mock_load


@pytest.fixture
def panel(qtbot, mock_config, mocker):
    """Istanza di TimbratureBotPanel per i test."""
    mocker.patch("PySide6.QtCore.QTimer.singleShot")
    mocker.patch("src.gui.styles.ui_effects.UIEffectsManager.apply_shadow")
    mocker.patch("src.gui.styles.ui_effects.UIEffectsManager.animate_fade")

    # Mocking get_credentials to return valid credentials
    mocker.patch("src.gui.panels.base.BaseBotPanel.get_credentials", return_value=("u", "p"))

    p = TimbratureBotPanel()
    qtbot.addWidget(p)
    return p


class TestTimbratureBotPanel:
    """Test suite per TimbratureBotPanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione del pannello."""
        assert panel.bot_id == "timbrature"
        assert panel.params_widget is not None
        assert panel.create_db_btn is not None

    def test_load_saved_data(self, qtbot, panel, mock_config):
        """Verifica il caricamento dei dati salvati."""
        panel._load_saved_data()

        assert panel.params_widget.get_societa() == "ISAB"
        assert panel.params_widget.get_fornitore() == "COEMI"

        # Verifica date (default ieri)
        yesterday = QDate.currentDate().addDays(-1).toString("dd.MM.yyyy")
        date_da, date_a = panel.params_widget.get_dates()
        assert date_da == yesterday
        assert date_a == yesterday

    def test_start_bot_trigger(self, qtbot, panel, mocker):
        """Verifica lbl'avvio del bot."""
        panel.params_widget.set_fornitore("COEMI")

        mock_worker_cls = mocker.patch("src.gui.panels.timbrature_bot.BotWorker")
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker

        mocker.patch.object(panel, "window", return_value=MagicMock())

        panel._on_start()

        assert mock_worker_cls.called
        assert mock_worker.start.called

        # Verifica log tramite conteggio widget (1 stretch iniziale + 1 log)
        assert panel.log_widget.log_layout.count() >= 2

    def test_create_database_clicked(self, qtbot, panel, mocker):
        """Verifica lbl'avvio della ricostruzione database."""
        mocker.patch.object(QInputDialog, "getInt", return_value=(2025, True))

        mock_start = mocker.patch.object(panel, "_on_start")
        panel.params_widget.set_fornitore("COEMI")

        qtbot.mouseClick(panel.create_db_btn, Qt.MouseButton.LeftButton)

        assert mock_start.called
        __args, kwargs = mock_start.call_args
        params = kwargs.get("params_override")
        assert "ranges" in params
        assert len(params["ranges"]) >= 1

    def test_generate_quarterly_ranges(self, panel):
        """Verifica la generazione dei trimestri."""
        ranges = panel._generate_quarterly_ranges(2026)
        assert len(ranges) >= 1
        assert "data_da" in ranges[0]
        assert ranges[0]["data_da"] == "01.01.2026"
        assert ranges[0]["data_a"] == "31.03.2026"

    def test_validate_ready(self, panel):
        """Verifica la validazione."""
        # Per testare il fallimento, forziamo il testo del combo a vuoto
        panel.params_widget.fornitore_combo.clear()

        ready, msg = panel.validate_ready()
        assert ready is False
        assert "fornitore" in msg.lower()

        # Ripristiniamo e testiamo successo
        panel.params_widget.fornitore_combo.addItems(["COEMI"])
        panel.params_widget.set_fornitore("COEMI")
        ready, msg = panel.validate_ready()
        assert ready is True

    def test_on_worker_finished_custom(self, qtbot, panel, mocker):
        """Verifica lbl'emissione del segnale di aggiornamento dati."""
        with qtbot.waitSignal(panel.data_updated):
            panel._on_worker_finished_custom(True)
