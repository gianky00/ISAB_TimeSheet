import pytest

from src.infrastructure.utils.resource_manager import ResourceManager


class TestResourceManager:
    @pytest.fixture(autouse=True)
    def setup_test(self, tmp_path, mocker):
        # Mock PROJECT_ROOT
        mocker.patch("src.infrastructure.utils.resource_manager.ResourceManager.PROJECT_ROOT", tmp_path)
        # Mock _get_config_dir to return our tmp config path
        mocker.patch(
            "src.infrastructure.utils.resource_manager.ResourceManager._get_config_dir",
            return_value=tmp_path / "config",
        )
        # Update other class attrs derived from PROJECT_ROOT
        mocker.patch("src.infrastructure.utils.resource_manager.ResourceManager.ASSETS_DIR", tmp_path / "assets")
        mocker.patch(
            "src.infrastructure.utils.resource_manager.ResourceManager.ICONS_DIR",
            tmp_path / "assets" / "icons",
        )
        mocker.patch(
            "src.infrastructure.utils.resource_manager.ResourceManager.STYLES_DIR",
            tmp_path / "assets" / "styles",
        )
        mocker.patch("src.infrastructure.utils.resource_manager.ResourceManager.TEMP_DIR", tmp_path / "temp")
        yield

    def test_ensure_structure(self, tmp_path):
        ResourceManager.ensure_structure()
        assert (tmp_path / "temp").exists()
        assert (tmp_path / "config" / "data").exists()
        assert (tmp_path / "config" / "logs").exists()

    def test_get_icon(self, tmp_path):
        icon_dir = tmp_path / "assets" / "icons"
        icon_dir.mkdir(parents=True)
        (icon_dir / "test.svg").touch()

        path = ResourceManager.get_icon("test")
        assert path.endswith("test.svg")

        # Non existent
        assert ResourceManager.get_icon("missing") == ""

    def test_get_style(self, tmp_path):
        style_dir = tmp_path / "assets" / "styles"
        style_dir.mkdir(parents=True)
        (style_dir / "dark.qss").touch()

        path = ResourceManager.get_style("dark")
        assert path.endswith("dark.qss")

    def test_get_temp_path(self, tmp_path):
        path = ResourceManager.get_temp_path("session.tmp")
        assert str(path).startswith(str(tmp_path / "temp"))
        assert path.name == "session.tmp"
