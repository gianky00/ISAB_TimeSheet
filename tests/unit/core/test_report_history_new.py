import json
from unittest.mock import patch

import pytest

from src.core.report_history import ReportHistory


class TestReportHistory:
    @pytest.fixture(autouse=True)
    def setup_mock_history(self, fs):
        from src.core.paths import DB_DIR

        fs.create_dir(str(DB_DIR))
        self.history_file = ReportHistory.HISTORY_FILE
        # Resetta lo stato interno (il file è la fonte di verità)
        if self.history_file.exists():
            self.history_file.unlink()

    def test_ensure_file(self, fs):
        ReportHistory._ensure_file()
        assert self.history_file.exists()
        data = json.loads(self.history_file.read_text(encoding="utf-8"))
        assert data["last_report"] is None
        assert data["history"] == []

    def test_save_report_and_rotate(self, fs):
        # Primo report
        w1 = [{"id": "1", "cognome": "R1"}]
        e1 = [{"badge": "B1"}]
        ReportHistory.save_report(w1, e1)

        last = ReportHistory.get_last_report()
        assert last["warning_count"] == 1
        assert last["expired_count"] == 1
        assert "1" in last["warning_ids"]
        assert "B1" in last["expired_ids"]

        # Secondo report (deve ruotare il primo in history)
        w2 = []
        e2 = []
        ReportHistory.save_report(w2, e2)

        data = ReportHistory._load_data()
        assert data["last_report"]["warning_count"] == 0
        assert len(data["history"]) == 1
        assert data["history"][0]["warning_count"] == 1

    def test_calculate_trend(self, fs):
        # Setup preesistente
        w_list = [{"id": "1"}, {"id": "2"}]
        e_list = [{"badge": "B1"}]
        ReportHistory.save_report(w_list, e_list)

        # Trend rispetto a 3 warning e 0 expired
        trend = ReportHistory.calculate_trend(3, 0)
        assert trend["warning_diff"] == 1  # 3 - 2
        assert trend["expired_diff"] == -1  # 0 - 1
        assert trend["last_date"] is not None

    def test_calculate_trend_none(self, fs):
        assert ReportHistory.calculate_trend(0, 0) is None

    def test_get_history_limit(self, fs):
        # Salva 5 report
        for _i in range(5):
            ReportHistory.save_report([], [])

        history = ReportHistory.get_history(limit=3)
        assert len(history) == 3

    def test_load_error_handling(self, fs):
        fs.create_file(str(self.history_file), contents="corrupt")
        with patch("src.core.report_history.logger") as mock_logger:
            data = ReportHistory._load_data()
            assert data["history"] == []
            assert mock_logger.exception.called
