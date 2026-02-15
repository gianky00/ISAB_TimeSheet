"""
Tests for SafeWorkPDLBot.run refactoring.
Aims for high coverage and regression testing without infinite loops.
"""

import os
import sys
from unittest.mock import MagicMock, patch

# Mock preventivo TOTALE prima di importare il bot
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
sys.modules["selenium.webdriver.support.expected_conditions"] = MagicMock()
sys.modules["win32print"] = MagicMock()
sys.modules["win32ui"] = MagicMock()
sys.modules["win32con"] = MagicMock()

import pytest  # noqa: E402

from src.bots.safework.pdl.bot import SafeWorkPDLBot  # noqa: E402


@pytest.fixture(autouse=True)
def mock_waits():
    """Mock globale delle attese per evitare loop infiniti nei test."""
    with (
        patch("src.bots.safework.base.WebDriverWait"),
        patch("src.bots.safework.pdl.bot.WebDriverWait"),
    ):
        yield


@pytest.fixture(autouse=True)
def mock_time_and_sleep():
    """Patch time.sleep per non attendere e time.time per i loop di polling."""
    # Simula il tempo che avanza velocemente per rompere i loop 'while time.time() < scadenza'
    current_time = [1000.0]

    def fast_time():
        current_time[0] += 10.0
        return current_time[0]

    with patch("time.sleep"), patch("time.time", side_effect=fast_time):
        yield


@pytest.fixture(autouse=True)
def mock_settings(tmp_path):
    """Isola i log e i download."""
    with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
        yield


@pytest.fixture
def mock_bot(tmp_path):
    """Crea un'istanza del bot con dipendenze mockate."""
    bot = SafeWorkPDLBot("user", "pass", download_path=str(tmp_path / "downloads"))
    bot.driver = MagicMock()
    bot.wait = MagicMock()
    bot.download_path = str(tmp_path / "downloads")
    os.makedirs(bot.download_path, exist_ok=True)
    return bot


def test_run_success_full_workflow(mock_bot, mocker, tmp_path):
    """Test workflow completo di successo per un PDL."""
    data = [{"pdl_number": "123456", "print_enabled": True, "printer_name": "TestPrinter"}]

    mock_search_field = MagicMock()
    mock_bot.wait.until.return_value = mock_search_field

    mocker.patch.object(mock_bot, "_gestisci_ricerca_estesa", return_value=False)
    mocker.patch.object(mock_bot, "_gestisci_alert_ricerca", return_value=False)
    mocker.patch.object(mock_bot, "_attendi_scomparsa_overlay")
    mocker.patch.object(mock_bot, "_espandi_parte_seconda", return_value=True)

    p1 = tmp_path / "downloads" / "p1.pdf"
    p1.write_bytes(b"p1")
    p2 = tmp_path / "downloads" / "p2.pdf"
    p2.write_bytes(b"p2")

    # Mock download return paths (metodi corretti del bot)
    mocker.patch.object(mock_bot, "_scarica_parte_prima", return_value=str(p1))
    mocker.patch.object(mock_bot, "_scarica_parte_seconda", return_value=str(p2))

    mock_doc = MagicMock()
    mock_doc.page_count = 1
    mocker.patch("src.bots.safework.pdl.bot.fitz.open", return_value=mock_doc)
    m_merge = mocker.patch("src.utils.document_processor.DocumentProcessor.merge_pdfs", return_value=True)
    mocker.patch("src.bots.safework.pdl.bot.print_pdf")

    success = mock_bot.run(data)
    assert success is True
    assert len(mock_bot.downloaded_files) == 1
    assert m_merge.called


def test_run_pdl_not_found(mock_bot, mocker):
    """Test caso PDL non trovato (ricerca estesa fallita)."""
    data = [{"pdl_number": "999999"}]
    # Se la ricerca fallisce, _esegui_ricerca_pdl ritorna False
    mocker.patch.object(mock_bot, "_esegui_ricerca_pdl", return_value=False)

    success = mock_bot.run(data)
    # Se anche solo un PDL fallisce, run() ritorna False (success_count != total)
    assert success is False


def test_run_download_timeout_p1(mock_bot, mocker):
    """Test timeout download Parte 1."""
    data = [{"pdl_number": "123456"}]
    mocker.patch.object(mock_bot, "_gestisci_ricerca_estesa", return_value=False)
    mocker.patch.object(mock_bot, "_gestisci_alert_ricerca", return_value=False)
    mocker.patch.object(mock_bot, "_scarica_parte_prima", return_value=None)

    success = mock_bot.run(data)
    assert success is False
    assert len(mock_bot.downloaded_files) == 0


def test_run_alert_handled(mock_bot, mocker, tmp_path):
    """Test gestione alert durante la ricerca."""
    data = [{"pdl_number": "123456"}]
    mocker.patch.object(mock_bot, "_gestisci_ricerca_estesa", return_value=False)
    mocker.patch.object(mock_bot, "_gestisci_alert_ricerca", return_value=True)
    mocker.patch.object(mock_bot, "_espandi_parte_seconda", return_value=True)

    p1 = tmp_path / "downloads" / "p1.pdf"
    p1.write_bytes(b"p1")
    p2 = tmp_path / "downloads" / "p2.pdf"
    p2.write_bytes(b"p2")
    mocker.patch.object(mock_bot, "_scarica_parte_prima", return_value=str(p1))
    mocker.patch.object(mock_bot, "_scarica_parte_seconda", return_value=str(p2))

    mocker.patch("src.bots.safework.pdl.bot.fitz.open")
    mocker.patch("src.utils.document_processor.DocumentProcessor.merge_pdfs", return_value=True)

    success = mock_bot.run(data)
    assert success is True


def test_run_p2_expand_error(mock_bot, mocker, tmp_path):
    """Test errore apertura Parte Seconda."""
    data = [{"pdl_number": "123456"}]
    mocker.patch.object(mock_bot, "_gestisci_ricerca_estesa", return_value=False)
    mocker.patch.object(mock_bot, "_gestisci_alert_ricerca", return_value=False)
    mocker.patch.object(mock_bot, "_espandi_parte_seconda", return_value=False)

    p1 = tmp_path / "downloads" / "p1.pdf"
    p1.write_bytes(b"p1")
    mocker.patch.object(mock_bot, "_scarica_parte_prima", return_value=str(p1))
    mocker.patch.object(mock_bot, "_scarica_parte_seconda", return_value=None)

    success = mock_bot.run(data)
    assert success is False


def test_run_merge_session_failure(mock_bot, mocker, tmp_path):
    """Test fallimento unione sessione."""
    data = [{"pdl_number": "123456", "merge_all_session": True}]

    p1 = tmp_path / "downloads" / "p1.pdf"
    p1.write_bytes(b"p1")
    p2 = tmp_path / "downloads" / "p2.pdf"
    p2.write_bytes(b"p2")
    mocker.patch.object(mock_bot, "_scarica_parte_prima", return_value=str(p1))
    mocker.patch.object(mock_bot, "_scarica_parte_seconda", return_value=str(p2))

    m_merge = mocker.patch("src.utils.document_processor.DocumentProcessor.merge_pdfs")
    m_merge.side_effect = [True, False]  # Success individual, Fail session

    mocker.patch("src.bots.safework.pdl.bot.fitz.open")
    mocker.patch("os.rename")
    mocker.patch("os.remove")

    success = mock_bot.run(data)
    assert success is True
    assert m_merge.call_count == 2


def test_check_stop_during_loop(mock_bot, mocker):
    """Test interruzione durante il loop."""
    data = [{"pdl_number": "1"}, {"pdl_number": "2"}]

    def side_effect(*args, **kwargs):
        mock_bot.request_stop()
        return False

    mocker.patch.object(mock_bot, "_gestisci_ricerca_estesa", side_effect=side_effect)

    with pytest.raises(InterruptedError):
        mock_bot.run(data)
