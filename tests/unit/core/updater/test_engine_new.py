import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

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
    @pytest.fixture(autouse=True)
    def mock_sleep(self):
        with patch("time.sleep", return_value=None):
            yield

    def test_get_local_setup_path(self):
        url = "http://example.com/setup.exe"
        path = get_local_setup_path(url)
        assert path.endswith("setup.exe")

        path_net = "\\\\server\\share\\update.msi"
        path = get_local_setup_path(path_net)
        assert path.endswith("update_setup.exe")

    @patch("src.core.updater.engine.requests.get")
    def test_run_http_download_success(self, mock_get, fs):
        setup_path = "/tmp/setup.exe"
        fs.create_dir("/tmp")

        # Simula risposta HTTP con chunk
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.headers = {"content-length": "10"}
        # iter_content deve tornare un iteratore
        mock_res.iter_content.return_value = iter([b"01234", b"56789"])
        mock_get.return_value = mock_res

        worker = DownloadWorker("http://test.com/s.exe")
        with patch("src.core.updater.engine.get_local_setup_path", return_value=setup_path):
            # Invece di _run_http_download che ha il loop di retry, testiamo lo stream
            # Ma vogliamo testare che il loop finisca.
            # Assicuriamoci che total_size e downloaded coincidano.
            worker._run_http_download(setup_path)

        assert Path(setup_path).exists()
        assert Path(setup_path).read_bytes() == b"0123456789"

    def test_run_network_copy_success(self, fs):
        src = "/net/setup.exe"
        dst = "/tmp/setup.exe"
        fs.create_file(src, contents=b"NET_DATA")
        fs.create_dir("/tmp")

        worker = DownloadWorker(src)
        worker._run_network_copy(dst)

        assert Path(dst).read_bytes() == b"NET_DATA"

    @patch("src.core.updater.engine.requests.get")
    def test_get_web_update_info(self, mock_get):
        with patch("src.core.version.UPDATE_URL", "http://up.it"):
            mock_res = MagicMock()
            mock_res.status_code = 200
            mock_res.json.return_value = {"version": "2.0"}
            mock_get.return_value = mock_res

            info = get_web_update_info()
            assert info["version"] == "2.0"

    def test_get_network_update_info(self, fs):
        net_dir = "/volumes/share"
        fs.create_dir(net_dir)
        fs.create_file(net_dir + "/version.json", contents=json.dumps({"version": "3.0", "url": "setup.exe"}))

        with patch("src.core.version.NETWORK_UPDATE_PATH", net_dir):
            info = get_network_update_info()
            assert info["version"] == "3.0"
            assert "setup.exe" in info["url"]

    def test_pending_update_logic(self, fs):
        fake_path = "/tmp/pending.exe"
        fs.create_file(fake_path)

        set_pending_installer(fake_path)
        assert has_pending_update() is True

        set_pending_installer(None)
        # Non serve più il file per has_pending_update se resettiamo la variabile globale
        # ma assicuriamoci di pulire
        assert has_pending_update() is False

    @patch("src.core.updater.engine.subprocess.Popen")
    @patch("src.core.updater.engine.sys.exit")
    def test_run_installer_and_exit(self, mock_exit, mock_popen, fs):
        setup = "/tmp/inst.exe"
        fs.create_file(setup)

        run_installer_and_exit(setup)

        assert mock_popen.called
        assert mock_exit.called
