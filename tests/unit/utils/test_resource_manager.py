from unittest.mock import patch

import pytest

from src.utils.resource_manager import ResourceManager


class TestResourceManager:
    @pytest.fixture(autouse=True)
    def setup_fs(self, fs):
        # pyfakefs needs the base directory to exist for some operations
        # and ResourceManager.PROJECT_ROOT points to BASE_DIR which is the real CWD
        fs.create_dir(str(ResourceManager.PROJECT_ROOT))
        fs.create_dir(str(ResourceManager.ASSETS_DIR))
        fs.create_dir(str(ResourceManager.ICONS_DIR))
        fs.create_dir(str(ResourceManager.STYLES_DIR))
        fs.create_dir(str(ResourceManager.TEMP_DIR))
        fs.create_dir(str(ResourceManager._get_config_dir()))

    def test_project_root_detection_non_frozen(self):
        assert ResourceManager.PROJECT_ROOT is not None

    def test_get_config_dir(self):
        assert ResourceManager._get_config_dir() is not None

    def test_get_logs_dir(self):
        log_dir = ResourceManager.get_logs_dir()
        assert log_dir.name == "logs"

    def test_get_data_dir(self):
        data_dir = ResourceManager.get_data_dir()
        assert data_dir.name == "data"

    def test_get_asset_path(self):
        path = ResourceManager.get_asset_path("icons/test.svg")
        assert "icons" in path
        assert "test.svg" in path

    def test_get_icon(self, fs):
        icon_path = ResourceManager.ICONS_DIR / "test_icon.svg"
        fs.create_file(str(icon_path))

        assert ResourceManager.get_icon("test_icon.svg") == str(icon_path)
        assert ResourceManager.get_icon("test_icon") == str(icon_path)
        assert ResourceManager.get_icon("non_existent") == ""

    def test_get_style(self, fs):
        style_path = ResourceManager.STYLES_DIR / "light.qss"
        fs.create_file(str(style_path))
        assert ResourceManager.get_style("light") == str(style_path)

    def test_get_temp_path(self):
        tmp = ResourceManager.get_temp_path("test.tmp")
        assert tmp.name == "test.tmp"
        assert tmp.parent == ResourceManager.TEMP_DIR

    @patch("src.utils.resource_manager.shutil.copy2")
    @patch("webdriver_manager.chrome.ChromeDriverManager.install")
    def test_ensure_automation_driver_download(self, mock_install, mock_copy, fs):
        # Driver non esistente
        d_exe = ResourceManager.get_writable_drivers_dir() / "chromedriver.exe"
        if fs.exists(str(d_exe)):
            fs.remove(str(d_exe))

        mock_install.return_value = "/fake/download/chromedriver.exe"
        fs.create_file("/fake/download/chromedriver.exe")

        path = ResourceManager.ensure_automation_driver()
        assert path is not None
        assert mock_install.called

    def test_ensure_automation_driver_existing(self, fs):
        d_exe = ResourceManager.get_writable_drivers_dir() / "chromedriver.exe"
        fs.create_file(str(d_exe))

        path = ResourceManager.ensure_automation_driver()
        assert path == str(d_exe.resolve())

    def test_ensure_structure(self):
        ResourceManager.ensure_structure()
        assert ResourceManager.TEMP_DIR.exists()
        assert ResourceManager.get_logs_dir().exists()
        assert ResourceManager.get_data_dir().exists()
