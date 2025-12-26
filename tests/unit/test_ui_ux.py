"""
Bot TS - UX Tests
Test micro-UX improvements.
"""
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))

from PyQt6.QtWidgets import QLineEdit

class TestSearchUX:
    """Test UX improvements on search bars."""

    @pytest.fixture
    def mock_db(self):
        """Mock database connections to avoid runtime errors during init."""
        with patch('sqlite3.connect') as mock_sql, \
             patch('src.core.contabilita_manager.ContabilitaManager.get_available_years', return_value=[]), \
             patch('src.core.contabilita_manager.ContabilitaManager.get_data_by_year', return_value=[]), \
             patch('pathlib.Path.exists', return_value=True):
            yield mock_sql

    def test_timbrature_search_has_clear_button(self, qapp, qtbot, mock_db):
        """TimbratureDBPanel search bar should have clear button enabled."""
        from src.gui.panels import TimbratureDBPanel

        panel = TimbratureDBPanel()
        qtbot.addWidget(panel)

        assert isinstance(panel.search_input, QLineEdit)
        assert panel.search_input.isClearButtonEnabled() is True

    def test_contabilita_search_has_clear_button(self, qapp, qtbot, mock_db):
        """ContabilitaPanel search bar should have clear button enabled."""
        from src.gui.contabilita_panel import ContabilitaPanel

        panel = ContabilitaPanel()
        qtbot.addWidget(panel)

        assert isinstance(panel.search_input, QLineEdit)
        assert panel.search_input.isClearButtonEnabled() is True
