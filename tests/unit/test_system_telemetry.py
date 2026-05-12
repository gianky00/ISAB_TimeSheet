from unittest.mock import MagicMock, PropertyMock, patch

from src.utils.system_telemetry import get_current_process_ram_mb


class TestSystemTelemetry:
    @patch("src.utils.system_telemetry.ctypes")
    @patch("src.utils.system_telemetry.sizeof")
    @patch("src.utils.system_telemetry.byref")
    def test_get_current_process_ram_mb_success(self, mock_byref, mock_sizeof, mock_ctypes):
        # Setup mocks
        mock_psapi = MagicMock()
        mock_kernel32 = MagicMock()
        mock_ctypes.windll.psapi = mock_psapi
        mock_ctypes.windll.kernel32 = mock_kernel32

        # Mocking the structure class
        with patch("src.utils.system_telemetry.ProcessMemoryCountersEx") as mock_struct_cls:
            instance = mock_struct_cls.return_value
            # Use a PropertyMock for WorkingSetSize
            type(instance).WorkingSetSize = PropertyMock(return_value=100 * 1024 * 1024)

            mock_psapi.GetProcessMemoryInfo.return_value = True
            mock_kernel32.GetCurrentProcess.return_value = 1

            mock_sizeof.return_value = 64
            mock_byref.return_value = "byref_obj"

            ram = get_current_process_ram_mb()
            assert ram == 100.0

    @patch("src.utils.system_telemetry.ctypes")
    def test_get_current_process_ram_mb_failure(self, mock_ctypes):
        mock_ctypes.windll.psapi.GetProcessMemoryInfo.return_value = False
        assert get_current_process_ram_mb() == 0.0

    @patch("src.utils.system_telemetry.ctypes")
    def test_get_current_process_ram_mb_no_windll(self, mock_ctypes):
        # Simula assenza di windll in ctypes per testare il fallback RAM su piattaforme non-Windows
        # Eliminiamo l'attributo dal mock per forzare il ramo condizionale
        with patch("src.utils.system_telemetry.ctypes", spec=[]):
            assert get_current_process_ram_mb() == 0.0
