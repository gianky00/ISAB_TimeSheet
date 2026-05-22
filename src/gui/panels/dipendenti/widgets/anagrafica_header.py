"""SyncroJob - Anagrafica Header Widget.

Widget che racchiude la barra di ricerca, i pulsanti di azione e le card statistiche.
"""

import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.panels.dipendenti.shared import InteractiveStatusCard
from src.gui.styles import COLORS, LABEL_MUTED, LINEEDIT_STYLE
from src.gui.widgets.core_widgets import SearchInput
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class AnagraficaHeaderWidget(QWidget):
    """Header della pagina Anagrafica con ricerca, azioni e statistiche.

    Inizializza l'header dell'anagrafica.

    Args:
      parent: Widget genitore opzionale.

    Attributes:
        filter_changed: Segnale o attributo della classe.
        import_requested: Segnale o attributo della classe.
        report_requested: Segnale o attributo della classe.
        search_changed: Segnale o attributo della classe.
        update_requested: Segnale o attributo della classe.
    """

    search_changed = Signal(str)
    import_requested = Signal()
    report_requested = Signal()
    update_requested = Signal()
    filter_changed = Signal(str)  # tipo filtro ("ok", "warning", etc.)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout dei filtri, della ricerca e delle card statistiche."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self._setup_filter_bar(layout)
        self._setup_stats_cards(layout)

    def _setup_filter_bar(self, layout: QVBoxLayout) -> None:
        """Configura la barra superiore con ricerca e azioni."""
        self.filter_card = QFrame()
        self.filter_card.setObjectName("filterBar")
        self.filter_card.setStyleSheet(f"""
            QFrame#filterBar {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 12px;
            }}
        """)

        filter_layout = QHBoxLayout(self.filter_card)
        filter_layout.setContentsMargins(15, 10, 15, 10)
        filter_layout.setSpacing(15)

        self._setup_search_section(filter_layout)
        filter_layout.addStretch()
        self._setup_actions_section(filter_layout)

        layout.addWidget(self.filter_card)

    def _setup_search_section(self, layout: QHBoxLayout) -> None:
        """Configura la sezione di ricerca nell'header."""
        search_v = QVBoxLayout()
        search_v.setSpacing(4)
        search_label = QLabel("CERCA DIPENDENTE")
        search_label.setStyleSheet(LABEL_MUTED)

        self.search_input = SearchInput()
        self.search_input.setPlaceholderText("Nome, Cognome, CF o Badge...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)
        self.search_input.textChanged.connect(self.search_changed.emit)

        search_v.addWidget(search_label)
        search_v.addWidget(self.search_input)
        layout.addLayout(search_v)

    def _setup_actions_section(self, layout: QHBoxLayout) -> None:
        """Configura i pulsanti di azione nell'header."""
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lbl_sync_status = QLabel("")
        self.lbl_sync_status.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        info_v.addWidget(self.lbl_sync_status)

        actions_h = QHBoxLayout()
        actions_h.setSpacing(8)

        import_btn = ModernButton(
            "IMPORTA CSV",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.UPLOAD),
        )
        import_btn.clicked.connect(lambda: self.import_requested.emit())

        email_report_btn = ModernButton(
            "REPORT EMAIL",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.SEND),
        )
        email_report_btn.clicked.connect(lambda: self.report_requested.emit())

        self.btn_bot_update = ModernButton(
            "AGGIORNA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.btn_bot_update.clicked.connect(lambda: self.update_requested.emit())

        for b in (import_btn, email_report_btn, self.btn_bot_update):
            actions_h.addWidget(b)

        info_v.addLayout(actions_h)
        layout.addLayout(info_v)

    def _setup_stats_cards(self, layout: QVBoxLayout) -> None:
        """Configura le card statistiche interattive."""
        self.cards_container = QWidget()
        cards_layout = QHBoxLayout(self.cards_container)
        cards_layout.setContentsMargins(0, 5, 0, 5)
        cards_layout.setSpacing(15)

        self.card_ok = InteractiveStatusCard(
            "Operativi", COLORS["success_dark"], Icons.CHECK_CIRCLE, "Ultimo accesso \u226420gg", "ok"
        )
        self.card_warning = InteractiveStatusCard(
            "In Scadenza", COLORS["warning_orange"], Icons.ALERT_TRIANGLE, "Accesso 21-30gg fa", "warning"
        )
        self.card_expired = InteractiveStatusCard(
            "Scaduti", COLORS["error_red"], Icons.X_CIRCLE, "Accesso >30gg fa", "expired"
        )
        self.card_excluded = InteractiveStatusCard(
            "Esclusi", COLORS["text_muted"], Icons.EYE_OFF, "Non monitorati", "excluded"
        )

        for card in (self.card_ok, self.card_warning, self.card_expired, self.card_excluded):
            card.clicked.connect(self.filter_changed.emit)
            cards_layout.addWidget(card, stretch=1)

        layout.addWidget(self.cards_container)

    def set_sync_status(self, text: str) -> None:
        """Aggiorna il testo informativo dell'ultimo sync.

        Args:
          text: Testo formattato da visualizzare.
        """
        self.lbl_sync_status.setText(text)

    def update_counts(self, counts: dict[str, int]) -> None:
        """Aggiorna i contatori numerici sulle card statistiche.

        Args:
          counts: Dizionario con chiavi 'ok', 'warning', 'expired', 'excluded'.
        """
        self.card_ok.setValue(counts.get("ok", 0))
        self.card_warning.setValue(counts.get("warning", 0))
        self.card_expired.setValue(counts.get("expired", 0))
        self.card_excluded.setValue(counts.get("excluded", 0))

    def update_card_styles(self, current_filter: str | None) -> None:
        """Evidenzia la card corrispondente al filtro attualmente attivo.

        Args:
          current_filter: Tipo di filtro selezionato.
        """
        for card in (self.card_ok, self.card_warning, self.card_expired, self.card_excluded):
            is_active = card.filter_type == current_filter
            gradient = (
                f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS['bg_success_pastel']}, stop:1 {COLORS['bg_light']})"
                if is_active
                else f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_alt']})"
            )
            style = f"background: {gradient}; border: {'3px' if is_active else '2px'} solid {card.base_color}; border-radius: 12px;"
            card.setStyleSheet(f"InteractiveStatusCard {{ {style} }}")
