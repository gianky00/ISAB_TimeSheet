"""Unit tests for ROITab."""

from src.gui.panels.settings.tabs.roi_tab import ROITab, ROIWeightsPage


class TestROIWeightsPage:
    """Test suite per ROIWeightsPage."""

    def test_initialization(self, qtbot):
        page = ROIWeightsPage()
        qtbot.addWidget(page)

        assert len(page.tasks) >= 8
        assert "Scarico TS" in page.task_inputs
        assert page.task_inputs["Scarico TS"]["min"].value() == 0

    def test_load_from_config(self, qtbot):
        page = ROIWeightsPage()
        qtbot.addWidget(page)

        config = {
            "roi_weights": {
                "Scarico TS": 5.5,  # 5 min 30 sec
                "Carico TS": 2.25,  # 2 min 15 sec
            }
        }
        page.load_from_config(config)

        assert page.task_inputs["Scarico TS"]["min"].value() == 5
        assert page.task_inputs["Scarico TS"]["sec"].value() == 30
        assert page.task_inputs["Carico TS"]["min"].value() == 2
        assert page.task_inputs["Carico TS"]["sec"].value() == 15

    def test_save_to_config(self, qtbot):
        page = ROIWeightsPage()
        qtbot.addWidget(page)

        page.task_inputs["Scarico TS"]["min"].setValue(10)
        page.task_inputs["Scarico TS"]["sec"].setValue(45)

        config = {}
        page.save_to_config(config)

        assert config["roi_weights"]["Scarico TS"] == 10.75  # 10 + 45/60

    def test_settings_changed_signal(self, qtbot):
        page = ROIWeightsPage()
        qtbot.addWidget(page)

        with qtbot.waitSignal(page.settings_changed):
            page.task_inputs["Scarico TS"]["min"].setValue(1)


class TestROITab:
    """Test suite per ROITab."""

    def test_initialization(self, qtbot):
        widget = ROITab()
        qtbot.addWidget(widget)
        assert widget.weights_page is not None

    def test_load_save_delegation(self, qtbot):
        widget = ROITab()
        qtbot.addWidget(widget)

        config = {"roi_weights": {"Scarico TS": 1.0}}
        widget.load_from_config(config)
        assert widget.weights_page.task_inputs["Scarico TS"]["min"].value() == 1

        widget.weights_page.task_inputs["Scarico TS"]["min"].setValue(2)
        new_config = {}
        widget.save_to_config(new_config)
        assert new_config["roi_weights"]["Scarico TS"] == 2.0
