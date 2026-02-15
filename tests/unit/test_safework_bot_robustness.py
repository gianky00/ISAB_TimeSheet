"""
Tests per la logica di robustezza di SafeWorkPDLBot.
Verifica la gestione di popup, pulizia file e strategie di espansione.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from selenium.webdriver.common.by import By

from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLBotRobustness:
    @pytest.fixture
    def bot(self, mocker):
        bot = SafeWorkPDLBot("user", "pass", download_path="/tmp/downloads")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        # Mock filesystem ops to avoid real errors
        mocker.patch("src.bots.safework.pdl.bot.Path.rename")
        mocker.patch("src.bots.safework.pdl.bot.Path.unlink")
        mocker.patch("src.bots.safework.pdl.bot.Path.exists", return_value=True)
        return bot

    def test_preventive_cleanup_part1(self, bot, mocker):
        """Verifica che il bot elimini il file prima dello scarico (Parte 1)."""
        mock_remove = mocker.patch.object(bot, "_safe_remove")
        mocker.patch("src.bots.base.wait_helpers.poll_for_new_file", return_value="/tmp/new.pdf")
        mocker.patch.object(bot, "_clean_pdf")
        mocker.patch.object(bot, "_attendi_scomparsa_overlay")

        # Simula click riusciti
        bot.wait.until.return_value = MagicMock()

        bot._scarica_parte_prima("566360/C")

        # Deve aver cercato di rimuovere 566360C.pdf
        expected_path = str(Path("/tmp/downloads/566360C.pdf"))
        mock_remove.assert_any_call(expected_path)

    def test_preventive_cleanup_part2(self, bot, mocker):
        """Verifica che il bot elimini ReportPdLRinnovi.pdf prima dello scarico."""
        mock_remove = mocker.patch.object(bot, "_safe_remove")
        mocker.patch("src.bots.base.wait_helpers.poll_for_new_file", return_value="/tmp/new.pdf")
        mocker.patch.object(bot, "_espandi_parte_seconda", return_value=True)
        mocker.patch.object(bot, "_attendi_scomparsa_overlay")

        bot.wait.until.return_value = MagicMock()

        bot._scarica_parte_seconda("123456/S")

        expected_path = str(Path("/tmp/downloads/ReportPdLRinnovi.pdf"))
        mock_remove.assert_any_call(expected_path)

    def test_espandi_parte_seconda_strategies(self, bot):
        """Verifica che il bot provi diverse strategie per aprire la parte seconda."""
        # Simula elemento non visibile all'inizio
        mock_el_hidden = MagicMock()
        mock_el_hidden.is_displayed.return_value = False
        bot.driver.find_element.return_value = mock_el_hidden

        # Strategia 1 (ID) fallisce, Strategia 2 (XPATH) fallisce, Strategia 3 (IDTXT) riesce
        # find_element viene chiamato molte volte:
        # 1. check visibility (ID lblPAFoglio) -> False
        # 2. click Strategia 1 (ID lblTitoloParteSeconda) -> Exception
        # 3. click Strategia 2 (XPATH) -> Exception
        # 4. click Strategia 3 (CSS idtxt) -> Success

        def find_side_effect(by, value):
            if value == "lblPAFoglio":
                return mock_el_hidden
            if value == "lblTitoloParteSeconda":
                raise Exception("ID not found")
            if "PARTE SECONDA" in value:
                raise Exception("XPATH not found")
            if "2E20B56F" in value:
                return MagicMock()  # Successo click
            return MagicMock()

        bot.driver.find_element.side_effect = find_side_effect

        success = bot._espandi_parte_seconda()
        assert success is True
        # Verifichiamo che abbia provato a cliccare l'idtxt
        bot.driver.find_element.assert_any_call(By.CSS_SELECTOR, "span[idtxt='2E20B56F']")

    def test_gestisci_alert_ricerca_resilience(self, bot):
        """Verifica che il bot chiuda l'alert e attenda il caricamento."""
        mock_ok_btn = MagicMock()
        mock_ok_btn.is_displayed.return_value = True
        bot.driver.find_element.return_value = mock_ok_btn

        with patch("src.bots.safework.pdl.bot.WebDriverWait") as mock_wait_class:
            # Mock per l'invisibility del modal
            mock_wait_instance = mock_wait_class.return_value

            res = bot._gestisci_alert_ricerca()

            assert res is True
            mock_ok_btn.click.assert_called_once()
            # Deve aver atteso la scomparsa del modal
            assert mock_wait_instance.until.called

    def test_run_with_handle_session_merge_integration(self, bot, mocker):
        """Verifica che il merge sessione venga chiamato con i percorsi corretti."""
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=True)
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="p2.pdf")
        mocker.patch.object(
            bot,
            "_unisci_e_stampa",
            side_effect=lambda num, p1, p2, item, paths: paths.append("merged.pdf") or True,
        )
        mock_session_merge = mocker.patch.object(bot, "_handle_session_merge")
        mocker.patch.object(bot, "_check_stop")

        data = [{"pdl_number": "123", "merge_all_session": True}]
        bot.run(data)

        # Deve aver chiamato il merge sessione passandogli "merged.pdf"
        mock_session_merge.assert_called_with(data, ["merged.pdf"])
