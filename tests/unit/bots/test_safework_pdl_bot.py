from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.selenium_bot_config import SeleniumBotConfig
from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLBot:
    @pytest.fixture
    def bot_config(self):
        return SeleniumBotConfig(username="user", password="pass", headless=True)

    @pytest.fixture
    def bot(self, bot_config):
        return SafeWorkPDLBot(username="user", password="pass", config=bot_config, account_type="Esecutore")

    def test_sanitizza_pdl_number(self, bot):
        assert bot._sanitizza_pdl_number("123456") == "123456/S"
        assert bot._sanitizza_pdl_number("500000") == "500000/C"

    def test_validate_data(self, bot):
        data = {"rows": [{"numero_pdl": "123456"}]}
        valid, _msg = bot.validate_data(data)
        assert valid is True

    @patch("src.bots.safework.pdl.bot.SafeWorkPDLBot._process_pdl_pipeline")
    @patch("src.bots.safework.pdl.bot.SafeWorkPDLBot._handle_session_merge")
    def test_run_success(self, mock_merge, mock_pipeline, bot):
        mock_pipeline.return_value = True
        data = {"rows": [{"numero_pdl": "123456"}]}
        res = bot.run(data)
        assert res is True

    def test_esegui_ricerca_pdl_success(self, bot):
        mock_driver = MagicMock()
        bot.driver = mock_driver
        bot.wait = MagicMock()
        with patch.object(bot, "_attendi_scomparsa_overlay"):
            with patch.object(bot, "_gestisci_ricerca_estesa", return_value=False):
                with patch.object(bot, "_gestisci_alert_ricerca", return_value=False):
                    res = bot._esegui_ricerca_pdl("123456/S")
                    assert res is True

    @patch("src.bots.safework.pdl.bot.poll_for_new_file")
    @patch("src.bots.safework.pdl.bot.fitz.open")
    def test_scarica_parte_prima_success(self, mock_fitz, mock_poll, bot, fs):
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.download_path = "/downloads"
        fs.create_dir("/downloads")
        fake_downloaded = "/downloads/downloaded.pdf"
        fs.create_file(fake_downloaded, contents=b"pdf")
        mock_poll.return_value = fake_downloaded
        mock_doc = MagicMock()
        mock_doc.page_count = 1
        mock_fitz.return_value = mock_doc
        with patch.object(bot, "_attendi_scomparsa_overlay"):
            with patch.object(bot, "click_robusto"):
                res = bot._scarica_parte_prima("123456/S")
                assert res is not None

    def test_espandi_parte_seconda(self, bot):
        bot.driver = MagicMock()
        bot.wait = MagicMock()

        # Caso 1: Già visibile
        mock_el = MagicMock()
        mock_el.is_displayed.return_value = True
        # find_elements deve tornare una lista con l'elemento
        bot.driver.find_elements.return_value = [mock_el]
        assert bot._espandi_parte_seconda() is True

        # Caso 2: Da cliccare
        mock_el.is_displayed.return_value = False
        # Mock find_element per il click
        mock_btn = MagicMock()
        bot.driver.find_element.return_value = mock_btn
        assert bot._espandi_parte_seconda() is True
        assert mock_btn.click.called

    @patch("src.utils.document_processor.DocumentProcessor.merge_pdfs")
    @patch("src.bots.safework.pdl.bot.print_pdf")
    def test_unisci_e_stampa(self, mock_print, mock_merge, bot):
        mock_merge.return_value = True
        bot.download_path = "/downloads"
        item = {"print_enabled": True, "printer_name": "PRN1"}
        all_paths = []
        res = bot._unisci_e_stampa("123456/S", "p1.pdf", "p2.pdf", item, all_paths)
        assert res is True
