from unittest.mock import MagicMock, patch

from src.application.services.logging.migration import LoggingAdapter, get_logger, migrate_logging_call


class TestLoggingMigration:
    def test_get_logger_helper(self):
        logger = get_logger("test_module")
        assert isinstance(logger, LoggingAdapter)

    def test_logging_adapter_debug(self):
        with patch("src.application.services.logging.migration.get_new_logger") as mock_get_new:
            mock_structured = MagicMock()
            mock_get_new.return_value = mock_structured

            adapter = LoggingAdapter("test")
            adapter.debug("Msg %s", "Arg1", extra={"key": "val"})

            mock_structured.debug.assert_called_with("Msg Arg1", key="val")

    def test_logging_adapter_info(self):
        with patch("src.application.services.logging.migration.get_new_logger") as mock_get_new:
            mock_structured = MagicMock()
            mock_get_new.return_value = mock_structured

            adapter = LoggingAdapter("test")
            adapter.info("Msg %s", "Arg1", extra={"key": "val"})

            mock_structured.info.assert_called_with("Msg Arg1", key="val")

    def test_logging_adapter_warning(self):
        with patch("src.application.services.logging.migration.get_new_logger") as mock_get_new:
            mock_structured = MagicMock()
            mock_get_new.return_value = mock_structured

            adapter = LoggingAdapter("test")
            adapter.warning("Msg %s", "Arg1", extra={"key": "val"})

            mock_structured.warning.assert_called_with("Msg Arg1", key="val")

    def test_logging_adapter_error(self):
        with patch("src.application.services.logging.migration.get_new_logger") as mock_get_new:
            mock_structured = MagicMock()
            mock_get_new.return_value = mock_structured

            adapter = LoggingAdapter("test")
            adapter.error("Msg", extra={"k": "v"})

            mock_structured.error.assert_called_with("Msg", k="v")

    def test_logging_adapter_critical(self):
        with patch("src.application.services.logging.migration.get_new_logger") as mock_get_new:
            mock_structured = MagicMock()
            mock_get_new.return_value = mock_structured

            adapter = LoggingAdapter("test")
            adapter.critical("Crit", extra={"a": "b"})

            mock_structured.critical.assert_called_with("Crit", a="b")

    def test_logging_adapter_exception_with_exc(self):
        with patch("src.application.services.logging.migration.get_new_logger") as mock_get_new:
            mock_structured = MagicMock()
            mock_get_new.return_value = mock_structured

            adapter = LoggingAdapter("test")

            try:
                raise ValueError("Test error")  # noqa: TRY301
            except ValueError as e:
                adapter.exception("Fail %s", "now")

            assert mock_structured.exception.called
            args, kwargs = mock_structured.exception.call_args
            assert args[0] == "Fail now"
            assert isinstance(kwargs["exc"], ValueError)

    def test_logging_adapter_exception_without_exc(self):
        with patch("src.application.services.logging.migration.get_new_logger") as mock_get_new:
            mock_structured = MagicMock()
            mock_get_new.return_value = mock_structured

            adapter = LoggingAdapter("test")
            adapter.exception("No exc")

            assert mock_structured.error.called
            assert mock_structured.error.call_args[0][0] == "No exc"

    def test_migrate_logging_call(self):
        old_code = "import logging\nlogger = logging.getLogger(__name__)\nlogger.log(logging.INFO, 'Msg')"

        new_code = migrate_logging_call(old_code)

        assert "from src.application.services.logging import get_logger" in new_code
        assert "logger = get_logger(__name__)" in new_code
        assert "logger.info( 'Msg')" in new_code
