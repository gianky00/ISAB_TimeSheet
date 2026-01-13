"""
Baseline tests for ScaricaTSBot.
Ensures high coverage and functional parity before refactoring.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot


@pytest.fixture
def mock_bot(tmp_path):
    """Crea un'istanza del bot con dipendenze mockate."""
    bot = ScaricaTSBot(
        username="test_user",
        password="test_password",
        fornitore="Test Fornitore",
        download_path=str(tmp_path / "dest")
    )
    bot.driver = MagicMock()
    bot.wait = MagicMock()
    bot.long_wait = MagicMock()
    bot.download_path = str(tmp_path / "dest")
    os.makedirs(bot.download_path, exist_ok=True)
    return bot

@pytest.fixture(autouse=True)
def mock_time_and_sleep():
    """Mock time.sleep e time.time per i test."""
    current_time = [1000.0]
    def fast_time():
        current_time[0] += 5.0
        return current_time[0]

    with patch("time.sleep"), \
         patch("time.time", side_effect=fast_time):
        yield

def test_validate_data(mock_bot):
    # Valid data
    assert mock_bot.validate_data([{"numero_oda": "1"}])[0] is True
    # No fornitore
    mock_bot.fornitore = ""
    assert mock_bot.validate_data([{"numero_oda": "1"}])[0] is False
    # Empty data
    mock_bot.fornitore = "F"
    assert mock_bot.validate_data([])[0] is False

def test_run_success_standard(mock_bot, mocker, tmp_path):
    """Test workflow standard senza elaborazione TS."""
    data = [{"numero_oda": "ODA1", "posizione_oda": "10"}]

    mocker.patch.object(mock_bot, "_navigate_to_timesheet", return_value=True)
    mocker.patch.object(mock_bot, "_setup_filters", return_value=True)
    mocker.patch.object(mock_bot, "_attendi_scomparsa_overlay")

    mocker.patch("src.bots.portale_fornitori.scarico_ts.bot.Path.home", return_value=tmp_path)

    final_file = tmp_path / "dest" / "TS_ODA1-10.xlsx"
    mocker.patch.object(mock_bot, "_download_excel", return_value=final_file)

    success = mock_bot.run(data)
    assert success is True
    assert mock_bot._download_excel.called

def test_run_with_elabora_ts(mock_bot, mocker, tmp_path):
    """Test workflow con elaborazione TS (Logica VBA)."""
    data = {"rows": [{"numero_oda": "ODA1"}], "elabora_ts": True}

    mocker.patch.object(mock_bot, "_navigate_to_timesheet", return_value=True)
    mocker.patch.object(mock_bot, "_setup_filters", return_value=True)
    mocker.patch.object(mock_bot, "_attendi_scomparsa_overlay")

    final_file = tmp_path / "downloads" / "TS_ODA1.xlsx"
    mocker.patch.object(mock_bot, "_download_excel", return_value=final_file)

    m_proc = mocker.patch("src.core.timesheet_processor.TimesheetProcessor.process_and_move", return_value=(True, "OK"))

    success = mock_bot.run(data)
    assert success is True
    assert m_proc.called

def test_download_excel_logic(mock_bot, mocker, tmp_path):
    """Test interno di _download_excel."""
    source_dir = tmp_path / "Downloads"
    source_dir.mkdir(parents=True, exist_ok=True)
    dest_dir = tmp_path / "Dest"
    dest_dir.mkdir(parents=True, exist_ok=True)

    mock_bot.elabora_ts = False

    # Simulate download: new file appears
    new_file = source_dir / "new.xlsx"

    def side_effect(*args, **kwargs):
        new_file.write_text("new content")
        return MagicMock()

    mock_bot.wait.until.return_value.click.side_effect = side_effect

    # We need to ensure new_file is detected.
    # The loop checks source_dir.iterdir() - files_before.
    # files_before is empty if we don't create anything before.

    with patch("shutil.move") as m_move:
        res = mock_bot._download_excel(source_dir, dest_dir, "ODA123", "10")
        assert res is not None
        assert m_move.called
        args, _ = m_move.call_args
        assert "TS_ODA123-10.xlsx" in str(args[1])

def test_download_excel_elabora_ts_true(mock_bot, mocker, tmp_path):
    """Test _download_excel quando elabora_ts è True (rinomina solo in temp)."""
    source_dir = tmp_path / "Downloads"
    source_dir.mkdir(parents=True, exist_ok=True)
    dest_dir = tmp_path / "Dest"

    mock_bot.elabora_ts = True

    new_file = source_dir / "downloaded.xlsx"

    def side_effect(*args, **kwargs):
        new_file.write_text("data")
        return MagicMock()

    mock_bot.wait.until.return_value.click.side_effect = side_effect

    with patch("shutil.move") as m_move:
        res = mock_bot._download_excel(source_dir, dest_dir, "ODA", "POS")
        assert res is not None
        # Should move within source_dir
        args, _ = m_move.call_args
        assert str(source_dir) in str(args[1])

def test_navigate_to_timesheet_failure(mock_bot, mocker):
    mock_bot.wait.until.side_effect = Exception("Element not found")
    assert mock_bot._navigate_to_timesheet() is False

def test_setup_filters_failure(mock_bot, mocker):
    mock_bot.wait.until.side_effect = Exception("Filter error")
    assert mock_bot._setup_filters() is False
