"""
SyncroJob - Help Panel
Pannello Guida interattivo con navigazione gerarchica e supporto Markdown.
Fornisce documentazione operativa, assistenza tecnica e informazioni sulle licenze.
"""

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.version import __version__ as VERSION
from src.utils.helpers import get_asset_path, get_colored_icon


class HelpPanel(QWidget):
    """
    Pannello Guida Tecnico-Operativo Professionale.
    Implementa un browser Markdown per la visualizzazione dei contenuti e un indice laterale filtrabile.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello guida.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.sections: list[tuple[str, str, str]] = []
        self._setup_ui()
        self._load_documentation()

    def _setup_ui(self) -> None:
        """Configura l'interfaccia utente con header hero, sidebar e visualizzatore contenuti."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header Hero Moderno
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet("QFrame { background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0; }")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)

        title_container = QVBoxLayout()
        title_container.setSpacing(2)
        title = QLabel("Knowledge Base")
        title.setStyleSheet("color: #263238; font-size: 24px; font-weight: 800;")
        subtitle = QLabel(f"Documentazione Ufficiale SyncroJob v{VERSION}")
        subtitle.setStyleSheet("color: #78909C; font-size: 13px; font-weight: 500;")
        title_container.addStretch()
        title_container.addWidget(title)
        title_container.addWidget(subtitle)
        title_container.addStretch()
        header_layout.addLayout(title_container)
        header_layout.addStretch()

        icon_lbl = QLabel()
        icon_lbl.setPixmap(get_colored_icon(get_asset_path(Icons.HELP), "#009688").pixmap(48, 48))
        header_layout.addWidget(icon_lbl)
        layout.addWidget(header)

        # Splitter per Indice e Contenuto
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: #ECEFF1; width: 1px; }")

        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 20)
        sidebar_layout.setSpacing(15)
        sidebar.setFixedWidth(320)
        sidebar.setStyleSheet("background-color: #FAFAFA;")

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Cerca nella guida...")
        self.search_edit.setMinimumHeight(42)
        self.search_edit.setStyleSheet(
            "QLineEdit { border: 1px solid #CFD8DC; border-radius: 8px; padding: 0 15px; background-color: white; font-size: 14px; }"
        )
        self.search_edit.textChanged.connect(self._filter_index)
        sidebar_layout.addWidget(self.search_edit)

        self.index_list = QListWidget()
        self.index_list.setIconSize(QSize(20, 20))
        self.index_list.setStyleSheet(
            "QListWidget { background-color: transparent; border: none; } QListWidget::item { padding: 12px 15px; border-radius: 10px; color: #455A64; font-weight: 500; } QListWidget::item:selected { background-color: #E0F2F1; color: #00796B; font-weight: 700; }"
        )
        self.index_list.currentRowChanged.connect(self._on_index_changed)
        sidebar_layout.addWidget(self.index_list, 1)

        # Browser
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setReadOnly(True)
        self.browser.setStyleSheet(
            "QTextBrowser { background-color: white; border: none; padding: 50px 60px; font-family: 'Segoe UI', sans-serif; font-size: 16px; line-height: 1.8; color: #263238; }"
        )

        self.splitter.addWidget(sidebar)
        self.splitter.addWidget(self.browser)
        self.splitter.setStretchFactor(1, 1)
        layout.addWidget(self.splitter)

    def _load_documentation(self) -> None:
        """Inizializza le sezioni della documentazione e popola l'indice."""
        self.sections = [
            ("Benvenuto", self._get_intro_md(), Icons.HOME),
            ("Novità", self._get_news_md(), Icons.SPARKLES),
            ("Configurazione Telegram", self._get_telegram_md(), Icons.SEND),
            ("Scarico & Elaborazione", self._get_scarico_md(), Icons.DOWNLOAD),
            ("Dettagli OdA", self._get_oda_md(), Icons.LIST),
            ("Timbrature & Autopilot", self._get_timbrature_md(), Icons.CLOCK),
            ("Strumentale & KPI", self._get_contabilita_md(), Icons.BAR_CHART),
            ("Lyra AI Assistant", self._get_lyra_md(), Icons.CPU),
            ("Scorciatoie Veloci", self._get_shortcuts_md(), Icons.ROCKET),
            ("Risoluzione Problemi", self._get_troubleshooting_md(), Icons.ALERT),
            ("Sicurezza & Licenza", self._get_license_md(), Icons.SHIELD),
            ("Supporto & Contatti", self._get_contacts_md(), Icons.USER),
        ]

        self.index_list.blockSignals(True)
        for title, _content, icon_key in self.sections:
            item = QListWidgetItem(title)
            item.setIcon(get_colored_icon(get_asset_path(icon_key), "#546E7A"))
            self.index_list.addItem(item)
        self.index_list.blockSignals(False)

    def _on_index_changed(self, row: int) -> None:
        """Visualizza il contenuto Markdown corrispondente alla sezione selezionata."""
        if row < 0:
            return
        item = self.index_list.item(row)
        if not item:
            return
        title = item.text()
        for section_title, content, _ in self.sections:
            if section_title == title:
                self.browser.setMarkdown(content)
                break

    def _filter_index(self, text: str) -> None:
        """Filtra le voci dell'indice in base al testo inserito nella barra di ricerca."""
        text = text.lower()
        self.index_list.clear()
        for title, _content, icon_key in self.sections:
            if text in title.lower():
                item = QListWidgetItem(title)
                item.setIcon(get_colored_icon(get_asset_path(icon_key), "#546E7A"))
                self.index_list.addItem(item)
        if self.index_list.count() > 0:
            self.index_list.setCurrentRow(0)

    def open_section(self, section_title: str) -> None:
        """
        Naviga direttamente a una sezione specifica della guida.

        Args:
            section_title: Titolo (o parte del titolo) della sezione da aprire.
        """
        for i in range(self.index_list.count()):
            item = self.index_list.item(i)
            if item is not None and section_title.lower() in item.text().lower():
                self.index_list.setCurrentRow(i)
                break

    def _get_intro_md(self) -> str:
        """Restituisce il Markdown per la sezione di benvenuto."""
        return f"# Benvenuto in SyncroJob v{VERSION}\nLa piattaforma integrata per la gestione automatizzata dell'appalto ISAB."

    def _get_news_md(self) -> str:
        """Restituisce il Markdown per le novità della versione."""
        return f"# 🆕 Novità Versione {VERSION}\n### ⚡ Navigazione 'Clean Line'\nL'interfaccia è stata ridisegnata per massimizzare la produttività."

    def _get_telegram_md(self) -> str:
        """Restituisce il Markdown per la guida di Telegram."""
        return "# 📱 Controllo Remoto Telegram\nGestisci SyncroJob dal tuo smartphone."

    def _get_scarico_md(self) -> str:
        """Restituisce il Markdown per lo scarico/carico TS."""
        return "# 📥 Scarico & Carico TS\nGestione completa del ciclo di vita dei Timesheet."

    def _get_oda_md(self) -> str:
        """Restituisce il Markdown per OdA e BP."""
        return (
            "# 📋 Dettagli OdA & Prenotazioni\nScarica i dettagli completi per alimentare la ricerca globale."
        )

    def _get_timbrature_md(self) -> str:
        """Restituisce il Markdown per le timbrature."""
        return "# ⏱️ Timbrature\nIl cuore della gestione presenze."

    def _get_contabilita_md(self) -> str:
        """Restituisce il Markdown per la contabilità."""
        return "# 📊 Strumentale (Contabilità)\nVisione economica completa dell'appalto."

    def _get_lyra_md(self) -> str:
        """Restituisce il Markdown per l'AI Lyra."""
        return "# ✨ Lyra AI\nIl tuo assistente analista personale basato su intelligenza artificiale."

    def _get_shortcuts_md(self) -> str:
        """Restituisce il Markdown per le scorciatoie."""
        return "# ⚡ Scorciatoie\n* **F5**: Aggiorna dati\n* **Ctrl + F**: Cerca"

    def _get_troubleshooting_md(self) -> str:
        """Restituisce il Markdown per il troubleshooting."""
        return "# 🛠️ Risoluzione Problemi\nControlla Chrome e la VPN ISAB."

    def _get_license_md(self) -> str:
        """Restituisce il Markdown per la licenza."""
        return "# 🔑 Licenza\nSyncroJob è protetto da licenza digitale hardware."

    def _get_contacts_md(self) -> str:
        """Restituisce il Markdown per i contatti."""
        return "# 📞 Contatti & Supporto\ngianky.allegretti@gmail.com"
