import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.config_manager import (
    _reset_configuration_for_testing,
    add_account,
    get_default_account,
    import_configuration,
    load_config,
    set_config_value,
)


class TestConfigManagerRobust:
    @pytest.fixture(autouse=True)
    def setup_config(self, tmp_path):
        """Setup ambiente di test per ConfigManager."""
        # 1. Reset cache
        _reset_configuration_for_testing()

        # 2. Mock Paths
        self.mock_config_dir = tmp_path / "SyncroJob"
        self.mock_config_dir.mkdir()
        self.mock_config_file = self.mock_config_dir / "config.json"

        # Patch variabili globali
        with patch("src.core.config_manager.CONFIG_DIR", self.mock_config_dir):
            with patch("src.core.config_manager.CONFIG_FILE", self.mock_config_file):
                # Mock SecretsManager per evitare keyring
                with patch("src.core.config_manager.SecretsManager") as mock_sec:
                    mock_sec.is_available.return_value = (
                        False  # Force file encryption fallback
                    )
                    yield

    def test_load_config_defaults(self):
        """Test caricamento configurazione di default."""
        config = load_config()
        assert config["browser_timeout"] == 30
        assert config["reparti"] == ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"]
        assert self.mock_config_dir.exists()

    def test_save_and_reload(self):
        """Test persistenza configurazione."""
        set_config_value("browser_timeout", 60)

        # Reload pulito
        _reset_configuration_for_testing()
        config = load_config()

        assert config["browser_timeout"] == 60
        # Verifica su file
        with open(self.mock_config_file) as f:
            data = json.load(f)
            assert data["browser_timeout"] == 60

    def test_env_var_override(self):
        """Test override tramite variabili d'ambiente."""
        with patch.dict(
            os.environ,
            {"SYNCROJOB_BROWSER_HEADLESS": "true", "SYNCROJOB_BROWSER_TIMEOUT": "120"},
        ):
            _reset_configuration_for_testing()
            config = load_config()

            assert config["browser_headless"] is True
            assert config["browser_timeout"] == 120

    def test_account_management(self):
        """Test aggiunta, default e rimozione account."""
        # Add first (default)
        add_account("user1", "pass1")
        config = load_config()
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "user1"
        assert config["accounts"][0]["default"] is True

        # Add second
        add_account("user2", "pass2")
        config = load_config()
        assert len(config["accounts"]) == 2
        assert config["accounts"][1]["username"] == "user2"
        assert config["accounts"][1]["default"] is False  # user1 ancora default

        # Get Default
        acc = get_default_account()
        assert acc["username"] == "user1"

        # Remove user1
        from src.core.config_manager import remove_account

        remove_account("user1")
        config = load_config()
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "user2"
        assert config["accounts"][0]["default"] is True  # user2 promosso default

    def test_legacy_migration(self):
        """Test migrazione vecchia configurazione."""
        legacy_data = {"isab_username": "legacy_user", "isab_password": "legacy_pass"}
        with open(self.mock_config_file, "w") as f:
            json.dump(legacy_data, f)

        _reset_configuration_for_testing()
        config = load_config()

        assert "isab_username" not in config
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "legacy_user"
        # Password decriptata (qui simulata come plain perché mockata)
        assert config["accounts"][0]["password"] == "legacy_pass"

    def test_import_configuration(self, tmp_path):
        """Test importazione configurazione da file esterno."""
        import_file = tmp_path / "import.json"
        with open(import_file, "w") as f:
            json.dump({"browser_timeout": 999, "accounts": []}, f)

        success, msg = import_configuration(str(import_file))

        assert success is True
        assert "successo" in msg

        # Verifica applicazione
        _reset_configuration_for_testing()
        config = load_config()
        assert config["browser_timeout"] == 999

        # Verifica backup creato
        backups = list(self.mock_config_dir.glob("config_backup_*.json"))
        assert len(backups) == 1

    def test_import_invalid_json(self, tmp_path):
        """Test importazione file corrotto."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{bad")

        success, msg = import_configuration(str(bad_file))
        assert success is False
        assert "non è un JSON" in msg

    def test_path_getters(self):
        """Test getter dei percorsi."""
        from src.core.config_manager import get_data_path, get_logs_path

        data = get_data_path()
        logs = get_logs_path()

        assert str(self.mock_config_dir / "data") == data
        assert str(self.mock_config_dir / "logs") == logs
        assert Path(data).exists()
        assert Path(logs).exists()

    @patch("src.core.config_manager.SecretsManager")
    def test_credential_encryption_fallback(self, mock_sec):
        """Test crittografia locale password se keyring non disponibile."""
        mock_sec.is_available.return_value = False
        mock_sec.get_credential.return_value = None  # Force fallback to file

        # Setup mock encryption
        with patch(
            "src.utils.security.password_manager.encrypt",
            side_effect=lambda x: f"ENC_{x}",
        ):
            with patch(
                "src.utils.security.password_manager.decrypt",
                side_effect=lambda x: x.replace("ENC_", ""),
            ):
                add_account("user_enc", "secret")

                # Verifica su disco che sia criptata
                with open(self.mock_config_file) as f:
                    disk_data = json.load(f)
                    acc = disk_data["accounts"][0]
                    assert acc["password"] == "ENC_secret"

                # Verifica in memoria che sia decriptata
                _reset_configuration_for_testing()
                config = load_config()
                assert config["accounts"][0]["password"] == "secret"
