from unittest.mock import MagicMock, patch

import pytest

from src.core.logging.decorators import log_entry_exit, measure_time


class TestDecorators:
    @patch("src.core.logging.decorators.get_logger")
    @patch("src.core.logging.decorators.get_tracker")
    def test_measure_time_success(self, mock_tracker, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        @measure_time(threshold_ms=100)
        def my_func(x):
            return x * 2

        res = my_func(5)
        assert res == 10
        assert mock_tracker.return_value.track.called
        assert mock_logger.log.called

    @patch("src.core.logging.decorators.time.perf_counter")
    @patch("src.core.logging.decorators.get_logger")
    @patch("src.core.logging.decorators.get_tracker")
    def test_measure_time_slow(self, mock_tracker, mock_get_logger, mock_perf):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        # Simula 1 secondo di esecuzione (1000ms)
        mock_perf.side_effect = [0.0, 1.0, 0.0, 1.0]  # Chiamate multiple per context e wrapper

        @measure_time(threshold_ms=100)
        def slow_func():
            return True

        slow_func()
        # Il livello deve essere WARNING perché 1000 > 100
        assert mock_logger.log.call_args[0][0] == "WARNING"

    @patch("src.core.logging.decorators.get_logger")
    def test_measure_time_failure(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        @measure_time()
        def fail_func():
            raise ValueError("Boom")

        with pytest.raises(ValueError):
            fail_func()

        assert mock_logger.exception.called

    @patch("src.core.logging.decorators.get_logger")
    def test_log_entry_exit_basic(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        @log_entry_exit(log_args=True, log_result=True)
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        # 1. Entering
        assert "Entering" in mock_logger.debug.call_args_list[0][0][0]
        # 2. Exiting
        assert "Exiting" in mock_logger.debug.call_args_list[1][0][0]

    @patch("src.core.logging.decorators.get_logger")
    def test_log_entry_exit_error(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        @log_entry_exit()
        def fail():
            raise RuntimeError()

        with pytest.raises(RuntimeError):
            fail()

        assert mock_logger.exception.called
