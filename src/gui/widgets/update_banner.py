from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class UpdateBanner(QFrame):
    """Banner per la notifica di aggiornamenti disponibili."""

    download_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("updateBanner")
        self.setVisible(False)
        self._download_url = ""
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self.update_label = QLabel("🚀 Nuova versione disponibile!")
        layout.addWidget(self.update_label)

        layout.addStretch()

        self.download_btn = QPushButton("Scarica e Installa")
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(self._on_download_clicked)
        layout.addWidget(self.download_btn)

    def show_update(self, version: str, download_url: str, changelog: str = ""):
        """Mostra il banner con le informazioni dell'aggiornamento."""
        self._download_url = download_url
        self.update_label.setText(f"🚀 Nuova versione disponibile: v{version}")
        self.update_label.setToolTip(
            f"Novità:\n{changelog}" if changelog else "Clicca per scaricare"
        )
        self.setVisible(True)

    def _on_download_clicked(self):
        if self._download_url:
            self.download_requested.emit(self._download_url)
            self.setVisible(False)
