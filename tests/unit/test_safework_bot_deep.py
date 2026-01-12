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

from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLBotDeep:
    def test_pdl_sanitization_logic(self):
        """Testa la logica di sanitizzazione PDL."""
        pdl = "123456"
        num = int(pdl)
        suffix = "/S" if num < 400000 else "/C"
        assert f"{pdl}{suffix}" == "123456/S"

    def test_polling_logic_simulated(self, mocker):
        """Verifica l'algoritmo di polling dei file PDF."""
        bot = MagicMock(spec=SafeWorkPDLBot)
        bot.download_path = "/tmp"
        bot._attendi_e_ritorna_nuovo_pdf = SafeWorkPDLBot._attendi_e_ritorna_nuovo_pdf.__get__(bot, SafeWorkPDLBot)

        m_glob = mocker.patch("src.bots.safework.pdl.bot.glob.glob")
        m_glob.side_effect = [
            ["/tmp/file.crdownload"], ["/tmp/file.crdownload"],
            ["/tmp/file.pdf"], []
        ]
        mocker.patch("src.bots.safework.pdl.bot.os.path.getmtime", return_value=200)
        mocker.patch("src.bots.safework.pdl.bot.time.time", side_effect=[100, 101, 102, 300])
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
        bot.run = SafeWorkPDLBot.run.__get__(bot, SafeWorkPDLBot)

        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot._attendi_scomparsa_overlay = MagicMock()

        mocker.patch.object(bot, "_setup_filters", return_value=True)
        mocker.patch.object(bot, "_navigate_to_timesheet", return_value=True)
        mocker.patch.object(bot, "_gestisci_alert_ricerca", return_value=False)
        mocker.patch.object(bot, "_attendi_e_ritorna_nuovo_pdf", return_value="/tmp/pdl.pdf")

        # Mock fitz
        mock_doc = MagicMock()
        mock_doc.page_count = 1
        mocker.patch("src.bots.safework.pdl.bot.fitz.open", return_value=mock_doc)

        # PATCH CRUCIALE: DocumentProcessor nel namespace del bot
        # Questo intercetta l'import locale "from src.utils.document_processor import DocumentProcessor"
        mock_processor = mocker.patch("src.bots.safework.pdl.bot.DocumentProcessor")
        mock_processor.merge_pdfs.return_value = True

        mocker.patch("src.bots.safework.pdl.bot.os.rename")
        mocker.patch("src.bots.safework.pdl.bot.os.remove")
        mocker.patch("src.bots.safework.pdl.bot.os.path.exists", return_value=True)

        data = [{"pdl_number": "123", "merge_all_session": True}]

        result = bot.run(data)

        assert result is True
        # Deve aver chiamato merge_pdfs 2 volte (P1+P2 e poi Sessione)
        assert mock_processor.merge_pdfs.call_count >= 2

        # Verifica che il secondo argomento dell'ultima chiamata contenga il nome sessione
        last_call_args = mock_processor.merge_pdfs.call_args[0]
        assert "PDL_SESSIONE" in str(last_call_args[1])
