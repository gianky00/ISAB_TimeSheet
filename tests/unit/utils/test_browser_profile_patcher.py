import json
from pathlib import Path
from unittest.mock import patch

from src.utils.browser_profile_patcher import _patch_file, _set_nested_value, patch_browser_profile


class TestBrowserProfilePatcher:
    def test_set_nested_value(self):
        d = {"a": {"b": 1}}
        # Cambia valore esistente
        assert _set_nested_value(d, "a.b", 2) is True
        assert d["a"]["b"] == 2

        # Aggiunge nuovo valore
        assert _set_nested_value(d, "a.c", 3) is True
        assert d["a"]["c"] == 3

        # Crea percorso intermedio
        assert _set_nested_value(d, "x.y.z", 10) is True
        assert d["x"]["y"]["z"] == 10

        # Valore uguale non cambia
        assert _set_nested_value(d, "a.b", 2) is False

    def test_patch_file_creates_new(self, fs):
        path = Path("/fake/prefs")
        download_path = Path("/downloads")

        assert _patch_file(path, download_path) is True
        assert path.exists()

        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["password_manager"]["enabled"] is False
        assert data["download"]["default_directory"] == str(download_path)

    def test_patch_file_modifies_existing(self, fs):
        path = Path("/fake/prefs")
        fs.create_file(str(path), contents=json.dumps({"a": 1, "password_manager": {"enabled": True}}))

        assert _patch_file(path, Path("/dl")) is True
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["a"] == 1
        assert data["password_manager"]["enabled"] is False

    @patch("src.utils.browser_profile_patcher._patch_file")
    def test_patch_browser_profile_logic(self, mock_patch_file, fs):
        user_dir = Path("/user_data")
        fs.create_dir(str(user_dir))

        # Simula che il file Preferences esista nella root
        fs.create_file(str(user_dir / "Preferences"))

        res = patch_browser_profile(user_dir, "/dl")

        assert res is True
        # Deve aver tentato di patchare Default/Preferences e Preferences
        assert mock_patch_file.call_count >= 1

    def test_patch_browser_profile_integration(self, fs):
        user_dir = Path("/user_data_int")
        # Nessun file esiste -> ne crea uno in Default/Preferences
        patch_browser_profile(user_dir)

        pref_file = user_dir / "Default" / "Preferences"
        assert pref_file.exists()
        data = json.loads(pref_file.read_text(encoding="utf-8"))
        assert data["password_manager"]["enabled"] is False
