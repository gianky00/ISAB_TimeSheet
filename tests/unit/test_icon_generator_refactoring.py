"""
Baseline tests for Icon Generator.
"""

import sys
from pathlib import Path

# Add path with spaces to sys.path
script_path = Path(__file__).parent.parent.parent / "admin" / "Crea Setup"
sys.path.append(str(script_path))

from generate_icons import generate_icons  # noqa: E402


def test_icon_generation_output(tmp_path, monkeypatch):  # noqa: ANN001
    """Test that the icon files are physically created in the assets directory."""
    # Mock get_assets_path to use tmp_path
    monkeypatch.setattr("generate_icons.get_assets_path", lambda: tmp_path)

    generate_icons()

    app_ico = tmp_path / "app.ico"
    setup_ico = tmp_path / "setup.ico"

    assert app_ico.exists()
    assert app_ico.stat().st_size > 0
    assert setup_ico.exists()
    assert setup_ico.stat().st_size > 0
