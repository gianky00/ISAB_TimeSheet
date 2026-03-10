from unittest.mock import patch

import pytest
from PyQt6.QtWidgets import QApplication

from src.gui.panels.lyra.lyra_panel import LyraPanel


class TestLyraPanelEnhanced:
    @pytest.fixture
    def panel(self, qtbot, mocker):
        # Patch del worker PRIMA dell'istanziazione per evitare chiamate reali nel costruttore
        mocker.patch("src.gui.panels.lyra.lyra_panel.ModelListWorker")

        with (
            patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake_key"),
            patch(
                "src.gui.panels.lyra.lyra_panel.config_manager.get_config_value",
                side_effect=lambda k, d=None: d
                if k not in ["ai_provider", "ai_model", "ollama_url"]
                else (
                    "gemini"
                    if k == "ai_provider"
                    else ("gemini-1.5-pro" if k == "ai_model" else "http://localhost:11434")
                ),
            ),
        ):
            p = LyraPanel()
            qtbot.addWidget(p)
            return p

    @pytest.mark.skip(reason="isVisible() restituisce False in ambiente headless Windows nonostante show().")
    def test_ask_lyra_thinking_feedback(self, panel, qtbot):
        with patch("src.gui.panels.lyra.lyra_panel.LyraWorker") as mock_worker_cls:
            mock_worker = mock_worker_cls.return_value
            mock_worker.isRunning.return_value = True
            panel.ask_lyra("Ciao")
            QApplication.processEvents()
            assert panel.chat_area.is_typing_visible()

    @pytest.mark.skip(reason="isVisible() restituisce False in ambiente headless Windows nonostante show().")
    def test_on_answer_removes_thinking(self, panel, qtbot):
        panel.chat_area.set_typing(True)
        panel._on_answer("Ecco la risposta")
        assert not panel.chat_area.is_typing_visible()

    def test_fetch_models_provider_aware(self, panel, mocker):
        """Verifica che il fetch modelli passi il provider corretto."""
        # Recuperiamo il mock già creato nella fixture
        import src.gui.panels.lyra.lyra_panel as lp_mod
        mock_worker_cls = lp_mod.ModelListWorker

        mock_worker_cls.return_value.isRunning.return_value = False

        # Simuliamo un cambio provider e un refresh manuale
        with patch("src.gui.panels.lyra.lyra_panel.config_manager.get_config_value", return_value="ollama"):
            panel._fetch_models()

            assert mock_worker_cls.return_value.start.called
            # Verifica kwargs dell'ultima chiamata (V9.0 ModelListWorker(api_key, provider, ollama_url))
            _, kwargs = mock_worker_cls.call_args
            assert kwargs.get("provider") == "ollama"
