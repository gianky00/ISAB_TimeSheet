"""
Unit tests for SafeWorkPDLSearchBot (Final Corrected).
"""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot


class TestSafeWorkPDLSearchBot:
    @pytest.fixture
    def bot(self):
        bot = SafeWorkPDLSearchBot("user", "pass")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        return bot

    def test_initialization(self, bot):
        assert bot.name == "ricerca_pdl"

    @patch("src.bots.safework.pdl.search_bot.pd.read_excel")
    @patch("src.bots.base.wait_helpers.poll_for_new_file")
    def test_run_success(self, mock_poll, mock_read, bot, mocker):
        """Simula ricerca massiva con export Excel e import DB."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_attendi_scomparsa_overlay")
        mocker.patch.object(bot, "click_robusto")

        # Mock Page Objects
        bot.ricerca_pdl_page = MagicMock()
        bot.ricerca_pdl_page.seleziona_sito_e_cerca.return_value = True
        bot.ricerca_pdl_page.esporta_excel.return_value = True

        # Mock Download Excel
        mock_poll.return_value = "results.xlsx"

        # Mock DataFrame con colonne richieste
        df = pd.DataFrame([{"N° PDL": "123", "STATO": "Attivo"}])
        mock_read.return_value = df

        # Mock database connection
        m_db = mocker.patch("src.core.database.db_manager.get_connection")

        data = [{"site_selection": "ISAB Sud"}]
        res = bot.run(data)

        assert res is True
        bot.ricerca_pdl_page.seleziona_sito_e_cerca.assert_called_with("ISAB Sud")
        assert m_db.called

    def test_validate_data(self, bot):
        valid, _msg = bot.validate_data([{"site_selection": "Sud"}])
        assert valid is True

        # Il bot base fallisce se data è vuoto
        valid, _msg = bot.validate_data([])
        assert valid is False
