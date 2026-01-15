from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot


class TestScaricaTSBotDeep:
    @pytest.fixture
    def bot(self):
        return ScaricaTSBot(username="user", password="pw", fornitore="Fornitore Test")

    def test_validate_data(self, bot):
        # Valid data
        valid, msg = bot.validate_data([{"numero_oda": "123"}])
        assert valid is True

        # Missing fornitore
        bot.fornitore = ""
        valid, msg = bot.validate_data([{"numero_oda": "123"}])
        assert valid is False
        assert "Fornitore" in msg

    def test_run_lifecycle(self, bot):
        # Mock the browser and navigation
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.long_wait = MagicMock()

        data = {"rows": [{"numero_oda": "12345", "posizione_oda": "10"}], "fornitore": "F1"}

        with patch.object(bot, "_navigate_to_timesheet", return_value=True), \
             patch.object(bot, "_setup_filters", return_value=True), \
             patch.object(bot, "_download_excel", return_value=Path("test.xlsx")), \
             patch.object(bot, "_check_stop"):

            # Mock internal waits to avoid import issues
            bot.wait.until = MagicMock()

            success = bot.run(data)
            assert success is True
            assert bot.fornitore == "F1"

    def test_download_excel_logic(self, bot):
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        source_dir = Path("./fake_source")
        dest_dir = Path("./fake_dest")

        # Mocking time.time to control the loop
        with patch("pathlib.Path.iterdir") as mock_iter, \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.unlink"), \
             patch("pathlib.Path.mkdir"), \
             patch("shutil.move") as mock_move:

            # Setup mock file
            new_file = MagicMock(spec=Path)
            new_file.suffix = ".xlsx"
            new_file.name = "download.xlsx"
            new_file.exists.return_value = True
            new_file.__str__.return_value = str(source_dir / "download.xlsx")

            # Important: mock stat().st_mtime correctly on the object
            new_file.stat.return_value.st_mtime = 1000

            # Simulate: Before download (empty), During (crdownload), After (xlsx)
            # We need enough items to satisfy all calls
            mock_iter.side_effect = [
                set(), # files_before
                set(), # _wait_for_new_file -> any (.crdownload)
                {new_file}, # _wait_for_new_file -> current_files (.xlsx)
                set(), # extra fallback
                set()
            ]

            with patch("time.time", side_effect=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
                # Mock button click
                bot.wait.until.return_value = MagicMock()

                path = bot._download_excel(source_dir, dest_dir, "12345", "10")
                assert path is not None
                assert "TS_12345-10" in path.name
                mock_move.assert_called()
