from unittest.mock import MagicMock

import pytest

from src.application.services.logging.analytics import PatternDetector


class TestPatternDetector:
    @pytest.fixture
    def mock_viewer(self):
        return MagicMock()

    def test_find_repeated_errors_none(self, mock_viewer):
        detector = PatternDetector(viewer=mock_viewer)
        mock_viewer.get_error_summary.return_value = []

        patterns = detector.find_repeated_errors()
        assert len(patterns) == 0

    def test_find_repeated_errors_found(self, mock_viewer):
        detector = PatternDetector(viewer=mock_viewer)
        mock_viewer.get_error_summary.return_value = [
            {"message": "Timeout", "count": 10},
            {"message": "Low count", "count": 1},
        ]

        patterns = detector.find_repeated_errors(min_count=3)
        assert len(patterns) == 1
        assert patterns[0].message == "Timeout"
        assert patterns[0].count == 10
        assert patterns[0].type == "repeated_error"

    def test_detect_all_integration(self, mock_viewer):
        detector = PatternDetector(viewer=mock_viewer)
        mock_viewer.get_error_summary.return_value = [{"message": "Error A", "count": 5}]

        patterns = detector.detect_all()
        assert len(patterns) == 1
        assert patterns[0].message == "Error A"
