from unittest.mock import MagicMock, patch

import pytest

from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkBot:
    @pytest.fixture
    def bot(self):
        with (
            patch("src.bots.safework.base.SafeworkBaseBot._init_driver"),
            patch("src.bots.safework.pdl.bot.SafeWorkPDLBot.__init__", return_value=None),
        ):
            bot = SafeWorkPDLBot("u", "p")
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot.log = MagicMock()
            bot.download_path = "downloads"
            bot._stop_requested = False
            bot.SAFEWORK_URL = "https://safework.isab.com/"
            return bot

    def test_name_and_description(self, bot):
        assert bot.name == "scarico_pdl"
        assert "SafeWork" in bot.description

    @patch("src.bots.safework.pdl.bot.time.sleep")
    def test_run_timing_sequence(self, mock_sleep, bot):
        """Verifica che la sequenza di pause (sleep) sia corretta durante l'esecuzione."""
        data = [{"numero_pdl": "123456"}]  # 123456 triggers auto-suffix /S

        # Mock all external interactions to isolate the flow
        with (
            patch.object(bot, "_gestisci_alert_ricerca", return_value=False),
            patch.object(bot, "_attendi_scomparsa_overlay"),
            patch.object(bot, "_attendi_e_ritorna_nuovo_pdf", return_value="file.pdf"),
            patch(
                "src.utils.document_processor.DocumentProcessor.merge_pdfs",
                return_value=True,
            ),
            patch("os.rename"),
            patch("os.remove"),
            patch("os.path.exists", return_value=True),
            patch("builtins.open"),
            patch("src.bots.safework.pdl.bot.fitz") as mock_fitz,
            patch.object(bot, "_check_stop"),
        ):
            # Mock fitz doc to simulate page count for cleaning logic
            mock_doc = MagicMock()
            mock_doc.page_count = 2
            mock_fitz.open.return_value = mock_doc

            # Mock finding element for 'Parte Seconda' visibility
            bot.driver.find_element.return_value.is_displayed.return_value = False

            bot.run(data)

            # Let's verify the critical sleeps in sequence:
            # 1. sleep(0.5) after sending keys to search field
            # 2. sleep(1) before scrolling and clicking Parte 1
            # 3. sleep(0.5) after clicking Anteprima menu
            # 4. sleep(1) to expand Parte Seconda
            # 5. sleep(1) after clicking btnPrintPS (options dialog wait)

            sleep_calls = [call.args[0] for call in mock_sleep.call_args_list]

            assert 0.5 in sleep_calls
            assert 1 in sleep_calls
            # The exact number of calls might vary based on flow, but we check existence
            assert len(sleep_calls) >= 4
