import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from src.core.report_history import ReportHistory


class TestReportHistory:
    @pytest.fixture(autouse=True)
    def setup_history(self, fs):
        # Mocking DB_DIR via local variable patch in ReportHistory
        # DB_DIR è importato da src.core.paths
        # Usiamo pyfakefs per gestire il file
        fs.create_dir("/data")
        self.test_file = Path("/data/report_history.json")
        ReportHistory.HISTORY_FILE = self.test_file

    def test_ensure_file(self):
        ReportHistory._ensure_file()
        assert self.test_file.exists()
        data = json.loads(self.test_file.read_text())
        assert data["last_report"] is None

    def test_save_report(self):
        warnings = [{"id": "1"}, {"id": "2"}]
        expired = [{"id": "3"}]

        ReportHistory.save_report(warnings, expired)

        data = json.loads(self.test_file.read_text())
        last = data["last_report"]
        assert last["warning_count"] == 2
        assert last["expired_count"] == 1
        assert "1" in last["warning_ids"]
        assert "3" in last["expired_ids"]

    def test_history_rotation(self):
        # Primo report
        ReportHistory.save_report([{"id": "W1"}], [])
        # Secondo report
        ReportHistory.save_report([{"id": "W2"}], [])

        data = json.loads(self.test_file.read_text())
        assert data["last_report"]["warning_ids"] == ["W2"]
        assert data["history"][0]["warning_ids"] == ["W1"]

    def test_calculate_trend(self):
        # Setup last report: 5 warning, 2 expired
        old_date = datetime(2023, 1, 1, tzinfo=UTC).isoformat()
        initial_data = {
            "last_report": {"date": old_date, "warning_count": 5, "expired_count": 2},
            "history": [],
        }
        self.test_file.write_text(json.dumps(initial_data))

        # Current: 7 warning (+2), 1 expired (-1)
        trend = ReportHistory.calculate_trend(7, 1)

        assert trend["warning_diff"] == 2
        assert trend["expired_diff"] == -1
        assert trend["last_date"] == "01/01/2023"

    def test_get_history(self):
        # Crea 5 report fittizi
        for i in range(5):
            ReportHistory.save_report([{"id": f"W{i}"}], [])

        history = ReportHistory.get_history(limit=3)
        assert len(history) == 3
        # L'ultimo inserito è W4
        assert history[0]["warning_ids"] == ["W4"]

    def test_load_corrupted_json(self, fs):
        self.test_file.write_text("invalid")
        # Deve resettare senza crash
        data = ReportHistory._load_data()
        assert data["last_report"] is None
