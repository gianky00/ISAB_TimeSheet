import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.application.services.updater.engine import (
    DownloadWorker,
    get_local_setup_path,
    get_network_update_info,
    get_pending_installer_path,
    get_web_update_info,
    has_pending_update,
    set_pending_installer,
)


class TestUpdaterEngine:
    def test_get_local_setup_path(self):
        url = "http://example.com/myapp.exe"
        path = get_local_setup_path(url)
        assert path.endswith("myapp.exe")

        url_no_exe = "http://example.com/myapp"
        path = get_local_setup_path(url_no_exe)
        assert path.endswith("update_setup.exe")

        win_path = "C:\\Downloads\\installer.exe"
        path = get_local_setup_path(win_path)
        assert path.endswith("installer.exe")

    def test_pending_installer_state(self, tmp_path):
        installer = tmp_path / "setup.exe"
        installer.write_text("dummy")

        set_pending_installer(str(installer))
        assert get_pending_installer_path() == str(installer)
        assert has_pending_update() is True

        # Inexistent file
        set_pending_installer("/non/existent.exe")
        assert has_pending_update() is False

    @patch("src.application.services.updater.engine.requests.get")
    def test_get_web_update_info(self, mock_get):
        from src.application.services import version

        with patch.object(version, "UPDATE_URL", "http://update.com"):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"version": "2.0"}
            mock_get.return_value = mock_resp

            info = get_web_update_info()
            assert info["version"] == "2.0"

    def test_get_network_update_info(self, tmp_path):
        from src.application.services import version

        net_dir = tmp_path / "network"
        net_dir.mkdir()
        v_json = net_dir / "version.json"
        v_json.write_text(json.dumps({"version": "1.5", "url": "setup.exe"}))

        with patch.object(version, "NETWORK_UPDATE_PATH", str(net_dir)):
            info = get_network_update_info()
            assert info["version"] == "1.5"
            assert "network" in info["url"]

    def test_download_worker_network_copy(self, qtbot, tmp_path):
        src = tmp_path / "source.exe"
        src.write_text("A" * 1024 * 10)  # 10KB

        worker = DownloadWorker(str(src))

        with qtbot.wait_signal(worker.finished_download, timeout=5000):
            worker.start()

        worker.wait()  # Ensure thread is done
        dest = Path(get_local_setup_path(str(src)))
        assert dest.exists()
        assert dest.stat().st_size == src.stat().st_size

        if dest.exists():
            dest.unlink()

    def test_download_worker_http_logic_direct(self, tmp_path):
        """Testa la logica di download HTTP chiamando i metodi direttamente (no thread)."""
        url = "http://fake.com/setup_logic.exe"
        worker = DownloadWorker(url)

        # Mock Response info
        mock_resp = MagicMock()
        # iter_content deve restituire un iteratore di bytes
        mock_resp.iter_content.return_value = iter([b"0123456789"])

        # Prepariamo il path di destinazione
        setup_path = get_local_setup_path(url)
        if os.path.exists(setup_path):
            os.remove(setup_path)

        # Mocking _get_http_response
        with patch.object(DownloadWorker, "_get_http_response", return_value=(mock_resp, 0, 10)):
            # Chiamiamo il metodo che gestisce il download
            worker._run_http_download(setup_path)

        assert os.path.exists(setup_path)
        with open(setup_path, "rb") as f:
            content = f.read()
            assert content == b"0123456789"

        if os.path.exists(setup_path):
            os.remove(setup_path)
