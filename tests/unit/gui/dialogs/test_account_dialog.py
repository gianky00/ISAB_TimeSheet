"""Unit tests for AccountDialog."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit

from src.gui.dialogs.account_dialog import AccountDialog


class TestAccountDialog:
    """Test suite per AccountDialog."""

    def test_initialization(self, qtbot):
        dialog = AccountDialog(username="user1", password="pw1", account_type="ISAB", show_type=True)
        qtbot.addWidget(dialog)

        assert dialog.username_edit.text() == "user1"
        assert dialog.password_edit.text() == "pw1"
        assert dialog.password_edit.echoMode() == QLineEdit.EchoMode.Password
        assert dialog.type_combo.currentText() == "ISAB"
        assert not dialog.type_combo.isHidden()

    def test_initialization_no_type(self, qtbot):
        dialog = AccountDialog(show_type=False)
        qtbot.addWidget(dialog)
        assert dialog.type_combo.isHidden()

    def test_toggle_password_visibility(self, qtbot):
        dialog = AccountDialog(password="secret")
        qtbot.addWidget(dialog)

        # Inizialmente nascosta
        assert dialog.password_edit.echoMode() == QLineEdit.EchoMode.Password

        # Click occhio -> Mostra
        qtbot.mouseClick(dialog.toggle_pass_btn, Qt.MouseButton.LeftButton)
        assert dialog.password_edit.echoMode() == QLineEdit.EchoMode.Normal

        # Click occhio -> Nascondi
        qtbot.mouseClick(dialog.toggle_pass_btn, Qt.MouseButton.LeftButton)
        assert dialog.password_edit.echoMode() == QLineEdit.EchoMode.Password

    def test_get_data(self, qtbot):
        dialog = AccountDialog()
        qtbot.addWidget(dialog)

        dialog.username_edit.setText("new_user")
        dialog.password_edit.setText("new_pw")
        dialog.type_combo.setCurrentText("Esecutore")

        u, p, t = dialog.get_data()
        assert u == "new_user"
        assert p == "new_pw"
        assert t == "Esecutore"

    def test_accept_reject(self, qtbot):
        dialog = AccountDialog()
        qtbot.addWidget(dialog)

        # Ok
        with qtbot.waitSignal(dialog.accepted):
            dialog.accept()

        # Reject
        dialog2 = AccountDialog()
        qtbot.addWidget(dialog2)
        with qtbot.waitSignal(dialog2.rejected):
            dialog2.reject()
        # Nota: usiamo i bottoni reali nel codice se possibile per testare la connessione
