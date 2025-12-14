import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox, QFormLayout, QGroupBox,
                               QTextEdit)
from PySide6.QtCore import Qt
from utils.config import load_config, save_config
from bot.worker import BotWorker

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        group_box = QGroupBox("Credenziali Portale Fornitori")
        form_layout = QFormLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setText(self.config.get("username", ""))

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setText(self.config.get("password", ""))

        form_layout.addRow("Username:", self.username_edit)
        form_layout.addRow("Password:", self.password_edit)

        group_box.setLayout(form_layout)
        layout.addWidget(group_box)

        save_btn = QPushButton("Salva Configurazioni")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        layout.addStretch()
        self.setLayout(layout)

    def save_settings(self):
        self.config["username"] = self.username_edit.text()
        self.config["password"] = self.password_edit.text()
        save_config(self.config)
        QMessageBox.information(self, "Successo", "Configurazioni salvate con successo.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automazione Portale Fornitori")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Placeholder for other tabs (will be implemented in next steps)
        self.settings_tab = SettingsWidget()

        # We will add Activity and Download tabs later, for now we can create empty widgets or minimal placeholders
        from gui.activity_widget import ActivityWidget
        from gui.download_widget import DownloadWidget
        self.activity_tab = ActivityWidget()
        self.download_tab = DownloadWidget()

        self.tabs.addWidget(self.settings_tab, "Impostazioni")
        self.tabs.addWidget(self.activity_tab, "Attività")
        self.tabs.addWidget(self.download_tab, "Scarico TS")

        # Log Output Area
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFixedHeight(150)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(QLabel("Log Operazioni:"))
        main_layout.addWidget(self.log_output)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connect Download Widget Signal
        self.download_tab.start_download_signal.connect(self.start_bot)

        self.bot_thread = None

    def start_bot(self, download_tasks, data_da):
        if self.bot_thread and self.bot_thread.isRunning():
            QMessageBox.warning(self, "Attenzione", "Il Bot è già in esecuzione.")
            return

        self.log_output.append(f"--- Avvio Bot con {len(download_tasks)} task (Data: {data_da}) ---")
        self.bot_thread = BotWorker(download_tasks, data_da=data_da)
        self.bot_thread.log_signal.connect(self.log_msg)
        self.bot_thread.error_signal.connect(self.log_error)
        self.bot_thread.finished_signal.connect(self.bot_finished)
        self.bot_thread.start()

    def log_msg(self, msg):
        self.log_output.append(msg)

    def log_error(self, msg):
        self.log_output.append(f"<span style='color:red'>{msg}</span>")

    def bot_finished(self):
        self.log_output.append("--- Bot terminato ---")
        QMessageBox.information(self, "Info", "Operazioni Bot completate.")
        self.bot_thread = None

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
