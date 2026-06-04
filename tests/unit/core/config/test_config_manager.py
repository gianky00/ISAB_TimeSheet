from src.application.services.config_manager import _reset_configuration_for_testing, load_config, save_config


def test_load_config_defaults(tmp_path, mocker):
    _reset_configuration_for_testing()
    mocker.patch("src.application.services.config_manager.CONFIG_FILE", tmp_path / "config.json")
    config = load_config()
    assert isinstance(config, dict)
    assert "browser_timeout" in config


def test_save_and_load_config(tmp_path, mocker):
    _reset_configuration_for_testing()
    config_file = tmp_path / "config_save.json"
    mocker.patch("src.application.services.config_manager.CONFIG_FILE", config_file)
    mocker.patch("src.application.services.config_manager.CONFIG_DIR", tmp_path)

    config = load_config()
    config["test_val"] = 123
    # Forza salvataggio sincrono per evitare race condition
    save_config(config, async_save=False)

    _reset_configuration_for_testing()
    new_config = load_config()
    assert new_config["test_val"] == 123
