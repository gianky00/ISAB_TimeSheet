from unittest.mock import MagicMock, patch

import pytest

from src.core.telegram_bridge import TelegramUIBridge


class TestTelegramUIBridge:
    @pytest.fixture
    def mock_mw(self):
        mw = MagicMock()
        mw.telegram = MagicMock()
        return mw

    @pytest.fixture
    def bridge(self, mock_mw):
        # Patch QObject.__init__ per evitare inizializzazione Qt reale
        with patch("src.core.telegram_bridge.QObject.__init__"):
            return TelegramUIBridge(mock_mw)

    def test_setup_connections(self, bridge):
        """Verifica il collegamento dei segnali Telegram."""
        bridge.setup_connections()
        bridge.telegram.command_received.connect.assert_called()
        bridge.telegram.data_received.connect.assert_called()
        bridge.telegram.status_requested.connect.assert_called()
        bridge.telegram.query_received.connect.assert_called()

    def test_dispatch_command_run_ts(self, bridge):
        """Verifica la delega del comando run_ts a ui_commands."""
        with patch.object(bridge.ui_commands, "run_ts_bot") as mock_run:
            bridge._dispatch_command("run_ts", {})
            mock_run.assert_called_once()

    def test_dispatch_command_run_pdl(self, bridge):
        """Verifica la delega del comando run_pdl a ui_commands."""
        params = {"id": "123"}
        with patch.object(bridge.ui_commands, "run_pdl_bot") as mock_run:
            bridge._dispatch_command("run_pdl", params)
            mock_run.assert_called_with(params)

    def test_dispatch_data_pdl(self, bridge):
        """Verifica la delega del processamento dati PDL a data_processor."""
        items = ["PDL1", "PDL2"]
        with patch.object(bridge.data_processor, "process_pdl_items") as mock_proc:
            bridge._dispatch_data("pdl", items)
            mock_proc.assert_called_with(items)

    @patch("src.core.telegram_bridge.SecretsManager.get_gemini_api_key", return_value=None)
    def test_handle_ai_query_no_key(self, mock_key, bridge):
        """Verifica segnalazione errore se manca API Key."""
        bridge._handle_ai_query(123, "ciao")
        bridge.telegram.send_message_sync.assert_called_with("⚠️ API Key mancante.")

    @patch("src.core.telegram_bridge.LyraClient")
    @patch("src.core.telegram_bridge.SecretsManager.get_gemini_api_key", return_value="fake")
    def test_handle_ai_query_success(self, mock_key, mock_lyra_cls, bridge):
        """Verifica avvio thread per query AI."""
        mock_lyra = mock_lyra_cls.return_value
        mock_lyra.ask.return_value = "Risposta"

        with patch("src.core.telegram_bridge.threading.Thread") as mock_thread:
            bridge._handle_ai_query(123, "test")
            assert mock_thread.called
            # Recuperiamo la funzione passata al thread ed eseguiamola
            thread_fn = mock_thread.call_args[1]["target"]
            thread_fn()

            bridge.telegram.send_message_sync.assert_called()
            args = bridge.telegram.send_message_sync.call_args[0][0]
            assert "Risposta" in args
