# mypy: disable-error-code="no-untyped-def, no-untyped-call, unused-ignore, arg-type"
from PySide6.QtCore import (  # type: ignore
    Property,
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    Signal,
    Slot,
)
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import PrimaryButton
from src.gui.widgets.wave_progress import WaveProgressBar
from src.utils.helpers import get_asset_path, get_colored_icon

# Stile forzato per i tooltip in Light Mode
TOOLTIP_CSS = """
QToolTip {
  background-color: #FFFFFF;
  color: #212121;
  border: 1px solid #BBBBBB;
  border-radius: 6px;
  padding: 8px 12px;
}
"""


class UpdateBanner(QFrame):
    """Banner per la notifica e il progresso di aggiornamenti disponibili."""

    download_requested = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("updateBanner")
        # Forza Light Mode per il banner
        self.setStyleSheet(f"""
      QFrame#updateBanner {{
        background-color: {COLORS["bg_white"]};
        border-bottom: 1px solid {COLORS["border_medium"]};
      }}
      QLabel {{
        color: {COLORS["text_dark"]};
      }}
      {TOOLTIP_CSS}
    """)
        self.setVisible(False)
        self._download_url = ""
        self._is_complete = False

        self._setup_ui()

        # Inizializza animazione per progressione fluida
        self.animation = QPropertyAnimation(self, b"current_value")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def _setup_ui(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(15, 10, 15, 10)
        self.main_layout.setSpacing(15)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(
            get_colored_icon(get_asset_path(Icons.ROCKET), COLORS["text_dark"]).pixmap(20, 20)
        )
        self.main_layout.addWidget(self.icon_label)

        self.update_label = QLabel("Nuova versione disponibile!")
        self.update_label.setStyleSheet(f"color: {COLORS['text_dark']}; font-weight: bold; font-size: 13px;")
        self.main_layout.addWidget(self.update_label)

        # Container per il progresso (nascosto inizialmente)
        self.progress_container = QFrame()
        self.progress_container.setVisible(False)
        prog_layout = QHBoxLayout(self.progress_container)
        prog_layout.setContentsMargins(0, 0, 0, 0)
        prog_layout.setSpacing(10)

        self.details_label = QLabel("")
        self.details_label.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 11px; font-weight: bold;")
        prog_layout.addWidget(self.details_label)

        self.progress_bar = WaveProgressBar()
        self.progress_bar.setFixedHeight(22)  # Altezza ottimizzata per il banner
        self.progress_bar.setMinimumWidth(200)
        self.progress_bar.setValue(0)
        prog_layout.addWidget(self.progress_bar, 1)

        self.main_layout.addWidget(self.progress_container, 1)

        self.main_layout.addStretch()

        self.download_btn = PrimaryButton("Scarica e Installa")
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(self._on_download_clicked)
        self.main_layout.addWidget(self.download_btn)

    def show_update(
        self,
        version: str,
        download_url: str,
        changelog: str = "",
        is_partial: bool = False,
        is_complete: bool = False,
    ) -> None:
        """Mostra il banner con le informazioni dell'aggiornamento."""
        self._download_url = download_url
        self._is_complete = is_complete

        if is_complete:
            self.update_label.setText(f"Aggiornamento v{version} Pronto")
            self.download_btn.setText("Installa Ora")
        else:
            self.update_label.setText(f"Nuova Versione v{version}")
            # Imposta testo pulsante in base allo stato del download locale
            if is_partial:
                self.download_btn.setText("Riprendi Download")
            else:
                self.download_btn.setText("Scarica e Installa")

        self.update_label.setToolTip(f"Novità:\n{changelog}" if changelog else "Clicca per scaricare")

        # Reset stato download
        self.progress_container.setVisible(False)
        self.download_btn.setVisible(True)

        self.setVisible(True)

    @Slot(int, int, float, float)
    def update_progress(self, downloaded: int, total: int, speed: float, eta: float) -> None:
        """Aggiorna il progresso del download nel banner."""
        if not self.progress_container.isVisible():
            self.progress_container.setVisible(True)
            self.download_btn.setVisible(False)
            self.update_label.setText("Scaricamento in corso...")

        if total > 0:
            self.progress_bar.setMaximum(100)
            percentage = int((downloaded / total) * 100)

            # Avvia animazione fluida
            if self.animation.state() == QPropertyAnimation.State.Running:
                self.animation.stop()
            self.animation.setStartValue(self.progress_bar.value())
            self.animation.setEndValue(percentage)
            self.animation.start()

            mb_down = downloaded / (1024 * 1024)
            mb_total = total / (1024 * 1024)
            speed_mb = speed / (1024 * 1024)

            # Formattazione ETA in minuti e secondi
            if eta > 0:
                mins = int(eta // 60)
                secs = int(eta % 60)
                eta_str = f" - {mins}m {secs}s" if mins > 0 else f" - {secs}s"
            else:
                eta_str = ""

            self.details_label.setText(f"{mb_down:.2f}/{mb_total:.2f} MB ({speed_mb:.2f} MB/s{eta_str})")
        else:
            self.progress_bar.setMaximum(0)

    def _on_download_clicked(self) -> None:
        if self._download_url:
            self.download_requested.emit(self._download_url)
            self.download_btn.setVisible(False)
            self.progress_container.setVisible(True)
            self.update_label.setText("Scaricamento...")

    def show_error(self, message: str) -> None:
        """Mostra un messaggio di errore nel banner e ripristina il pulsante."""
        self.progress_container.setVisible(False)
        self.download_btn.setVisible(True)
        self.download_btn.setText("Riprova")
        self.update_label.setText(f"Errore: {message}")
        self.update_label.setStyleSheet(
            f"color: {COLORS['status_error']}; font-weight: bold; font-size: 13px;"
        )

    def get_current_value(self) -> int:
        """Getter per QPropertyAnimation."""
        return self.progress_bar.value()

    def set_current_value(self, val: int) -> None:
        """Setter per QPropertyAnimation."""
        self.progress_bar.setValue(val)

    # Propriet  Qt per l'animazione (NECESSARIA per QPropertyAnimation in PySide6)
    current_value = Property(int, fget=get_current_value, fset=set_current_value)
