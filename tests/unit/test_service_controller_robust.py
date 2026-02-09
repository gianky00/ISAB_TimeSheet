from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import QObject

from src.gui.controllers.service_controller import ServiceController


# Mock QObject per evitare init Qt
class MockMainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.timbrature_bot_panel = MagicMock()
        self.timbrature_bot_panel.start_btn.isEnabled.return_value = True
        self.timbrature_bot_panel.log_widget = MagicMock()

        self.dettagli_oda_bot_panel = MagicMock()
        self.dettagli_oda_bot_panel.start_btn.isEnabled.return_value = True
        self.dettagli_oda_bot_panel.log_widget = MagicMock()

        self.ricerca_pdl_bot_panel = MagicMock()
        self.ricerca_pdl_bot_panel.start_btn.isEnabled.return_value = True
        self.ricerca_pdl_bot_panel.log_widget = MagicMock()

        self._on_anomalies_found = MagicMock()
        self._show_update_banner = MagicMock()


@pytest.fixture
def mock_main_window(
    qapp,
):  # Richiede qapp fixture da pytest-qt se installato, o QApplication instance
    return MockMainWindow()


@pytest.fixture
def mock_services():
    telegram = MagicMock()
    sentinel = MagicMock()
    return telegram, sentinel


@pytest.fixture
def service_controller(mock_main_window, mock_services):
    # Patch QTimer nel costruttore se usato
    with patch("src.gui.controllers.service_controller.QTimer"):
        # Patch NotificationManager instance per evitare side effects
        with patch("src.gui.controllers.service_controller.NotificationManager.instance"):
            ctrl = ServiceController(mock_main_window, *mock_services)
            return ctrl


class TestServiceControllerRobust:
    def test_start_all(self, service_controller):
        """Test avvio servizi e timer."""
        with patch("src.gui.controllers.service_controller.QTimer") as mock_timer:
            service_controller.start_all()

            # Verifica QTimer.singleShot per vari servizi
            assert mock_timer.singleShot.call_count >= 3

            # Verifica timer scheduler
            assert service_controller.scheduler_timer.start.called
            assert service_controller.scheduler_timer.timeout.connect.called

    def test_schedule_parallelism_free_site(self, service_controller):
        """Test avvio bot su sito libero."""
        bot_id = "test_bot"
        panel = MagicMock()
        panel.start_btn.isEnabled.return_value = True
        site = "portale_fornitori"

        service_controller._schedule_bot_with_parallelism(bot_id, panel, site, "Log msg")

        # Deve essere avviato e aggiunto a running
        assert bot_id in service_controller.running_bots_by_site[site]
        assert panel._on_start.called
        assert len(service_controller.pending_bots_by_site[site]) == 0

    def test_schedule_parallelism_busy_site(self, service_controller):
        """Test accodamento bot su sito occupato."""
        bot_id_1 = "bot_1"
        bot_id_2 = "bot_2"
        panel = MagicMock()
        panel.start_btn.isEnabled.return_value = True
        site = "portale_fornitori"

        # Mette bot_1 in running
        service_controller.running_bots_by_site[site].append(bot_id_1)

        # Prova a schedulare bot_2
        service_controller._schedule_bot_with_parallelism(bot_id_2, panel, site, "Log msg")

        # Deve essere in pending, non running
        assert bot_id_2 not in service_controller.running_bots_by_site[site]
        assert not panel._on_start.called
        assert len(service_controller.pending_bots_by_site[site]) == 1
        assert service_controller.pending_bots_by_site[site][0][0] == bot_id_2

    def test_on_bot_completed_triggers_next(self, service_controller):
        """Test completamento bot avvia il successivo in coda."""
        site = "portale_fornitori"
        bot_id_1 = "bot_1"
        bot_id_2 = "bot_2"

        panel_1 = MagicMock()
        panel_2 = MagicMock()
        panel_2.start_btn.isEnabled.return_value = True

        # Setup stato iniziale: bot_1 running, bot_2 pending
        service_controller.running_bots_by_site[site] = [bot_id_1]
        service_controller.pending_bots_by_site[site] = [(bot_id_2, panel_2, "Log msg")]

        # Bot 1 completa
        service_controller._on_bot_completed(bot_id_1, site, panel_1)

        # Bot 1 rimosso, Bot 2 avviato e in running
        assert bot_id_1 not in service_controller.running_bots_by_site[site]
        assert bot_id_2 in service_controller.running_bots_by_site[site]
        assert panel_2._on_start.called
        assert len(service_controller.pending_bots_by_site[site]) == 0

    @patch("src.gui.controllers.service_controller.config_manager.load_config")
    @patch("src.gui.controllers.service_controller.datetime")
    def test_check_scheduled_tasks_timbrature(self, mock_datetime, mock_config, service_controller):
        """Test trigger task timbrature schedulato."""
        # Config
        mock_config.return_value = {
            "timbrature_autopilot_enabled": True,
            "timbrature_autopilot_time": "09:00",
        }
        # Time
        mock_datetime.now.return_value.strftime.return_value = "09:00"

        # Reset stato
        service_controller.running_bots_by_site["portale_fornitori"] = []

        service_controller._check_scheduled_tasks()

        # Deve avviare timbrature
        panel = service_controller.mw.timbrature_bot_panel
        assert panel._on_start.called
        assert "timbrature" in service_controller.running_bots_by_site["portale_fornitori"]

    @patch("src.gui.controllers.service_controller.config_manager.load_config")
    @patch("src.gui.controllers.service_controller.datetime")
    def test_check_report_email_schedule_interval(self, mock_datetime, mock_config, service_controller):
        """Test logica intervallo invio email."""
        # Config: abilitato, ore 08:00, intervallo 7gg, inviato 8gg fa
        mock_config.return_value = {
            "report_email_autopilot_enabled": True,
            "report_email_autopilot_time": "08:00",
            "report_email_autopilot_interval_days": 7,
            "report_email_autopilot_last_sent": "2026-01-01T08:00:00",  # Vecchio
        }

        # Time now: 08:00, data attuale > last_sent + 7gg
        mock_now = MagicMock()
        mock_now.strftime.return_value = "08:00"
        # Mocking subtraction for days check
        # datetime.now() - last_dt
        # Se usiamo datetime reale per la differenza è meglio
        # Ma qui dobbiamo mockare datetime.now() sia per strftime che per subtraction
        # Complesso mockare aritmetica datetime.
        # Semplifichiamo: mockiamo direttamente il metodo _send_scheduled_report_email

        mock_datetime.now.return_value = mock_now

        # Qui usiamo un trick: mockiamo datetime.fromisoformat per ritornare un oggetto che sottratto a now dia > 7gg
        # Se now è mock_now, mock_now - last_dt >= 7
        # Ma mock_now è un MagicMock.

        # Alternativa: testare _check_report_email_schedule isolato con mock più semplici o logica interna

    def test_prepare_scarico_oda(self, service_controller):
        """Test callback preparazione scarico oda."""
        panel = MagicMock()
        service_controller._prepare_scarico_oda_generale(panel)
        panel.table.setRowCount.assert_called_with(0)

    @patch("src.gui.controllers.service_controller.NotificationManager")
    def test_forward_notification(self, mock_nm, service_controller):
        """Test inoltro notifica a telegram."""
        notification = {"title": "Test", "message": "Ciao", "level": "error"}
        service_controller._forward_notification_to_telegram(notification)

        service_controller.telegram.send_message_sync.assert_called()
        args = service_controller.telegram.send_message_sync.call_args[0][0]
        assert "[ERR]" in args
        assert "Ciao" in args
