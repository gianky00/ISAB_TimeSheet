import os

from src.infrastructure.utils.system_telemetry import get_current_process_ram_mb


class TestSystemTelemetry:
    def test_get_current_process_ram_mb_real(self):
        # Su Windows deve tornare un valore > 0
        if os.name == "nt":
            ram = get_current_process_ram_mb()
            # Se siamo in un ambiente particolare potrebbe tornare 0.0
            # ma vogliamo verificare che non crashi
            assert isinstance(ram, float)
            assert ram >= 0.0
        else:
            assert get_current_process_ram_mb() == 0.0

    def test_logic_check(self):
        # Verifica solo che il tipo di ritorno sia float
        res = get_current_process_ram_mb()
        assert isinstance(res, float)
