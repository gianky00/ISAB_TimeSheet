"""Test unitari per AutopilotScheduler."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.core.autopilot.scheduler import AutopilotScheduler


@pytest.fixture
def scheduler() -> AutopilotScheduler:
    """Fixture per creare un'istanza di AutopilotScheduler."""
    return AutopilotScheduler()


def test_scheduler_signals_emission(scheduler: AutopilotScheduler) -> None:
    """Verifica che i segnali vengano emessi correttamente all'orario giusto."""
    # Configurazione fittizia per far scattare tutti i bot e report
    mock_config = {
        "timbrature_autopilot_time": "09:00",
        "timbrature_autopilot_enabled": True,
        "scarico_oda_generale_autopilot_time": "09:00",
        "scarico_oda_generale_autopilot_enabled": True,
        "ricerca_pdl_autopilot_time": "09:00",
        "ricerca_pdl_autopilot_enabled": True,
        "report_email_autopilot_time": "09:00",
        "report_email_autopilot_enabled": True,
        "certificati_autopilot_time": "09:00",
        "certificati_autopilot_enabled": True,
    }

    # Mock del config_manager.load_config
    with patch("src.core.config_manager.load_config", return_value=mock_config):
        # Mock di datetime per restituire le 09:00:02 (così scatta il log ed è l'orario esatto)
        mock_now = datetime(2026, 5, 22, 9, 0, 2)
        with patch("src.core.autopilot.scheduler.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

            # Collegamento dei segnali a mock slot
            bot_mock = MagicMock()
            report_mock = MagicMock()
            cert_mock = MagicMock()

            scheduler.bot_triggered.connect(bot_mock)
            scheduler.report_triggered.connect(report_mock)
            scheduler.certificati_triggered.connect(cert_mock)

            # Esecuzione del controllo schedulato
            scheduler.check_scheduled_tasks()

            # Verifichiamo che i bot standard siano scattati
            assert bot_mock.call_count == 3
            bot_mock.assert_any_call("timbrature", "timbrature_bot_panel", "portale_fornitori")
            bot_mock.assert_any_call("scarico_oda_generale", "dettagli_panel", "portale_fornitori")
            bot_mock.assert_any_call("ricerca_pdl", "pdl_search_panel", "safework")

            # Verifichiamo che report e certificati siano scattati
            report_mock.assert_called_once_with(mock_config)
            cert_mock.assert_called_once_with(mock_config)


def test_scheduler_disabled_tasks(scheduler: AutopilotScheduler) -> None:
    """Verifica che nessun segnale venga emesso se le pianificazioni sono disabilitate."""
    mock_config = {
        "timbrature_autopilot_time": "09:00",
        "timbrature_autopilot_enabled": False,
        "scarico_oda_generale_autopilot_time": "09:00",
        "scarico_oda_generale_autopilot_enabled": False,
        "ricerca_pdl_autopilot_time": "09:00",
        "ricerca_pdl_autopilot_enabled": False,
        "report_email_autopilot_time": "09:00",
        "report_email_autopilot_enabled": False,
        "certificati_autopilot_time": "09:00",
        "certificati_autopilot_enabled": False,
    }

    with patch("src.core.config_manager.load_config", return_value=mock_config):
        mock_now = datetime(2026, 5, 22, 9, 0, 0)
        with patch("src.core.autopilot.scheduler.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_now

            bot_mock = MagicMock()
            report_mock = MagicMock()
            cert_mock = MagicMock()

            scheduler.bot_triggered.connect(bot_mock)
            scheduler.report_triggered.connect(report_mock)
            scheduler.certificati_triggered.connect(cert_mock)

            scheduler.check_scheduled_tasks()

            bot_mock.assert_not_called()
            report_mock.assert_not_called()
            cert_mock.assert_not_called()
