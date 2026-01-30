from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot


class TestDettagliOdaBotDeep:
    @pytest.fixture
    def bot(self):
        return DettagliOdABot(username="u", password="p", fornitore="F1")

    def test_bot_initialization(self, bot):
        assert bot.name == "Dettagli OdA"
        assert bot.fornitore == "F1"

    def test_validate_data(self, bot):
        # Valid data list format
        data = [{"numero_oda": "123", "contratto": "C1"}]
        assert bot.validate_data(data)[0] is True

        # Missing data - Now should be True as it allows general list search
        assert bot.validate_data([])[0] is True

    def test_run_success_simulation(self, bot):
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.long_wait = MagicMock()

        # Mock page objects
        with patch(
            "src.bots.portale_fornitori.dettagli_oda.bot.DettagliOdAPage"
        ) as mock_page_cls:
            mock_page = mock_page_cls.return_value
            mock_page.navigate_to_dettagli.return_value = True
            mock_page.setup_supplier.return_value = True
            from pathlib import Path

            mock_page.process_oda.return_value = Path("dummy_oda.xlsx")

            data = {
                "rows": [],  # Empty rows
                "fornitore": "F1",
                "date_da": "01.01.2024",
                "date_a": "31.12.2024",
            }

            res = bot.run(data)
            assert res is True
            # Should be called once with empty ODA
            mock_page.process_oda.assert_called_once()
            args = mock_page.process_oda.call_args[0]
            assert args[0] == ""
