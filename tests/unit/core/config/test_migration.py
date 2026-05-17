from src.core.config.migration import deep_update_paths, migrate_legacy_keys


class TestConfigMigration:
    def test_deep_update_paths(self):
        """Testa la sostituzione ricorsiva dei path."""
        data = {
            "path": "C:/old/path/file.txt",
            "list": ["C:/old/path/1.txt", "C:/old/path/2.txt"],
            "nested": {"inner": "C:/old/path/inner.txt"},
        }
        old_path = "C:/old/path"
        new_path = "D:/new/path"

        updated = deep_update_paths(data, old_path, new_path)

        assert updated["path"] == "D:/new/path/file.txt"
        assert updated["list"][0] == "D:/new/path/1.txt"
        assert updated["nested"]["inner"] == "D:/new/path/inner.txt"

    def test_migrate_legacy_keys(self):
        """Testa la migrazione delle vecchie chiavi isab_username/password."""
        config = {"isab_username": "olduser", "isab_password": "oldpass", "other_setting": True}

        changed = migrate_legacy_keys(config)
        assert changed is True
        assert "accounts" in config
        assert config["accounts"][0]["username"] == "olduser"
        assert config["accounts"][0]["password"] == "oldpass"
        assert "isab_username" not in config
        assert "isab_password" not in config

    def test_migrate_legacy_keys_already_migrated(self):
        """Testa che non faccia nulla se già migrato o chiavi assenti."""
        config = {"accounts": [{"username": "user1"}]}
        assert migrate_legacy_keys(config) is False

        config = {"other": 1}
        assert migrate_legacy_keys(config) is False
