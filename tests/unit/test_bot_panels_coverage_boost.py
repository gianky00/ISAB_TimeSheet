from unittest.mock import MagicMock, patch

from src.gui.panels import ScaricoPDLPanel, TimbratureBotPanel


class TestBotPanelsFinalCoverage:
    def test_timbrature_bot_panel_autopilot(self, qapp, qtbot):
        with patch("src.gui.panels.config_manager.load_config", return_value={"fornitori": ["F1"]}):
            panel = TimbratureBotPanel()
            qtbot.addWidget(panel)

            panel.autopilot_check.setChecked(True)
            with patch("src.core.config_manager.set_config_value") as mock_set:
                panel._save_data()
                assert mock_set.called

    def test_scarico_pdl_panel_params(self, qapp, qtbot):
        with patch("src.gui.panels.get_installed_printers", return_value=["P1"]):
            panel = ScaricoPDLPanel()
            qtbot.addWidget(panel)

            panel.print_check.setChecked(True)
            with patch("src.core.config_manager.set_config_value") as mock_set:
                panel._save_data()
                assert mock_set.called

    def test_timbrature_bot_start_logic(self, qapp, qtbot):
        with patch("src.gui.panels.config_manager.load_config", return_value={"fornitori": ["F1"]}), \
             patch("src.gui.panels.BotWorker") as MockWorker:  # Mock the Worker class

            # Setup mock worker instance
            mock_worker_instance = MockWorker.return_value
            mock_worker_instance.start = MagicMock()

            panel = TimbratureBotPanel()
            qtbot.addWidget(panel)

            # Mock the main window to provide 'telegram'
            mock_win = MagicMock()
            mock_win.telegram = MagicMock()
            with patch.object(panel, "window", return_value=mock_win):
                # Mock validation success
                with patch.object(panel, "get_credentials", return_value=("u", "p")), \
                     patch.object(panel.params_widget, "get_fornitore", return_value="F1"), \
                     patch.object(panel.params_widget, "get_dates", return_value=("01.01.2024", "01.01.2024")), \
                     patch("src.bots.create_bot") as mock_create:

                    panel._on_start()
                    assert mock_create.called
                    assert panel.worker is not None
                    # Verify worker started
                    mock_worker_instance.start.assert_called_once()
