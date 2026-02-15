"""
Tests for SafeWorkPDLBot PDF cleaning logic.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLBotCleaning:
    @pytest.fixture
    def bot(self):
        return SafeWorkPDLBot("user", "pass")

    @patch("src.bots.safework.pdl.bot.fitz.open")
    def test_clean_pdf_removes_page_2(self, mock_fitz_open, bot):
        """Verifica che _clean_pdf rimuova la pagina 2 se presente."""
        mock_doc = MagicMock()
        mock_doc.page_count = 3
        mock_fitz_open.return_value = mock_doc

        bot._clean_pdf("test.pdf")

        # Deve aver chiamato delete_page(1) [zero-indexed, quindi pagina 2]
        mock_doc.delete_page.assert_called_once_with(1)
        mock_doc.save.assert_called_once()
        mock_doc.close.assert_called_once()

    @patch("src.bots.safework.pdl.bot.fitz.open")
    def test_clean_pdf_ignores_single_page(self, mock_fitz_open, bot):
        """Verifica che _clean_pdf non faccia nulla se il PDF ha una sola pagina."""
        mock_doc = MagicMock()
        mock_doc.page_count = 1
        mock_fitz_open.return_value = mock_doc

        bot._clean_pdf("single.pdf")

        mock_doc.delete_page.assert_not_called()
        mock_doc.save.assert_not_called()
        mock_doc.close.assert_called_once()

    @patch("src.bots.safework.pdl.bot.fitz.open")
    def test_clean_pdf_handles_exception(self, mock_fitz_open, bot):
        """Verifica che _clean_pdf non esploda in caso di errore fitz."""
        mock_fitz_open.side_effect = Exception("Fitz Error")

        # Non deve sollevare eccezione
        bot._clean_pdf("corrupt.pdf")

        # logger.debug dovrebbe essere stato chiamato (difficile da verificare senza patchare logger)
