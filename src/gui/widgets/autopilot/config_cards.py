"""Card di configurazione per il sistema Autopilot.

Permettono all'utente di abilitare e programmare l'esecuzione automatica dei bot.
"""

from typing import TypedDict

from PySide6.QtCore import Qt, QTime, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import StandardCheckBox, StandardSpinBox
from src.utils.helpers import get_asset_path, get_colored_icon


class BotVisualInfo(TypedDict):
    """Informazioni visuali per la rappresentazione di un bot nell'Autopilot."""

    bot_id: str
    bot_name: str
    icon_path: str
    color: str


class AutopilotConfigCard(QFrame):
    """Card per configurare un bot programmato.

    Inizializza la card di configurazione.

    Supporta sia il nuovo pattern (info: BotVisualInfo) che quello legacy (bot_id, bot_name, icon, color).

    Args:
      info: Informazioni visuali del bot o ID del bot.
      bot_name: Nome del bot (legacy).
      icon_path: Percorso icona (legacy).
      color: Colore associato (legacy).
      parent: Widget genitore.
    """

    def __init__(
        self,
        info: BotVisualInfo | str,
        bot_name: str | None = None,
        icon_path: str | None = None,
        color: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        if isinstance(info, dict):
            # Nuovo pattern (TypedDict)
            self.bot_id = info["bot_id"]
            self.bot_name = info["bot_name"]
            self.icon_path = info["icon_path"]
            self.color = info["color"]
            self.parent_widget = parent
        else:
            # Pattern legacy (Parametri posizionali)
            self.bot_id = info
            self.bot_name = bot_name or ""
            self.icon_path = icon_path or ""
            self.color = color or COLORS["primary_blue"]
            self.parent_widget = parent

        self._setup_style()
        self._setup_ui()
        self._load_config()

    def _setup_style(self) -> None:
        """Configura lo stile della card."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            f"""
      AutopilotConfigCard {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS["bg_light"]}, stop:1 {COLORS["bg_white"]});
        border-radius: 12px;
        border-left: 4px solid {self.color};
        border-top: 1px solid {COLORS["border_light"]};
        border-right: 1px solid {COLORS["border_light"]};
        border-bottom: 1px solid {COLORS["border_light"]};
      }}
    """
        )

    def _setup_ui(self) -> None:
        """Configura i componenti dell'interfaccia."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self._add_header(layout)
        self._add_enable_checkbox(layout)
        self._add_time_picker(layout)

    def _add_header(self, layout: QVBoxLayout) -> None:
        """Aggiunge l'header con icona e nome."""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setFixedSize(28, 28)
        icon_label.setPixmap(
            get_colored_icon(get_asset_path(self.icon_path), COLORS["bg_white"]).pixmap(18, 18)
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"QLabel {{ background-color: {self.color}; border-radius: 14px; border: none; padding: 5px; }}"
        )
        header_layout.addWidget(icon_label)

        name_lbl = QLabel(self.bot_name)
        name_lbl.setStyleSheet(
            f"QLabel {{ font-weight: 600; font-size: 14px; color: {COLORS['text_dark']}; border: none; background: transparent; }}"
        )
        header_layout.addWidget(name_lbl)
        header_layout.addStretch()

        layout.addLayout(header_layout)

    def _add_enable_checkbox(self, layout: QVBoxLayout) -> None:
        """Aggiunge la checkbox di abilitazione."""
        self.enable_check = StandardCheckBox("Abilita esecuzione automatica")
        self.enable_check.setStyleSheet(
            f"""
      QCheckBox {{ font-size: 13px; color: {COLORS["text_dark"]}; spacing: 8px; }}
      QCheckBox::indicator {{ width: 18px; height: 18px; border-radius: 4px; border: 2px solid {COLORS["border_medium"]}; background: {COLORS["bg_white"]}; }}
      QCheckBox::indicator:checked {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS["primary_blue"]}, stop:1 {COLORS["primary_dark"]});
        border-color: {COLORS["primary_dark"]};
        image: url(assets/icons/check.svg);
      }}
    """
        )
        self.enable_check.stateChanged.connect(lambda: self._on_config_changed())
        layout.addWidget(self.enable_check)

    def _add_time_picker(self, layout: QVBoxLayout) -> None:
        """Aggiunge il selettore orario."""
        time_layout = QHBoxLayout()
        time_layout.setSpacing(10)

        time_label = QLabel("Orario esecuzione:")
        time_label.setStyleSheet(f"QLabel {{ font-size: 13px; color: {COLORS['text_dark']}; }}")
        time_layout.addWidget(time_label)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(9, 0))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setStyleSheet(
            f"""
      QTimeEdit {{ padding: 6px 10px; border: 1px solid {COLORS["border_medium"]}; border-radius: 6px; background: {COLORS["bg_white"]}; font-size: 13px; color: {COLORS["text_dark"]}; }}
      QTimeEdit:focus {{ border-color: {COLORS["primary_dark"]}; }}
    """
        )
        self.time_edit.timeChanged.connect(lambda: self._on_config_changed())
        time_layout.addWidget(self.time_edit)
        time_layout.addStretch()

        layout.addLayout(time_layout)

    def _load_config(self) -> None:
        """Carica la configurazione salvata per questo bot."""
        config = config_manager.load_config()
        enabled_key = f"{self.bot_id}_autopilot_enabled"
        time_key = f"{self.bot_id}_autopilot_time"

        is_enabled = bool(config.get(enabled_key, False))
        self.enable_check.setChecked(is_enabled)

        saved_time = str(config.get(time_key, "09:00"))
        self.time_edit.setTime(QTime.fromString(saved_time, "HH:mm"))

    def _on_config_changed(self) -> None:
        """Salva la configurazione quando viene modificata."""
        config_manager.set_config_value(f"{self.bot_id}_autopilot_enabled", self.enable_check.isChecked())
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_time", self.time_edit.time().toString("HH:mm")
        )

        # Notifica il parent widget per refresh
        if self.parent_widget and hasattr(self.parent_widget, "refresh_events"):
            # Usa un timer per evitare loop di refresh durante il cambio
            QTimer.singleShot(100, self.parent_widget.refresh_events)

        # Aggiorna anche il footer (Account & Status Cards)
        if self.parent_widget:
            if hasattr(self.parent_widget, "footer_left_widget") and self.parent_widget.footer_left_widget:
                QTimer.singleShot(100, self.parent_widget.footer_left_widget.refresh_accounts)

            if hasattr(self.parent_widget, "status_bar") and self.parent_widget.status_bar:
                QTimer.singleShot(100, self.parent_widget.status_bar.update_autopilot_ui)


class AutopilotConfigCardWithInterval(QFrame):
    """Card per configurare un task programmato con intervallo in giorni.

    Usato per report email e altri task non giornalieri.

    Inizializza la card di configurazione con intervallo.

    Supporta sia il nuovo pattern (info: BotVisualInfo) che quello legacy (bot_id, bot_name, icon, color).

    Args:
      info: Informazioni visuali del bot o ID del bot.
      bot_name: Nome del bot (legacy).
      icon_path: Percorso icona (legacy).
      color: Colore associato (legacy).
      parent: Widget genitore.
    """

    def __init__(
        self,
        info: BotVisualInfo | str,
        bot_name: str | None = None,
        icon_path: str | None = None,
        color: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        if isinstance(info, dict):
            # Nuovo pattern (TypedDict)
            self.bot_id = info["bot_id"]
            self.bot_name = info["bot_name"]
            self.icon_path = info["icon_path"]
            self.color = info["color"]
            self.parent_widget = parent
        else:
            # Pattern legacy (Parametri posizionali)
            self.bot_id = info
            self.bot_name = bot_name or ""
            self.icon_path = icon_path or ""
            self.color = color or COLORS["success_dark"]
            self.parent_widget = parent

        self._setup_style()
        self._setup_ui()
        self._load_config()

    def _setup_style(self) -> None:
        """Configura lo stile della card con intervallo."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            f"""
      AutopilotConfigCardWithInterval {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS["bg_light"]}, stop:1 {COLORS["bg_white"]});
        border-radius: 12px;
        border-left: 4px solid {self.color};
        border-top: 1px solid {COLORS["border_light"]};
        border-right: 1px solid {COLORS["border_light"]};
        border-bottom: 1px solid {COLORS["border_light"]};
      }}
    """
        )

    def _setup_ui(self) -> None:
        """Configura i componenti dell'interfaccia."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self._add_header(layout)
        self._add_enable_checkbox(layout)
        self._add_interval_settings(layout)

    def _add_header(self, layout: QVBoxLayout) -> None:
        """Aggiunge l'header con icona e nome."""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setFixedSize(28, 28)
        icon_label.setPixmap(
            get_colored_icon(get_asset_path(self.icon_path), COLORS["bg_white"]).pixmap(18, 18)
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"QLabel {{ background-color: {self.color}; border-radius: 14px; border: none; padding: 5px; }}"
        )
        header_layout.addWidget(icon_label)

        name_lbl = QLabel(self.bot_name)
        name_lbl.setStyleSheet(
            f"QLabel {{ font-weight: 600; font-size: 14px; color: {COLORS['text_dark']}; border: none; background: transparent; }}"
        )
        header_layout.addWidget(name_lbl)
        header_layout.addStretch()

        layout.addLayout(header_layout)

    def _add_enable_checkbox(self, layout: QVBoxLayout) -> None:
        """Aggiunge la checkbox di abilitazione."""
        self.enable_check = StandardCheckBox("Abilita invio automatico")
        self.enable_check.setStyleSheet(
            f"""
      QCheckBox {{ font-size: 13px; color: {COLORS["text_dark"]}; spacing: 8px; }}
      QCheckBox::indicator {{ width: 18px; height: 18px; border-radius: 4px; border: 2px solid {COLORS["border_medium"]}; background: {COLORS["bg_white"]}; }}
      QCheckBox::indicator:checked {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS["primary_blue"]}, stop:1 {COLORS["primary_dark"]});
        border-color: {COLORS["primary_dark"]};
        image: url(assets/icons/check.svg);
      }}
    """
        )
        self.enable_check.stateChanged.connect(lambda: self._on_config_changed())
        layout.addWidget(self.enable_check)

    def _add_interval_settings(self, layout: QVBoxLayout) -> None:
        """Aggiunge le impostazioni di orario e intervallo."""
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(15)

        # Time picker
        time_label = QLabel("Ore:")
        time_label.setStyleSheet(f"font-size: 12px; color: {COLORS['text_dark']};")
        settings_layout.addWidget(time_label)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(8, 0))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setFixedWidth(70)
        self.time_edit.setStyleSheet(
            f"""
      QTimeEdit {{ padding: 4px 8px; border: 1px solid {COLORS["border_medium"]}; border-radius: 4px; background: {COLORS["bg_white"]}; font-size: 12px; color: {COLORS["text_dark"]}; }}
      QTimeEdit:focus {{ border-color: {COLORS["primary_dark"]}; }}
    """
        )
        self.time_edit.timeChanged.connect(lambda: self._on_config_changed())
        settings_layout.addWidget(self.time_edit)

        # Intervallo giorni
        interval_label = QLabel("Ogni:")
        interval_label.setStyleSheet(f"font-size: 12px; color: {COLORS['text_dark']};")
        settings_layout.addWidget(interval_label)

        self.interval_spin = StandardSpinBox()
        self.interval_spin.setRange(1, 30)
        self.interval_spin.setValue(7)
        self.interval_spin.setSuffix(" gg")
        self.interval_spin.setFixedWidth(70)
        self.interval_spin.setStyleSheet(
            f"""
      QSpinBox {{ padding: 4px 8px; border: 1px solid {COLORS["border_medium"]}; border-radius: 4px; background: {COLORS["bg_white"]}; font-size: 12px; color: {COLORS["text_dark"]}; }}
      QSpinBox:focus {{ border-color: {COLORS["primary_dark"]}; }}
    """
        )
        self.interval_spin.valueChanged.connect(lambda: self._on_config_changed())
        settings_layout.addWidget(self.interval_spin)
        settings_layout.addStretch()

        layout.addLayout(settings_layout)

    def _load_config(self) -> None:
        """Carica la configurazione salvata per questo task."""
        config = config_manager.load_config()

        is_enabled = bool(config.get(f"{self.bot_id}_autopilot_enabled", False))
        self.enable_check.setChecked(is_enabled)

        saved_time = str(config.get(f"{self.bot_id}_autopilot_time", "08:00"))
        self.time_edit.setTime(QTime.fromString(saved_time, "HH:mm"))

        interval_days = int(config.get(f"{self.bot_id}_autopilot_interval_days", 7))
        self.interval_spin.setValue(interval_days)

    def _on_config_changed(self) -> None:
        """Salva la configurazione quando viene modificata."""
        config_manager.set_config_value(f"{self.bot_id}_autopilot_enabled", self.enable_check.isChecked())
        config_manager.set_config_value(
            f"{self.bot_id}_autopilot_time", self.time_edit.time().toString("HH:mm")
        )
        config_manager.set_config_value(f"{self.bot_id}_autopilot_interval_days", self.interval_spin.value())

        # Notifica il parent widget per refresh
        if self.parent_widget and hasattr(self.parent_widget, "refresh_events"):
            QTimer.singleShot(100, self.parent_widget.refresh_events)

        # Aggiorna anche il footer (Account & Status Cards)
        if self.parent_widget:
            if hasattr(self.parent_widget, "footer_left_widget") and self.parent_widget.footer_left_widget:
                QTimer.singleShot(100, self.parent_widget.footer_left_widget.refresh_accounts)

            if hasattr(self.parent_widget, "status_bar") and self.parent_widget.status_bar:
                QTimer.singleShot(100, self.parent_widget.status_bar.update_autopilot_ui)
