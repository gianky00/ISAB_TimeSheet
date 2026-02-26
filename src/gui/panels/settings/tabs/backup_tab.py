"""
SyncroJob - Backup Tab (Next-Gen)
Pannello per la gestione dei backup e dei log strutturato a Card.
"""

from typing import Any

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class SettingCard(QFrame):
    """Container a card con ombra e stile moderno per un gruppo di impostazioni."""

    def __init__(self, title: str, subtitle: str, icon_key: str, content_widget: QWidget) -> None:
        """
        Inizializza la card di impostazione.

        Args:
            title: Titolo della sezione.
            subtitle: Descrizione breve.
            icon_key: Chiave icona.
            content_widget: Widget contenuto.
        """
        super().__init__()
        self.setObjectName("settingCard")
        self.setStyleSheet("""
            QFrame#settingCard {
                background-color: white;
                border: 1px solid #ECEFF1;
                border-radius: 15px;
            }
        """)

        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Header della Card
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(get_colored_icon(get_asset_path(icon_key), "#009688").pixmap(24, 24))
        header_layout.addWidget(icon_lbl)

        text_container = QVBoxLayout()
        text_container.setSpacing(2)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #263238;")
        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet("font-size: 12px; font-weight: 500; color: #90A4AE;")
        text_container.addWidget(title_lbl)
        text_container.addWidget(subtitle_lbl)
        header_layout.addLayout(text_container)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Separatore sottile
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #F5F7F9;")
        layout.addWidget(line)

        # Contenuto
        layout.addWidget(content_widget)
        content_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)


class BackupTab(QWidget):
    """
    Tab dedicato alla sicurezza dei dati.
    Permette la gestione dei backup del database e la pulizia dei log operativi.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il tab di backup.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout a card per backup e log."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area
        self.scroll_container = QScrollArea()
        self.scroll_container.setWidgetResizable(True)
        self.scroll_container.setStyleSheet("background: transparent; border: none;")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(scroll_content)
        self.cards_layout.setContentsMargins(30, 30, 30, 30)
        self.cards_layout.setSpacing(25)

        # 1. Database Backup
        backup_widget = QWidget()
        backup_layout = QVBoxLayout(backup_widget)
        backup_layout.setContentsMargins(0, 10, 0, 0)

        self.btn_backup = ModernButton("Esegui Backup Database", icon=get_asset_path(Icons.CLOUD_UPLOAD))
        self.btn_restore = ModernButton("Ripristina Backup", variant=ModernButton.Variant.GHOST, icon=get_asset_path(Icons.UNDO))
        self.lbl_last_backup = QLabel("Ultimo Backup: Non eseguito")
        self.lbl_last_backup.setStyleSheet("color: #78909C; font-style: italic;")

        backup_layout.addWidget(self.btn_backup)
        backup_layout.addWidget(self.btn_restore)
        backup_layout.addWidget(self.lbl_last_backup)

        self.cards_layout.addWidget(SettingCard(
            "Sicurezza Dati",
            "Gestione copie di sicurezza del database di sistema.",
            Icons.DATABASE, backup_widget
        ))

        # 2. Logs Management
        logs_widget = QWidget()
        logs_layout = QVBoxLayout(logs_widget)
        logs_layout.setContentsMargins(0, 10, 0, 0)

        self.btn_open_logs = ModernButton("Apri Cartella Log", icon=get_asset_path(Icons.FOLDER_OPEN))
        self.btn_clear_logs = ModernButton("Pulisci Log Vecchi", variant=ModernButton.Variant.DANGER, icon=get_asset_path(Icons.TRASH))

        logs_layout.addWidget(self.btn_open_logs)
        logs_layout.addWidget(self.btn_clear_logs)

        self.cards_layout.addWidget(SettingCard(
            "Manutenzione Log",
            "Analisi e pulizia dei file di log generati dai bot.",
            Icons.FILE_TEXT, logs_widget
        ))

        self.cards_layout.addStretch()
        self.scroll_container.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_container)

    def load_from_config(self, config: dict[str, Any]) -> None:
        """
        Carica i metadati del backup dalla configurazione.

        Args:
            config: Dizionario di configurazione.
        """
        last = config.get("last_db_backup", "Mai")
        self.lbl_last_backup.setText(f"Ultimo Backup: {last}")
