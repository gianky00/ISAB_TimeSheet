from unittest.mock import MagicMock, patch

import pytest

from src.core.logging.config import LoggingConfig
from src.core.logging.logger import StructuredLogger, get_logger


@pytest.fixture
def mock_config():
    config = MagicMock(spec=LoggingConfig)
    config.default_level = "INFO"
    config.console_enabled = True
    config.json_log_file = None
    config.human_log_file = None
    config.errors_log_file = None
    config.ensure_directories = MagicMock()
    return config


def test_logger_initialization(mock_config):
    logger = StructuredLogger("test_logger", config=mock_config)
    assert logger.name == "test_logger"
    assert logger.min_level == 20


def test_parse_level():
    logger = StructuredLogger("test")
    assert logger._parse_level("DEBUG") == 10
    assert logger._parse_level("INFO") == 20
    assert logger._parse_level("ERROR") == 40
    assert logger._parse_level("INVALID") == 20


def test_should_log():
    logger = StructuredLogger("test")
    logger.min_level = 20
    assert logger._should_log("INFO") is True
    assert logger._should_log("WARNING") is True
    assert logger._should_log("DEBUG") is False


@patch("src.core.logging.logger.get_config")
def test_get_logger_factory(mock_get_config):
    mock_get_config.return_value = MagicMock()
    logger1 = get_logger("test1")
    logger2 = get_logger("test1")
    assert logger1 is logger2
    assert isinstance(logger1, StructuredLogger)
