from unittest.mock import patch

from src.application.services.config.account_manager import (
    add_account_logic,
    remove_account_logic,
    set_default_account_logic,
    switch_default_account_logic,
)


class TestAccountManager:
    def test_add_account_logic_first(self):
        config = {}
        username = "user1"
        password = "pwd1"
        # Il primo account deve diventare default automaticamente
        new_config = add_account_logic(config, username, password)
        assert len(new_config["accounts"]) == 1
        assert new_config["accounts"][0]["username"] == "user1"
        assert new_config["accounts"][0]["default"] is True

    def test_add_account_logic_multiple(self):
        config = {"accounts": [{"username": "user1", "default": True}]}
        new_config = add_account_logic(config, "user2", "pwd2", is_default=True)
        assert len(new_config["accounts"]) == 2
        # Verifica che il vecchio default sia stato rimosso
        user1 = next(a for a in new_config["accounts"] if a["username"] == "user1")
        user2 = next(a for a in new_config["accounts"] if a["username"] == "user2")
        assert user1["default"] is False
        assert user2["default"] is True

    def test_add_account_logic_safework(self):
        config = {}
        new_config = add_account_logic(config, "sw_user", "pwd", account_type="Esecutore")
        assert "safework_accounts" in new_config
        assert new_config["safework_accounts"][0]["type"] == "Esecutore"

    @patch("src.application.services.secrets_manager.SecretsManager.is_available", return_value=True)
    @patch("src.application.services.secrets_manager.SecretsManager.delete_credential")
    def test_remove_account_logic(self, mock_delete, mock_avail):
        config = {
            "accounts": [{"username": "user1", "default": True}, {"username": "user2", "default": False}]
        }
        new_config = remove_account_logic(config, "user1")
        assert len(new_config["accounts"]) == 1
        # user2 deve essere diventato il nuovo default
        assert new_config["accounts"][0]["username"] == "user2"
        assert new_config["accounts"][0]["default"] is True
        assert mock_delete.called

    def test_set_default_account_logic(self):
        config = {
            "accounts": [{"username": "user1", "default": True}, {"username": "user2", "default": False}]
        }
        found = set_default_account_logic(config, "user2")
        assert found is True
        assert config["accounts"][0]["default"] is False
        assert config["accounts"][1]["default"] is True

    def test_switch_default_account_logic(self):
        config = {
            "accounts": [
                {"username": "user1", "default": True},
                {"username": "user2", "default": False},
                {"username": "user3", "default": False},
            ]
        }
        success, next_user = switch_default_account_logic(config)
        assert success is True
        assert next_user == "user2"
        assert config["accounts"][1]["default"] is True

        # Switch ancora
        success, next_user = switch_default_account_logic(config)
        assert next_user == "user3"

        # Torna all'inizio
        success, next_user = switch_default_account_logic(config)
        assert next_user == "user1"

    def test_switch_default_account_logic_single(self):
        config = {"accounts": [{"username": "user1", "default": True}]}
        success, next_user = switch_default_account_logic(config)
        assert success is False
        assert next_user is None
