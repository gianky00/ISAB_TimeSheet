import pytest
from unittest.mock import MagicMock, patch
from src.bots.safework.pdl.bot import SafeWorkPDLBot
from pathlib import Path

class TestSafeWorkPDLBotDeep:
    @pytest.fixture
    def bot(self):
        # Username and password are required
        return SafeWorkPDLBot(username="u", password="p")

    def test_validate_data(self, bot):
        # Valid data list of dicts
        data = [{"pdl_number": "123456/C"}]
        assert bot.validate_data(data)[0] is True
        
        # Missing data
        assert bot.validate_data([])[0] is False

    @patch("src.bots.safework.pdl.bot.WebDriverWait")
    def test_run_lifecycle(self, mock_wait, bot):
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        
        data = [{"pdl_number": "123456/C", "print_enabled": False}]
        
        with patch.object(bot, "_login", return_value=True), \
             patch.object(bot, "_attendi_caricamento_sistema"), \
             patch.object(bot, "_gestisci_alert_ricerca", return_value=False), \
             patch.object(bot, "_attendi_scomparsa_overlay"), \
             patch.object(bot, "_attendi_e_ritorna_nuovo_pdf", side_effect=[Path("p1.pdf"), Path("p2.pdf")]), \
             patch("src.utils.document_processor.DocumentProcessor.merge_pdfs", return_value=True), \
             patch("os.rename"), \
             patch("os.path.exists", return_value=True), \
             patch("fitz.open") as mock_fitz:
            
            # Mock fitz doc
            mock_doc = MagicMock()
            mock_doc.page_count = 1
            mock_fitz.return_value = mock_doc
            
            # We mock find_element for search field
            bot.driver.find_element.return_value = MagicMock()
            
            res = bot.run(data)
            assert res is True