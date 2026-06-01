"""Unit tests for Splash Standalone components."""

from src.gui.dialogs.splash_standalone import SplashCommunicator, StandaloneSplash


class TestStandaloneSplash:
    """Test suite per StandaloneSplash."""

    def test_initialization(self, qtbot):
        splash = StandaloneSplash()
        qtbot.addWidget(splash)

        assert splash.windowOpacity() == 1.0
        assert splash.status.text() == "AVVIO IN CORSO..."

    def test_update_status_logs(self, qtbot, mocker):
        """Verifica che lbl'update_status logghi correttamente."""
        mock_logger = mocker.patch("src.gui.dialogs.splash_standalone.logger.info")
        splash = StandaloneSplash()
        qtbot.addWidget(splash)

        splash.update_status("Loading...", 50)

        assert mock_logger.called
        assert "50%" in mock_logger.call_args[0][0]
        assert splash.progress._value == 50


class TestSplashCommunicator:
    """Test suite per SplashCommunicator."""

    def test_signals(self, qtbot):
        comm = SplashCommunicator()

        with qtbot.waitSignal(comm.update_signal) as blocker:
            comm.update_signal.emit("Msg", 10)
        assert blocker.args == ["Msg", 10]

        with qtbot.waitSignal(comm.close_signal):
            comm.close_signal.emit()

        with qtbot.waitSignal(comm.license_received) as blocker:
            comm.license_received.emit("C", "H", "S")
        assert blocker.args == ["C", "H", "S"]
