from unittest.mock import MagicMock, patch

from src.utils.system_telemetry import get_current_process_ram_mb


class TestSystemTelemetry:
    @patch("src.utils.system_telemetry.ProcessMemoryCountersEx")
    @patch("src.utils.system_telemetry.ctypes")
    def test_get_current_process_ram_mb_success(self, mock_ctypes, mock_counters_class):
        # Setup mock DLLs
        mock_psapi = MagicMock()
        mock_kernel32 = MagicMock()
        mock_ctypes.windll.psapi = mock_psapi
        mock_ctypes.windll.kernel32 = mock_kernel32

        # Simula counters
        mock_counters = mock_counters_class.return_value
        mock_counters.WorkingSetSize = 100 * 1024 * 1024  # 100 MB

        # Simula successo API
        mock_psapi.GetProcessMemoryInfo.return_value = True

        ram = get_current_process_ram_mb()
        assert ram == 100.0

    @patch("src.utils.system_telemetry.ctypes")
    def test_get_current_process_ram_mb_no_win(self, mock_ctypes):
        # Simula sistema non-windows (rimuoviamo windll dal mock)
        # hasattr(mock, 'windll') è True per default, dobbiamo cancellarlo o usare spec
        mock_ctypes.configure_mock(windll=None)
        # Ma hasattr(None, 'psapi') fallirà diversamente.
        # Meglio mockare hasattr o configurare il mock per fallire il check
        with patch(
            "src.utils.system_telemetry.hasattr",
            side_effect=lambda obj, attr: attr != "windll",
        ):
            assert get_current_process_ram_mb() == 0.0

    @patch("src.utils.system_telemetry.ctypes")
    def test_get_current_process_ram_mb_fail(self, mock_ctypes):
        mock_ctypes.windll.psapi.GetProcessMemoryInfo.return_value = False
        assert get_current_process_ram_mb() == 0.0
