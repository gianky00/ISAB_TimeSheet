from unittest.mock import patch

from PyQt6.QtCore import Qt


class TestSidebarWidget:
    """Test suite per SidebarWidget V9.0 (Navigazione Profonda)."""

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_initialization(self, mock_asset, qapp, qtbot):
        mock_asset.return_value = ""
        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)
        assert sidebar._is_collapsed is True

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_palette_click_emits_signal(self, mock_asset, qapp, qtbot):
        mock_asset.return_value = ""
        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)
        sidebar._set_collapsed(False)
        with qtbot.waitSignal(sidebar.palette_requested, timeout=1000):
            qtbot.mouseClick(sidebar.btn_palette, Qt.MouseButton.LeftButton)

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_monitoraggio_group_exists(self, mock_asset, qapp, qtbot):
        mock_asset.return_value = ""
        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)

        # Il gruppo esiste ancora come group_notifiche (titolo "Monitoraggio")
        assert hasattr(sidebar, "group_notifiche")

        # In V9.0 i bottoni child sono in notif_child_btns
        # Verifichiamo che il numero di bottoni aggiunti al gruppo sia 3
        assert len(sidebar.notif_child_btns) == 3

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_navigation_signal(self, mock_asset, qapp, qtbot):
        mock_asset.return_value = ""
        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)
        sidebar._set_collapsed(False)

        with qtbot.waitSignal(sidebar.navigation_requested, timeout=1000) as blocker:
            qtbot.mouseClick(sidebar.btn_home, Qt.MouseButton.LeftButton)

        # Home -> Page 0, Sub -1, Bot -1
        assert blocker.args == [0, -1, -1]

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_expand_collapse_state(self, mock_asset, qapp, qtbot):
        mock_asset.return_value = ""
        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)

        sidebar._set_collapsed(False)
        assert sidebar._is_collapsed is False
        sidebar._set_collapsed(True)
        assert sidebar._is_collapsed is True
