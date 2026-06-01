"""Unit tests for ProgrammazioneTab."""

from unittest.mock import MagicMock

import pytest

from src.gui.panels.pdl.programmazione_tab import ProgrammazioneTab


@pytest.fixture
def mock_pdl_service(mocker):
    mocker.patch("src.core.pdl.pdl_service.PDLService.get_unique_requesters", return_value=["REQ1", "REQ2"])

    # Mock data con la chiave 'programmazione' richiesta dalla tabella
    # Ogni entry in programmazione è un dict con 'tcl' e 'tgo' (bool)
    results = [
        {
            "richiedente": "REQ1",
            "area": "Area 1",
            "pdl": "123",
            "descrizione": "D1",
            "programmazione": [{"tcl": True, "tgo": False} for _ in range(7)],
        },
        {
            "richiedente": "REQ2",
            "area": "Area 2",
            "pdl": "456",
            "descrizione": "D2",
            "programmazione": [{"tcl": False, "tgo": True} for _ in range(7)],
        },
    ]
    mocker.patch("src.core.pdl.pdl_service.PDLService.get_programming_results_by_week", return_value=results)
    return mocker


@pytest.fixture
def mock_period_manager(mocker):
    mocker.patch(
        "src.core.pdl.period_manager.PDLPeriodManager.get_week_range",
        return_value=("01.01.2026", "07.01.2026", MagicMock()),
    )
    mocker.patch(
        "src.core.pdl.period_manager.PDLPeriodManager.get_table_headers",
        return_value=["H1", "H2", "H3", "H4", "H5", "D1", "D2", "D3", "D4", "D5", "D6", "D7"],
    )
    return mocker


class TestProgrammazioneTab:
    """Test suite per ProgrammazioneTab."""

    def test_initialization(self, qtbot, mock_pdl_service, mock_period_manager, mocker):
        """Verifica lbl'inizializzazione del tab."""
        mocker.patch("src.core.config_manager.get_config_value", return_value=[])

        widget = ProgrammazioneTab()
        qtbot.addWidget(widget)

        assert widget.week_selector.count() == 2
        assert widget.req_filter.items == ["REQ1", "REQ2"]
        assert len(widget.last_results) == 2
        assert len(widget.tables) > 0

    def test_on_week_changed(self, qtbot, mock_pdl_service, mock_period_manager, mocker):
        """Verifica il rinfresco al cambio settimana."""
        widget = ProgrammazioneTab()
        qtbot.addWidget(widget)

        mock_load = mocker.patch.object(widget, "_load_persisted_data")

        widget.week_selector.setCurrentIndex(1)
        assert mock_load.called

    def test_on_group_mode_changed(self, qtbot, mock_pdl_service, mock_period_manager, mocker):
        """Verifica il raggruppamento delle tabelle."""
        widget = ProgrammazioneTab()
        qtbot.addWidget(widget)

        widget.group_selector.setCurrentText("Tabella Unica")
        assert widget.tables_layout.count() >= 2

        widget.group_selector.setCurrentText("Area")
        assert len(widget.tables) == 2

    def test_apply_filters(self, qtbot, mock_pdl_service, mock_period_manager):
        """Verifica lbl'applicazione dei filtri sulla visibilità delle righe."""
        widget = ProgrammazioneTab()
        qtbot.addWidget(widget)

        # Filtriamo per REQ1
        widget.view_filter.selected = ["REQ1"]
        widget._apply_filters()

        table = widget.tables[0]
        # In Tabella Unica, row 0 è REQ1, row 1 è REQ2
        assert not table.isRowHidden(0)
        assert table.isRowHidden(1)

    def test_on_run_clicked_no_creds(self, qtbot, mock_pdl_service, mock_period_manager, mocker):
        """Verifica errore se mancano credenziali."""
        widget = ProgrammazioneTab()
        qtbot.addWidget(widget)

        mocker.patch.object(widget, "get_safework_credentials", return_value=("", "", ""))
        mock_toast = mocker.patch("src.gui.widgets.toast.ToastManager.show")

        widget._on_run_clicked()
        assert mock_toast.called
        assert "credenziali" in mock_toast.call_args[0][0].lower()

    def test_on_run_clicked_start(self, qtbot, mock_pdl_service, mock_period_manager, mocker):
        """Verifica lbl'avvio del bot worker."""
        widget = ProgrammazioneTab()
        qtbot.addWidget(widget)

        mocker.patch.object(widget, "get_safework_credentials", return_value=("u", "p", "type"))
        widget.req_filter.selected = ["REQ1"]

        mock_worker_cls = mocker.patch("src.gui.panels.pdl.programmazione_tab.BotWorker")
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker
        mocker.patch("src.gui.panels.pdl.programmazione_tab.SafeWorkProgrammazioneBot")

        widget._on_run_clicked()

        assert mock_worker_cls.called
        assert mock_worker.start.called
        assert not widget.btn_run.isEnabled()

    def test_on_worker_finished_success(self, qtbot, mock_pdl_service, mock_period_manager, mocker):
        """Verifica salvataggio risultati al termine."""
        widget = ProgrammazioneTab()
        qtbot.addWidget(widget)

        mock_save = mocker.patch("src.core.pdl.pdl_service.PDLService.save_programming_results")

        widget.worker = MagicMock()
        widget.worker.bot = MagicMock()
        widget.worker.bot.results = [{"pdl": "X"}]

        widget._on_worker_finished(True)

        assert mock_save.called
        assert widget.btn_run.isEnabled()
