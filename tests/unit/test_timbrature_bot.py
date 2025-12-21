"""
Unit tests for TimbratureBot logic (Mocked).
"""
import pytest
from unittest.mock import MagicMock, patch, ANY, PropertyMock
from pathlib import Path
import pandas as pd

from src.bots.timbrature.bot import TimbratureBot
from src.bots.timbrature.storage import TimbratureStorage
from src.bots.timbrature.pages.timbrature_page import TimbraturePage

@pytest.fixture
def mock_driver():
    return MagicMock()

@pytest.fixture
def timbrature_bot(mock_driver):
    # Patch BaseBot init to avoid real browser launch
    with patch('src.bots.base.BaseBot.__init__') as mock_base_init:
        bot = TimbratureBot(username="test", password="pwd")
        bot.driver = mock_driver
        bot.log = MagicMock()
        return bot

class TestTimbraturePage:
    """Test Page Object logic."""

    def test_navigate_to_timbrature_success(self, mock_driver):
        """Should navigate successfully."""
        page = TimbraturePage(mock_driver)
        # Mock wait
        page.wait = MagicMock()
        page._wait_for_overlay = MagicMock()
        page.wait.until.return_value = MagicMock() # element

        # Act
        result = page.navigate_to_timbrature()

        # Assert
        assert result is True
        page.wait.until.assert_called()

    def test_set_filters_success(self, mock_driver):
        """Should set filters correctly."""
        page = TimbraturePage(mock_driver)
        page._select_supplier = MagicMock()
        page._wait_for_overlay = MagicMock()

        # Act
        result = page.set_filters("FornitoreX", "01.01.2023", "31.01.2023")

        # Assert
        assert result is True
        page._select_supplier.assert_called_with("FornitoreX")

class TestTimbratureStorage:
    """Test Database logic."""

    @patch('sqlite3.connect')
    @patch('pandas.read_excel')
    def test_import_excel_success(self, mock_read_excel, mock_connect):
        """Should import valid Excel data."""
        # Setup Mock DataFrame
        mock_df = MagicMock()
        # Mocking columns property to return a MagicMock that has a .str accessor
        mock_cols = MagicMock()
        mock_cols.str.strip.return_value = pd.Index(["Data Timbratura", "Ora Ingresso"])
        # We need __iter__ to work for the 'not in df.columns' check
        mock_cols.__iter__.return_value = ["Data Timbratura", "Ora Ingresso"]
        type(mock_df).columns = PropertyMock(return_value=mock_cols)

        # However, it's easier to just use a real DataFrame for data logic
        real_df = pd.DataFrame([
            {'Data Timbratura': '2023-01-01', 'Ora Ingresso': '08:00'}
        ])
        mock_read_excel.return_value = real_df

        # Mock iterrows (removed as we use real_df now)

        # Setup DB Mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        storage = TimbratureStorage(Path(":memory:"))
        # Override columns map for test simplicity
        storage.COLUMNS_MAP = {"Data Timbratura": "data", "Ora Ingresso": "ingresso"}

        # Act
        result = storage.import_excel("dummy.xlsx")

        # Assert
        assert result is True
        mock_cursor.execute.assert_called()
        assert mock_cursor.execute.call_count >= 1 # Create table + Insert

class TestTimbratureBot:
    """Test Main Bot Orchestration."""

    @patch('src.bots.timbrature.bot.TimbraturePage')
    @patch('src.bots.timbrature.bot.TimbratureStorage')
    def test_run_success(self, MockStorage, MockPage, timbrature_bot):
        """Should run full workflow successfully."""
        # Setup Mocks
        page_instance = MockPage.return_value
        page_instance.navigate_to_timbrature.return_value = True
        page_instance.set_filters.return_value = True
        page_instance.download_excel.return_value = "temp_file.xlsx"

        storage_instance = MockStorage.return_value
        timbrature_bot.storage = storage_instance

        # Act
        data = {'data_da': '01.01.2023'}
        with patch('os.path.exists', return_value=True), \
             patch('os.remove') as mock_remove:

            result = timbrature_bot.run(data)

        # Assert
        assert result is True
        page_instance.navigate_to_timbrature.assert_called_once()
        page_instance.set_filters.assert_called_once()
        page_instance.download_excel.assert_called_once()
        storage_instance.import_excel.assert_called_with("temp_file.xlsx", ANY)
        mock_remove.assert_called_with("temp_file.xlsx")
