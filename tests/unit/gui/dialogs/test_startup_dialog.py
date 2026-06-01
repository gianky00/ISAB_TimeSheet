"""Unit tests for StartupDialog."""

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QMouseEvent

from src.gui.dialogs.startup_dialog import StartupDialog


class TestStartupDialog:
    """Test suite per StartupDialog."""

    def test_initialization(self, qtbot):
        """Verifica che il dialogo si inizializzi con tutti i componenti."""
        dialog = StartupDialog()
        qtbot.addWidget(dialog)

        assert dialog.objectName() == "StartupDialog"
        assert dialog.CONTENT_WIDTH == 850
        assert dialog.particles is not None
        assert dialog.border is not None
        assert dialog.progress is not None
        assert dialog.logo is not None
        assert dialog.status.text() == "AVVIO IN CORSO..."

    def test_update_status_progress(self, qtbot):
        """Verifica lbl'aggiornamento dello stato e del progresso."""
        from src.gui.styles import COLORS

        dialog = StartupDialog()
        qtbot.addWidget(dialog)

        # Test progress basso (Inizializzazione)
        dialog.update_status("Inizializzazione database", 10)
        assert "DATABASE" in dialog.status.text()
        assert dialog.progress._value == 10
        assert dialog.loading_pulse.color == QColor(COLORS["warning_orange"])

        # Test progress medio
        dialog.update_status("Caricamento moduli core", 60)
        assert "CORE" in dialog.status.text()
        assert dialog.progress._value == 60
        assert dialog.loading_pulse.color == QColor(COLORS["primary_blue"])

        # Test progress alto (Completamento)
        dialog.update_status("Sistema pronto", 95)
        assert "PRONTO" in dialog.status.text()
        assert dialog.progress._value == 95
        assert dialog.loading_pulse.color == QColor(COLORS["success_green"])

    def test_console_logging_rotation(self, qtbot):
        """Verifica che la console mantenga solo le ultime 5 righe."""
        dialog = StartupDialog()
        qtbot.addWidget(dialog)

        for i in range(10):
            dialog.update_status(f"Log riga {i}", i)

        assert len(dialog.current_logs) == 5
        assert dialog.current_logs[-1] == "> Log riga 9"
        assert dialog.current_logs[0] == "> Log riga 5"

    def test_macro_status_mapping(self, qtbot):
        """Verifica il corretto mapping dei messaggi in macro-fasi."""
        dialog = StartupDialog()
        qtbot.addWidget(dialog)

        assert dialog._map_macro_status("SQL tables created", 20) == "INIZIALIZZAZIONE DATABASE"
        assert dialog._map_macro_status("Loading GUI widgets", 40) == "PREPARAZIONE INTERFACCIA UTENTE"
        assert dialog._map_macro_status("Validating license", 80) == "SICUREZZA E LICENZA"
        assert dialog._map_macro_status("Unknown task", 50) == "OTTIMIZZAZIONE AMBIENTE"

    def test_mouse_drag_functionality(self, qtbot):
        """Verifica che il trascinamento della finestra funzioni."""
        dialog = StartupDialog()
        qtbot.addWidget(dialog)
        dialog.show()

        initial_pos = dialog.pos()

        # Simuliamo il press (start drag)
        press_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(100, 10),
            QPointF(100, 10),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        dialog.mousePressEvent(press_event)

        # Simuliamo il move (drag)
        move_event = QMouseEvent(
            QMouseEvent.Type.MouseMove,
            QPointF(150, 20),
            QPointF(150, 20),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        dialog.mouseMoveEvent(move_event)

        assert dialog.pos() != initial_pos

    def test_update_license_display(self, qtbot):
        """Verifica lbl'aggiornamento asincrono dei dati di licenza."""
        dialog = StartupDialog()
        qtbot.addWidget(dialog)

        dialog.update_license_display("COEMI SRL", "HW-12345", "31/12/2026")

        assert dialog.lbl_val_cliente.text() == "COEMI SRL"
        assert dialog.lbl_val_hwid.text() == "HW-12345"
        assert dialog.lbl_val_scadenza.text() == "31/12/2026"
        # TypewriterLabel imposta _full_text
        assert dialog.lbl_validated._full_text == "LICENZA VALIDATA"

    def test_close_event_cleanup(self, qtbot, mocker):
        """Verifica che la chiusura fermi i timer e i thread."""
        dialog = StartupDialog()
        qtbot.addWidget(dialog)

        # Mock dei timer per verificare lo stop
        mock_particle_timer = mocker.patch.object(dialog.particles.timer, "stop")
        mock_border_timer = mocker.patch.object(dialog.border.timer, "stop")
        mock_clock_timer = mocker.patch.object(dialog.clock_timer, "stop")

        dialog.close()

        assert mock_particle_timer.called
        assert mock_border_timer.called
        assert mock_clock_timer.called
