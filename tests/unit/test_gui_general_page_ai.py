import pytest
from PyQt6.QtCore import Qt
from unittest.mock import MagicMock, patch
from src.gui.panels.settings.pages.general_page import GeneralPage

class TestGeneralPageAI:
    @pytest.fixture
    def page(self, qtbot):
        with patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake_key"):
            p = GeneralPage()
            qtbot.addWidget(p)
            return p

    def test_provider_switch_visibility(self, page, qtbot):
        """Verifica che cambiare provider mostri/nasconda l'URL di Ollama."""
        page.provider_combo.setCurrentText("ollama")
        assert not page.ollama_url_container.isHidden()

        page.provider_combo.setCurrentText("gemini")
        assert page.ollama_url_container.isHidden()

    def test_load_from_config_ai(self, page):
        """Verifica il caricamento dei valori AI dalla configurazione."""
        config = {
            "ai_provider": "ollama",
            "ai_model": "llama3:latest",
            "ollama_url": "http://192.168.1.10:11434",
            "browser_headless": True,
            "browser_timeout": 45,
        }
        page.load_from_config(config)

        assert page.provider_combo.currentText() == "ollama"
        assert page.model_combo.currentText() == "llama3:latest"
        assert page.ollama_url_edit.text() == "http://192.168.1.10:11434"

    def test_save_to_config_ai(self, page):
        """Verifica che il salvataggio dei dati AI in un dizionario sia corretto."""
        page.provider_combo.setCurrentText("ollama")
        page.model_combo.setEditText("mistral")
        page.ollama_url_edit.setText("http://localhost:1234")

        # In V9.0 save_to_config accetta un dict
        config = {}
        page.save_to_config(config)

        assert config["ai_provider"] == "ollama"
        assert config["ai_model"] == "mistral"
        assert config["ollama_url"] == "http://localhost:1234"

    @patch("src.gui.panels.settings.pages.general_page.ModelListWorker")
    def test_refresh_models_trigger(self, mock_worker_cls, page, qtbot):
        """Verifica che il refresh modelli venga avviato al click."""
        mock_worker = mock_worker_cls.return_value
        mock_worker.isRunning.return_value = False

        # Clicca il bottone refresh
        qtbot.mouseClick(page.btn_refresh_models, Qt.MouseButton.LeftButton)

        assert mock_worker.start.called
        assert not page.btn_refresh_models.isEnabled()
        assert "Recupero" in page.btn_refresh_models.text()
