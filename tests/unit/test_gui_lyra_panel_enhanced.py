"""
Tests for LyraPanel UI and worker interaction.
"""

from unittest.mock import patch

import pytest
from PyQt6.QtWidgets import QLabel

from src.gui.panels.lyra.lyra_panel import LyraPanel
from src.gui.widgets.message_bubble import MessageBubble


class TestLyraPanelEnhanced:
    @pytest.fixture
    def panel(self, qtbot):
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

    def test_ask_lyra_thinking_feedback(self, panel, qtbot):
        """Verifica che appaia il feedback 'sta pensando' durante la richiesta."""
        with patch("src.gui.panels.lyra.lyra_panel.LyraWorker") as mock_worker_cls:
            # Mock del worker per non farlo finire subito
            mock_worker = mock_worker_cls.return_value

            panel.ask_lyra("Ciao")

            # Verifichiamo la chat area
            # L'ultima bolla dovrebbe essere "sta pensando"
            last_item = panel.chat_area.chat_layout.itemAt(panel.chat_area.chat_layout.count() - 2)
            assert last_item is not None
            last_widget = last_item.widget()
            assert isinstance(last_widget, MessageBubble)

            labels = last_widget.findChildren(QLabel)
            found = any("sta pensando" in label.text() for label in labels)
            assert found
            assert not panel.input_bar.send_btn.isEnabled()

    def test_on_answer_removes_thinking(self, panel, qtbot):
        """Verifica che la risposta sostituisca il messaggio di attesa."""
        # 1. Aggiungiamo un messaggio di attesa manuale per simulare
        panel.chat_area.append_message("Lyra", "<i>Lyra sta pensando...</i>")
        initial_count = panel.chat_area.chat_layout.count()

        # 2. Chiamiamo _on_answer
        panel._on_answer("Ecco la risposta")

        # Il conteggio non dovrebbe essere aumentato di 1 (perché uno è stato rimosso)
        assert panel.chat_area.chat_layout.count() == initial_count

        # L'ultimo messaggio ora è la risposta reale
        last_item = panel.chat_area.chat_layout.itemAt(panel.chat_area.chat_layout.count() - 2)
        last_widget = last_item.widget()
        labels = last_widget.findChildren(QLabel)
        assert any("Ecco la risposta" in label.text() for label in labels)

    @patch("src.gui.panels.lyra.lyra_panel.ModelListWorker")
    def test_fetch_models_provider_aware(self, mock_worker_cls, panel):
        """Verifica che il fetch modelli passi il provider corretto."""
        # Fermiamo il worker attuale se presente
        if hasattr(panel, "model_worker") and panel.model_worker:
            panel.model_worker.terminate()
            panel.model_worker = None

        mock_worker_cls.return_value.isRunning.return_value = False

        # Mockiamo config_manager nel modulo lyra_panel
        with patch("src.gui.panels.lyra.lyra_panel.config_manager.get_config_value", return_value="ollama"):
            panel._fetch_models()
            assert mock_worker_cls.return_value.start.called
            # Verifica argomenti passati al costruttore nell'ultima chiamata
            _args, kwargs = mock_worker_cls.call_args
            assert kwargs.get("provider") == "ollama"
