import json
from pathlib import Path

from src.utils.browser_profile_patcher import _patch_file, _set_nested_value, patch_browser_profile


class TestBrowserProfilePatcher:
    def test_set_nested_value(self):
        dic = {"a": {"b": 1}}
        assert _set_nested_value(dic, "a.b", 2) is True
        assert dic["a"]["b"] == 2
        assert _set_nested_value(dic, "a.b", 2) is False
        assert _set_nested_value(dic, "x.y.z", 10) is True
        assert dic["x"]["y"]["z"] == 10

    def test_patch_browser_profile_new(self, fs):
        user_dir = "/tmp/chrome"
        fs.create_dir(user_dir)
        down_dir = "/tmp/down"

        success = patch_browser_profile(user_dir, download_dir=down_dir)

        assert success is True
        pref_path = Path(user_dir) / "Default" / "Preferences"
        assert pref_path.exists()

        with pref_path.open("r") as f:
            data = json.load(f)
            assert data["password_manager"]["enabled"] is False
            # Confronto agnostico rispetto al sistema (posix)
            actual_dir = Path(data["download"]["default_directory"]).as_posix()
            expected_dir = Path(down_dir).as_posix()
            assert actual_dir.endswith("/tmp/down")

    def test_patch_browser_profile_existing(self, fs):
        user_dir = "/tmp/chrome"
        pref_path = Path(user_dir) / "Preferences"
        fs.create_file(str(pref_path), contents='{"password_manager": {"enabled": true}}')

        success = patch_browser_profile(user_dir)

        assert success is True
        with pref_path.open("r") as f:
            data = json.load(f)
            assert data["password_manager"]["enabled"] is False

    def test_patch_file_direct_error(self, fs):
        path = Path("/tmp/bad.json")
        fs.create_file(str(path), contents="invalid json")
        assert _patch_file(path, download_path=Path("/tmp")) is False

    def test_patch_browser_profile_recovery(self, fs):
        user_dir = "/tmp/chrome"
        fs.create_file(str(Path(user_dir) / "Preferences"), contents="!!!")
        success = patch_browser_profile(user_dir)
        assert success is True
        assert (Path(user_dir) / "Default" / "Preferences").exists()
