import json
import os
from unittest.mock import MagicMock, patch

from src.core.updater.engine import (
    DownloadWorker,
    get_local_setup_path,
    get_network_update_info,
    get_web_update_info,
    has_pending_update,
    run_installer_and_exit,
    set_pending_installer,
)


class TestUpdaterEngine:
    def test_get_local_setup_path(self):
        url = "http://example.com/setup.exe"
        path = get_local_setup_path(url)
        assert path.endswith("setup.exe")

    @patch("src.core.updater.engine.requests.get")
    def test_get_web_update_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"version": "1.2.3"}
        mock_get.return_value = mock_response
        with patch("src.core.version.UPDATE_URL", "http://update.com"):
            assert get_web_update_info() == {"version": "1.2.3"}

    def test_get_network_update_info_success(self, fs):
        net_path = "/fake/network"
        fs.create_dir(net_path)
        fs.create_file(
            f"{net_path}/version.json", contents=json.dumps({"version": "2.0.0", "url": "setup.exe"})
        )
        with patch("src.core.version.NETWORK_UPDATE_PATH", net_path):
            info = get_network_update_info()
            assert info["version"] == "2.0.0"

    def test_pending_update_state(self, fs):
        installer = "/tmp/installer.exe"
        fs.create_file(installer)
        set_pending_installer(installer)
        assert has_pending_update() is True

    @patch("src.core.updater.engine.subprocess.Popen")
    @patch("src.core.updater.engine.sys.exit")
    def test_run_installer_and_exit(self, mock_exit, mock_popen, fs):
        setup_path = "/tmp/setup.exe"
        fs.create_file(setup_path)
        run_installer_and_exit(setup_path)
        assert mock_popen.called

    @patch("src.core.updater.engine.requests.get")
    def test_download_worker_http(self, mock_get, fs):
        url = "http://example.com/setup.exe"
        setup_path = get_local_setup_path(url)

        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-length": "10"}
        mock_response.iter_content.return_value = iter([b"0123456789"])
        mock_get.return_value = mock_response

        worker = DownloadWorker(url)
        # Forza terminazione impostando _is_cancelled dopo la prima iterazione o mockando bene
        # In realtà iter_content finirà e _stream_download uscirà.
        # Il problema è il loop esterno in _run_http_download che ricontrolla downloaded >= total_size

        finished_path = None

        def on_finished(p):
            nonlocal finished_path
            finished_path = p

        worker.finished_download.connect(on_finished)

        # Eseguiamo run()
        worker.run()

        assert finished_path is not None
        assert os.path.exists(setup_path)

    def test_download_worker_network(self, fs):
        src_path = "/net/setup.exe"
        fs.create_file(src_path, contents=b"net_content")
        setup_path = get_local_setup_path(src_path)

        worker = DownloadWorker(src_path)
        finished_path = None

        def on_finished(p):
            nonlocal finished_path
            finished_path = p

        worker.finished_download.connect(on_finished)

        worker.run()
        assert finished_path == setup_path
