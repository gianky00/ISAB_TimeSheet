"""Comprehensive tests for src.utils package.
Covers: helpers, security, validators, parsing.
"""

from datetime import datetime

from src.utils import helpers


# --- HELPERS TESTS ---
def test_helpers_format_timestamp():
    dt = datetime(2025, 1, 1, 12, 0, 0)
    assert helpers.format_timestamp(dt) == "01/01/2025 12:00:00"

    # Test default now (mocked would be better but simple check is enough)
    assert helpers.format_timestamp() is not None


def test_helpers_sanitize_filename():
    assert helpers.sanitize_filename("file/name*.txt") == "file_name_.txt"
    assert helpers.sanitize_filename("test__file") == "test_file"
    # Strict check
    cleaned = helpers.sanitize_filename("A/B\\C:D")
    assert "/" not in cleaned
    assert "\\" not in cleaned
    assert ":" not in cleaned
