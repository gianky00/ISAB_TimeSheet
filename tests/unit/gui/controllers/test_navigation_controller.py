from unittest.mock import MagicMock, patch

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QStackedWidget, QWidget

from src.gui.controllers.navigation_controller import NavigationController
from src.gui.main_window.page_index import PageIndex


class MockMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.sidebar = MagicMock()


def test_navigation_controller_init(qtbot):
    mw = MockMainWindow()
    qtbot.addWidget(mw)

    # Mock core controllers initialization to avoid DB connections
    with (
        patch("src.core.oda.oda_controller.ODAController"),
        patch("src.core.dipendenti.anagrafica_controller.AnagraficaController"),
        patch("src.core.pdl.pdl_controller.PDLController"),
        patch("src.core.contabilita.scarico_ore.controller.ScaricoOreController"),
        patch("src.core.contabilita.consuntivo.consuntivo_controller.ConsuntivoController"),
    ):
        nav = NavigationController(mw)
        assert nav.mw == mw
        # Check if placeholders were added
        assert mw.stacked_widget.count() == len(PageIndex)


def test_navigate_to_valid(qtbot):
    mw = MockMainWindow()
    qtbot.addWidget(mw)

    with (
        patch("src.core.oda.oda_controller.ODAController"),
        patch("src.core.dipendenti.anagrafica_controller.AnagraficaController"),
        patch("src.core.pdl.pdl_controller.PDLController"),
        patch("src.core.contabilita.scarico_ore.controller.ScaricoOreController"),
        patch("src.core.contabilita.consuntivo.consuntivo_controller.ConsuntivoController"),
    ):
        nav = NavigationController(mw)

        # Mock panel factory to return a real widget
        test_panel = QWidget()
        qtbot.addWidget(test_panel)
        nav.panel_factory.create_panel = MagicMock(return_value=test_panel)

        nav.navigate_to(PageIndex.DASHBOARD)

        assert mw.stacked_widget.currentIndex() == PageIndex.DASHBOARD
        assert mw.stacked_widget.currentWidget() == test_panel
        mw.sidebar.set_active_button.assert_called_once()


def test_detach_reattach_panel(qtbot):
    mw = MockMainWindow()
    qtbot.addWidget(mw)

    with (
        patch("src.core.oda.oda_controller.ODAController"),
        patch("src.core.dipendenti.anagrafica_controller.AnagraficaController"),
        patch("src.core.pdl.pdl_controller.PDLController"),
        patch("src.core.contabilita.scarico_ore.controller.ScaricoOreController"),
        patch("src.core.contabilita.consuntivo.consuntivo_controller.ConsuntivoController"),
    ):
        nav = NavigationController(mw)

        test_panel = QWidget()
        qtbot.addWidget(test_panel)
        test_panel.TITLE = "Test Panel"
        nav.panel_factory.create_panel = MagicMock(return_value=test_panel)

        # Detach
        with patch("src.gui.controllers.navigation_controller.DetachedPanelWindow") as mock_window_cls:
            # We need a mock that HAS the signal attribute
            class MockWindow(QObject):
                panel_closed_signal = Signal(int)

                def show(self):
                    pass

                def close(self):
                    pass

            mock_window = MockWindow()
            mock_window_cls.return_value = mock_window

            nav.detach_panel(PageIndex.DASHBOARD)

            assert PageIndex.DASHBOARD in nav._detached_panels
            # Check if placeholder is in stack
            from src.gui.components.popout.popout_manager import PopoutPlaceholderWidget

            assert isinstance(mw.stacked_widget.widget(PageIndex.DASHBOARD), PopoutPlaceholderWidget)

            # Reattach
            nav.reattach_panel(PageIndex.DASHBOARD)
            assert PageIndex.DASHBOARD not in nav._detached_panels
            assert mw.stacked_widget.widget(PageIndex.DASHBOARD) == test_panel


def test_navigate_to_panel_key(qtbot):
    mw = MockMainWindow()
    qtbot.addWidget(mw)

    with (
        patch("src.core.oda.oda_controller.ODAController"),
        patch("src.core.dipendenti.anagrafica_controller.AnagraficaController"),
        patch("src.core.pdl.pdl_controller.PDLController"),
        patch("src.core.contabilita.scarico_ore.controller.ScaricoOreController"),
        patch("src.core.contabilita.consuntivo.consuntivo_controller.ConsuntivoController"),
    ):
        nav = NavigationController(mw)
        nav.navigate_to = MagicMock()

        nav.navigate_to_panel("scarico_pdl")
        nav.navigate_to.assert_called_once_with(PageIndex.AUTOMAZIONI, sub_index=1, bot_index=0)
