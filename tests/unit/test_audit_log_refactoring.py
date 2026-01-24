"""
Baseline tests for AuditLogWidget refresh logic.
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtGui import QIcon, QPixmap

from src.gui.panels.notifications_panel import AuditLogWidget


@pytest.fixture
def audit_widget(qtbot, mocker):
    # Mock manager to avoid real DB access
    m_manager_class = mocker.patch("src.gui.panels.notifications_panel.AuditManager")
    m_instance = m_manager_class.instance.return_value

    m_instance.verify_integrity.return_value = True
    m_instance.get_logs.return_value = [
        {
            "timestamp": "2025-01-13T10:00:00",
            "user_id": "admin",
            "action": "LOGIN",
            "entity": "SYSTEM",
            "params": "{}",
            "status": "success",
            "severity": "low",
        },
        {
            "timestamp": "2025-01-13T10:05:00",
            "user_id": "admin",
            "action": "ERROR_OP",
            "entity": "DATABASE",
            "params": '{"id": 1}',
            "status": "error",
            "severity": "high",
        },
    ]
    # Mock get_filtered_logs to return the list + count
    m_instance.get_filtered_logs.return_value = (m_instance.get_logs.return_value, 2)

    # CRITICAL: Mock icons and assets to prevent crashes in headless environment
    dummy_pixmap = QPixmap(10, 10)
    dummy_pixmap.fill(0)
    dummy_icon = QIcon(dummy_pixmap)

    mocker.patch(
        "src.gui.panels.notifications_panel.get_asset_path", return_value="dummy.svg"
    )
    mocker.patch(
        "src.gui.panels.notifications_panel.get_colored_icon", return_value=dummy_icon
    )
    mocker.patch("src.gui.models.audit_model.get_asset_path", return_value="dummy.svg")
    mocker.patch("src.gui.models.audit_model.get_colored_icon", return_value=dummy_icon)

    # CRITICAL: Mock QTimer to prevent background live refresh
    with patch("PyQt6.QtCore.QTimer"):
        widget = AuditLogWidget()
        # MOCK UI Heavy operations that cause crashes in CI
        widget.table_view.resizeColumnsToContents = MagicMock()
        widget.table_view.setColumnWidth = MagicMock()
        widget.table_view.columnWidth = MagicMock(return_value=100)

        qtbot.addWidget(widget)
        return widget


@pytest.mark.skipif(
    os.environ.get("CI") == "true", reason="Skipping Qt heavy test in CI"
)
def test_audit_refresh_population(audit_widget):
    """Test that logs are correctly populated in the table."""
    audit_widget.refresh()
    model = audit_widget.model
    assert model.rowCount() == 2

    # Check first row (Action is col 5 in AuditTableModel)
    idx_action = model.index(0, 5)
    assert model.data(idx_action, 0) == "LOGIN"

    # Check second row (Action is col 5)
    idx_error = model.index(1, 5)
    assert model.data(idx_error, 0) == "ERROR_OP"

    # Verify background color for error row (BackgroundRole is 8)
    idx_bg = model.index(1, 0)
    bg_color = model.data(idx_bg, 8)
    assert bg_color is not None
    assert bg_color.name() == "#fff5f5"


@pytest.mark.skipif(
    os.environ.get("CI") == "true", reason="Skipping Qt heavy test in CI"
)
def test_integrity_display(audit_widget, mocker):
    """Test integrity label updates."""
    # Test valid
    audit_widget.manager.verify_integrity.return_value = True
    audit_widget.refresh()
    assert "Integro" in audit_widget.integrity_lbl.text()

    # Test manipulated
    audit_widget.manager.verify_integrity.return_value = False
    audit_widget.refresh()
    assert "Legacy/Manomesso" in audit_widget.integrity_lbl.text()
