from unittest.mock import patch

import pytest
from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import QLabel

from src.core.constants import Icons
from src.gui.widgets.autopilot.config_cards import (
    AutopilotConfigCard,
    AutopilotConfigCardWithInterval,
)
from src.gui.widgets.autopilot.event_card import AutopilotEventCard
from src.gui.widgets.autopilot.main_widget import AutopilotWidget


class TestAutopilotGUI:
    @pytest.fixture(autouse=True)
    def setup_qt(self, qtbot):
        self.qtbot = qtbot

    @pytest.fixture
    def autopilot(self):
        with patch("src.core.config_manager.load_config", return_value={}):
            widget = AutopilotWidget()
            # Mostra il widget per rendere isVisible() affidabile
            widget.show()
            self.qtbot.addWidget(widget)
            return widget

    def test_initial_state(self, autopilot):
        """Verifica lo stato iniziale del widget."""
        assert not autopilot.view_widget.isHidden()
        assert autopilot.config_widget.isHidden()
        # Verifica indicator LIVE
        assert autopilot.live_text.text() == "LIVE"

    def test_toggle_mode(self, autopilot):
        """Testa il passaggio tra modalità visualizzazione e configurazione."""
        # Mock animazioni per velocità ed evitare side effects
        with patch.object(autopilot, "_animate_transition"):
            # Passa a config
            autopilot._toggle_mode()
            assert autopilot._config_mode is True

            # Reset animating flag per permettere il secondo toggle
            autopilot._animating = False

            # Passa a view
            autopilot._toggle_mode()
            assert autopilot._config_mode is False

    def test_refresh_events_dynamic(self, autopilot):
        """Testa che le card degli eventi vengano create in base alla configurazione."""
        mock_config = {
            "timbrature_autopilot_enabled": True,
            "timbrature_autopilot_time": "10:30",
            "ricerca_pdl_autopilot_enabled": True,
            "ricerca_pdl_autopilot_time": "14:00",
        }

        with patch("src.core.config_manager.load_config", return_value=mock_config):
            autopilot.refresh_events()

            # Conta le card nel view_layout
            cards = []
            for i in range(autopilot.view_layout.count()):
                w = autopilot.view_layout.itemAt(i).widget()
                if isinstance(w, AutopilotEventCard):
                    cards.append(w)

            assert len(cards) == 2
            # Verifica dettagli di una card tramite attributi
            assert any("Timbrature" in c.bot_name for c in cards)
            assert any(c.target_time_str == "10:30" for c in cards)

    def test_config_card_loading(self, qtbot, mocker):
        """Testa il caricamento dei dati in una config card."""
        # Creiamo un dizionario di configurazione ad hoc
        test_config = {
            "test_bot_autopilot_enabled": True,
            "test_bot_autopilot_time": "11:45",
        }

        # Mocking radicale del config_manager nel modulo della card
        mock_manager = mocker.patch("src.gui.widgets.autopilot.config_cards.config_manager")
        mock_manager.load_config.return_value = test_config

        card = AutopilotConfigCard("test_bot", "Test Bot", Icons.CLOCK, "#ff0000")
        qtbot.addWidget(card)

        # Verifica enabled
        assert card.enable_check.isChecked() is True

        # Verifica time
        assert card.time_edit.time().toString("HH:mm") == "11:45"

    def test_config_card_save(self, qtbot):
        """Testa il salvataggio dei dati quando la card viene modificata."""
        with (
            patch("src.core.config_manager.load_config", return_value={}),
            patch("src.core.config_manager.set_config_value") as mock_set,
        ):
            card = AutopilotConfigCard("test_bot", "Test Bot", Icons.CLOCK, "#ff0000")
            qtbot.addWidget(card)

            # Simula cambio stato checkbox
            card.enable_check.setChecked(True)
            mock_set.assert_any_call("test_bot_autopilot_enabled", True)

            # Simula cambio orario
            new_time = QTime(15, 30)
            card.time_edit.setTime(new_time)
            mock_set.assert_any_call("test_bot_autopilot_time", "15:30")

    def test_config_card_interval_save(self, qtbot):
        """Testa il salvataggio per la card con intervallo."""
        with (
            patch("src.core.config_manager.load_config", return_value={}),
            patch("src.core.config_manager.set_config_value") as mock_set,
        ):
            card = AutopilotConfigCardWithInterval("report", "Report", Icons.SEND, "#00ff00")
            qtbot.addWidget(card)

            card.interval_spin.setValue(10)
            mock_set.assert_any_call("report_autopilot_interval_days", 10)

    def test_empty_events_placeholder(self, autopilot):
        """Verifica il placeholder quando non ci sono bot programmati."""
        with patch("src.core.config_manager.load_config", return_value={}):
            autopilot.refresh_events()

            # Cerca la label di placeholder
            found_placeholder = False
            for i in range(autopilot.view_layout.count()):
                w = autopilot.view_layout.itemAt(i).widget()
                if isinstance(w, QLabel) and "Nessun bot" in w.text():
                    found_placeholder = True
                    break
            assert found_placeholder is True
