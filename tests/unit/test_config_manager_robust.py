import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.application.services.config_manager import (
    _reset_configuration_for_testing,
    add_account,
    get_default_account,
    import_config_from_file,
    load_config,
    remove_account,
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

        # Patch variabili globali in entrambi i moduli che le usano
        with (
            patch("src.application.services.config_manager.CONFIG_DIR", self.mock_config_dir),
            patch("src.application.services.config_manager.CONFIG_FILE", self.mock_config_file),
            patch("src.application.services.paths.CONFIG_DIR", self.mock_config_dir),
            patch("src.application.services.paths.CONFIG_FILE", self.mock_config_file),
            patch("src.application.services.paths.DB_DIR", self.mock_config_dir / "data"),
            patch("src.application.services.paths.LOGS_DIR", self.mock_config_dir / "logs"),
            patch("src.application.services.config.security.SecretsManager") as mock_sec,
        ):
            # Crea fisicamente le directory per i path getters
            (self.mock_config_dir / "data").mkdir(parents=True, exist_ok=True)
            (self.mock_config_dir / "logs").mkdir(parents=True, exist_ok=True)

            # Mock SecretsManager per evitare keyring e MagicMock nel JSON
            mock_sec.is_available.return_value = False
            mock_sec.get_credential.return_value = None
            yield

    def test_load_config_defaults(self):
        """Test caricamento configurazione di default."""
        config = load_config()
        assert config["browser_timeout"] == 300
        assert config["reparti"] == ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"]
        assert self.mock_config_dir.exists()

    def test_save_and_reload(self):
        """Test persistenza configurazione."""
        set_config_value("browser_timeout", 60, async_save=False)

        # Reload pulito
        _reset_configuration_for_testing()
        config = load_config()

        assert config["browser_timeout"] == 60
        # Verifica su file
        data = json.loads(self.mock_config_file.read_text(encoding="utf-8"))
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
        add_account("isab", {"username": "user1", "password": "pass1", "is_default": True}, async_save=False)
        config = load_config()
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "user1"
        assert config["accounts"][0]["default"] is True

        # Add second
        add_account("isab", {"username": "user2", "password": "pass2", "is_default": False}, async_save=False)
        config = load_config()
        assert len(config["accounts"]) == 2
        assert config["accounts"][1]["username"] == "user2"
        # In V9.0 il flag 'default' viene gestito internamente
        assert config["accounts"][1].get("default", False) is False

        # Get Default
        acc = get_default_account("isab")
        assert acc["username"] == "user1"

        # Remove user1
        remove_account("isab", "user1", async_save=False)
        config = load_config()
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "user2"
        # user2 dovrebbe essere diventato default essendo l'unico
        assert get_default_account("isab")["username"] == "user2"

    def test_legacy_migration(self):
        """Test migrazione vecchia configurazione."""
        legacy_data = {"isab_username": "legacy_user", "isab_password": "legacy_pass"}
        self.mock_config_file.write_text(json.dumps(legacy_data), encoding="utf-8")

        _reset_configuration_for_testing()
        config = load_config()

        assert "isab_username" not in config
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "legacy_user"
        # Password decriptata (qui simulata come plain perché mockata)
        assert config["accounts"][0]["password"] == "legacy_pass"

    def test_import_configuration(self, tmp_path):
        """Test importazione configurazione da file esterno."""
        # Crea un file pre-esistente per forzare il backup
        self.mock_config_file.write_text(json.dumps({"old": "data"}), encoding="utf-8")

        import_file = tmp_path / "import.json"
        import_file.write_text(json.dumps({"browser_timeout": 999, "accounts": []}), encoding="utf-8")

        # Passa l'oggetto Path, non la stringa (firma V9.0)
        success, msg = import_config_from_file(import_file, async_save=False)

        assert success is True
        assert "successo" in msg
        assert "Backup precedente" in msg

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

        success, msg = import_config_from_file(bad_file)
        assert success is False
        assert "non è un JSON" in msg

    def test_path_getters(self):
        """Test getter dei percorsi."""
        from src.application.services.paths import get_data_path, get_logs_path

        data_path = get_data_path()
        logs_path = get_logs_path()

        # In V9.0 i path sono basati sulla CONFIG_DIR mockata
        assert str(self.mock_config_dir / "data") == data_path
        assert str(self.mock_config_dir / "logs") == logs_path
        assert Path(data_path).exists()
        assert Path(logs_path).exists()

    @patch("src.application.services.config.security.SecretsManager")
    def test_credential_encryption_fallback(self, mock_sec):
        """Test crittografia locale password se keyring non disponibile."""
        mock_sec.is_available.return_value = False
        mock_sec.get_credential.return_value = None  # Force fallback to file

        # Setup mock encryption
        with (
            patch(
                "src.infrastructure.utils.security.password_manager.encrypt",
                side_effect=lambda x: f"ENC:v2:{x}",
            ),
            patch(
                "src.infrastructure.utils.security.password_manager.decrypt",
                side_effect=lambda x: x.replace("ENC:v2:", ""),
            ),
        ):
            add_account("isab", {"username": "user_enc", "password": "secret"}, async_save=False)

            # Verifica su disco che sia criptata
            disk_data = json.loads(self.mock_config_file.read_text(encoding="utf-8"))
            acc = disk_data["accounts"][0]
            assert acc["password"] == "ENC:v2:secret"

            # Verifica in memoria che sia decriptata
            _reset_configuration_for_testing()
            config = load_config()
            assert config["accounts"][0]["password"] == "secret"
