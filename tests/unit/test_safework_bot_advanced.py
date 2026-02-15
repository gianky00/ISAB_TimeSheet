"""
Advanced tests for SafeWorkPDLBot.
Covers search management, session merging and more robust scenarios.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLBotAdvanced:
    @pytest.fixture
    def bot(self, mocker):
        bot = SafeWorkPDLBot("user", "pass", download_path="/tmp")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        mocker.patch("src.bots.safework.pdl.bot.Path.rename")
        mocker.patch("src.bots.safework.pdl.bot.Path.unlink")
        mocker.patch("src.bots.safework.pdl.bot.Path.exists", return_value=True)
        return bot

    def test_gestisci_ricerca_estesa_true(self, bot):
        """Testa quando il PdL non esiste e viene chiesta la ricerca estesa."""
        # 1. Trova il messaggio di "estendere ricerca"
        # 2. Clicca SI
        # 3. Verifica numPermessiTrovati == "0"

        mock_msg = MagicMock()
        mock_msg.is_displayed.return_value = True

        mock_si = MagicMock()

        mock_num = MagicMock()
        mock_num.text = "0"

        def find_side_effect(by, value):
            if "1C51D77B" in value:
                return mock_msg  # Messaggio alert
            if "E421C594" in value:
                return mock_si  # Bottone SI
            if value == "numPermessiTrovati":
                return mock_num
            return MagicMock()

        bot.driver.find_element.side_effect = find_side_effect

        # Patch WebDriverWait per passare subito
        with patch("src.bots.safework.pdl.bot.WebDriverWait") as mock_wait:
            res = bot._gestisci_ricerca_estesa()
            assert res is True  # Indica PdL inesistente
            mock_si.click.assert_called()

    def test_handle_session_merge_multiple_files(self, bot, mocker):
        """Verifica che il merge di sessione venga eseguito correttamente."""
        mock_merge = mocker.patch(
            "src.utils.document_processor.DocumentProcessor.merge_pdfs", return_value=True
        )

        data = [{"merge_all_session": True}]
        paths = ["p1.pdf", "p2.pdf", "p3.pdf"]

        bot._handle_session_merge(data, paths)

        assert mock_merge.called
        assert len(bot.downloaded_files) == 1
        assert "PDL_SESSIONE" in bot.downloaded_files[0]

    def test_handle_session_merge_disabled(self, bot, mocker):
        """Verifica che il merge non avvenga se non richiesto."""
        mock_merge = mocker.patch("src.utils.document_processor.DocumentProcessor.merge_pdfs")

        data = [{"merge_all_session": False}]
        paths = ["p1.pdf"]

        bot._handle_session_merge(data, paths)
        assert not mock_merge.called

    def test_esegui_ricerca_pdl_with_alert(self, bot, mocker):
        """Testa la ricerca PDL quando appare un alert resiliente."""
        mocker.patch.object(bot, "_gestisci_ricerca_estesa", return_value=False)
        mocker.patch.object(bot, "_gestisci_alert_ricerca", return_value=True)  # Alert presente
        mocker.patch.object(bot, "_attendi_scomparsa_overlay")

        # Simula caricamento finale riuscito
        bot.wait.until.return_value = MagicMock()

        res = bot._esegui_ricerca_pdl("123456/S")

        assert res is True
        bot._gestisci_alert_ricerca.assert_called_once()
