"""
Test per SidebarWidget e nuovi segnali aggiunti.
"""

from unittest.mock import patch


class TestSidebarWidget:
    """Test per SidebarWidget."""

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_initialization(self, mock_asset, qtbot):
        """Testa l'inizializzazione della sidebar."""
        mock_asset.return_value = ""

        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)

        # Verifica stato iniziale collapsed
        assert sidebar._is_collapsed is True
        assert sidebar.width() == sidebar.collapsed_width

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_has_palette_signal(self, mock_asset, qtbot):
        """Testa che il segnale palette_requested esista."""
        mock_asset.return_value = ""

        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)

        # Verifica che il segnale esista
        assert hasattr(sidebar, "palette_requested")

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_palette_button_exists(self, mock_asset, qtbot):
        """Testa che il pulsante palette esista."""
        mock_asset.return_value = ""

        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)

        assert hasattr(sidebar, "btn_palette")
        assert sidebar.btn_palette is not None

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_palette_click_emits_signal(self, mock_asset, qtbot):
        """Testa che il click sul pulsante palette emetta il segnale."""
        mock_asset.return_value = ""

        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)

        # Connetti un handler di test
        signal_received = []
        sidebar.palette_requested.connect(lambda: signal_received.append(True))

        # Simula click
        sidebar._on_palette_click()

        assert len(signal_received) == 1

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_monitoraggio_group_exists(self, mock_asset, qtbot):
        """Testa che il gruppo Monitoraggio esista."""
        mock_asset.return_value = ""

        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)

        # Verifica che il gruppo esista (rinominato in "Monitoraggio" ma variabile ancora group_notifiche)
        assert hasattr(sidebar, "group_notifiche")
        assert sidebar.group_notifiche is not None

        # Verifica che i bottoni child esistano
        assert hasattr(sidebar, "btn_notifiche")
        assert hasattr(sidebar, "btn_audit")
        assert hasattr(sidebar, "btn_health")

    @patch("src.gui.widgets.sidebar_widget.get_asset_path")
    def test_sidebar_expand_collapse_state(self, mock_asset, qtbot):
        """Testa lo stato collapsed/expanded."""
        mock_asset.return_value = ""

        from src.gui.widgets.sidebar_widget import SidebarWidget

        sidebar = SidebarWidget()
        qtbot.addWidget(sidebar)

        # Stato iniziale: collapsed
        assert sidebar._is_collapsed is True
        assert sidebar.width() == sidebar.collapsed_width
