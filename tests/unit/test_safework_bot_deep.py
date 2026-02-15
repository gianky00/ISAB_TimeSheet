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
        # Mock bot for initialization
        bot = MagicMock(spec=SafeWorkPDLBot)
        bot._sanitizza_pdl_number = SafeWorkPDLBot._sanitizza_pdl_number.__get__(bot, SafeWorkPDLBot)

        assert bot._sanitizza_pdl_number("123456") == "123456/S"
        assert bot._sanitizza_pdl_number("567077") == "567077/C"
        assert bot._sanitizza_pdl_number("323630/S") == "323630/S"
        assert bot._sanitizza_pdl_number("messina") == "MESSINA"

    def test_run_pdl_logic_basic(self, mocker):
        """Verifica la logica principale di esecuzione del bot PDL."""
        # Setup instance
        bot = MagicMock(spec=SafeWorkPDLBot)
        bot.download_path = "/tmp"
        bot.log = MagicMock()
        bot._check_stop = MagicMock()
        bot.downloaded_files = []
        bot.progress_callback = None
        bot.wait = MagicMock()

        # Bind real run method
        bot.run = SafeWorkPDLBot.run.__get__(bot, SafeWorkPDLBot)
        bot._sanitizza_pdl_number = SafeWorkPDLBot._sanitizza_pdl_number.__get__(bot, SafeWorkPDLBot)
        bot._handle_session_merge = SafeWorkPDLBot._handle_session_merge.__get__(bot, SafeWorkPDLBot)
        bot._safe_remove = MagicMock()

        # Mock internal download/merge methods
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=True)
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="/tmp/p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="/tmp/p2.pdf")
        mocker.patch.object(bot, "_unisci_e_stampa", return_value=True)
        mock_merge = mocker.patch.object(bot, "_handle_session_merge")

        data = [{"pdl_number": "123456", "merge_all_session": True}]
        result = bot.run(data)

        assert result is True
        bot._esegui_ricerca_pdl.assert_called_with("123456/S")
        assert mock_merge.called
