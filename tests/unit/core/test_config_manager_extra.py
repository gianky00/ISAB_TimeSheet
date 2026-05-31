from src.core.config_manager import (
    _load_base_config,
    get_default_account,
    get_version,
    import_config_from_file,
    save_config,
    set_default_account,
    switch_default_account,
)


def test_get_version():
    from src.core.version import __version__

    assert get_version() == __version__


def test_load_base_config_exception(tmp_path, mocker):
    # simulate file exists but decode error
    f = tmp_path / "config.json"
    f.write_text("{bad json", encoding="utf-8")
    mocker.patch("src.core.config_manager.CONFIG_FILE", f)
    cfg = _load_base_config()
    assert isinstance(cfg, dict)


def test_save_config_exceptions(mocker):
    mocker.patch("src.core.config_manager.encrypt_all_credentials", side_effect=Exception("Encrypt fail"))
    # Test sync error fallback
    assert save_config({}, async_save=False) is False


def test_save_config_async_exception(mocker):
    # The exception inside _execute_save should not crash the app, just print
    mocker.patch(
        "src.core.config_manager.encrypt_all_credentials", side_effect=Exception("Async encrypt fail")
    )
    # The wrapper starts a thread, it will return True immediately
    assert save_config({}, async_save=True) is True


def test_set_default_account_fallback(mocker):
    mocker.patch("src.core.config_manager.set_default_account_logic", return_value=False)
    assert set_default_account("isab", "none", async_save=False) is False


def test_switch_default_account_fallback(mocker):
    mocker.patch("src.core.config_manager.switch_default_account_logic", return_value=(False, ""))
    assert switch_default_account("isab", async_save=False) is False


def test_get_default_account_no_default_flag(mocker):
    mock_config = {"accounts": [{"username": "u1"}, {"username": "u2"}]}
    mocker.patch("src.core.config_manager.load_config", return_value=mock_config)
    res = get_default_account("isab")
    assert res["username"] == "u1"


def test_import_config_from_file_exceptions(tmp_path, mocker):
    f = tmp_path / "foo.json"
    f.write_text('{"valid": true}', encoding="utf-8")
    mocker.patch("src.core.config_manager.save_config", side_effect=Exception("Critical disk error"))
    success, msg = import_config_from_file(f, async_save=False)
    assert success is False
    assert "Errore critico importazione" in msg

    mocker.patch("src.core.config_manager.save_config", return_value=False)
    success, msg = import_config_from_file(f, async_save=False)
    assert success is False
    assert "Errore durante il salvataggio" in msg
