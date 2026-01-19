"""
Baseline tests for AuditLogWidget refresh logic.
"""

import pytest

from src.gui.notifications_panel import AuditLogWidget


@pytest.fixture
def audit_widget(qtbot, mocker):
    # Mock manager to avoid real DB access
    # We must mock the .instance() call as it's a singleton
    m_manager_class = mocker.patch("src.gui.notifications_panel.AuditManager")
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

    widget = AuditLogWidget()
    qtbot.addWidget(widget)
    return widget


def test_audit_refresh_population(audit_widget):
    """Test that logs are correctly populated in the table."""
    audit_widget.refresh()
    assert audit_widget.table.rowCount() == 2

    # Check first row (success)
    assert audit_widget.table.item(0, 2).text() == "LOGIN"
    assert audit_widget.table.item(0, 5).text() == "SUCCESS"

    # Check second row (error colors)
    error_item = audit_widget.table.item(1, 5)
    assert error_item.text() == "ERROR"
    # high severity/error status should have red-ish foreground
    assert error_item.foreground().color().name().lower() in ["#dc3545", "#ff0000"]


def test_integrity_display(audit_widget, mocker):
    """Test integrity label updates."""
    # Test valid
    audit_widget.manager.verify_integrity.return_value = True
    audit_widget.refresh()
    assert "✅" in audit_widget.integrity_lbl.text()

    # Test manipulated
    audit_widget.manager.verify_integrity.return_value = False
    audit_widget.refresh()
    assert "⚠️" in audit_widget.integrity_lbl.text()
