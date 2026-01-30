"""
SyncroJob - Admin Secret Manager
Gestione sicura delle API Key nel Keyring di Windows.
"""

import sys

import keyring
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SecretItem(QFrame):
    def __init__(self, app_name, service_label, secret_key, parent=None):
        super().__init__(parent)
        self.app_name = app_name
        self.service_label = service_label
        self.secret_key = secret_key

        self.setStyleSheet(
            """
            SecretItem {
                background-color: white;
                border: 1px solid black;
                border-radius: 8px;
                padding: 10px;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"🔑 {service_label}"))

        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        self.input.setPlaceholderText("Chiave API...")
        self.input.setMinimumHeight(35)

        current_val = keyring.get_password(self.app_name, self.secret_key)
        if current_val:
            self.input.setText(current_val)

        row.addWidget(self.input)

        self.toggle_btn = QPushButton("👁️")
        self.toggle_btn.setFixedSize(35, 35)
        self.toggle_btn.clicked.connect(self._toggle)
        row.addWidget(self.toggle_btn)

        self.save_btn = QPushButton("Salva")
        self.save_btn.setMinimumHeight(35)
        self.save_btn.setStyleSheet(
            "font-weight: bold; border: 1px solid black; background: white;"
        )
        self.save_btn.clicked.connect(self._save)
        row.addWidget(self.save_btn)

        layout.addLayout(row)

    def _toggle(self):
        self.input.setEchoMode(
            QLineEdit.EchoMode.Normal
            if self.input.echoMode() == QLineEdit.EchoMode.Password
            else QLineEdit.EchoMode.Password
        )

    def _save(self):
        val = self.input.text().strip()
        try:
            if val:
                keyring.set_password(self.app_name, self.secret_key, val)
                QMessageBox.information(self, "OK", "Salvato.")
            else:
                keyring.delete_password(self.app_name, self.secret_key)
                QMessageBox.information(self, "OK", "Rimosso.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))


class AdminSecretsGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Secrets - SyncroJob")
        self.setFixedWidth(500)
        self.APP_NAME = "SyncroJob"
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("🛡️ Gestione API Key Admin"))

        container = QWidget()
        self.secrets_layout = QVBoxLayout(container)

        # Aggiungi qui le chiavi necessarie
        self.secrets_layout.addWidget(
            SecretItem(self.APP_NAME, "Exa API Key", "exa_api_key")
        )
        self.secrets_layout.addWidget(
            SecretItem(self.APP_NAME, "GitHub API Token", "github_api_key")
        )
        self.secrets_layout.addWidget(
            SecretItem(self.APP_NAME, "OpenAI API Key", "openai_api_key")
        )

        self.secrets_layout.addStretch()
        layout.addWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = AdminSecretsGUI()
    gui.show()
    sys.exit(app.exec())
