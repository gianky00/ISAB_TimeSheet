"""
Baseline tests for Icon Generator.
"""

import os
import sys
from pathlib import Path

# Add path with spaces to sys.path
script_path = Path(__file__).parent.parent.parent / "admin" / "Crea Setup"
sys.path.append(str(script_path))

from generate_icons import create_modern_icon  # noqa: E402


def test_icon_generation_output(tmp_path):
    """Test that the icon file is physically created and has content."""
    filename = str(tmp_path / "test_icon.ico")
    text = "TS"
    bg = (0, 150, 136, 255)
    txt_color = (255, 255, 255, 255)
    accent = (0, 121, 107, 255)

    create_modern_icon(text, bg, txt_color, filename, accent)

    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0
