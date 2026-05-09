"""
Integration Tests per SafeWork PDL Flow.
Simula un'esecuzione completa end-to-end con Page Object Model.
"""

from unittest.mock import MagicMock, patch

from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLIntegration:
    @patch("webdriver_manager.chrome.ChromeDriverManager")
    def test_full_pdl_flow_simulation(self, mock_dm, mocker):
        """Simulazione end-to-end del flusso PDL."""
        # 1. Setup Driver e Mocks
        mock_driver = MagicMock()
        mock_chrome = mocker.patch("selenium.webdriver.Chrome", return_value=mock_driver)

        bot = SafeWorkPDLBot("username", "password", download_path="/tmp/downloads")

        # Mock delle Page Objects interne
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=True)
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="/tmp/p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="/tmp/p2.pdf")
        mocker.patch.object(bot, "_unisci_e_stampa", return_value=True)
        mocker.patch.object(bot, "_handle_session_merge")
        mocker.patch.object(bot, "_safe_remove")

        # 2. Esecuzione
        data = [{"numero_pdl": "566360", "merge_all_session": True}]
        success = bot.execute(data)

        # 3. Verifiche
        assert success is True
        assert bot.status.name == "COMPLETED"

        # Verifica che la catena di chiamata sia corretta
        bot._login.assert_called_once()
        bot._esegui_ricerca_pdl.assert_called_with("566360/C")
        bot._unisci_e_stampa.assert_called()
        bot._handle_session_merge.assert_called_with(data, ANY_LIST := mocker.ANY)

    def test_pdl_flow_with_search_failure(self, mocker):
        """Verifica gestione fallimento ricerca nel flusso integrato."""
        bot = SafeWorkPDLBot("u", "p")
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=False)
        mocker.patch.object(bot, "cleanup")

        data = [{"numero_pdl": "999999"}]
        success = bot.execute(data)

        # Dovrebbe finire con successo (True) perché il bot conta i PDL mancanti come 'gestiti'
        # ma success_count sarà 0. In SafeWorkPDLBot.run() ritorna success_count == total.
        # Se la ricerca fallisce, ritorna False (comportamento attuale di run).
        assert success is False
        assert bot.status.name == "ERROR"
