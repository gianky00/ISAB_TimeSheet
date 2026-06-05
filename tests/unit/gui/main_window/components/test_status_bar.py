"""Unit tests for StatusBarComponent."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt, QTime
from PySide6.QtWidgets import QMainWindow

from src.gui.main_window.components.status_bar import StatusBarComponent


@pytest.fixture
def real_main_window(qtbot):
    """Istanza reale di QMainWindow per i test PySide6."""
    mw = QMainWindow()
    # Necessario per i test di visibilità in ambiente offscreen
    mw.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    mw.show()
    qtbot.addWidget(mw)
    return mw


@pytest.fixture
def mock_license_info(mocker):
    """Mock per get_license_info."""
    mock = mocker.patch("src.gui.main_window.components.status_bar.get_license_info")
    mock.return_value = {"Cliente": "TEST CLIENT", "Scadenza Licenza": "31/12/2026", "Hardware ID": "HW-TEST"}
    return mock


class TestStatusBarComponent:
    """Test suite per StatusBarComponent."""

    def test_initialization(self, qtbot, real_main_window):
        """Verifica lbl'inizializzazione dei widget della barra di stato."""
        comp = StatusBarComponent(real_main_window)

        assert comp.status_bar is not None
        assert comp.footer_left is not None
        assert comp.boot_telemetry is not None
        assert comp.status_portale._title_label.text() == "Portale Fornitori"
        assert comp.status_safework._title_label.text() == "SafeWork"

    def test_toggle_footer_stats(self, qtbot, real_main_window):
        """Verifica lo switch tra info licenza e telemetria."""
        comp = StatusBarComponent(real_main_window)

        # Forza uno stato noto
        comp.footer_left.show()
        comp.boot_telemetry.hide()
        comp._footer_stats_mode = False

        # Click toggle 1: Mostra Telemetria, Nasconde Licenza
        qtbot.mouseClick(comp.footer_toggle_btn, Qt.MouseButton.LeftButton)
        assert comp.footer_left.isHidden()
        assert not comp.boot_telemetry.isHidden()
        assert comp._footer_stats_mode is True

        # Click toggle 2: Nasconde Telemetria, Mostra Licenza
        qtbot.mouseClick(comp.footer_toggle_btn, Qt.MouseButton.LeftButton)
        assert not comp.footer_left.isHidden()
        assert comp.boot_telemetry.isHidden()
        assert comp._footer_stats_mode is False

    def test_update_license_info(self, qtbot, real_main_window, mock_license_info, mocker):
        """Verifica lbl'aggiornamento delle label di licenza."""
        mocker.patch(
            "src.application.services.config_manager.load_config",
            return_value={"last_login_date": "20/05/2026"},
        )
        mocker.patch("src.application.services.config_manager.set_config_value")

        comp = StatusBarComponent(real_main_window)
        comp.footer_left.update_info = MagicMock()

        comp.update_license_info()

        assert mock_license_info.called
        comp.footer_left.update_info.assert_called_with("TEST CLIENT", "31/12/2026", "20/05/2026", "HW-TEST")

    def test_show_operational_state(self, qtbot, real_main_window, mocker):
        """Verifica la transizione visiva allo stato operativo."""
        comp = StatusBarComponent(real_main_window)
        comp.show_operational_state()

        # Attendiamo la fine delle animazioni (600ms)
        qtbot.wait(800)

        assert comp.startup_console.isHidden()

    def test_update_autopilot_ui_pf(self, qtbot, real_main_window, mocker):
        """Verifica il calcolo del countdown Autopilot per Portale Fornitori."""
        mocker.patch("PySide6.QtCore.QTime.currentTime", return_value=QTime(8, 0))

        config = {"timbrature_autopilot_enabled": True, "timbrature_autopilot_time": "09:30"}
        mocker.patch("src.application.services.config_manager.load_config", return_value=config)

        comp = StatusBarComponent(real_main_window)
        comp.status_portale.setAutopilot = MagicMock()

        comp.update_autopilot_ui()

        args, _ = comp.status_portale.setAutopilot.call_args
        assert args[0] is True
        assert "TIMBRATURE" in args[1]
        assert "1H 30M" in args[1]

    def test_update_autopilot_ui_sw_next_day(self, qtbot, real_main_window, mocker):
        """Verifica il countdown quando il task è previsto per il giorno successivo."""
        mocker.patch("PySide6.QtCore.QTime.currentTime", return_value=QTime(22, 0))

        config = {"ricerca_pdl_autopilot_enabled": True, "ricerca_pdl_autopilot_time": "02:00"}
        mocker.patch("src.application.services.config_manager.load_config", return_value=config)

        comp = StatusBarComponent(real_main_window)
        comp.status_safework.setAutopilot = MagicMock()

        comp.update_autopilot_ui()

        args, _ = comp.status_safework.setAutopilot.call_args
        assert "4H 0M" in args[1]
