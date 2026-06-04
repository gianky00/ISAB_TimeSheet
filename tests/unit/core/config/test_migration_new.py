import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.application.services.config.migration import (
    check_and_migrate_local_config,
    deep_update_paths,
    migrate_legacy_keys,
)


class TestConfigMigration:
    def test_deep_update_paths(self):
        old = "C:\\Old\\Path"
        new = "/new/path"
        data = {
            "p1": "C:\\Old\\Path\\file.txt",
            "p2": ["C:\\Old\\Path\\dir", "other"],
            "inner": {"p3": "C:\\Old\\Path"},
        }
        res = deep_update_paths(data, old, new)

        assert res["p1"] == "/new/path/file.txt"
        assert res["p2"][0] == "/new/path/dir"
        assert res["inner"]["p3"] == "/new/path"

    def test_migrate_legacy_keys_success(self):
        config = {"isab_username": "mario", "isab_password": "pwd", "other": "val"}
        changed = migrate_legacy_keys(config)

        assert changed is True
        assert "accounts" in config
        assert config["accounts"][0]["username"] == "mario"
        assert "isab_username" not in config

    def test_migrate_legacy_keys_no_change(self):
        config = {"accounts": [], "other": "val"}
        assert migrate_legacy_keys(config) is False

    def test_check_and_migrate_local_config_success(self, fs):
        from src.application.services.constants import FileNames

        # Setup legacy dir e file
        legacy_dir = Path("/legacy_app")
        fs.create_dir(str(legacy_dir))
        old_data = {"isab_username": "old_user", "path": "/legacy_app/data"}
        fs.create_file(str(legacy_dir / FileNames.CONFIG), contents=json.dumps(old_data))

        # Setup target dir (standard)
        target_dir = Path("/target_config")
        fs.create_dir(str(target_dir))

        # Patching CONFIG_DIR in migration module
        with patch("src.application.services.config.migration.CONFIG_DIR", target_dir):
            with patch("src.application.services.config.migration.user_data_dir", return_value="/legacy_app"):
                load_mock = MagicMock(return_value={})
                write_mock = MagicMock()

                with patch("src.application.services.config.migration.sys") as mock_sys:
                    mock_sys.frozen = False

                    res = check_and_migrate_local_config(Path("/tmp"), load_mock, write_mock)

                    assert res is True
                    assert write_mock.called
                    # Verifica che il path sia stato aggiornato nella migrazione
                    saved_config = write_mock.call_args[0][1]
                    # deep_update_paths converte in /
                    assert str(target_dir).replace("\\", "/") in saved_config["path"].replace("\\", "/")
