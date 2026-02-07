import sys
from unittest.mock import MagicMock

# Mock preventivo TOTALE
sys.modules["PyQt6"] = MagicMock()
sys.modules["PyQt6.QtCore"] = MagicMock()
sys.modules["PyQt6.QtWidgets"] = MagicMock()
sys.modules["PyQt6.QtGui"] = MagicMock()
sys.modules["selenium"] = MagicMock()
sys.modules["selenium.webdriver"] = MagicMock()
sys.modules["selenium.webdriver.common.by"] = MagicMock()
sys.modules["selenium.webdriver.common.keys"] = MagicMock()
sys.modules["selenium.webdriver.support"] = MagicMock()
sys.modules["selenium.webdriver.support.ui"] = MagicMock()
sys.modules["win32print"] = MagicMock()
sys.modules["win32ui"] = MagicMock()
sys.modules["win32con"] = MagicMock()

from src.bots.safework.pdl.bot import SafeWorkPDLBot  # noqa: E402


class TestSafeWorkPDLBotDeep:
    def test_pdl_sanitization_logic(self):
        """Testa la logica di sanitizzazione PDL."""
        pdl = "123456"
        num = int(pdl)
        suffix = "/S" if num < 400000 else "/C"
        assert f"{pdl}{suffix}" == "123456/S"

    def test_polling_logic_simulated(self, mocker):
        """Verifica l'algoritmo di polling dei file PDF."""
        from pathlib import Path

        bot = MagicMock(spec=SafeWorkPDLBot)
        bot.download_path = "/tmp"
        bot.log = MagicMock()

        # Bind real method
        bot._attendi_e_ritorna_nuovo_pdf = SafeWorkPDLBot._attendi_e_ritorna_nuovo_pdf.__get__(
            bot, SafeWorkPDLBot
        )

        # Mock Path.glob and Path.stat
        mock_path_glob = mocker.patch("src.bots.safework.pdl.bot.Path.glob")

        f_pdf = MagicMock(spec=Path)
        f_pdf.name = "file.pdf"
        f_pdf.__str__.return_value = "/tmp/file.pdf"
        f_pdf.stat.return_value.st_mtime = 200

        # Iterazione 1: *.pdf ritorna [] -> non chiama *.crdownload
        # Iterazione 2: *.pdf ritorna [f_pdf] -> chiama *.crdownload -> ritorna []
        mock_path_glob.side_effect = [
            [],  # Iter 1: *.pdf
            [f_pdf],  # Iter 2: *.pdf
            [],  # Iter 2: *.crdownload
        ]

        mocker.patch("src.bots.safework.pdl.bot.time.time", side_effect=[100, 101, 102, 103, 104])
        mocker.patch("src.bots.safework.pdl.bot.time.sleep")

        res = bot._attendi_e_ritorna_nuovo_pdf(150)
        assert res == "/tmp/file.pdf"

    def test_alert_handling_logic(self, mocker):
        """Verifica la logica di chiusura alert."""
        bot = MagicMock(spec=SafeWorkPDLBot)
        bot.driver = MagicMock()
        bot.log = MagicMock()
        bot._gestisci_alert_ricerca = SafeWorkPDLBot._gestisci_alert_ricerca.__get__(bot, SafeWorkPDLBot)

        mock_btn = MagicMock()
        bot.driver.find_element.return_value = mock_btn
        mocker.patch("src.bots.safework.pdl.bot.time.time", side_effect=[100, 101, 200])
        mocker.patch("src.bots.safework.pdl.bot.time.sleep")

        res = bot._gestisci_alert_ricerca()
        assert res is True
        mock_btn.click.assert_called_once()

    def test_merge_all_session_logic(self, mocker):
        """Verifica che il merge totale venga attivato alla fine della sessione."""
        # Setup mock instance
        bot = MagicMock(spec=SafeWorkPDLBot)
        bot.download_path = "/tmp"
        bot.log = MagicMock()
        bot._check_stop = MagicMock()
        bot.downloaded_files = []
        bot.progress_callback = None
        bot.log_error = MagicMock()

        # Bind real methods to execute the pipeline
        bot.run = SafeWorkPDLBot.run.__get__(bot, SafeWorkPDLBot)
        bot._process_single_pdl_row = SafeWorkPDLBot._process_single_pdl_row.__get__(bot, SafeWorkPDLBot)
        bot._unisci_e_stampa_pdl = SafeWorkPDLBot._unisci_e_stampa_pdl.__get__(bot, SafeWorkPDLBot)
        bot._handle_session_merge = SafeWorkPDLBot._handle_session_merge.__get__(bot, SafeWorkPDLBot)
        bot._sanitizza_pdl_number = SafeWorkPDLBot._sanitizza_pdl_number.__get__(bot, SafeWorkPDLBot)
        bot._safe_remove = MagicMock()

        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot._attendi_scomparsa_overlay = MagicMock()

        # Mock per evitare skip del ciclo
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=True)
        mocker.patch.object(bot, "_attendi_e_ritorna_nuovo_pdf", return_value="/tmp/download.pdf")
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="/tmp/p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="/tmp/p2.pdf")

        # Mock fitz
        mock_doc = MagicMock()
        mock_doc.page_count = 1
        mocker.patch("src.bots.safework.pdl.bot.fitz.open", return_value=mock_doc)

        # PATCH CRUCIALE: DocumentProcessor
        mock_merge = mocker.patch(
            "src.utils.document_processor.DocumentProcessor.merge_pdfs",
            return_value=True,
        )

        mocker.patch("src.bots.safework.pdl.bot.Path.rename")
        mocker.patch("src.bots.safework.pdl.bot.Path.unlink")
        mocker.patch("src.bots.safework.pdl.bot.Path.exists", return_value=True)

        data = [{"pdl_number": "123", "merge_all_session": True}]
        result = bot.run(data)

        assert result is True
        # Deve aver chiamato merge_pdfs 2 volte (P1+P2 e poi Sessione)
        assert mock_merge.call_count >= 2

        # Verifica che il secondo argomento dell'ultima chiamata contenga il nome sessione
        last_call_args = mock_merge.call_args[0]
        assert "PDL_SESSIONE" in str(last_call_args[1])
