from PyQt6.QtCore import Qt, QTime, QTimer
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.utils.helpers import get_asset_path, get_colored_icon


class AutopilotConfigCard(QFrame):
    """
    Card per configurare un bot programmato.
    """

    def __init__(
        self, bot_id: str, bot_name: str, icon_path: str, color: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.icon_path = icon_path
        self.color = color
        self.parent_widget = parent

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            f"""
            AutopilotConfigCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #ffffff);
                border-radius: 12px;
                border-left: 4px solid {color};
                border-top: 1px solid #e9ecef;
                border-right: 1px solid #e9ecef;
                border-bottom: 1px solid #e9ecef;
            }}
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Header con icona e nome
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setFixedSize(28, 28)
        icon_label.setPixmap(get_colored_icon(get_asset_path(icon_path), "#ffffff").pixmap(18, 18))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                border-radius: 14px;
                border: none;
                padding: 5px;
            }}
        """
        )
        header_layout.addWidget(icon_label)

        name_lbl = QLabel(bot_name)
        name_lbl.setStyleSheet(
            """
            QLabel {
                font-weight: 600;
                font-size: 14px;
                color: #212529;
                border: none;
                background: transparent;
            }
        """
        )
        header_layout.addWidget(name_lbl)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Checkbox abilitazione
        self.enable_check = QCheckBox("Abilita esecuzione automatica")
        self.enable_check.setStyleSheet(
            """
            QCheckBox {
                font-size: 13px;
                color: #495057;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #ced4da;
                background: #ffffff;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0d6efd, stop:1 #0a58ca);
                border-color: #0d6efd;
                image: url(assets/icons/check.svg);
            }
        """
        )
        self.enable_check.stateChanged.connect(lambda: self._on_config_changed())
        layout.addWidget(self.enable_check)

        # Time picker
        time_layout = QHBoxLayout()
        time_layout.setSpacing(10)

        time_label = QLabel("Orario esecuzione:")
        time_label.setStyleSheet(
            """
            QLabel {
                font-size: 13px;
                color: #495057;
            }
        """
        )
        time_layout.addWidget(time_label)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(9, 0))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setStyleSheet(
            """
            QTimeEdit {
                padding: 6px 10px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background: #ffffff;
                font-size: 13px;
                color: #212529;
            }
            QTimeEdit:focus {
                border-color: #0d6efd;
            }
        """
        )
        self.time_edit.timeChanged.connect(lambda: self._on_config_changed())
        time_layout.addWidget(self.time_edit)
        time_layout.addStretch()

        layout.addLayout(time_layout)

        # Carica configurazione salvata
        self._load_config()

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
    """
    Card per configurare un task programmato con intervallo in giorni.
    Usato per report email e altri task non giornalieri.
    """

    def __init__(
        self, bot_id: str, bot_name: str, icon_path: str, color: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.icon_path = icon_path
        self.color = color
        self.parent_widget = parent

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            f"""
            AutopilotConfigCardWithInterval {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #ffffff);
                border-radius: 12px;
                border-left: 4px solid {color};
                border-top: 1px solid #e9ecef;
                border-right: 1px solid #e9ecef;
                border-bottom: 1px solid #e9ecef;
            }}
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header con icona e nome
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setFixedSize(28, 28)
        icon_label.setPixmap(get_colored_icon(get_asset_path(icon_path), "#ffffff").pixmap(18, 18))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                border-radius: 14px;
                border: none;
                padding: 5px;
            }}
        """
        )
        header_layout.addWidget(icon_label)

        name_lbl = QLabel(bot_name)
        name_lbl.setStyleSheet(
            """
            QLabel {
                font-weight: 600;
                font-size: 14px;
                color: #212529;
                border: none;
                background: transparent;
            }
        """
        )
        header_layout.addWidget(name_lbl)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Checkbox abilitazione
        self.enable_check = QCheckBox("Abilita invio automatico")
        self.enable_check.setStyleSheet(
            """
            QCheckBox {
                font-size: 13px;
                color: #495057;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #ced4da;
                background: #ffffff;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0d6efd, stop:1 #0a58ca);
                border-color: #0d6efd;
                image: url(assets/icons/check.svg);
            }
        """
        )
        self.enable_check.stateChanged.connect(lambda: self._on_config_changed())
        layout.addWidget(self.enable_check)

        # Riga: Orario + Intervallo giorni
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(15)

        # Time picker
        time_label = QLabel("Ore:")
        time_label.setStyleSheet("font-size: 12px; color: #495057;")
        settings_layout.addWidget(time_label)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(8, 0))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setFixedWidth(70)
        self.time_edit.setStyleSheet(
            """
            QTimeEdit {
                padding: 4px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background: #ffffff;
                font-size: 12px;
                color: #212529;
            }
            QTimeEdit:focus {
                border-color: #0d6efd;
            }
        """
        )
        self.time_edit.timeChanged.connect(lambda: self._on_config_changed())
        settings_layout.addWidget(self.time_edit)

        # Intervallo giorni
        interval_label = QLabel("Ogni:")
        interval_label.setStyleSheet("font-size: 12px; color: #495057;")
        settings_layout.addWidget(interval_label)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 30)
        self.interval_spin.setValue(7)
        self.interval_spin.setSuffix(" gg")
        self.interval_spin.setFixedWidth(70)
        self.interval_spin.setStyleSheet(
            """
            QSpinBox {
                padding: 4px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background: #ffffff;
                font-size: 12px;
                color: #212529;
            }
            QSpinBox:focus {
                border-color: #0d6efd;
            }
        """
        )
        self.interval_spin.valueChanged.connect(lambda: self._on_config_changed())
        settings_layout.addWidget(self.interval_spin)
        settings_layout.addStretch()

        layout.addLayout(settings_layout)

        # Carica configurazione salvata
        self._load_config()

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
