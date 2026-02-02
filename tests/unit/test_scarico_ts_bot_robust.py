import unittest
from unittest.mock import MagicMock, patch, PropertyMock, call
from pathlib import Path
from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot

class TestScaricaTSBotRobust(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        
        # Patch BaseBot logger
        self.logger_patcher = patch('src.bots.base.base_bot.get_logger', return_value=self.mock_logger)
        self.logger_patcher.start()

        # Patch TimesheetProcessor
        self.processor_patcher = patch('src.bots.portale_fornitori.scarico_ts.bot.TimesheetProcessor')
        self.mock_processor = self.processor_patcher.start()

    def tearDown(self):
        self.logger_patcher.stop()
        self.processor_patcher.stop()

    def test_initialization_defaults(self):
        """Test initialization with default values."""
        bot = ScaricaTSBot(username="u", password="p")
        self.assertEqual(bot.data_da, "01.01.2025")
        self.assertEqual(bot.fornitore, "")
        self.assertFalse(bot.elabora_ts)
        self.assertEqual(bot.name, "Scarico TS")

    def test_validate_data_success(self):
        """Test data validation with valid input."""
        bot = ScaricaTSBot(username="u", password="p", fornitore="Test Provider")
        valid_data = [{"numero_oda": "123", "posizione_oda": "001"}]
        
        is_valid, msg = bot.validate_data(valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

    def test_validate_data_missing_provider(self):
        """Test validation fails if provider is missing in both bot config and data."""
        bot = ScaricaTSBot(username="u", password="p", fornitore="")
        invalid_data = [{"numero_oda": "123"}]
        
        is_valid, msg = bot.validate_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("Fornitore non specificato", msg)

    def test_validate_data_provider_in_data(self):
        """Test validation succeeds if provider is in the data dict."""
        bot = ScaricaTSBot(username="u", password="p", fornitore="")
        valid_data = {
            "fornitore": "Dynamic Provider",
            "rows": [{"numero_oda": "123"}]
        }
        
        is_valid, msg = bot.validate_data(valid_data)
        self.assertTrue(is_valid)

    @patch('src.bots.portale_fornitori.scarico_ts.bot.Path')
    def test_prepare_run_environment(self, mock_path):
        """Test extraction of data and directory setup."""
        bot = ScaricaTSBot(username="u", password="p", download_path="/tmp/downloads")
        data = {
            "rows": [{"numero_oda": "123"}],
            "fornitore": "TestProv",
            "data_da": "01.01.2024",
            "elabora_ts": True
        }

        # Setup mock path resolution
        mock_resolved_path = MagicMock()
        mock_path.return_value.resolve.return_value = mock_resolved_path
        
        rows, dest_dir = bot._prepare_run_environment(data)
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(bot.fornitore, "TestProv")
        self.assertEqual(bot.data_da, "01.01.2024")
        self.assertTrue(bot.elabora_ts)
        self.assertEqual(dest_dir, mock_resolved_path)

    @patch('src.bots.portale_fornitori.scarico_ts.bot.ActionChains')
    def test_setup_filters_success(self, mock_action_chains):
        """Test successful setting of provider and date filters."""
        bot = ScaricaTSBot(username="u", password="p", fornitore="Test Provider", data_da="01.01.2024")
        
        # Setup mocks
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.long_wait = MagicMock()
        
        # Mock elements
        mock_arrow = MagicMock()
        mock_option = MagicMock()
        mock_date_input = MagicMock()
        
        bot.wait.until.side_effect = [mock_arrow, mock_date_input]
        bot.long_wait.until.return_value = mock_option
        
        success = bot._setup_filters()
        
        self.assertTrue(success)
        # Verify provider selection interactions
        mock_action_chains.assert_called_with(bot.driver)
        bot.driver.execute_script.assert_any_call("arguments[0].click();", mock_option)
        # Verify date input
        mock_date_input.clear.assert_called()
        mock_date_input.send_keys.assert_called_with("01.01.2024")

    def test_search_oda_success(self):
        """Test searching for an OdA."""
        bot = ScaricaTSBot(username="u", password="p")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        
        # Mock elements
        mock_num_field = MagicMock()
        mock_pos_field = MagicMock()
        mock_search_btn = MagicMock()
        
        # Sequence of presence_of_element/element_to_be_clickable calls
        bot.wait.until.side_effect = [
            mock_num_field, # NumeroOda
            mock_pos_field, # PosizioneOda
            mock_search_btn # Cerca button
        ]
        
        # Mock overlay disappearance
        bot._attendi_scomparsa_overlay = MagicMock()

        success = bot._search_oda("123", "001")
        
        self.assertTrue(success)
        # Verify scripts executed to set values (React/ExtJS workaround)
        self.assertEqual(bot.driver.execute_script.call_count, 4) # 2 sets + 2 dispatches
        bot._attendi_scomparsa_overlay.assert_called_with(90)

    @patch('src.bots.portale_fornitori.scarico_ts.bot.Path')
    @patch('src.bots.portale_fornitori.scarico_ts.bot.time')
    @patch('src.bots.portale_fornitori.scarico_ts.bot.shutil')
    @patch('src.bots.portale_fornitori.scarico_ts.bot.sanitize_filename', side_effect=lambda x: x)
    def test_download_excel_success(self, mock_sanitize, mock_shutil, mock_time, mock_path_cls):
        """Test successful file download sequence."""
        bot = ScaricaTSBot(username="u", password="p")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        
        # Mock time.time() to return floats for timeout comparison
        mock_time.time.side_effect = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]
        
        # Configure Path mock
        source_dir = MagicMock(spec=Path)
        mock_path_cls.return_value = source_dir
        
        dest_dir = MagicMock(spec=Path)
        
        # Setup source dir existence
        source_dir.resolve.return_value = source_dir
        source_dir.exists.return_value = True

        # 1. Files before: empty
        # 2. Files after: one new .xlsx
        file_before = MagicMock(spec=Path)
        file_before.suffix = ".txt"

        new_file = MagicMock(spec=Path)
        new_file.suffix = ".xlsx"
        new_file.name = "new_report.xlsx"
        new_file.is_file.return_value = True
        new_file.stat.return_value.st_mtime = 100

        # Mock iterdir sequence
        # Call 1: files_before -> []
        # Call 2: check crdownload -> [new_file]
        # Call 3: current_files -> [new_file]
        source_dir.iterdir.side_effect = [
            [],
            [new_file],
            [new_file],
            [new_file],
            [new_file]
        ]

        # Mock click export
        bot._click_excel_export_button = MagicMock(return_value=True)

        # Mock destination path logic
        expected_dest = dest_dir / "TS_123-001.xlsx"
        expected_dest.exists.return_value = False
        dest_dir.resolve.return_value = dest_dir

        # Run
        # We pass strings, Path(string) will return source_dir mock
        result = bot._download_excel("/source", dest_dir, "123", "001")
        
        self.assertIsNotNone(result)
        mock_shutil.move.assert_called()
        self.assertEqual(result, expected_dest)

    @patch('src.bots.portale_fornitori.scarico_ts.bot.time')
    def test_download_excel_timeout(self, mock_time):
        """Test download failure when file doesn't appear."""
        bot = ScaricaTSBot(username="u", password="p")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        
        source_dir = MagicMock(spec=Path)
        dest_dir = MagicMock(spec=Path)
        source_dir.resolve.return_value = source_dir
        source_dir.exists.return_value = True
        
        # iterdir always empty
        source_dir.iterdir.return_value = []
        
        bot._click_excel_export_button = MagicMock(return_value=True)
        
        # Force timeout loop to break
        mock_time.time.side_effect = [0, 10, 20, 30] # Start, loop 1, loop 2, timeout

        result = bot._download_excel(source_dir, dest_dir, "123", "001")
        
        self.assertIsNone(result)

    def test_run_orchestration(self):
        """Test the main run loop orchestration."""
        bot = ScaricaTSBot(username="u", password="p")
        
        # Mocks for internal methods
        bot._navigate_to_timesheet = MagicMock(return_value=True)
        bot._setup_filters = MagicMock(return_value=True)
        bot._search_oda = MagicMock(return_value=True)
        
        # Mock download returning a path
        mock_path = MagicMock(spec=Path)
        bot._download_excel = MagicMock(return_value=mock_path)
        
        # Data
        data = {
            "rows": [
                {"numero_oda": "A", "posizione_oda": "1"},
                {"numero_oda": "B", "posizione_oda": "2"}
            ],
            "fornitore": "Test"
        }
        
        success = bot.run(data)
        
        self.assertTrue(success)
        self.assertEqual(bot._search_oda.call_count, 2)
        self.assertEqual(bot._download_excel.call_count, 2)

    def test_run_orchestration_partial_fail(self):
        """Test run loop when one item fails."""
        bot = ScaricaTSBot(username="u", password="p")
        
        bot._navigate_to_timesheet = MagicMock(return_value=True)
        bot._setup_filters = MagicMock(return_value=True)
        
        # First ODA succeeds, second fails (search returns False or raises)
        bot._search_oda = MagicMock(side_effect=[True, Exception("Search failed")])
        bot._download_excel = MagicMock(return_value=MagicMock(spec=Path))
        
        data = {
            "rows": [
                {"numero_oda": "A"},
                {"numero_oda": "B"}
            ],
            "fornitore": "Test"
        }
        
        success = bot.run(data)
        
        self.assertFalse(success) # Should be False because not all rows succeeded
        self.assertEqual(bot._search_oda.call_count, 2) # Tried both