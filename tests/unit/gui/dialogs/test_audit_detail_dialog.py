"""Unit tests for AuditDetailDialog."""

import json
from unittest.mock import MagicMock

import pytest

from src.gui.dialogs.audit_detail_dialog import AuditDetailDialog


@pytest.fixture
def log_data():
    """Mock di un log di audit."""
    return {
        "timestamp": "2026-05-24T10:00:00",
        "module": "TEST_MOD",
        "user_id": "test_user",
        "action": "ACTION_X",
        "status": "success",
        "duration_ms": 1500,
        "params": json.dumps({"key": "value", "id": 123}),
    }


class TestAuditDetailDialog:
    """Test suite per AuditDetailDialog."""

    def test_initialization(self, qtbot, log_data):
        """Verifica lbl'inizializzazione del dialog con i dati forniti."""
        dialog = AuditDetailDialog(log_data)
        qtbot.addWidget(dialog)

        assert dialog.windowTitle() == "Dettagli Audit Log"

        # Verifica contenuto tabella info
        from PySide6.QtWidgets import QLabel

        labels = dialog.findChildren(QLabel)
        header_text = labels[0].text()  # La prima label ha la tabella HTML
        assert "TEST_MOD" in header_text
        assert "test_user" in header_text
        assert "1.50s" in header_text  # 1500ms -> 1.50s

        # Verifica JSON viewer
        json_text = dialog.text_edit.toPlainText()
        assert '"key": "value"' in json_text

    def test_copy_to_clipboard(self, qtbot, log_data, mocker):
        """Verifica la copia negli appunti."""
        from PySide6.QtGui import QGuiApplication

        mock_cb = MagicMock()
        mocker.patch.object(QGuiApplication, "clipboard", return_value=mock_cb)
        mocker.patch("PySide6.QtWidgets.QMessageBox.information")

        dialog = AuditDetailDialog(log_data)
        qtbot.addWidget(dialog)

        dialog._copy_to_clipboard()

        assert mock_cb.setText.called
        assert '"id": 123' in mock_cb.setText.call_args[0][0]

    def test_invalid_json_handling(self, qtbot):
        """Verifica la gestione di JSON corrotto nei params."""
        bad_data = {"params": "{invalid json", "action": "test"}
        dialog = AuditDetailDialog(bad_data)
        qtbot.addWidget(dialog)

        assert dialog.text_edit.toPlainText() == "{invalid json"

    def test_no_params_handling(self, qtbot):
        """Verifica comportamento senza params."""
        data = {"action": "no_params"}
        dialog = AuditDetailDialog(data)
        qtbot.addWidget(dialog)

        assert "{}" in dialog.text_edit.toPlainText()  # Default {} if missing
