"""
SyncroJob - Config Tab (Next-Gen)
Pannello di configurazione strutturato a Card Moderne con navigazione fluida.
Sostituisce il vecchio QToolBox con un design 'System Hub' ad alta leggibilità.
"""

from typing import Any

from src.gui.widgets.core_widgets import (PrimaryButton, SecondaryButton, DangerButton, GhostButton, IconButton, SearchInput, StandardInput, StandardTextEdit, FilterComboBox, StandardCheckBox, StandardSpinBox, StandardTable, StandardListWidget, StandardTreeWidget, StandardGroupBox, StandardProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.panels.settings.pages.diag_page import DiagPage
from src.gui.panels.settings.pages.general_page import GeneralPage
from src.gui.panels.settings.pages.lists_page import ListsPage
from src.gui.panels.settings.pages.paths_page import PathsPage
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class SettingCard(QFrame):
    """
    Container a card con ombra e stile moderno per un gruppo di impostazioni.
    Fornisce un'intestazione con icona, titolo e sottotitolo.
    """

    def __init__(self, title: str, subtitle: str, icon_key: str, content_widget: QWidget) -> None:
        """
        Inizializza la card di impostazione.

        Args:
            title: Titolo della sezione.
            subtitle: Descrizione breve dello scopo.
            icon_key: Chiave dell'icona in Icons.
            content_widget: Widget contenente i controlli reali.
        """
        super().__init__()
        self.title_text = title
        self.subtitle_text = subtitle

        self.setObjectName("settingCard")
        self.setStyleSheet(f"""
            QFrame#settingCard {{
                background-color: {COLORS['bg_white']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 15px;
            }}
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
        icon_lbl.setPixmap(get_colored_icon(get_asset_path(icon_key), COLORS["teal_accent"]).pixmap(24, 24))
        header_layout.addWidget(icon_lbl)

        text_container = QVBoxLayout()
        text_container.setSpacing(2)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {COLORS['text_dark']};")
        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet(f"font-size: 12px; font-weight: 500; color: {COLORS['text_muted']};")
        text_container.addWidget(title_lbl)
        text_container.addWidget(subtitle_lbl)
        header_layout.addLayout(text_container)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Separatore sottile
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet(f"background-color: {COLORS['bg_alt']};")
        layout.addWidget(line)

        # Contenuto (la pagina reale)
        layout.addWidget(content_widget)

        # Assicura che la card non si schiacci ma cresca con il contenuto
        content_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)


class ConfigTab(QWidget):
    """
    Tab di configurazione d'élite.
    Organizza le impostazioni in Card tematiche scorrevoli.
    """

    settings_changed = pyqtSignal()
    """Segnale emesso quando un'impostazione interna viene variata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il tab di configurazione.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.pages: list[QWidget] = []
        self.cards: list[SettingCard] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Costruisce il layout a card verticali con scroll area."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- TOP STATUS BAR (Search) ---
        self.header_bar = QFrame()
        self.header_bar.setFixedHeight(50)
        self.header_bar.setStyleSheet(f"background: {COLORS['bg_light']}; border-bottom: 1px solid {COLORS['border_light']};")
        header_layout = QHBoxLayout(self.header_bar)
        header_layout.setContentsMargins(20, 0, 20, 0)

        search_icon = QLabel()
        search_icon.setPixmap(get_colored_icon(get_asset_path(Icons.SEARCH), COLORS["text_light"]).pixmap(16, 16))
        header_layout.addWidget(search_icon)

        self.search_bar = SearchInput()
        self.search_bar.setPlaceholderText("Filtra impostazioni...")
        self.search_bar.setStyleSheet("border: none; background: transparent; font-size: 13px; font-weight: 500;")
        self.search_bar.textChanged.connect(self._filter_cards)
        header_layout.addWidget(self.search_bar)
        header_layout.addStretch()

        self.status_lbl = QLabel("Stato Sistema: Operativo")
        self.status_lbl.setStyleSheet(f"color: {COLORS['success_dark']}; font-weight: 700; font-size: 12px;")
        header_layout.addWidget(self.status_lbl)

        main_layout.addWidget(self.header_bar)

        # --- SCROLL AREA PER LE CARDS ---
        self.scroll_container = QScrollArea()
        self.scroll_container.setWidgetResizable(True)
        self.scroll_container.setStyleSheet("background: transparent; border: none;")
        self.scroll_container.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_container.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(scroll_content)
        self.cards_layout.setContentsMargins(30, 30, 30, 30)
        self.cards_layout.setSpacing(30)

        # --- 1. GENERALE ---
        self.general_page = GeneralPage()
        self.general_page.settings_changed.connect(self.settings_changed.emit)
        card_gen = SettingCard(
            "Interfaccia & Automazione",
            "Configura il comportamento del browser e l'aspetto grafico.",
            Icons.CPU, self.general_page
        )
        self.cards_layout.addWidget(card_gen)
        self.cards.append(card_gen)
        self.pages.append(self.general_page)

        # --- 2. LISTE & ACCOUNT ---
        self.lists_page = ListsPage()
        self.lists_page.settings_changed.connect(self.settings_changed.emit)
        self.pages.append(self.lists_page)

        # Card Account ISAB
        card_isab = SettingCard(
            "Account Portale Fornitori",
            "Gestione credenziali per l'accesso ai servizi ISAB.",
            Icons.LOCK, self.lists_page.account_section
        )
        self.cards_layout.addWidget(card_isab)
        self.cards.append(card_isab)

        # Card Account SafeWork
        card_sw = SettingCard(
            "Account SafeWork",
            "Configurazione accessi per il portale SafeWork (PDL).",
            Icons.SHIELD, self.lists_page.sw_account_section
        )
        self.cards_layout.addWidget(card_sw)
        self.cards.append(card_sw)

        # Card Anagrafiche Operative (Fornitori e Contratti)
        ops_container = QWidget()
        ops_layout = QHBoxLayout(ops_container)
        ops_layout.setContentsMargins(0, 0, 0, 0)
        ops_layout.setSpacing(20)
        ops_layout.addWidget(self.lists_page.fornitori_section)
        ops_layout.addWidget(self.lists_page.contract_section)

        card_ops = SettingCard(
            "Liste Operative",
            "Anagrafica fornitori e numeri di contratto attivi.",
            Icons.LIST, ops_container
        )
        self.cards_layout.addWidget(card_ops)
        self.cards.append(card_ops)

        # Card Struttura Aziendale (Reparti e Cantieri)
        geo_container = QWidget()
        geo_layout = QHBoxLayout(geo_container)
        geo_layout.setContentsMargins(0, 0, 0, 0)
        geo_layout.setSpacing(20)
        geo_layout.addWidget(self.lists_page.reparti_section)
        geo_layout.addWidget(self.lists_page.cantieri_section)

        card_geo = SettingCard(
            "Organizzazione Cantiere",
            "Definizione reparti e cantieri per la catalogazione dati.",
            Icons.PDL, geo_container
        )
        self.cards_layout.addWidget(card_geo)
        self.cards.append(card_geo)

        # --- 3. PERCORSI ---
        self.paths_page = PathsPage()
        self.paths_page.settings_changed.connect(self.settings_changed.emit)
        card_paths = SettingCard(
            "Archiviazione & Integrazioni",
            "Definisci le cartelle di destinazione e i database esterni.",
            Icons.DATABASE, self.paths_page
        )
        self.cards_layout.addWidget(card_paths)
        self.cards.append(card_paths)
        self.pages.append(self.paths_page)

        # --- 4. DIAGNOSTICA ---
        self.diag_page = DiagPage()
        card_diag = SettingCard(
            "Diagnostica di Sistema",
            "Strumenti di verifica integrità e risoluzione problemi.",
            Icons.ACTIVITY, self.diag_page
        )
        self.cards_layout.addWidget(card_diag)
        self.cards.append(card_diag)
        self.pages.append(self.diag_page)

        self.cards_layout.addStretch()
        self.scroll_container.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_container)

    def _filter_cards(self, text: str) -> None:
        """Filtra le card visualizzate in base al testo di ricerca."""
        search_term = text.lower().strip()
        for card in self.cards:
            match = (search_term in card.title_text.lower() or
                     search_term in card.subtitle_text.lower())
            card.setVisible(match or not search_term)

    def load_from_config(self, config: dict[str, Any]) -> None:
        """Carica i dati in tutte le pagine gestite dal tab."""
        for page in self.pages:
            if hasattr(page, "load_from_config"):
                page.load_from_config(config)

    def save_to_config(self, config_manager: Any) -> None:
        """Persiste i dati di tutte le pagine nella configurazione globale."""
        for page in self.pages:
            if hasattr(page, "save_to_config"):
                page.save_to_config(config_manager)
