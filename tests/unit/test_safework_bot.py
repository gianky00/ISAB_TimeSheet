from unittest.mock import MagicMock, patch

import pytest

from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkBot:

    @pytest.fixture
    def bot(self):
        with patch("src.bots.safework.base.SafeworkBaseBot._init_driver"), patch(
            "src.bots.safework.pdl.bot.SafeWorkPDLBot.__init__", return_value=None
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
    @patch.object(SafeWorkPDLBot, "_process_single_pdl_mock", create=True)  # Mock logic
    def test_run_loop(self, mock_process, mock_sleep, bot):
        data = [{"numero_pdl": "123"}, {"pdl_number": "456", "print_enabled": True}]

        # We need to patch the run method or the internal calls
        with patch.object(bot, "_gestisci_alert_ricerca", return_value=True), patch.object(
            bot, "_attendi_scomparsa_overlay", return_value=True
        ), patch.object(bot, "_attendi_e_ritorna_nuovo_pdf", return_value="file.pdf"), patch.object(
            bot, "_unisci_pdf", return_value=True
        ), patch(
            "os.rename"
        ), patch(
            "os.remove"
        ), patch(
            "os.path.exists", return_value=True
        ):

            success = bot.run(data)
            assert success is True

    @patch("src.bots.safework.pdl.bot.time.sleep")
    @patch("src.bots.safework.pdl.bot.fitz")
    def test_unisci_pdf(self, mock_fitz, mock_sleep, bot):
        mock_doc = MagicMock()
        mock_fitz.open.return_value = mock_doc
        # context manager
        mock_fitz.open.return_value.__enter__.return_value = mock_doc

        result = bot._unisci_pdf("a.pdf", "b.pdf", "out.pdf")

        assert result is True
        assert mock_doc.insert_pdf.call_count == 2
        mock_doc.save.assert_called_with("out.pdf")
