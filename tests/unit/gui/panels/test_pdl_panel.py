from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from src.application.services.pdl.pdl_controller import PDLController
from src.gui.panels.pdl.pdl_panel import PDLDBPanel


class MockSubWidget(QWidget):
    """Real QWidget to avoid addWidget failures."""

    filter_changed = Signal(dict)
    site_changed = Signal()
    area_changed = Signal()
    update_clicked = Signal()
    reset_clicked = Signal()
    export_clicked = Signal()

    # PDLTableView signals
    header_clicked = Signal(int)
    row_double_clicked = Signal()
    selection_changed_custom = Signal()
    context_menu_requested = Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.search_input = MagicMock()
        self.lbl_sync_status = MagicMock()
        self.site_filter = MagicMock()
        self.area_filter = MagicMock()
        self.unit_filter = MagicMock()
        self.group_filter = MagicMock()
        self.update_details = MagicMock()
        self.optimize_columns = MagicMock()

    def get_filters(self):
        return {}

    def clear(self):
        pass

    def set_pdl(self, pdl):
        pass

    def update_details(self, details, interventions):
        pass

    def optimize_columns(self, count):
        pass

    def setVisible(self, visible):  # noqa: N802
        super().setVisible(visible)


class MockTabs(QWidget):
    """Real QWidget for AnimatedTabWidget."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.addTab = MagicMock()


@pytest.fixture
def mock_pdl_controller():
    controller = MagicMock(spec=PDLController)
    controller.process_master_rows.return_value = []
    return controller


@pytest.fixture(autouse=True)
def global_pdl_mocks(mocker):
    """Applica patch globali per isolare il pannello PDL dal DB e dai Worker reali."""
    mocker.patch("src.gui.panels.pdl.pdl_panel.PDLFilterWidget", return_value=MockSubWidget())
    mocker.patch("src.gui.panels.pdl.pdl_panel.PDLTableView", return_value=MockSubWidget())
    mocker.patch("src.gui.panels.pdl.pdl_panel.PDLDetailView", return_value=MockSubWidget())
    mocker.patch("src.gui.panels.pdl.pdl_panel.AnimatedTabWidget", return_value=MockTabs())
    mocker.patch("src.gui.panels.pdl.pdl_panel.ProgrammazioneTab", return_value=MockSubWidget())
    mocker.patch("src.gui.panels.pdl.pdl_panel.PDLDataWorker")
    mocker.patch("src.application.services.sync_tracker.SyncTracker.get_formatted_status", return_value="N/D")
    mocker.patch("src.application.services.database.repositories.pdl_repository.PdlRepository")
    mocker.patch("src.gui.panels.pdl.pdl_panel.PDLService")


def test_pdl_db_panel_init(qtbot, mock_pdl_controller):
    panel = PDLDBPanel(controller=mock_pdl_controller)
    qtbot.addWidget(panel)
    panel.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)

    assert panel.controller == mock_pdl_controller
    assert panel.model is not None


def test_pdl_db_panel_refresh(qtbot, mock_pdl_controller, mocker):
    mock_worker_cls = mocker.patch("src.gui.panels.pdl.pdl_panel.PDLDataWorker")
    mock_worker = MagicMock()
    mock_worker_cls.return_value = mock_worker

    panel = PDLDBPanel(controller=mock_pdl_controller)
    qtbot.addWidget(panel)

    panel.refresh_data()
    assert mock_worker.start.called


def test_on_selection_changed(qtbot, mock_pdl_controller, mocker):
    # Mock PDLService.get_pdl_interventions
    mock_service = mocker.patch("src.gui.panels.pdl.pdl_panel.PDLService")
    mock_service.get_pdl_interventions.return_value = []

    panel = PDLDBPanel(controller=mock_pdl_controller)
    qtbot.addWidget(panel)

    mock_pdl = MagicMock()
    mock_pdl.to_full_list.return_value = []
    panel._raw_full_data = [mock_pdl]

    # Mock table selection
    mock_sel_model = MagicMock()
    mock_idx = MagicMock()
    mock_idx.row.return_value = 0
    mock_sel_model.selectedRows.return_value = [mock_idx]
    panel.table.selectionModel = MagicMock(return_value=mock_sel_model)

    panel._on_selection_changed()
    assert panel.detail_view.update_details.called
