from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QItemSelectionModel, Qt
from PySide6.QtGui import QStandardItem

from src.application.services.oda.oda_controller import ODAController
from src.gui.panels.storico_oda.oda_panel import StoricoOdaPanel


class TestStoricoOdaPanel:
    @pytest.fixture(autouse=True)
    def mock_sync_worker(self, mocker):
        """Forza il worker ODA ad essere sincrono."""

        def mock_start(instance):
            instance.run()

        mocker.patch("src.gui.workers.oda_data_worker.ODADataWorker.start", mock_start)

    @pytest.fixture
    def controller(self):
        c = MagicMock(spec=ODAController)
        c.get_grouped_data.return_value = []
        return c

    @pytest.fixture
    def panel(self, controller, qtbot):
        with (
            patch(
                "src.application.services.sync_tracker.SyncTracker.get_formatted_status", return_value="N/D"
            ),
            patch("src.gui.styles.ui_effects.UIEffectsManager.apply_shadow"),
            patch("src.gui.styles.ui_effects.UIEffectsManager.animate_fade"),
        ):
            p = StoricoOdaPanel(controller)
            qtbot.addWidget(p)
            p.show()
            return p

    def test_initialization(self, panel):
        assert panel.controller is not None
        assert panel.model is not None
        assert panel.tree is not None
        assert panel.detail_view is not None

    def test_refresh_data_empty(self, panel, controller, qtbot):
        controller.get_grouped_data.return_value = []
        panel.refresh_data()

        assert panel.model.rowCount() == 0
        qtbot.wait_until(lambda: panel.empty_state.isVisible())

    def test_refresh_data_with_items(self, panel, controller, qtbot):
        controller.get_grouped_data.return_value = [
            {
                "oda": "123",
                "data": "2024-01-01",
                "creatore": "Admin",
                "descrizione": "Desc",
                "valore_totale": 100.0,
                "stato": "S",
                "rilascio": "R",
                "raw_first": ["val" for _ in range(32)],
                "positions": [
                    (
                        "v",
                        "v",
                        "v",
                        "10",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "v",
                        "0",
                        1.0,
                        "PZ",
                        10.0,
                        "Short",
                    )
                ],
            }
        ]

        panel.refresh_data()

        assert panel.model.rowCount() == 1
        assert panel.model.item(0).rowCount() == 1
        qtbot.wait_until(lambda: not panel.empty_state.isVisible())

    def test_on_selection_changed_bold(self, panel, qtbot):
        item = QStandardItem("ODA")
        panel.model.appendRow([item, QStandardItem("Data")])

        # Select row
        panel.tree.selectionModel().select(
            panel.model.index(0, 0),
            QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows,
        )
        panel._on_selection_changed()

        # Check item from model directly
        actual_item = panel.model.item(0, 0)
        assert actual_item.font().bold() is True

    def test_open_detail_for_index(self, panel):
        item = QStandardItem("ODA")
        raw_data = ["val" for _ in range(32)]
        item.setData(raw_data, Qt.ItemDataRole.UserRole)
        panel.model.appendRow([item])

        panel._open_detail_for_index(panel.model.index(0, 0))

        assert panel.detail_view.isVisible()
        assert panel.detail_view.detail_labels["Org. Acq."].text() == "val"

    @patch("src.gui.panels.storico_oda.oda_panel.QFileDialog.getOpenFileName")
    def test_on_import_clicked(self, mock_file, panel):
        mock_file.return_value = ("/fake/file.xlsx", "")
        with patch("src.gui.panels.storico_oda.oda_panel.OdaIOWorker") as mock_worker:
            panel._on_import_clicked()
            assert mock_worker.called

    def test_on_io_finished_success(self, panel, qtbot):
        with patch("src.gui.widgets.toast.ToastManager.show") as mock_toast:
            panel._on_io_finished(True, "OK", {"added": 5, "removed": 0})
            assert mock_toast.called
            assert "+5 OdA" in mock_toast.call_args[0][0]
