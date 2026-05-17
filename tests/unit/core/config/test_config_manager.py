import json
from unittest.mock import patch

import pytest

from src.core.config_manager import _reset_configuration_for_testing, load_config, save_config


@pytest.fixture(autouse=True)
def reset_config():
    _reset_configuration_for_testing()
    yield
    _reset_configuration_for_testing()


@patch("src.core.config_manager.CONFIG_FILE")
def test_load_config_defaults(mock_config_file):
    mock_config_file.exists.return_value = False

    config = load_config()
    assert config is not None
    assert "accounts" in config


@patch("src.core.config_manager.CONFIG_FILE")
def test_save_and_load_config(mock_config_file, tmp_path):
    # Setup temp path for config
    test_config_path = tmp_path / "config.json"
    mock_config_file.exists.return_value = True
    mock_config_file.read_text.return_value = json.dumps({"test_key": "test_value"})
    mock_config_file.with_suffix.return_value = tmp_path / "config.tmp"
    mock_config_file.parent = tmp_path

    # Mock for atomic write
    with patch("src.core.config_manager.CONFIG_FILE", test_config_path):
        config = load_config()
        config["new_key"] = "new_value"
        save_config(config)

        # Invalidate cache to force reload
        _reset_configuration_for_testing()

        reloaded_config = load_config()
        assert reloaded_config["new_key"] == "new_value"
