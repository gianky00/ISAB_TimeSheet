"""
Card per visualizzare stato con icona e animazioni.
"""

from typing import Optional

from PyQt6.QtCore import QPropertyAnimation, QSize, Qt, pyqtProperty  # type: ignore
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon

from ..design.colors import get_palette
from ..design.spacing import BorderRadius, Spacing


class StatusCard(QFrame):
    """Card per mostrare stato operazione."""

    class Status:
        """Costanti per definire lo stato visualizzato nella card."""

        IDLE = "idle"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        WARNING = "warning"

    STATUS_CONFIG = {
        Status.IDLE: (Icons.CLOCK, "In attesa", "secondary"),  # Placeholder generic
        Status.RUNNING: (Icons.REFRESH, "In esecuzione...", "info"),
        Status.SUCCESS: (Icons.CHECK_CIRCLE, "Completato", "success"),
        Status.ERROR: (Icons.X_CIRCLE, "Errore", "error"),
        Status.WARNING: (Icons.ALERT, "Attenzione", "warning"),
    }

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._status = self.Status.IDLE
        self._palette = get_palette()
        self._pulse_opacity = 1.0

        self._setup_ui(title)
        self._setup_animation()
        # Stile base statico
        self._base_style_template = f"""
            StatusCard {{
                background-color: {self._palette.surface};
                border: 1px solid {self._palette.border};
                border-radius: {BorderRadius.md}px;
                border-left: 4px solid {{accent}};
            }}
        """
        self._apply_style()

    def _setup_ui(self, title: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(Spacing.sm, Spacing.xxs, Spacing.sm, Spacing.xxs)
        layout.setSpacing(Spacing.xs)

        # Icon
        self._icon_label = QLabel()
        self._icon_label.setFixedSize(24, 24)
        self._icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._icon_label.setStyleSheet("border: none; background: transparent;")
        self._icon_label.setScaledContents(True)
        layout.addWidget(self._icon_label)

        # Text container
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        self._title_label = QLabel(title)
        self._title_label.setStyleSheet(
            f"font-weight: 600; font-size: 13px; color: {self._palette.on_surface}; border: none; background: transparent;"
        )

        self._status_label = QLabel()
        self._status_label.setStyleSheet(
            f"font-size: 11px; color: {self._palette.on_surface}; opacity: 0.7; border: none; background: transparent;"
        )

        text_layout.addWidget(self._title_label)
        text_layout.addWidget(self._status_label)
        layout.addLayout(text_layout, 1)

        self._update_status_display()

    def _setup_animation(self):
        """Inizializza l'animazione di pulsazione per lo stato 'RUNNING'."""
        self._pulse_anim = QPropertyAnimation(self, b"pulseOpacity")
        self._pulse_anim.setDuration(1000)
        self._pulse_anim.setLoopCount(-1)  # Infinite
        self._pulse_anim.setStartValue(1.0)
        self._pulse_anim.setEndValue(0.5)

    def get_pulse_opacity(self) -> float:
        """Restituisce il valore corrente dell'opacità di pulsazione."""
        return self._pulse_opacity

    def set_pulse_opacity(self, value: float):
        """Imposta il valore dell'opacità di pulsazione."""
        self._pulse_opacity = value
        # Update just the icon opacity via stylesheet would be expensive,
        # so we trigger a repaint or set style on icon only if needed.
        pass

    pulseOpacity = pyqtProperty(float, fget=get_pulse_opacity, fset=set_pulse_opacity)

    def setStatus(self, status: str, message: Optional[str] = None):
        """
        Imposta lo stato della card e aggiorna l'interfaccia.

        Args:
            status: Il nuovo stato (idle, running, success, error, warning).
            message: Messaggio personalizzato opzionale.
        """
        self._status = status
        self._update_status_display(message)

        if status == self.Status.RUNNING:
            self._pulse_anim.start()
        else:
            self._pulse_anim.stop()
            self._pulse_opacity = 1.0

    def _update_status_display(self, custom_message: Optional[str] = None):
        """Aggiorna icone e testi in base allo stato corrente."""
        icon_path_const, default_msg, color_key = self.STATUS_CONFIG.get(
            self._status, self.STATUS_CONFIG[self.Status.IDLE]
        )

        # Load and set Pixmap
        full_path = get_asset_path(icon_path_const)
        pixmap = get_colored_icon(full_path, "#000000").pixmap(QSize(24, 24))
        self._icon_label.setPixmap(pixmap)

        self._status_label.setText(custom_message or default_msg)
        self._apply_style()

    def _apply_style(self):
        """Applica il foglio di stile QSS dinamico con il colore dell'accento di stato."""
        _, _, color_key = self.STATUS_CONFIG.get(
            self._status, self.STATUS_CONFIG[self.Status.IDLE]
        )

        accent = getattr(self._palette, color_key, self._palette.primary)
        self.setStyleSheet(self._base_style_template.format(accent=accent))
