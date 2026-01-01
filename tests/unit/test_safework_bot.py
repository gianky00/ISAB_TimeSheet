import pytest
from unittest.mock import patch, MagicMock
from src.bots.safework.pdl.bot import SafeWorkPDLBot

class TestSafeWorkBot:

    @pytest.fixture
    def bot(self):
        with patch('src.bots.safework.base.SafeworkBaseBot._init_driver'), \
             patch('src.bots.safework.pdl.bot.SafeWorkPDLBot.__init__', return_value=None):
            bot = SafeWorkPDLBot("u", "p")
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot.log = MagicMock()
            bot.download_path = "downloads"
            bot._stop_requested = False
            return bot

    def test_name_and_description(self, bot):
        assert bot.name == "scarico_pdl"
        assert "SafeWork" in bot.description

    @patch('src.bots.safework.pdl.bot.time.sleep') # Mock sleep to be instant
    @patch('src.bots.safework.pdl.bot.SafeWorkPDLBot._process_single_pdl')
    def test_run_loop(self, mock_process, mock_sleep, bot):
        data = [
            {"pdl_number": "123"},
            {"pdl_number": "456", "print_enabled": True}
        ]
        
        mock_process.return_value = True
        
        success = bot.run(data)
        
        assert success is True
        assert mock_process.call_count == 2
        
    @patch('src.bots.safework.pdl.bot.time.sleep')
    @patch('src.bots.safework.pdl.bot.SafeWorkPDLBot._gestisci_alert_ricerca')
    @patch('src.bots.safework.pdl.bot.SafeWorkPDLBot._attendi_scomparsa_overlay')
    @patch('src.bots.safework.pdl.bot.SafeWorkPDLBot._download_parte_prima')
    @patch('src.bots.safework.pdl.bot.SafeWorkPDLBot._vai_a_parte_seconda')
    @patch('src.bots.safework.pdl.bot.SafeWorkPDLBot._download_parte_seconda')
    @patch('src.bots.safework.pdl.bot.SafeWorkPDLBot._unisci_pdf')
    @patch('src.bots.safework.pdl.bot.print_pdf')
    def test_process_single_pdl_success(self, mock_print, mock_unisci, mock_dl2, mock_nav2, mock_dl1, mock_overlay, mock_alert, mock_sleep, bot):
        # Setup mocks
        bot.wait.until.return_value = MagicMock() # Search field
        mock_dl1.return_value = "p1.pdf"
        mock_dl2.return_value = "p2.pdf"
        mock_unisci.return_value = True
        
        # Run
        result = bot._process_single_pdl("123", True, "MyPrinter")
        
        assert result is True
        mock_dl1.assert_called_once()
        mock_nav2.assert_called_once()
        mock_dl2.assert_called_once()
        mock_unisci.assert_called_once()
        mock_print.assert_called_once()

    @patch('src.bots.safework.pdl.bot.fitz')
    def test_unisci_pdf(self, mock_fitz, bot):
        mock_doc = MagicMock()
        mock_fitz.open.return_value = mock_doc
        # context manager for open(file)
        mock_fitz.open.return_value.__enter__.return_value = mock_doc
        
        result = bot._unisci_pdf("a.pdf", "b.pdf", "out.pdf")
        
        assert result is True
        assert mock_doc.insert_pdf.call_count == 2
        mock_doc.save.assert_called_with("out.pdf")
