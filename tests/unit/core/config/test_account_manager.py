from src.core.config.account_manager import (
    add_account_logic,
    remove_account_logic,
    set_default_account_logic,
    switch_default_account_logic,
)


class TestAccountManagerLogic:
    def test_add_account_logic_first(self):
        """Testa l'aggiunta del primo account (deve diventare default)."""
        config = {}
        add_account_logic(config, "user1", "pass1")
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "user1"
        assert config["accounts"][0]["default"] is True

    def test_add_account_logic_multiple(self):
        """Testa l'aggiunta di più account."""
        config = {"accounts": [{"username": "user1", "default": True}]}
        add_account_logic(config, "user2", "pass2", is_default=True)

        assert len(config["accounts"]) == 2
        # user1 non deve più essere default
        u1 = next(a for a in config["accounts"] if a["username"] == "user1")
        assert u1["default"] is False

        u2 = next(a for a in config["accounts"] if a["username"] == "user2")
        assert u2["default"] is True

    def test_remove_account_logic(self, mocker):
        """Testa la rimozione di un account."""
        mocker.patch("src.core.secrets_manager.SecretsManager.is_available", return_value=False)
        config = {
            "accounts": [{"username": "user1", "default": True}, {"username": "user2", "default": False}]
        }

        remove_account_logic(config, "user1")
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "user2"
        # user2 deve essere diventato default automaticamente
        assert config["accounts"][0]["default"] is True

    def test_set_default_account_logic(self):
        """Testa il setting manuale del default."""
        config = {
            "accounts": [{"username": "user1", "default": True}, {"username": "user2", "default": False}]
        }

        success = set_default_account_logic(config, "user2")
        assert success is True
        assert config["accounts"][1]["default"] is True
        assert config["accounts"][0]["default"] is False

        success = set_default_account_logic(config, "non-existent")
        assert success is False

    def test_switch_default_account_logic(self):
        """Testa il round-robin switch."""
        config = {
            "accounts": [
                {"username": "user1", "default": True},
                {"username": "user2", "default": False},
                {"username": "user3", "default": False},
            ]
        }

        # Primo switch: user2
        success, next_user = switch_default_account_logic(config)
        assert success is True
        assert next_user == "user2"
        assert config["accounts"][1]["default"] is True

        # Secondo switch: user3
        success, next_user = switch_default_account_logic(config)
        assert next_user == "user3"

        # Terzo switch: torna a user1
        success, next_user = switch_default_account_logic(config)
        assert next_user == "user1"

    def test_switch_default_account_logic_fail(self):
        """Testa switch con meno di 2 account."""
        config = {"accounts": [{"username": "u1", "default": True}]}
        success, next_user = switch_default_account_logic(config)
        assert success is False
        assert next_user is None
