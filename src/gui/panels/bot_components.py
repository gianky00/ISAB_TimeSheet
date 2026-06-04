"""SyncroJob - Bot UI Components.

Sotto-componenti specializzati per i pannelli dei bot.
Conformit  SRP: Ogni componente gestisce una specifica area della UI.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QWidget

from src.application.services.constants import Icons
from src.gui.components.activity_timeline import ActivityTimelineWidget
from src.gui.design.spacing import Spacing
from src.gui.widgets import TimelineWidget
from src.gui.widgets.modern_button import ModernButton
from src.infrastructure.utils.helpers import get_asset_path


class BotControlComponent(QWidget):
    """Componente per i controlli di avvio e interruzione del bot.

    Inizializza la classe.
    """

    start_clicked = Signal()
    stop_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.sm)

        self.start_btn = ModernButton(
            "Avvia",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.MEDIUM,
            icon=get_asset_path(Icons.PLAY),
        )
        self.start_btn.setMinimumWidth(110)
        self.start_btn.clicked.connect(lambda: self.start_clicked.emit())
        layout.addWidget(self.start_btn)

        self.stop_btn = ModernButton(
            "Stop",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.MEDIUM,
            icon=get_asset_path(Icons.STOP),
        )
        self.stop_btn.setMinimumWidth(90)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(lambda: self.stop_clicked.emit())
        layout.addWidget(self.stop_btn)

    def set_running(self, running: bool) -> None:
        """Aggiorna lo stato di abilitazione dei pulsanti."""
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)


class BotTimelineComponent(ActivityTimelineWidget):
    """Versione specializzata della timeline per i bot.

    Inizializza la classe.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setContentsMargins(10, 10, 10, 10)

    def reset(self) -> None:
        """Ripristina la timeline allo stato iniziale."""
        # Nota: ActivityTimelineWidget gestisce internamente lo stato degli step


class BotLogComponent(TimelineWidget):
    """Versione specializzata della console log per i bot.

    Inizializza la classe.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def log_success(self, message: str) -> None:
        """Scrive un messaggio positivo nella console del bot."""
        self.append(message, "SUCCESS")

    def log_error(self, message: str) -> None:
        """Scrive un messaggio di errore nella console del bot."""
        self.append(message, "ERROR")

    def log_warning(self, message: str) -> None:
        """Scrive un messaggio di avviso nella console del bot."""
        self.append(message, "WARNING")

    def set_mood(self, mood: str) -> None:
        """Imposta l'effetto visivo della console."""
        if hasattr(super(), "set_mood"):
            super().set_mood(mood)
