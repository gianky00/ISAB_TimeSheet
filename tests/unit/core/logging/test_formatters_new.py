import json
from unittest.mock import patch

from src.application.services.logging.formatters import HumanFormatter, JSONFormatter


class TestFormatters:
    def test_json_formatter_basic(self):
        formatter = JSONFormatter(mask_sensitive=True)
        res = formatter.format("INFO", "test_logger", "Test message")
        data = json.loads(res)
        assert data["level"] == "INFO"
        assert data["message"] == "Test message"

    def test_json_formatter_masking(self):
        formatter = JSONFormatter(mask_sensitive=True)
        extra = {"password": "secret_pwd", "user": "mario"}
        res = formatter.format("INFO", "L", "M", extra=extra)
        data = json.loads(res)
        assert data["data"]["password"] == "***MASKED***"
        assert data["security"]["pii_masked"] is True

    def test_json_formatter_exception(self):
        formatter = JSONFormatter()

        def trigger_error():
            raise ValueError("Crash")

        try:
            trigger_error()
        except Exception as e:
            res = formatter.format("ERROR", "L", "M", exception=e)
        data = json.loads(res)
        assert data["exception"]["type"] == "ValueError"

    def test_json_formatter_tags(self):
        formatter = JSONFormatter()
        # "completato" attiva il tag success
        res = formatter.format("INFO", "L", "Download completato", extra={"bot_type": "ts"})
        data = json.loads(res)
        tags = data["tags"]
        assert "info" in tags
        assert "download" in tags
        assert "success" in tags

    def test_human_formatter_basic(self):
        formatter = HumanFormatter(colorize=False, show_context=True)
        res = formatter.format("INFO", "test_logger", "Hello")
        assert "INFO" in res

    def test_human_formatter_with_exception(self):
        formatter = HumanFormatter(colorize=False)
        res = formatter.format("ERROR", "L", "Fail", exception=ValueError("Oops"))
        assert "Exception: ValueError: Oops" in res

    def test_human_formatter_colorize(self):
        with patch.object(HumanFormatter, "_supports_color", return_value=True):
            formatter = HumanFormatter(colorize=True)
            res = formatter.format("ERROR", "L", "M")
            assert "\033[31m" in res
