"""
SyncroJob - Bot Parameters Widget
Widget riutilizzabile per la configurazione dei parametri comuni a tutti i bot (Fornitore, Date, Percorso).
"""

from contextlib import suppress

from PyQt6.QtCore import QDate, QSize, pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFrame,
    QGraphicsDropShadowEffect,
)

from src.core import config_manager
from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon

from .calendar_date_edit import CalendarDateEdit


class BotParametersWidget(QWidget):
    """
    Widget che raggruppa in un'unica riga i parametri comuni per i bot:
    - Selezione Fornitore (con pulsante gestione rapida)
    - Selezione Data (singola o range temporale)
    - Percorso di destinazione per i file scaricati
    
    Implementa un design Neon & Shadow standard per tutte le viste.
    """

    settings_requested = pyqtSignal()
    """Segnale emesso quando viene richiesto di aprire le impostazioni fornitori."""

    changed = pyqtSignal()
    """Segnale emesso quando uno qualsiasi dei parametri viene modificato."""

    def __init__(
        self, show_date_range: bool = False, show_dest_path: bool = True, parent: QWidget | None = None
    ) -> None:
        """
        Inizializza il widget dei parametri.

        Args:
            show_date_range: Se True, visualizza anche il campo 'Data A'.
            show_dest_path: Se True, visualizza il campo selezione cartella.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.show_date_range = show_date_range
        self.show_dest_path = show_dest_path
        self._setup_ui()
        self.refresh_fornitori()

    def _setup_ui(self) -> None:
        """Configura il layout orizzontale e i componenti interni con stile Neon & Shadow."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 15)
        main_layout.setSpacing(0)

        # --- CONTAINER PRINCIPALE (La "Card" con ombra e neon) ---
        self.container = QFrame()
        self.container.setObjectName("paramsContainer")
        self.container.setStyleSheet("""
            QFrame#paramsContainer {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-bottom: 3px solid #00E5FF; /* Neon Accent Bottom */
                border-radius: 12px;
            }
            QLabel {
                color: #424242;
                font-weight: bold;
                font-size: 13px;
                background: transparent;
            }
            QComboBox, QLineEdit, QDateEdit {
                border: 1px solid #cfd8dc;
                border-radius: 6px;
                padding: 5px 10px;
                background-color: #f8f9fa;
                min-height: 32px;
            }
            QComboBox:focus, QLineEdit:focus, QDateEdit:focus {
                border: 2px solid #00E5FF;
                background-color: #ffffff;
            }
        """)

        # Applica Ombra (Shadow Effect)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(Qt.GlobalColor.black if Qt.GlobalColor.black else "#000000")
        # Nota: Qt.GlobalColor.black non accetta opacità direttamente qui, 
        # meglio usare un colore con alpha se possibile o un valore hex per QColor.
        from PyQt6.QtGui import QColor
        shadow.setColor(QColor(0, 0, 0, 40)) # 40/255 opacità (molto morbida)
        self.container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(15, 15, 15, 15)

        # --- Riga Unica: Fornitore, Date, Destinazione ---
        self.main_row_layout = QHBoxLayout()
        self.main_row_layout.setSpacing(15)

        # Fornitore
        vbox_forn = QVBoxLayout()
        vbox_forn.addWidget(QLabel("Fornitore"))
        
        hbox_forn = QHBoxLayout()
        self.fornitore_combo = QComboBox()
        self.fornitore_combo.setMinimumHeight(38)
        self.fornitore_combo.setMinimumWidth(180)
        self.fornitore_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.fornitore_combo.currentIndexChanged.connect(self.changed.emit)
        hbox_forn.addWidget(self.fornitore_combo)

        # Pulsante Settings
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), "#00E5FF"))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.setFixedSize(38, 38)
        self.settings_btn.setToolTip("Gestisci fornitori")
        self.settings_btn.clicked.connect(self.settings_requested.emit)
        self.settings_btn.setStyleSheet(self._get_icon_btn_style())
        hbox_forn.addWidget(self.settings_btn)
        
        vbox_forn.addLayout(hbox_forn)
        self.main_row_layout.addLayout(vbox_forn)

        # Separatore Neon Verticale (Opzionale)
        # self.main_row_layout.addWidget(self._create_separator())

        # Data Da
        vbox_da = QVBoxLayout()
        vbox_da.addWidget(QLabel("Data Da"))
        self.date_da = CalendarDateEdit()
        self.date_da.setMinimumHeight(38)
        self.date_da.dateChanged.connect(self.changed.emit)
        vbox_da.addWidget(self.date_da)
        self.main_row_layout.addLayout(vbox_da)

        # Data A (opzionale)
        if self.show_date_range:
            vbox_a = QVBoxLayout()
            vbox_a.addWidget(QLabel("Data A"))
            self.date_a = CalendarDateEdit()
            self.date_a.setMinimumHeight(38)
            self.date_a.dateChanged.connect(self.changed.emit)
            vbox_a.addWidget(self.date_a)
            self.main_row_layout.addLayout(vbox_a)

        # Destinazione (opzionale)
        if self.show_dest_path:
            vbox_dest = QVBoxLayout()
            vbox_dest.addWidget(QLabel("Destinazione"))
            
            hbox_dest = QHBoxLayout()
            self.dest_path_edit = QLineEdit()
            self.dest_path_edit.setPlaceholderText("Download utente (default)")
            self.dest_path_edit.setReadOnly(True)
            self.dest_path_edit.setMinimumWidth(180)
            self.dest_path_edit.setMinimumHeight(38)
            self.dest_path_edit.textChanged.connect(self.changed.emit)
            hbox_dest.addWidget(self.dest_path_edit)

            self.browse_btn = QPushButton()
            self.browse_btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), "#00E5FF"))
            self.browse_btn.setIconSize(QSize(20, 20))
            self.browse_btn.setFixedSize(38, 38)
            self.browse_btn.clicked.connect(self._browse_path)
            self.browse_btn.setStyleSheet(self._get_icon_btn_style())
            hbox_dest.addWidget(self.browse_btn)
            
            vbox_dest.addLayout(hbox_dest)
            self.main_row_layout.addLayout(vbox_dest)

        self.main_row_layout.addStretch()
        container_layout.addLayout(self.main_row_layout)
        
        main_layout.addWidget(self.container)

    def _create_separator(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        line.setStyleSheet("background-color: #e0e0e0; max-width: 1px; margin: 5px 0;")
        return line

    def add_widget_to_row(self, widget: QWidget) -> None:
        """
        Aggiunge un widget personalizzato alla riga dei parametri (prima dello stretch).

        Args:
            widget: Il widget QWidget da aggiungere.
        """
        # Raggiungiamo il layout della riga
        # Rimuovi lo stretch finale temporaneamente
        item = self.main_row_layout.takeAt(self.main_row_layout.count() - 1)

        # Se il widget è un checkbox o simile, lo mettiamo in un vbox per allineamento
        container = QVBoxLayout()
        container.addWidget(QLabel("Opzioni"))
        container.addWidget(widget)
        
        self.main_row_layout.addSpacing(5)
        self.main_row_layout.addLayout(container)

        # Rimetti lo stretch
        if item:
            self.main_row_layout.addItem(item)

    def _get_icon_btn_style(self) -> str:
        """Restituisce lo stile QSS standard per i pulsanti icona con accento neon."""
        return """
            QPushButton {
                background-color: #ffffff;
                color: #00E5FF;
                border: 1px solid #cfd8dc;
                border-radius: 6px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #E0F7FA;
                border-color: #00E5FF;
            }
            QPushButton:pressed {
                background-color: #e1bee7;
            }
        """

    def _update_dest_width(self) -> None:
        """Metodo placeholder per l'aggiornamento della larghezza (deprecato)."""

    def _browse_path(self) -> None:
        """Apre il dialogo di selezione cartella di sistema per impostare la destinazione."""
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella destinazione")
        if path:
            self.dest_path_edit.setText(path)

    def refresh_fornitori(self) -> None:
        """Ricarica l'elenco dei fornitori attingendo dalla configurazione globale persistente."""
        fornitori = config_manager.load_config().get("fornitori", [])
        current = self.fornitore_combo.currentText()

        self.fornitore_combo.clear()
        if fornitori:
            self.fornitore_combo.addItems(fornitori)
            index = self.fornitore_combo.findText(current)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)

    # --- Getters / Setters ---
    def get_fornitore(self) -> str:
        """
        Restituisce il fornitore attualmente selezionato.

        Returns:
            str: Testo selezionato nella combo box.
        """
        return self.fornitore_combo.currentText()

    def set_fornitore(self, fornitore: str) -> None:
        """
        Imposta il fornitore selezionato nella combo box.

        Args:
            fornitore: Nome del fornitore da cercare e attivare.
        """
        index = self.fornitore_combo.findText(fornitore)
        if index >= 0:
            self.fornitore_combo.setCurrentIndex(index)

    def get_dates(self) -> tuple[str, str | None]:
        """
        Restituisce le date impostate nel widget.

        Returns:
            tuple: (data_inizio in formato GG.MM.AAAA, data_fine o None).
        """
        date_da = self.date_da.date().toString("dd.MM.yyyy")
        date_a = self.date_a.date().toString("dd.MM.yyyy") if self.show_date_range else None
        return date_da, date_a

    def set_dates(self, date_da_str: str, date_a_str: str | None = None) -> None:
        """
        Imposta le date visualizzate convertendo le stringhe fornite.

        Args:
            date_da_str: Stringa data inizio (formato DD.MM.YYYY).
            date_a_str: Stringa data fine opzionale (formato DD.MM.YYYY).
        """
        with suppress(Exception):
            d, m, y = map(int, date_da_str.split("."))
            self.date_da.setDate(QDate(y, m, d))
            if self.show_date_range and date_a_str:
                d, m, y = map(int, date_a_str.split("."))
                self.date_a.setDate(QDate(y, m, d))

    def get_dest_path(self) -> str:
        """
        Restituisce il percorso di destinazione attualmente visualizzato.

        Returns:
            str: Il path assoluto o stringa vuota.
        """
        return self.dest_path_edit.text() if self.show_dest_path else ""

    def set_dest_path(self, path: str) -> None:
        """
        Imposta il percorso di destinazione nel campo di testo.

        Args:
            path: Percorso assoluto della directory.
        """
        if self.show_dest_path:
            self.dest_path_edit.setText(path)
