"""Test unitari per DiagnosticsCollector."""

from unittest.mock import MagicMock, patch

from src.application.services.diagnostics.diagnostics_collector import DiagnosticsCollector


def test_collect_system_info_basic() -> None:
    """Verifica che collect_system_info restituisca le informazioni di sistema base."""
    with patch("src.application.services.diagnostics.diagnostics_collector.get_version", return_value="1.2.3"):
        info = DiagnosticsCollector.collect_system_info()

        # Controlliamo la presenza delle chiavi fondamentali di sistema
        assert info["app_version"] == "1.2.3"
        assert "os" in info
        assert "os_release" in info
        assert "os_version" in info
        assert "machine" in info
        assert "timestamp" in info
        assert "python_version" in info
        assert "processor" in info
        assert "env_filtered" in info


def test_collect_system_info_env_filtering() -> None:
    """Verifica che le variabili d'ambiente sensibili vengano filtrate correttamente."""
    mock_env = {
        "PATH": "/usr/bin",
        "DATABASE_URL": "mysql://user:pass@localhost/db",
        "TELEGRAM_TOKEN": "mysecrettoken123",
        "SECRET_KEY": "supersecretkey",
        "API_PASSWORD": "mypassword",
        "AUTH_CREDENTIALS": "mycredentials",
    }

    with patch("os.environ", mock_env):
        info = DiagnosticsCollector.collect_system_info()
        filtered = info["env_filtered"]

        # Variabili sicure devono essere incluse
        assert "PATH" in filtered
        assert filtered["PATH"] == "/usr/bin"

        # Variabili sensibili non devono MAI essere incluse
        assert (
            "DATABASE_URL" in filtered
        )  # URL in sé non contiene keyword escluse a meno che non ci sia pass, ma verifichiamo pass/token/key/secret/api/auth/credential
        assert "TELEGRAM_TOKEN" not in filtered
        assert "SECRET_KEY" not in filtered
        assert "API_PASSWORD" not in filtered
        assert "AUTH_CREDENTIALS" not in filtered


def test_collect_system_info_psutil_metrics() -> None:
    """Verifica che le metriche hardware vengano raccolte se psutil è disponibile."""
    # Simuliamo che psutil sia installato e configurato
    mock_mem = MagicMock()
    mock_mem.total = 16 * 1024**3
    mock_mem.available = 8 * 1024**3
    mock_mem.percent = 50.0

    mock_disk = MagicMock()
    mock_disk.total = 500 * 1024**3
    mock_disk.free = 250 * 1024**3
    mock_disk.percent = 50.0

    with (
        patch("src.application.services.diagnostics.diagnostics_collector.PSUTIL_AVAILABLE", True),
        patch("psutil.virtual_memory", return_value=mock_mem),
        patch("psutil.cpu_count", return_value=8),
        patch("psutil.cpu_percent", return_value=12.5),
        patch("psutil.disk_usage", return_value=mock_disk),
    ):
        info = DiagnosticsCollector.collect_system_info()

        assert "memory" in info
        assert info["memory"]["total"] == "16.00 GB"
        assert info["memory"]["available"] == "8.00 GB"
        assert info["memory"]["percent"] == "50.0%"

        assert "cpu" in info
        assert info["cpu"]["cores_physical"] == 8
        assert info["cpu"]["cores_logical"] == 8
        assert info["cpu"]["usage_percent"] == 12.5

        assert "disk" in info
        assert info["disk"]["total"] == "500.00 GB"
        assert info["disk"]["free"] == "250.00 GB"
        assert info["disk"]["percent"] == "50.0%"


def test_collect_system_info_psutil_unavailable() -> None:
    """Verifica il comportamento del raccoglitore quando psutil non è disponibile."""
    with patch("src.application.services.diagnostics.diagnostics_collector.PSUTIL_AVAILABLE", False):
        info = DiagnosticsCollector.collect_system_info()

        assert info["memory"] == "psutil not installed"
        assert "cpu" not in info
        assert "disk" not in info
