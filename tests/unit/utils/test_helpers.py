from datetime import datetime

import pytest

from src.utils.helpers import format_timestamp, get_asset_path, get_months_list


def test_get_months_list():
    months = get_months_list()
    assert len(months) == 12
    assert months[0] == "Gennaio"
    assert months[11] == "Dicembre"


def test_format_timestamp():
    # Test con valore esplicito
    dt = datetime(2026, 5, 17, 12, 0, 0)
    formatted = format_timestamp(dt)
    assert formatted == "17/05/2026 12:00:00"

    # Test default (now)
    now_formatted = format_timestamp()
    assert len(now_formatted) > 0
    assert "/" in now_formatted


def test_get_asset_path():
    # Mockando ResourceManager (dipendenza esterna)
    with pytest.MonkeyPatch.context() as m:
        m.setattr("src.utils.resource_manager.ResourceManager.get_asset_path", lambda p: f"/mocked/{p}")
        path = get_asset_path("test.png")
        assert path == "/mocked/test.png"
