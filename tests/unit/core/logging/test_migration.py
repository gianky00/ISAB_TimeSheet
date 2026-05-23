from unittest.mock import MagicMock, patch

from src.core.logging.migration import LoggingAdapter, get_logger, migrate_logging_call


class TestLoggingMigration:
    def test_logging_adapter_delegation(self):
        with patch("src.core.logging.migration.get_new_logger") as mock_get:
            mock_struct = MagicMock()
            mock_get.return_value = mock_struct

            adapter = LoggingAdapter("test")

            # Debug
            adapter.debug("Msg %s", "arg", extra={"k": "v"})
            mock_struct.debug.assert_called_with("Msg arg", k="v")

            # Info
            adapter.info("Info")
            mock_struct.info.assert_called_with("Info")

            # Warning
            adapter.warning("Warn")
            mock_struct.warning.assert_called_with("Warn")

            # Error
            adapter.error("Err")
            mock_struct.error.assert_called_with("Err")

            # Critical
            adapter.critical("Crit")
            mock_struct.critical.assert_called_with("Crit")

    def test_logging_adapter_exception(self):
        with patch("src.core.logging.migration.get_new_logger") as mock_get:
            mock_struct = MagicMock()
            mock_get.return_value = mock_struct
            adapter = LoggingAdapter("test")

            # Case 1: no active exception
            adapter.exception("Fail")
            mock_struct.error.assert_called_with("Fail")

            # Case 2: active exception
            def trigger_error():
                raise ValueError("Crash")

            try:
                trigger_error()
            except ValueError:
                adapter.exception("Caught")

            assert mock_struct.exception.called
            args = mock_struct.exception.call_args
            assert args[0][0] == "Caught"
            assert isinstance(args[1]["exc"], ValueError)

    def test_get_logger_helper(self):
        adapter = get_logger("my_logger")
        assert isinstance(adapter, LoggingAdapter)

    def test_migrate_logging_call(self):
        old = "import logging\nlogger = logging.getLogger(__name__)\nlogger.log(logging.INFO, 'msg')"
        new = migrate_logging_call(old)

        assert "from src.core.logging import get_logger" in new
        assert "get_logger(__name__)" in new
        # Nota: rimane lo spazio dopo la virgola originale
        assert "logger.info( 'msg')" in new
