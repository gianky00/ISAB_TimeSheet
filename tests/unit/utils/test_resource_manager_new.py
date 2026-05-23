from unittest.mock import patch

import pytest

from src.utils.resource_manager import ResourceManager


class TestResourceManager:
    @pytest.fixture(autouse=True)
    def setup_fs(self, fs):
        # Assicura che la root esista per evitare FileNotFoundError
        fs.create_dir(str(ResourceManager.PROJECT_ROOT))
        fs.create_dir(str(ResourceManager.TEMP_DIR))
        fs.create_dir(str(ResourceManager.ASSETS_DIR))
        fs.create_dir(str(ResourceManager.ICONS_DIR))
        fs.create_dir(str(ResourceManager.STYLES_DIR))

    def test_get_asset_path(self):
        path = ResourceManager.get_asset_path("icons/test.svg")
        assert "assets" in path
        assert "icons" in path
        assert "test.svg" in path

    def test_get_icon_found(self, fs):
        icon_path = ResourceManager.ICONS_DIR / "check.svg"
        fs.create_file(str(icon_path))

        assert ResourceManager.get_icon("check") == str(icon_path)

    def test_get_icon_not_found(self):
        assert ResourceManager.get_icon("nonexistent") == ""

    def test_get_style(self, fs):
        style_path = ResourceManager.STYLES_DIR / "dark.qss"
        fs.create_file(str(style_path))
        assert ResourceManager.get_style("dark") == str(style_path)

    def test_get_temp_path(self, fs):
        res = ResourceManager.get_temp_path("test.txt")
        assert res.name == "test.txt"
        assert ResourceManager.TEMP_DIR in res.parents

    @patch("webdriver_manager.chrome.ChromeDriverManager.install")
    @patch("src.utils.resource_manager.shutil.copy2")
    def test_ensure_automation_driver_download(self, mock_copy, mock_install, fs):
        # Driver non esiste
        d_dir = ResourceManager.get_writable_drivers_dir()
        d_exe = d_dir / "chromedriver.exe"
        if fs.exists(str(d_exe)):
            fs.remove(str(d_exe))

        # Patching webdriver_manager directly since it's a local import in implementation
        mock_install.return_value = "/downloaded/chromedriver.exe"
        fs.create_file("/downloaded/chromedriver.exe")

        # Forziamo reload dei moduli se necessario o patchiamo l'import dove avviene
        # Poiché l'import è locale, patchare il modulo di origine dovrebbe funzionare
        res = ResourceManager.ensure_automation_driver()
        assert res == str(d_exe.resolve())
        assert mock_copy.called

    def test_ensure_automation_driver_exists(self, fs):
        d_dir = ResourceManager.get_writable_drivers_dir()
        d_exe = d_dir / "chromedriver.exe"
        fs.create_file(str(d_exe))

        res = ResourceManager.ensure_automation_driver()
        assert res == str(d_exe.resolve())

    def test_ensure_structure(self, fs):
        cfg = ResourceManager._get_config_dir()
        ResourceManager.ensure_structure()
        assert (cfg / "logs").exists()
        assert (cfg / "data").exists()
        assert ResourceManager.TEMP_DIR.exists()
