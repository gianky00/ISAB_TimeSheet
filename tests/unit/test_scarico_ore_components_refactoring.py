"""
Baseline tests for Scarico Ore Components.
Ensures data processing and tree building logic remains consistent during refactoring.
"""

from src.gui.components.scarico_ore.cache import CacheWorker
from src.gui.components.scarico_ore.filters.popup_date import DateFilterPopupWidget


def test_cache_worker_build_caches_logic(tmp_path):
    """Test the internal logic of _build_caches for data formatting consistency."""
    worker = CacheWorker(tmp_path / "dummy.json")
    # raw_row: 0:data, 1:pers1, 2:pers2, 3:odc, 4:pos, 5:dalle, 6:alle, 7:totale_ore, 8:desc, 9:finito, 10:commessa, 11:style_json
    raw_data = [
        [
            "2025-01-13",
            "Pers1",
            "Pers2",
            "ODC1",
            "10",
            "08:00",
            "17:00",
            8.0,
            "Desc",
            "Sì",
            "C1",
            '{"odc": {"bg": "#FF0000"}}',
        ],
        ["13/01/2025", "U1", None, "5400", "20", "", "", "4,5", None, "No", "", None],
    ]

    display, search, totals, styles, _date_keys = worker._build_caches(raw_data)

    # Check row 1 (ISO Date)

    assert display[0][0] == "13/01/2025"
    assert display[0][1] == "Pers1"
    assert totals[0] == 8.0
    assert styles[0]["odc"]["bg"] == "#FF0000"
    assert "pers1" in search[0]

    # Check row 2 (IT Date and None values)
    assert display[1][0] == "13/01/2025"
    assert display[1][2] == ""  # None converted to ""
    assert display[1][8] == ""  # None converted to ""
    assert totals[1] == 4.5  # 4,5 parsed to float
    assert styles[1] is None


def test_date_filter_tree_building(qtbot):
    """Test hierarchical tree building for date filters."""
    dates = ["13/01/2025", "14/01/2025", "01/02/2025", "10/01/2024"]
    widget = DateFilterPopupWidget(dates)
    qtbot.addWidget(widget)

    model = widget.model
    # 2025 and 2024
    assert model.rowCount() == 2

    # Check 2025 (first row because sorted reverse)
    year_2025 = model.item(0)
    assert year_2025.text() == "2025"
    # Months in 2025: 01 and 02
    assert year_2025.rowCount() == 2

    month_01 = year_2025.child(0)  # Sorted by key
    assert "Gennaio" in month_01.text()
    # Days in Jan 2025: 13 and 14
    assert month_01.rowCount() == 2
    assert month_01.child(0).text() == "13"


def test_date_filter_selection_logic(qtbot):
    """Test that selecting/unselecting nodes correctly updates the result."""
    dates = ["01/01/2025", "02/01/2025"]
    widget = DateFilterPopupWidget(dates, selected_values=["01/01/2025"])
    qtbot.addWidget(widget)

    # Initially only one selected
    selected = widget.get_selected_values()
    assert len(selected) == 1
    assert "01/01/2025" in selected

    # Select all
    widget.select_all()
    assert widget.get_selected_values() is None  # None means all

    # Select none
    widget.select_none()
    assert widget.get_selected_values() == []
