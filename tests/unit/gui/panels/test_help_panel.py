"""Unit tests for HelpPanel."""

import pytest

from src.gui.panels.help_panel import HelpPanel


@pytest.fixture
def mock_sections():
    """Dati di test per le sezioni della documentazione."""
    return [
        ("Introduzione", "# Benvenuto", "home"),
        ("Guida Rapida", "# Come fare", "rocket"),
        ("Troubleshooting", "# Problemi", "alert-triangle"),
    ]


class TestHelpPanel:
    """Test suite per HelpPanel."""

    def test_initialization(self, qtbot, mocker):
        """Verifica lbl'inizializzazione del pannello."""
        # Evitiamo lbl'avvio del thread reale
        mocker.patch("src.gui.panels.help_panel.HelpWorker.start")

        panel = HelpPanel()
        qtbot.addWidget(panel)

        assert panel.index_list is not None
        assert panel.browser is not None
        assert "Centro Risorse" in str(
            panel.findChildren(pytest.importorskip("PySide6.QtWidgets").QLabel)[0].text()
        )

    def test_on_docs_ready_populates_list(self, qtbot, mock_sections, mocker):
        """Verifica il popolamento dell'indice dopo il caricamento."""
        mocker.patch("src.gui.panels.help_panel.HelpWorker.start")
        panel = HelpPanel()
        qtbot.addWidget(panel)

        panel._on_docs_ready(mock_sections)

        assert panel.index_list.count() == 3
        assert panel.index_list.item(0).text() == "Introduzione"
        # Dovrebbe aver selezionato la prima riga
        assert panel.index_list.currentRow() == 0
        assert "# Benvenuto" in panel.browser.toMarkdown()

    def test_search_filtering(self, qtbot, mock_sections, mocker):
        """Verifica il filtro dell'indice tramite ricerca."""
        mocker.patch("src.gui.panels.help_panel.HelpWorker.start")
        panel = HelpPanel()
        qtbot.addWidget(panel)
        panel._on_docs_ready(mock_sections)

        # Filtriamo per "Guida"
        panel.search_edit.setText("Guida")

        assert not panel.index_list.item(1).isHidden()  # Guida Rapida
        assert panel.index_list.item(0).isHidden()  # Introduzione
        assert panel.index_list.item(2).isHidden()  # Troubleshooting

    def test_index_selection_updates_browser(self, qtbot, mock_sections, mocker):
        """Verifica che cambiando riga cambi il contenuto del browser."""
        mocker.patch("src.gui.panels.help_panel.HelpWorker.start")
        panel = HelpPanel()
        qtbot.addWidget(panel)
        panel._on_docs_ready(mock_sections)

        # Selezioniamo Troubleshooting (index 2)
        panel.index_list.setCurrentRow(2)

        assert "# Problemi" in panel.browser.toMarkdown()

    def test_open_section_api(self, qtbot, mock_sections, mocker):
        """Verifica lbl'API programmatica per aprire una sezione."""
        mocker.patch("src.gui.panels.help_panel.HelpWorker.start")
        panel = HelpPanel()
        qtbot.addWidget(panel)
        panel._on_docs_ready(mock_sections)

        panel.open_section("Troubleshooting")

        assert panel.index_list.currentRow() == 2
        assert "# Problemi" in panel.browser.toMarkdown()

    def test_content_markdown_methods(self, panel_no_worker):
        """Verifica che i metodi che generano MD non crashino."""
        panel = panel_no_worker
        assert "# Benvenuto" in panel._get_intro_md()
        assert "Workflow" in panel._get_scarico_md()
        assert "Supporto" in panel._get_contacts_md()


@pytest.fixture
def panel_no_worker(qtbot, mocker):
    """Pannello con worker disabilitato."""
    mocker.patch("src.gui.panels.help_panel.HelpWorker.start")
    p = HelpPanel()
    qtbot.addWidget(p)
    return p
