from unittest.mock import MagicMock, patch

import pytest

from src.core.pdl.pdl_controller import PDLController
from src.gui.panels.pdl.pdl_panel import PDLDBPanel


@pytest.fixture
def mock_pdl_controller():
    controller = MagicMock(spec=PDLController)
    controller.get_stats.return_value = {"total": 10, "open": 5}
    return controller


def test_pdl_db_panel_init(qtbot, mock_pdl_controller):
    with (
        patch("src.gui.panels.pdl.pdl_panel.PDLFilterWidget"),
        patch("src.gui.panels.pdl.pdl_panel.PDLTableView"),
        patch("src.gui.panels.pdl.pdl_panel.PDLDetailView"),
        patch("src.gui.panels.pdl.pdl_panel.AnimatedTabWidget"),
        patch("src.gui.panels.pdl.pdl_panel.ProgrammazioneTab"),
    ):
        panel = PDLDBPanel(controller=mock_pdl_controller)
        qtbot.addWidget(panel)

        assert panel.controller == mock_pdl_controller
        assert panel.model is not None
        assert panel.master_headers is not None


def test_pdl_db_panel_refresh(qtbot, mock_pdl_controller):
    with (
        patch("src.gui.panels.pdl.pdl_panel.PDLFilterWidget"),
        patch("src.gui.panels.pdl.pdl_panel.PDLTableView"),
        patch("src.gui.panels.pdl.pdl_panel.PDLDetailView"),
        patch("src.gui.panels.pdl.pdl_panel.AnimatedTabWidget"),
        patch("src.gui.panels.pdl.pdl_panel.ProgrammazioneTab"),
    ):
        panel = PDLDBPanel(controller=mock_pdl_controller)
        qtbot.addWidget(panel)

        with patch("src.gui.panels.pdl.pdl_panel.PDLDataWorker") as mock_worker_cls:
            mock_worker = MagicMock()
            mock_worker_cls.return_value = mock_worker

            panel.refresh_data()

            # Should start data worker
            mock_worker_cls.assert_called()
            mock_worker.start.assert_called()


def test_on_pdl_selected(qtbot, mock_pdl_controller):
    with (
        patch("src.gui.panels.pdl.pdl_panel.PDLFilterWidget"),
        patch("src.gui.panels.pdl.pdl_panel.PDLTableView"),
        patch("src.gui.panels.pdl.pdl_panel.PDLDetailView"),
        patch("src.gui.panels.pdl.pdl_panel.AnimatedTabWidget"),
        patch("src.gui.panels.pdl.pdl_panel.ProgrammazioneTab"),
    ):
        panel = PDLDBPanel(controller=mock_pdl_controller)
        qtbot.addWidget(panel)

        panel.detail_view = MagicMock()
        mock_pdl = {"N  PDL": "12345", "Area": "A1"}

        panel._on_pdl_selected(mock_pdl)

        panel.detail_view.set_pdl.assert_called_once_with(mock_pdl)
