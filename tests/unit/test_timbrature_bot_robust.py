import unittest
from unittest.mock import MagicMock, patch

from src.bots.portale_fornitori.timbrature.bot import TimbratureBot


class TestTimbratureBotRobust(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()

        # Patch BaseBot logger
        self.logger_patcher = patch(
            "src.bots.base.base_bot.get_logger", return_value=self.mock_logger
        )
        self.logger_patcher.start()

        # Patch TimbratureStorage
        self.storage_patcher = patch(
            "src.bots.portale_fornitori.timbrature.bot.TimbratureStorage"
        )
        self.mock_storage_cls = self.storage_patcher.start()
        self.mock_storage = self.mock_storage_cls.return_value

    def tearDown(self):
        self.logger_patcher.stop()
        self.storage_patcher.stop()

    def test_initialization(self):
        """Test initialization of TimbratureBot."""
        bot = TimbratureBot(
            username="u", password="p", data_da="01.01.2024", fornitore="Test"
        )
        self.assertEqual(bot.data_da, "01.01.2024")
        self.assertEqual(bot.fornitore, "Test")
        self.assertEqual(bot.name, "Timbrature")

    def test_validate_data_success(self):
        """Test data validation with valid parameters."""
        bot = TimbratureBot(
            username="u", password="p", data_da="01.01.2024", fornitore="Test"
        )
        is_valid, msg = bot.validate_data([{"some": "data"}])
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

    def test_validate_data_missing_params(self):
        """Test validation fails when parameters are missing."""
        bot = TimbratureBot(username="u", password="p")

        # Missing fornitore
        is_valid, msg = bot.validate_data([{"some": "data"}])
        self.assertFalse(is_valid)
        self.assertIn("Fornitore non specificato", msg)

        # Set fornitore, missing date
        bot.fornitore = "Test"
        is_valid, msg = bot.validate_data([{"some": "data"}])
        self.assertFalse(is_valid)
        self.assertIn("Data Inizio non specificata", msg)

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    @patch(
        "src.bots.portale_fornitori.timbrature.bot.os.path.exists", return_value=True
    )
    @patch("src.bots.portale_fornitori.timbrature.bot.os.remove")
    def test_run_success(self, mock_remove, mock_exists, mock_page_cls):
        """Test a successful bot run."""
        bot = TimbratureBot(
            username="u", password="p", data_da="01.01.2024", fornitore="Test"
        )
        bot.driver = MagicMock()

        mock_page = mock_page_cls.return_value
        mock_page.navigate_to_timbrature.return_value = True
        mock_page.set_filters.return_value = True
        mock_page.download_excel.return_value = "/tmp/report.xlsx"

        data = {"data_da": "02.01.2024", "fornitore": "New Supplier"}

        success = bot.run(data)

        self.assertTrue(success)
        self.assertEqual(bot.fornitore, "New Supplier")
        self.assertEqual(bot.data_da, "02.01.2024")

        # Verify interactions
        mock_page.navigate_to_timbrature.assert_called_once()
        mock_page.set_filters.assert_called_with("New Supplier", "02.01.2024", "")
        self.mock_storage.import_excel.assert_called_with("/tmp/report.xlsx", bot.log)
        mock_remove.assert_called_with("/tmp/report.xlsx")

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    def test_run_navigation_failure(self, mock_page_cls):
        """Test run failure during navigation."""
        bot = TimbratureBot(
            username="u", password="p", fornitore="Test", data_da="01.01.2024"
        )
        bot.driver = MagicMock()

        mock_page = mock_page_cls.return_value
        mock_page.navigate_to_timbrature.return_value = False

        success = bot.run({})

        self.assertFalse(success)
        mock_page.set_filters.assert_not_called()

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    def test_run_filter_failure(self, mock_page_cls):
        """Test run failure during filter setting."""
        bot = TimbratureBot(
            username="u", password="p", fornitore="Test", data_da="01.01.2024"
        )
        bot.driver = MagicMock()

        mock_page = mock_page_cls.return_value
        mock_page.navigate_to_timbrature.return_value = True
        mock_page.set_filters.return_value = False

        success = bot.run({})

        self.assertFalse(success)
        mock_page.download_excel.assert_not_called()

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    def test_run_no_data_found(self, mock_page_cls):
        """Test run behavior when no file is downloaded."""
        bot = TimbratureBot(
            username="u", password="p", fornitore="Test", data_da="01.01.2024"
        )
        bot.driver = MagicMock()

        mock_page = mock_page_cls.return_value
        mock_page.navigate_to_timbrature.return_value = True
        mock_page.set_filters.return_value = True
        mock_page.download_excel.return_value = ""  # No file

        success = bot.run({})

        self.assertTrue(
            success
        )  # Completion is still considered successful even if no data
        self.mock_storage.import_excel.assert_not_called()
