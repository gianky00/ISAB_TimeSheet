import json
from unittest.mock import patch

import pytest

from src.core.report_history import ReportHistory


class TestReportHistory:
    @pytest.fixture(autouse=True)
    def mock_history_file(self, tmp_path):  # noqa: ANN001
        history_file = tmp_path / "data" / "report_history.json"
        with patch.object(ReportHistory, "HISTORY_FILE", history_file):
            yield history_file

    def test_ensure_file_creates_directory(self, mock_history_file):  # noqa: ANN001
        ReportHistory._ensure_file()
        assert mock_history_file.exists()

    def test_save_report(self, mock_history_file):  # noqa: ANN001
        warning_list = [{"id": "1", "name": "Mario Rossi"}]
        expired_list = [
            {"id": "2", "name": "Luigi Verdi"},
            {"id": "3", "name": "Anna Bianchi"},
        ]

        ReportHistory.save_report(warning_list, expired_list)

        data = json.loads(mock_history_file.read_text())
        assert data["last_report"]["warning_count"] == 1
        assert data["last_report"]["expired_count"] == 2  # noqa: PLR2004
        assert "1" in data["last_report"]["warning_ids"]

    def test_get_last_report(self, mock_history_file):  # noqa: ANN001
        ReportHistory.save_report([{"id": "10"}], [])

        last = ReportHistory.get_last_report()
        assert last is not None
        assert last["warning_count"] == 1
        assert last["expired_count"] == 0

    def test_calculate_trend(self, mock_history_file):  # noqa: ANN001
        # Save initial report
        ReportHistory.save_report([{"id": "1"}], [{"id": "2"}])

        # Calculate trend with new values
        trend = ReportHistory.calculate_trend(current_warning=3, current_expired=2)

        assert trend is not None
        assert trend["warning_diff"] == 2  # 3 - 1  # noqa: PLR2004
        assert trend["expired_diff"] == 1  # 2 - 1

    def test_calculate_trend_no_previous(self, mock_history_file):  # noqa: ANN001
        trend = ReportHistory.calculate_trend(current_warning=5, current_expired=2)
        assert trend is None

    def test_get_history(self, mock_history_file):  # noqa: ANN001
        # Save multiple reports
        for i in range(5):
            ReportHistory.save_report([{"id": str(i)}], [])

        history = ReportHistory.get_history(limit=3)
        assert len(history) == 3  # noqa: PLR2004

    def test_history_max_entries(self, mock_history_file):  # noqa: ANN001
        # Save more than MAX_HISTORY_ENTRIES
        original_max = ReportHistory.MAX_HISTORY_ENTRIES
        ReportHistory.MAX_HISTORY_ENTRIES = 5

        try:
            for i in range(10):
                ReportHistory.save_report([{"id": str(i)}], [])

            data = json.loads(mock_history_file.read_text())
            # history should be capped at 5 (plus current last_report)
            assert len(data["history"]) <= 5  # noqa: PLR2004
        finally:
            ReportHistory.MAX_HISTORY_ENTRIES = original_max

    def test_load_data_handles_malformed_json(self, mock_history_file):  # noqa: ANN001
        mock_history_file.parent.mkdir(parents=True, exist_ok=True)
        mock_history_file.write_text("not valid json", encoding="utf-8")

        data = ReportHistory._load_data()
        assert data == {"last_report": None, "history": []}
