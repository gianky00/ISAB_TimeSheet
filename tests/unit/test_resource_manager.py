from unittest.mock import patch

from src.utils.resource_manager import ResourceManager


class TestResourceManager:
    def test_paths_definitions(self):
        assert ResourceManager.PROJECT_ROOT.exists()
        assert ResourceManager.ASSETS_DIR.exists()
        assert ResourceManager.ICONS_DIR.exists()

    def test_get_icon_logic(self):
        # Mocking Path.exists to test logic without real files
        with patch("src.utils.resource_manager.Path.exists") as mock_exists:
            mock_exists.return_value = True
            path = ResourceManager.get_icon("app")
            assert path.endswith("app.svg")

            path_ico = ResourceManager.get_icon("app.ico")
            assert path_ico.endswith("app.ico")

    def test_get_style_logic(self):
        with patch("src.utils.resource_manager.Path.exists") as mock_exists:
            mock_exists.return_value = True
            path = ResourceManager.get_style("light")
            assert path.endswith("light.qss")

    def test_get_temp_path(self):
        with patch("src.utils.resource_manager.Path.mkdir"):
            path = ResourceManager.get_temp_path("test.txt")
            assert path.name == "test.txt"
            assert "temp" in str(path)
