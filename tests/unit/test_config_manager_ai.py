"""
Tests for ConfigManager AI provider and model support.
"""

from unittest.mock import patch

from src.core import config_manager


class TestConfigManagerAI:
    def test_default_ai_config(self):
        """Verifica che i valori AI di default siano presenti."""
        defaults = config_manager.DEFAULT_CONFIG
        assert defaults["ai_provider"] == "gemini"
        assert defaults["ai_model"] == "gemini-1.5-pro"
        assert defaults["ollama_url"] == "http://localhost:11434"

    def test_set_ai_provider(self, tmp_path):
        """Verifica il salvataggio e recupero dell'AI provider."""
        # Reset cache per test pulito
        config_manager._reset_configuration_for_testing()
        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            config_manager.set_config_value("ai_provider", "ollama")
            config_manager.set_config_value("ai_model", "llama3")

            # Ricarichiamo per simulare persistenza
            config_manager._reset_configuration_for_testing()
            config = config_manager.load_config()
            assert config["ai_provider"] == "ollama"
            assert config["ai_model"] == "llama3"

    def test_get_ai_value_with_fallback(self, tmp_path):
        """Verifica che get_config_value restituisca i default corretti se non impostati."""
        config_manager._reset_configuration_for_testing()
        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            # Non mockiamo load_config, ma lasciamo che usi i DEFAULT_CONFIG
            # perché non troverà il file nel tmp_path vuoto
            val = config_manager.get_config_value("ai_provider", "fallback")
            assert val == "gemini"  # Default in DEFAULT_CONFIG

            # Se chiediamo una chiave non in DEFAULT_CONFIG e non caricata
            val_ext = config_manager.get_config_value("non_existent", "my_fallback")
            assert val_ext == "my_fallback"
