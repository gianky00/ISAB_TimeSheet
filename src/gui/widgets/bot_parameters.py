"""SyncroJob - Bot Parameters Widget.

Widget riutilizzabile per la configurazione dei parametri comuni a tutti i bot (Fornitore, Date, Percorso).
"""

from contextlib import suppress
from pathlib import Path
from typing import Any

from PySide6.QtCore import (
    Property,
    QDate,
    QEasingCurve,
    QPropertyAnimation,
    QSize,
    Signal,
)
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.gui.styles import COLORS, COMBOBOX_STYLE, LABEL_MUTED, LINEEDIT_STYLE
from src.gui.widgets.core_widgets import (
    FilterComboBox,
    IconButton,
    StandardInput,
)
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon, safe_open

from .calendar_date_edit import CalendarDateEdit


class HoverPulseFrame(QFrame):
    """Frame personalizzato che fa pulsare il bordo inferiore al passaggio del mouse.

    Fornisce un feedback visivo immediato sull'interattivitàdella card parametri.
    """

    pulse_value_changed = Signal(float)

    def __init__(self, accent_color: str | None = None, parent: QWidget | None = None) -> None:
        """Inizializza il frame pulsante.

        Args:
          accent_color: Colore hex del bordo.
          parent: Widget genitore.
        """
        super().__init__(parent)
        self._accent_color = QColor(accent_color or COLORS["text_dark"])
        self._pulse_val = 1.0

        self._anim = QPropertyAnimation(self, b"pulse_value")
        self._anim.setDuration(1500)
        self._anim.setStartValue(0.4)
        self._anim.setEndValue(1.0)
        self._anim.setLoopCount(-1)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutSine)

    def get_pulse_value(self) -> float:
        """Restituisce il valore corrente della pulsazione per l'animazione del bordo."""
        return self._pulse_val

    def set_pulse_value(self, v: float) -> None:
        """Imposta il valore della pulsazione e forza il ridisegno del widget."""
        if self._pulse_val != v:
            self._pulse_val = v
            self.pulse_value_changed.emit(v)
            self.update()

    pulse_value = Property(float, fget=get_pulse_value, fset=set_pulse_value, notify=pulse_value_changed)

    def enterEvent(self, event: Any) -> None:
        """Avvia l'animazione di pulsazione del bordo all'ingresso del mouse."""
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event: Any) -> None:
        """Interrompe l'animazione e ripristina lo stato solido all'uscita del mouse."""
        self._anim.stop()
        self.set_pulse_value(1.0)
        super().leaveEvent(event)

    def paintEvent(self, event: Any) -> None:
        """Disegna il bordo inferiore pulsante con il colore di accento configurato."""
        super().paintEvent(event)
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Disegna solo il bordo inferiore con l'alpha pulsante
            alpha = int(100 + (self._pulse_val * 155))
            pen = QPen(
                QColor(self._accent_color.red(), self._accent_color.green(), self._accent_color.blue(), alpha)
            )
            pen.setWidth(3)
            painter.setPen(pen)

            # Linea in basso (considerando il raggio del bordo del CSS)
            rect = self.rect()
            painter.drawLine(12, rect.height() - 2, rect.width() - 12, rect.height() - 2)
        finally:
            painter.end()


class BotParametersWidget(QWidget):
    """Widget che raggruppa in un'unica riga i parametri comuni per i bot:

    - Selezione Fornitore (con pulsante gestione rapida)
    - Selezione Data (singola o range temporale)
    - Percorso di destinazione per i file scaricati.

    Implementa un design Neon & Shadow standard per tutte le viste.
    """

    settings_requested = Signal()
    """Segnale emesso quando viene richiesto di aprire le impostazioni fornitori."""

    changed = Signal()
    """Segnale emesso quando uno qualsiasi dei parametri viene modificato."""

    def __init__(
        self, show_date_range: bool = False, show_dest_path: bool = True, parent: QWidget | None = None
    ) -> None:
        """Inizializza il widget dei parametri.

        Args:
          show_date_range: Se True, visualizza anche il campo 'Data À.
          show_dest_path: Se True, visualizza il campo selezione cartella.
          parent: Widget genitore.
        """
        super().__init__(parent)
        self.show_date_range = show_date_range
        self.show_dest_path = show_dest_path
        self._setup_ui()
        self.refresh_fornitori()

    def _setup_ui(self) -> None:
        """Configura il layout orizzontale e i componenti interni."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 15)
        main_layout.setSpacing(0)

        # Container Principale
        self.container = QFrame()
        self.container.setObjectName("filterBar")
        self.container.setStyleSheet(
            f"QFrame#filterBar {{ background-color: {COLORS['bg_white']}; border: 1px solid {COLORS['border_light']}; border-radius: 12px; }}"
        )

        self.main_row_layout = QHBoxLayout(self.container)
        self.main_row_layout.setContentsMargins(15, 10, 15, 10)
        self.main_row_layout.setSpacing(20)

        self._create_ui_sections()

        self.main_row_layout.addStretch()
        main_layout.addWidget(self.container)

    def _create_ui_sections(self) -> None:
        """Crea le sezioni della toolbar parametri."""
        self._setup_societa_section()
        self._add_divider()
        self._setup_fornitore_section()
        self._add_divider()
        self._setup_date_section()

        if self.show_dest_path:
            self._add_divider()
            self._setup_dest_path_section()

    def _setup_societa_section(self) -> None:
        """Configura la sezione di selezione della società(ISAB/PSER)."""
        vbox = QVBoxLayout()
        vbox.setSpacing(4)
        lbl = QLabel("Società")
        lbl.setStyleSheet(LABEL_MUTED)
        vbox.addWidget(lbl)

        self.societa_combo = FilterComboBox()
        self.societa_combo.addItems(["ISAB", "PSER"])
        self.societa_combo.setMinimumHeight(38)
        self.societa_combo.setFixedWidth(100)
        self.societa_combo.setStyleSheet(COMBOBOX_STYLE)
        self.societa_combo.currentIndexChanged.connect(lambda: self.changed.emit())
        vbox.addWidget(self.societa_combo)

        self.main_row_layout.addLayout(vbox)

    def _setup_fornitore_section(self) -> None:
        """Configura la sezione di selezione fornitore."""
        vbox = QVBoxLayout()
        vbox.setSpacing(4)
        lbl = QLabel("FORNITORE")
        lbl.setStyleSheet(LABEL_MUTED)
        vbox.addWidget(lbl)

        hbox = QHBoxLayout()
        hbox.setSpacing(8)
        self.fornitore_combo = FilterComboBox()
        self.fornitore_combo.setMinimumHeight(38)
        self.fornitore_combo.setMinimumWidth(200)
        self.fornitore_combo.setStyleSheet(COMBOBOX_STYLE)
        self.fornitore_combo.currentIndexChanged.connect(lambda: self.changed.emit())
        hbox.addWidget(self.fornitore_combo)

        self.settings_btn = IconButton()
        self.settings_btn.setIcon(get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), COLORS["text_dark"]))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.setFixedSize(38, 38)
        self.settings_btn.setToolTip("Gestisci fornitori")
        self.settings_btn.clicked.connect(lambda: self.settings_requested.emit())
        self.settings_btn.setStyleSheet(self._get_icon_btn_style())
        hbox.addWidget(self.settings_btn)

        vbox.addLayout(hbox)
        self.main_row_layout.addLayout(vbox)

    def _setup_date_section(self) -> None:
        """Configura la sezione delle date."""
        vbox_da = QVBoxLayout()
        vbox_da.setSpacing(4)
        lbl_da = QLabel("DATA INIZIO")
        lbl_da.setStyleSheet(LABEL_MUTED)
        vbox_da.addWidget(lbl_da)
        self.date_da = CalendarDateEdit()
        self.date_da.setMinimumHeight(38)
        self.date_da.setStyleSheet(COMBOBOX_STYLE)
        self.date_da.dateChanged.connect(lambda: self.changed.emit())
        vbox_da.addWidget(self.date_da)
        self.main_row_layout.addLayout(vbox_da)

        if self.show_date_range:
            vbox_a = QVBoxLayout()
            vbox_a.setSpacing(4)
            lbl_a = QLabel("DATA FINE")
            lbl_a.setStyleSheet(LABEL_MUTED)
            vbox_a.addWidget(lbl_a)
            self.date_a = CalendarDateEdit()
            self.date_a.setMinimumHeight(38)
            self.date_a.setStyleSheet(COMBOBOX_STYLE)
            self.date_a.dateChanged.connect(lambda: self.changed.emit())
            vbox_a.addWidget(self.date_a)
            self.main_row_layout.addLayout(vbox_a)

    def _setup_dest_path_section(self) -> None:
        """Configura la sezione del percorso di destinazione."""
        vbox = QVBoxLayout()
        vbox.setSpacing(4)
        lbl = QLabel("CARTELLA DESTINAZIONE")
        lbl.setStyleSheet(LABEL_MUTED)
        vbox.addWidget(lbl)

        hbox = QHBoxLayout()
        hbox.setSpacing(8)
        self.dest_path_edit = StandardInput()
        self.dest_path_edit.setPlaceholderText("Download utente (default)")
        self.dest_path_edit.setReadOnly(True)
        self.dest_path_edit.setMinimumWidth(200)
        self.dest_path_edit.setMinimumHeight(38)
        self.dest_path_edit.setStyleSheet(LINEEDIT_STYLE)
        self.dest_path_edit.textChanged.connect(lambda: self.changed.emit())
        hbox.addWidget(self.dest_path_edit)

        self.browse_btn = IconButton()
        self.browse_btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), COLORS["text_dark"]))
        self.browse_btn.setIconSize(QSize(20, 20))
        self.browse_btn.setFixedSize(38, 38)
        self.browse_btn.setToolTip("Seleziona cartella")
        self.browse_btn.clicked.connect(self._browse_path)
        self.browse_btn.setStyleSheet(self._get_icon_btn_style())
        hbox.addWidget(self.browse_btn)

        self.open_btn = ModernButton("APRI", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL)
        self.open_btn.setFixedSize(60, 38)
        self.open_btn.setStyleSheet(f"""
      QPushButton {{
        background-color: {COLORS["bg_white"]};
        color: {COLORS["text_dark"]};
        border: 1px solid {COLORS["border_medium"]};
        font-weight: bold;
      }}
      QPushButton:hover {{ background-color: {COLORS["table_selection_bg"]}; }}
    """)

        self.open_btn.setToolTip("Apri cartella nel file system")
        self.open_btn.clicked.connect(self._open_folder)
        hbox.addWidget(self.open_btn)
        vbox.addLayout(hbox)
        self.main_row_layout.addLayout(vbox)

    def _add_divider(self) -> None:
        """Aggiunge una linea di divisione verticale."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        line.setStyleSheet(f"color: {COLORS['border_light']};")
        self.main_row_layout.addWidget(line)

    def add_widget_to_row(self, widget: QWidget) -> None:
        """Aggiunge un widget personalizzato alla riga dei parametri.

        Args:
          widget: Il widget QWidget da aggiungere.
        """
        item = self.main_row_layout.takeAt(self.main_row_layout.count() - 1)
        container = QVBoxLayout()
        container.addWidget(QLabel("Opzioni"))
        container.addWidget(widget)
        self.main_row_layout.addSpacing(5)
        self.main_row_layout.addLayout(container)
        if item:
            self.main_row_layout.addItem(item)

    def _get_icon_btn_style(self) -> str:
        """Restituisce lo stile QSS per i pulsanti icona."""
        return f"""
      QPushButton {{
        background-color: {COLORS["bg_white"]};
        color: {COLORS["text_dark"]};
        border: 1px solid {COLORS["border_medium"]};
        border-radius: 6px;
        padding: 2px;
      }}
      QPushButton:hover {{
        background-color: {COLORS["table_selection_bg"]};
        border-color: {COLORS["text_dark"]};
      }}
      QPushButton:pressed {{
        background-color: {COLORS["bg_alt"]};
      }}
    """

    def _browse_path(self) -> None:
        """Apre il dialogo di selezione cartella di sistema."""
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella destinazione")
        if path:
            self.dest_path_edit.setText(path)

    def _open_folder(self) -> None:
        """Apre la cartella di destinazione nell'esplora risorse di sistema in modo sicuro."""
        path_str = self.dest_path_edit.text() or str(Path.home() / "Downloads")
        path = Path(path_str).resolve()

        if not path.exists():
            with suppress(Exception):
                path.mkdir(parents=True, exist_ok=True)

        if not safe_open(path):
            ToastManager.instance().show(f"Impossibile aprire la cartella: {path}", "error")

    def refresh_fornitori(self) -> None:
        """Ricarica l'elenco dei fornitori dalla configurazione globale."""
        fornitori = config_manager.load_config().get("fornitori", [])
        current = self.fornitore_combo.currentText()

        self.fornitore_combo.clear()
        if fornitori:
            self.fornitore_combo.addItems(fornitori)
            index = self.fornitore_combo.findText(current)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)

    def get_fornitore(self) -> str:
        """Restituisce il fornitore selezionato."""
        return self.fornitore_combo.currentText()

    def set_fornitore(self, fornitore: str) -> None:
        """Imposta il fornitore selezionato."""
        index = self.fornitore_combo.findText(fornitore)
        if index >= 0:
            self.fornitore_combo.setCurrentIndex(index)

    def get_societa(self) -> str:
        """Restituisce la societàselezionata (ISAB o PSER)."""
        return self.societa_combo.currentText()

    def set_societa(self, societa: str) -> None:
        """Imposta la societàselezionata."""
        index = self.societa_combo.findText(societa)
        if index >= 0:
            self.societa_combo.setCurrentIndex(index)

    def get_dates(self) -> tuple[str, str | None]:
        """Restituisce il range di date selezionato."""
        date_da = self.date_da.date().toString("dd.MM.yyyy")
        date_a = self.date_a.date().toString("dd.MM.yyyy") if self.show_date_range else None
        return date_da, date_a

    def set_dates(self, date_da_str: str, date_a_str: str | None = None) -> None:
        """Imposta le date nei campiùdi input."""
        with suppress(Exception):
            d, m, y = map(int, date_da_str.split("."))
            self.date_da.setDate(QDate(y, m, d))
            if self.show_date_range and date_a_str:
                d, m, y = map(int, date_a_str.split("."))
                self.date_a.setDate(QDate(y, m, d))

    def get_dest_path(self) -> str:
        """Restituisce il percorso di destinazione impostato."""
        return self.dest_path_edit.text() if self.show_dest_path else ""

    def set_dest_path(self, path: str) -> None:
        """Imposta il percorso di destinazione."""
        if self.show_dest_path:
            self.dest_path_edit.setText(path)
