import sys

import pytest
from PySide6.QtWidgets import QApplication

from src.gui.dialogs.account_dialog import AccountDialog


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    return app


def test_account_dialog_initialization(qapp):
    dialog = AccountDialog(username="user1", password="pw1")
    assert dialog.username_edit.text() == "user1"
    assert dialog.password_edit.text() == "pw1"


def test_password_visibility(qapp):
    dialog = AccountDialog(password="secret")

    # Check default (Password)
    from PySide6.QtWidgets import QLineEdit

    assert dialog.password_edit.echoMode() == QLineEdit.EchoMode.Password

    # Toggle visibility
    dialog._toggle_password_visibility()
    assert dialog.password_edit.echoMode() == QLineEdit.EchoMode.Normal

    # Toggle back
    dialog._toggle_password_visibility()
    assert dialog.password_edit.echoMode() == QLineEdit.EchoMode.Password


def test_get_data(qapp):
    dialog = AccountDialog(username="u", password="p", account_type="ISAB", show_type=True)
    assert dialog.get_data() == ("u", "p", "ISAB")
