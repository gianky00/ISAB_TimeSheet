"""
Unit tests for SafeWorkProgrammazioneBot.
"""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.bots.safework.programmazione.bot import SafeWorkProgrammazioneBot


class TestSafeWorkProgrammazioneBot:
    @pytest.fixture
    def bot(self):
        bot = SafeWorkProgrammazioneBot("user", "pass", download_path="/tmp")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.attivita_page = MagicMock()
        return bot

    def test_initialization(self, bot):
        assert bot.name == "programmazione_pdl"
        assert bot.get_name() == "Programmazione PDL"

    @patch("src.bots.safework.programmazione.bot.poll_for_new_file")
    def test_run_success(self, mock_poll, bot):
        """Test full run with mocked excel download."""
        mock_poll.return_value = "report.xlsx"

        # Mock class base methods to avoid hangs
        bot._attendi_scomparsa_overlay = MagicMock()
        bot.click_robusto = MagicMock()

        # Mock parsing to avoid real file reading
        with patch.object(bot, "_parse_excel_results") as mock_parse:
            with patch.object(bot, "_cleanup_temp_file"):
                data = [{"requesters": ["Req1"], "date_start": "01/01/2024", "date_end": "07/01/2024"}]

                res = bot.run(data)

                assert res is True
                bot.attivita_page.imposta_date.assert_called_with("01/01/2024", "07/01/2024")
                bot.attivita_page.esegui_ricerca.assert_called()
                mock_parse.assert_called_with("report.xlsx")

    def test_run_missing_params(self, bot):
        """Test fail on missing params."""
        assert bot.run([]) is False
        assert bot.run([{"requesters": []}]) is False

    @patch("pandas.read_excel")
    def test_parse_excel_results(self, mock_read, bot):
        """Test logic for parsing excel rows."""
        # Create a mock DataFrame simulating SafeWork export structure
        # Indices:
        # 0=PDL, 1=Desc, 2=MonTCL, 3=MonTGO ...
        # 17=Richiedente, 23=Unità, 24=Area

        # Row with NO programming
        row_no_prog = ["PDL1", "Desc1"] + ["No"] * 14 + ["Req1"] + [""] * 5 + ["U1", "Area1"]
        # Row with Programming (Mon TCL=Si)
        row_prog = ["PDL2", "Desc2", "Si", "No"] + ["No"] * 12 + ["Req2"] + [""] * 5 + ["U2", "Area2"]

        # Adjust lengths to match typical export width (at least 25 cols)
        # 2+14 = 16 cols for flags. Total cols needed >= 25
        # Indices: 0,1 .. 2-15 flags .. 16 .. 17(Req) .. 23(Unit) .. 24(Area)

        def make_row(pdl, has_flag=False):
            r = [""] * 30
            r[0] = pdl
            r[1] = "Description"
            r[17] = "Requester"
            r[23] = "Unit"
            r[24] = "Area"

            # Fill flags No
            for i in range(2, 16):
                r[i] = "No"

            if has_flag:
                r[2] = "Si"  # Mon TCL
            return r

        df = pd.DataFrame([make_row("PDL_NO"), make_row("PDL_YES", True)])

        mock_read.return_value = df

        bot._parse_excel_results("dummy.xlsx")

        assert len(bot.results) == 1
        res = bot.results[0]
        assert res["pdl"] == "PDL_YES"
        assert res["programmazione"][0]["tcl"] is True  # Monday
        assert res["unita"] == "Unit"
        assert res["area"] == "Area"

    def test_cleanup_safe(self, bot, mocker):
        """Test cleanup doesn't raise."""
        mocker.patch("src.bots.safework.programmazione.bot.Path.unlink", side_effect=Exception)
        bot._cleanup_temp_file("file")  # Should accept exception
