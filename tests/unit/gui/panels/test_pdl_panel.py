from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtWidgets import QWidget

from src.core.pdl.pdl_controller import PDLController
from src.gui.panels.pdl.pdl_panel import PDLDBPanel


class TestPDLDBPanel:
    @pytest.fixture(autouse=True)
    def mock_sync_worker(self, mocker):
        """Forza il worker PDL ad essere sincrono."""

        def mock_start(instance):
            instance.run()

        mocker.patch("src.gui.workers.pdl_data_worker.PDLDataWorker.start", mock_start)

    @pytest.fixture
    def controller(self):
        c = MagicMock(spec=PDLController)
        c.get_pdl_data.return_value = []
        c.process_master_rows.return_value = []
        return c

    @pytest.fixture
    def panel(self, controller, qtbot):
        # Mocking ProgrammazioneTab to avoid complex child setup
        with (
            patch("src.gui.panels.pdl.pdl_panel.ProgrammazioneTab", return_value=QWidget()),
            patch("src.core.sync_tracker.SyncTracker.get_formatted_status", return_value="N/D"),
            patch("src.core.database.db_manager.execute_query", return_value=[]),
        ):
            p = PDLDBPanel(controller)
            qtbot.addWidget(p)
            p.show()
            return p

    def test_initialization(self, panel):
        assert panel.controller is not None
        assert panel.model is not None
        assert panel.tabs.count() == 2

    def test_refresh_data_empty(self, panel, controller, qtbot):
        controller.get_pdl_data.return_value = []
        panel.refresh_data()

        assert panel.model.rowCount() == 0
        qtbot.wait_until(lambda: panel.empty_state.isVisible())

    def test_refresh_data_with_items(self, panel, controller, qtbot):
        mock_dto = MagicMock()
        mock_dto.n_pdl = "123"
        controller.get_pdl_data.return_value = [mock_dto]
        controller.process_master_rows.return_value = [("Data", "Req", "123", "Area", "Unit", "Stat", "Desc")]

        panel.refresh_data()

        qtbot.wait_until(lambda: not panel.empty_state.isVisible())
        assert panel.model.rowCount() == 1
        assert controller.get_pdl_data.called

    def test_reset_filters(self, panel):
        panel.filters.search_input.setText("test")
        panel._reset_filters()
        assert panel.filters.search_input.text() == ""

    def test_toggle_detail_view(self, panel, qtbot):
        # Detail view starts hidden
        assert not panel.detail_view.isVisible()
        panel._toggle_detail_view()
        assert panel.detail_view.isVisible()
        panel._toggle_detail_view()
        assert not panel.detail_view.isVisible()

    @patch("src.core.database.db_manager.execute_query")
    def test_update_areas(self, mock_query, panel):
        mock_query.return_value = [("Area 1",), ("Area 2",)]

        # Simula selezione sito per triggerare worker
        panel.filters.site_filter.setCurrentText("ISAB Sud")
        panel._update_areas()

        assert mock_query.called
        assert panel.filters.area_filter.count() >= 3

    def test_on_selection_changed(self, panel, controller, qtbot):
        # 1. Setup row in table
        mock_dto = MagicMock()
        mock_dto.n_pdl = "123/C"
        mock_dto.to_full_list.return_value = ["Detail" for _ in range(21)]
        panel._raw_full_data = [mock_dto]

        # 2. Update model and select
        panel.model.update_data([("D", "R", "123/C", "A", "U", "S", "D")])
        panel.table.selectRow(0)

        # 3. Verify detail view update
        with patch("src.core.pdl.pdl_service.PDLService.get_pdl_interventions", return_value=[]):
            panel._on_selection_changed()
            # Detail view labels are updated. "ID" is first header
            assert panel.detail_view.detail_labels["ID"].text() == "Detail"
