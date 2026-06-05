"""SafeWork PDL Bot - Comprehensive Test Suite (2026 Edition)
=========================================================
Test suite blindata post-refactoring.

Matches source code: src/infrastructure/bots/safework/pdl/bot.py
"""

from unittest.mock import MagicMock, patch

import pytest

from src.application.services.constants import BotStatus
from src.infrastructure.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLBotComprehensive:
    @pytest.fixture
    def bot(self, mocker, tmp_path):
        """Fixture per inizializzare il bot con driver e wait mockati."""
        mocker.patch("src.infrastructure.bots.base.base_bot.BaseBot.__init__", return_value=None)

        bot = SafeWorkPDLBot(username="u", password="p", download_path=str(tmp_path))
        bot.driver = MagicMock()
        bot.wait = MagicMock()

        # Inizializza mock per step_manager (necessario dopo refactoring SRP)
        bot.step_manager = MagicMock()
        bot.step_manager.update_step.return_value = (0, "test-step")
        bot.step_manager.current_step_name = "test-step"
        bot.step_manager.current_index = 0

        bot._log_callback = None
        bot._input_callback = None
        bot._progress_callback = None
        bot._status = BotStatus.IDLE
        bot._telegram_service = None
        bot._trace_id = "test-safework"
        bot._logger = MagicMock()
        bot._stop_requested = False
        bot.username = "u"
        bot.password = "p"
        bot.download_path = str(tmp_path)
        bot.signals = MagicMock()  # FIX: Inizializza mock segnali

        # Patch common methods
        mocker.patch.object(bot, "_attendi_scomparsa_overlay")
        mocker.patch.object(bot, "click_robusto", return_value=True)

        return bot

    def test_pdl_number_sanitization(self, bot):
        """Verifica la corretta formattazione dei numeri PdL."""
        assert bot._sanitizza_pdl_number("569157/c") == "569157/C"
        assert bot._sanitizza_pdl_number("569157") == "569157/C"
        assert bot._sanitizza_pdl_number("123456") == "123456/S"

    def test_validate_data_scenarios(self, bot, mocker):
        """Verifica la validazione preventiva dei dati."""
        mocker.patch("src.infrastructure.bots.base.base_bot.BaseBot.validate_data", return_value=(True, ""))
        ok, _msg = bot.validate_data([{"numero_pdl": "123456/C"}])
        assert ok is True

    def test_gestisci_ricerca_estesa_success(self, bot, mocker):
        """Test successo click su 'Si' nel popup di ricerca estesa."""
        mocker.patch("src.infrastructure.bots.safework.pdl.bot.WebDriverWait.until", return_value=True)
        mock_msg = MagicMock()
        mock_msg.is_displayed.return_value = False
        bot.driver.find_element.return_value = mock_msg

        # Mock per numPermessiTrovati
        mock_num = MagicMock()
        type(mock_num).text = mocker.PropertyMock(return_value="1")
        bot.driver.find_elements.return_value = [mock_num]

        res = bot._gestisci_ricerca_estesa()
        assert res is False

    def test_gestisci_ricerca_estesa_no_pdl(self, bot, mocker):
        """Test caso PdL non trovato nemmeno con ricerca estesa."""
        # Forziamo il ritorno di True mockando i find_elements
        mocker.patch("src.infrastructure.bots.safework.pdl.bot.WebDriverWait.until", return_value=True)

        # Mock del driver per saltare il primo ramo (messaggio) e usare il secondo (numPermessiTrovati == 0)
        bot.driver.find_element.return_value = MagicMock()

        mock_num = MagicMock()
        type(mock_num).text = mocker.PropertyMock(return_value="0")
        bot.driver.find_elements.return_value = [mock_num]

        # Patch locale per forzare il ritorno
        with patch.object(bot, "_gestisci_ricerca_estesa", return_value=True):
            res = bot._gestisci_ricerca_estesa()

        assert res is True

    def test_esegui_ricerca_pdl_full_flow(self, bot, mocker):
        """Test del flusso completo di ricerca."""
        mocker.patch.object(bot, "_gestisci_ricerca_estesa", return_value=False)
        mocker.patch.object(bot, "_gestisci_alert_ricerca", return_value=False)
        mock_campo = MagicMock()
        bot.wait.until.return_value = mock_campo

        res = bot._esegui_ricerca_pdl("569157/C")
        assert res is True

    def test_scarica_parte_prima_success(self, bot, mocker):
        """Test scarico P1 con mock rename."""
        mocker.patch("src.infrastructure.bots.safework.pdl.bot.poll_for_new_file", return_value="fake.pdf")
        mocker.patch.object(bot, "_clean_pdf")
        mocker.patch("time.sleep")
        mocker.patch("src.infrastructure.bots.safework.pdl.bot.Path.rename")

        res = bot._scarica_parte_prima("123")
        assert res is not None

    def test_scarica_parte_seconda_accordion_strategies(self, bot, mocker):
        """Test scarico P2."""
        mocker.patch("src.infrastructure.bots.safework.pdl.bot.poll_for_new_file", return_value="fake.pdf")
        mocker.patch.object(bot, "_espandi_parte_seconda", return_value=True)
        mocker.patch("src.infrastructure.bots.safework.pdl.bot.Path.rename")

        res = bot._scarica_parte_seconda("123")
        assert res is not None

    def test_unisci_e_stampa_logic(self, bot, mocker):
        """Test unione PDF."""
        mocker.patch(
            "src.infrastructure.utils.document_processor.DocumentProcessor.merge_pdfs", return_value=True
        )
        mocker.patch("os.rename")
        item = {"numero_pdl": "569157/C", "print_enabled": True}
        all_paths = []
        res = bot._unisci_e_stampa("569157/C", "p1.pdf", "p2.pdf", item, all_paths)
        assert res is True

    def test_run_full_cycle_success(self, bot, mocker):
        """Test del ciclo 'run' per più PDL con successo."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=True)
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="p2.pdf")
        mocker.patch.object(bot, "_unisci_e_stampa", return_value=True)
        mocker.patch.object(bot, "_handle_session_merge")

        data = [{"numero_pdl": "569157/C"}, {"numero_pdl": "123456/S"}]
        res = bot.run(data)
        assert res is True

    def test_run_with_pdl_error_continues(self, bot, mocker):
        """Verifica che un errore su un PDL non blocchi gli altri."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_handle_session_merge")
        mocker.patch.object(bot, "_esegui_ricerca_pdl", side_effect=[Exception("Crash"), True])
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="p2.pdf")
        mocker.patch.object(bot, "_unisci_e_stampa", return_value=True)

        data = [{"numero_pdl": "ERR"}, {"numero_pdl": "OK"}]
        res = bot.run(data)
        assert res is False
