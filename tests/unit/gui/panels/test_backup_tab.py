"""Unit tests for BackupTab."""

from src.gui.panels.settings.tabs.backup_tab import BackupTab


class TestBackupTab:
    """Test suite per BackupTab."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione del tab."""
        widget = BackupTab()
        qtbot.addWidget(widget)

        assert len(widget.cards) == 2
        assert widget.btn_backup is not None
        assert widget.btn_restore is not None
        assert widget.btn_open_logs is not None
        assert widget.btn_clear_logs is not None

    def test_load_from_config(self, qtbot):
        """Verifica il caricamento della data ultimo backup."""
        widget = BackupTab()
        qtbot.addWidget(widget)

        config = {"last_db_backup": "24/05/2026 15:00"}
        widget.load_from_config(config)

        assert "24/05/2026" in widget.lbl_last_backup.text()

    def test_filter_cards(self, qtbot):
        """Verifica la ricerca interna."""
        widget = BackupTab()
        qtbot.addWidget(widget)

        # Cerchiamo "Sicurezza"
        widget.search_bar.setText("Sicurezza")

        visible_cards = [c for c in widget.cards if not c.isHidden()]
        assert len(visible_cards) == 1
        assert "Sicurezza Dati" in visible_cards[0].title_text

    def test_buttons_visibility(self, qtbot):
        """Verifica che i bottoni principali siano presenti."""
        widget = BackupTab()
        qtbot.addWidget(widget)

        assert widget.btn_backup.text() == "Esegui Backup Database"
        assert widget.btn_clear_logs.text() == "Pulisci Log Vecchi"
