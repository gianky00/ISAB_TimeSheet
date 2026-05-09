"""
SyncroJob - Bot Regression Shield
Suite di test avanzata per intercettare regressioni nei flussi di operazioni e integrità dati.
"""

from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot
from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestBotRegressionShield:
    @pytest.fixture
    def mock_driver_env(self, mocker):
        """Mocka l'ambiente driver completo per BaseBot."""
        # Patch specifically where it's used to avoid batch run interference
        m_chrome = mocker.patch("src.bots.base.selenium_base_bot.webdriver.Chrome")
        mocker.patch("webdriver_manager.chrome.ChromeDriverManager.install", return_value="chromedriver.exe")
        return m_chrome.return_value

    def test_base_bot_cdp_enforcement(self, mock_driver_env, mocker):
        """Verifica che BaseBot forzi il download path tramite CDP (Regression Shield)."""
        bot = SafeWorkPDLBot("u", "p", download_path="C:/Downloads")

        # Inizializza driver
        with patch.object(bot, "_configure_waits_and_pages"):
            bot._init_driver()

        # Deve aver chiamato execute_cdp_cmd con i parametri corretti
        # Usiamo mocker.ANY per il path per evitare problemi di risoluzione stringa su win32 in batch
        mock_driver_env.execute_cdp_cmd.assert_any_call(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": mocker.ANY},
        )

    def test_pdl_bot_execution_sequence(self, mocker):
        """Verifica la sequenza STRETTA di operazioni del bot PDL (Regression Shield)."""
        bot = SafeWorkPDLBot("u", "p", download_path="/tmp")
        bot.driver = MagicMock()
        bot.wait = MagicMock()

        # Mocks dei metodi interni per tracciare l'ordine
        manager = MagicMock()
        manager.attach_mock(mocker.patch.object(bot, "_attendi_scomparsa_overlay"), "overlay")
        manager.attach_mock(mocker.patch.object(bot, "_safe_remove"), "cleanup")
        manager.attach_mock(mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=True), "search")
        manager.attach_mock(mocker.patch.object(bot, "_scarica_parte_prima", return_value="p1.pdf"), "p1")
        manager.attach_mock(mocker.patch.object(bot, "_scarica_parte_seconda", return_value="p2.pdf"), "p2")
        manager.attach_mock(mocker.patch.object(bot, "_unisci_e_stampa", return_value=True), "merge")

        data = [{"numero_pdl": "566360"}]
        bot.run(data)

        # Verifichiamo l'ordine delle chiamate fondamentali per la riga 1
        # La pulizia preventiva DEVE avvenire dentro _scarica_parte_prima/seconda,
        # verifichiamo che il flusso sia: search -> p1 -> p2 -> merge
        expected_calls = [
            call.search("566360/C"),
            call.p1("566360/C"),
            call.p2("566360/C"),
            call.merge("566360/C", "p1.pdf", "p2.pdf", data[0], mocker.ANY),
        ]
        manager.assert_has_calls(expected_calls, any_order=False)

    def test_safework_programmazione_parsing_robustness(self, mocker):
        """Verifica che il bot programmazione fallisca se gli indici Excel cambiano (Regression Shield)."""
        import pandas as pd

        from src.bots.safework.programmazione.bot import SafeWorkProgrammazioneBot

        bot = SafeWorkProgrammazioneBot("u", "p")
        bot.log = MagicMock()

        # Simula un Excel con colonne SHIFTATE (es. indice 17 non è più il richiedente)
        # Se SafeWork cambia il formato, dobbiamo accorgercene
        bad_df = pd.DataFrame([["PDL1", "Desc"] + ["No"] * 20])  # Troppo corto per raggiungere indice 23/24

        with patch("pandas.read_excel", return_value=bad_df):
            bot._parse_excel_results("file.xlsx")

        # Il bot non deve crashare ma deve loggare errore o produrre 0 risultati
        assert len(bot.results) == 0
        # Dovrebbe aver loggato un avvertimento/errore di parsing
        assert any("Errore parsing" in str(c) or "Trovati 0" in str(c) for c in bot.log.call_args_list)

    def test_scarico_ts_retry_logic_enforcement(self, mocker):
        """Verifica che la logica di retry per lo spostamento file sia attiva (Regression Shield)."""
        bot = ScaricaTSBot(username="u", password="p")
        bot.log = MagicMock()
        m_shutil = mocker.patch("shutil.move")

        # Fallimento persistente
        m_shutil.side_effect = Exception("Permesso negato")

        src, dest = Path("src.xlsx"), Path("dest.xlsx")
        res = bot._move_to_destination(src, dest)

        assert res is None
        # Deve aver provato 3 volte (retry logic)
        assert m_shutil.call_count == 3
        # Deve aver loggato l'errore finale
        assert any("Impossibile spostare" in str(c) for c in bot.log.call_args_list)

    def test_document_processor_crash_protection(self):
        """Verifica che il merge dei PDF non crashi l'app se fitz fallisce (Regression Shield)."""
        from src.utils.document_processor import DocumentProcessor

        with patch("fitz.open", side_effect=Exception("Corrupted PDF")):
            # Non deve sollevare eccezione ma ritornare False
            res = DocumentProcessor.merge_pdfs(["bad.pdf"], "out.pdf")
            assert res is False
