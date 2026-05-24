"""Unit tests for ChangelogPanel."""

import pytest
from PySide6.QtCore import Qt

from src.gui.panels.changelog_panel import ChangelogPanel, ReleaseCard


@pytest.fixture
def changelog_data():
    """Mock changelog data."""
    return [
        {
            "version": "1.1.0",
            "date": "2026-05-24",
            "notes": [
                "feat: Nuova feature incredibile",
                "fix: Risolto un bug fastidioso",
                "docs: Aggiornata documentazione",
            ],
        },
        {"version": "1.0.0", "date": "2026-05-20", "notes": ["Initial release"]},
    ]


class TestChangelogPanel:
    """Test suite per ChangelogPanel."""

    def test_initialization(self, qtbot):
        """Verifica che il pannello si inizializzi correttamente."""
        panel = ChangelogPanel()
        qtbot.addWidget(panel)
        assert panel is not None
        assert panel.active_filter == "all"
        assert panel.search_text == ""

    def test_on_changelog_ready(self, qtbot, changelog_data):
        """Verifica il caricamento dei dati nel pannello."""
        panel = ChangelogPanel()
        qtbot.addWidget(panel)

        # Simuliamo il segnale del worker
        panel._on_changelog_ready(changelog_data)

        # Verifichiamo che siano state create le card
        assert len(panel.release_rows) == len(changelog_data)
        assert isinstance(panel.release_rows[0][1], ReleaseCard)

    def test_filter_buttons(self, qtbot, changelog_data):
        """Verifica il funzionamento dei pulsanti di filtro."""
        panel = ChangelogPanel()
        qtbot.addWidget(panel)
        panel.show()  # Necessario per isVisible()
        panel._on_changelog_ready(changelog_data)

        # Filtro Bugfix
        danger_btn = panel.filter_buttons["danger"]
        qtbot.mouseClick(danger_btn, Qt.MouseButton.LeftButton)

        assert panel.active_filter == "danger"
        # La prima card dovrebbe essere visibile perché contiene un fix
        assert panel.release_rows[0][0].isVisible()
        # La seconda card non contiene fix, dovrebbe essere nascosta
        assert not panel.release_rows[1][0].isVisible()

    def test_search_filtering(self, qtbot, changelog_data):
        """Verifica il filtraggio tramite barra di ricerca."""
        panel = ChangelogPanel()
        qtbot.addWidget(panel)
        panel.show()  # Necessario per isVisible()
        panel._on_changelog_ready(changelog_data)

        # Cerchiamo un testo specifico
        panel.search_bar.setText("feature")

        assert panel.search_text == "feature"
        assert panel.release_rows[0][0].isVisible()
        assert not panel.release_rows[1][0].isVisible()

    def test_diagnostics_loading(self, qtbot):
        """Verifica lbl'aggiornamento delle label diagnostiche."""
        panel = ChangelogPanel()
        qtbot.addWidget(panel)

        panel._on_diagnostics_loaded("test-sha", "Test-Platform")

        assert panel.sha_lbl.text() == "test-sha"
        assert panel.platform_lbl.text() == "Test-Platform"


class TestReleaseCard:
    """Test suite per ReleaseCard."""

    def test_card_expansion(self, qtbot, changelog_data):
        """Verifica lbl'espansione della card al click."""
        release = changelog_data[0]
        card = ReleaseCard(release, is_latest=True)
        qtbot.addWidget(card)

        assert not card.is_expanded

        # Simuliamo il click sulla card (mousePressEvent)
        qtbot.mouseClick(card, Qt.MouseButton.LeftButton)

        assert card.is_expanded
        # Nota: lbl'animazione è asincrona, ma lo stato interno cambia subito

    def test_copy_to_clipboard(self, qtbot, changelog_data, mocker):
        """Verifica la copia negli appunti."""
        from PySide6.QtGui import QGuiApplication

        mock_cb_obj = mocker.MagicMock()
        mocker.patch.object(QGuiApplication, "clipboard", return_value=mock_cb_obj)

        card = ReleaseCard(changelog_data[0], is_latest=True)
        qtbot.addWidget(card)

        card._copy_to_clipboard()

        # Verifichiamo che setText sia stato chiamato
        assert mock_cb_obj.setText.called
        args, _ = mock_cb_obj.setText.call_args
        assert "## SyncroJob v1.1.0" in args[0]
        assert "- feat: Nuova feature incredibile" in args[0]

    def test_pill_creation(self, qtbot, changelog_data):
        """Verifica la corretta categorizzazione delle note."""
        card = ReleaseCard(changelog_data[0], is_latest=True)
        qtbot.addWidget(card)

        label, style = card._parse_note_category("feat: test")
        assert "FEATURE" in label
        assert style == "success"

        label, style = card._parse_note_category("fix: test")
        assert "BUGFIX" in label
        assert style == "danger"

        label, style = card._parse_note_category("something else")
        assert "UPDATE" in label
        assert style == "info"
