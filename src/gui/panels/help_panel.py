"""
SyncroJob - Help Panel (Next-Gen)
Pannello Guida interattivo con estetica 'Knowledge Hub', navigazione fluida e contenuti professionali.
"""

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.version import __version__ as VERSION  # noqa: N812
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import SearchInput, StandardListWidget
from src.utils.helpers import get_asset_path, get_colored_icon


class HelpPanel(QWidget):
    """
    Knowledge Hub Enterprise.
    Un'esperienza immersiva per la documentazione operativa con stile moderno e contenuti ricchi.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.sections: list[tuple[str, str, str]] = []
        self._setup_ui()
        self._load_documentation()

        # Selezione iniziale con leggero delay per caricamento layout
        QTimer.singleShot(100, lambda: self.index_list.setCurrentRow(0))

    def _setup_ui(self) -> None:
        """Costruisce un layout 'Documentation Portal' con Sidebar Glass e Content Card."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._setup_header(layout)
        self._setup_splitter(layout)

    def _setup_header(self, parent_layout: QVBoxLayout) -> None:
        """Inizializza l'header hero con gradiente e titolo."""
        header = QFrame()
        header.setFixedHeight(120)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLORS["glass_dark"]}, stop:1 {COLORS["glass_deep"]});
                border-bottom: 1px solid {COLORS["glass_border"]};
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 0, 40, 0)

        title_container = QVBoxLayout()
        title_container.setSpacing(4)

        title = QLabel("Centro Risorse & Documentazione")
        title.setStyleSheet(
            f"color: {COLORS['bg_white']}; font-size: 26px; font-weight: 900; letter-spacing: 0.5px;"
        )

        subtitle = QLabel(f"SyncroJob Enterprise v{VERSION} • Hub di Supporto Tecnico")
        subtitle.setStyleSheet(
            f"color: {COLORS['teal_accent']}; font-size: 14px; font-weight: 600; text-transform: uppercase;"
        )

        title_container.addStretch()
        title_container.addWidget(title)
        title_container.addWidget(subtitle)
        title_container.addStretch()

        header_layout.addLayout(title_container)
        header_layout.addStretch()

        # Icona decorativa con bagliore
        icon_badge = QFrame()
        icon_badge.setFixedSize(64, 64)
        icon_badge.setStyleSheet(
            f"background: rgba({QColor(COLORS['teal_accent']).red()}, {QColor(COLORS['teal_accent']).green()}, {QColor(COLORS['teal_accent']).blue()}, 0.15); border-radius: 32px; border: 1px solid rgba({QColor(COLORS['teal_accent']).red()}, {QColor(COLORS['teal_accent']).green()}, {QColor(COLORS['teal_accent']).blue()}, 0.3);"
        )
        badge_layout = QVBoxLayout(icon_badge)
        badge_layout.setContentsMargins(0, 0, 0, 0)
        badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(get_colored_icon(get_asset_path(Icons.HELP), COLORS["teal_accent"]).pixmap(32, 32))
        badge_layout.addWidget(icon_lbl)
        header_layout.addWidget(icon_badge)

        parent_layout.addWidget(header)

    def _setup_splitter(self, parent_layout: QVBoxLayout) -> None:
        """Inizializza l'area contenuti divisa tra sidebar e browser."""
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: transparent; width: 0px; }")

        sidebar = self._create_sidebar()
        content = self._create_content_browser()

        self.splitter.addWidget(sidebar)
        self.splitter.addWidget(content)
        parent_layout.addWidget(self.splitter)

    def _create_sidebar(self) -> QWidget:
        """Crea il widget sidebar per la navigazione interna."""
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet(
            f"background-color: {COLORS['bg_light']}; border-right: 1px solid {COLORS['border_light']};"
        )
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)
        sidebar_layout.setSpacing(20)

        # Search Bar
        search_container = QFrame()
        search_container.setStyleSheet(
            f"background: {COLORS['bg_white']}; border: 1px solid {COLORS['border_medium']}; border-radius: 10px;"
        )
        search_h_layout = QHBoxLayout(search_container)
        search_h_layout.setContentsMargins(12, 0, 12, 0)

        search_icon = QLabel()
        search_icon.setPixmap(
            get_colored_icon(get_asset_path(Icons.SEARCH), COLORS["text_muted"]).pixmap(16, 16)
        )
        search_h_layout.addWidget(search_icon)

        self.search_edit = SearchInput()
        self.search_edit.setPlaceholderText("Cerca modulo o comando...")
        self.search_edit.setStyleSheet(
            "border: none; padding: 12px 0; font-size: 14px; background: transparent;"
        )
        self.search_edit.textChanged.connect(self._filter_index)
        search_h_layout.addWidget(self.search_edit)
        sidebar_layout.addWidget(search_container)

        # Index List
        self.index_list = StandardListWidget()
        self.index_list.setIconSize(QSize(20, 20))
        self.index_list.setStyleSheet(f"""
            QListWidget {{ background: transparent; border: none; outline: none; }}
            QListWidget::item {{
                padding: 14px 18px; border-radius: 8px; color: {COLORS["text_dark"]};
                font-weight: 600; font-size: 13px; margin-bottom: 4px;
            }}
            QListWidget::item:hover {{ background-color: {COLORS["bg_hover"]}; color: {COLORS["text_dark"]}; }}
            QListWidget::item:selected {{ background-color: {COLORS["teal_accent"]}; color: white; }}
        """)
        self.index_list.currentRowChanged.connect(self._on_index_changed)
        sidebar_layout.addWidget(self.index_list)

        sb_footer = QLabel("SyncroJob Hub • Built for Excellence")
        sb_footer.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 700; text-transform: uppercase;"
        )
        sb_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(sb_footer)

        return sidebar

    def _create_content_browser(self) -> QWidget:
        """Crea il visualizzatore di contenuti Markdown."""
        content_container = QWidget()
        content_container.setStyleSheet(f"background-color: {COLORS['bg_white']};")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setReadOnly(True)
        self.browser.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {COLORS["bg_white"]}; border: none; padding: 60px 80px;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                font-size: 16px; color: {COLORS["text_dark"]};
            }}
        """)
        content_layout.addWidget(self.browser)
        return content_container

    def _load_documentation(self) -> None:
        """Carica contenuti professionali e dettagliati."""
        self.sections = [
            ("Introduzione", self._get_intro_md(), Icons.HOME),
            ("Workflow Automazioni", self._get_scarico_md(), Icons.CPU),
            ("Gestione Database", self._get_timbrature_md(), Icons.DATABASE),
            ("Sincronizzazione PDL", self._get_oda_md(), Icons.FILE_TEXT),
            ("KPI & Analisi", self._get_contabilita_md(), Icons.BAR_CHART),
            ("Notifiche & Audit", self._get_news_md(), Icons.BELL),
            ("Sicurezza Enterprise", self._get_license_md(), Icons.SHIELD),
            ("Shortcuts di Sistema", self._get_shortcuts_md(), Icons.ROCKET),
            ("Troubleshooting", self._get_troubleshooting_md(), Icons.ALERT_TRIANGLE),
            ("Contatti & Help Desk", self._get_contacts_md(), Icons.USER),
        ]

        self.index_list.blockSignals(True)
        for title, _content, icon_key in self.sections:
            item = QListWidgetItem(title)
            color = COLORS["teal_accent"] if title == "Introduzione" else COLORS["text_muted"]
            item.setIcon(get_colored_icon(get_asset_path(icon_key), color))
            self.index_list.addItem(item)
        self.index_list.blockSignals(False)

    def _on_index_changed(self, row: int) -> None:
        if row < 0 or row >= len(self.sections):
            return
        self.browser.setMarkdown(self.sections[row][1])
        # Smooth scroll to top
        bar = self.browser.verticalScrollBar()
        if bar:
            bar.setValue(0)

    def _filter_index(self, text: str) -> None:
        text = text.lower()
        for i in range(self.index_list.count()):
            item = self.index_list.item(i)
            if item:
                item.setHidden(text not in item.text().lower())

    def open_section(self, section_title: str) -> None:
        """Naviga alla sezione specificata nella lista dell'indice."""
        for i in range(self.index_list.count()):
            item = self.index_list.item(i)
            if item and section_title.lower() in item.text().lower():
                self.index_list.setCurrentRow(i)
                break

    # --- PROFESSIONALLY WRITTEN CONTENT ---

    def _get_intro_md(self) -> str:
        return f"""
# Benvenuto in SyncroJob Enterprise
### L'ecosistema definitivo per l'automazione del cantiere ISAB.

SyncroJob v{VERSION} è una suite software di classe enterprise progettata per eliminare le inefficienze operative attraverso l'automazione intelligente dei processi sul **Portale Fornitori ISAB** e **SafeWork**.

#### 🎯 Obiettivi Chiave
*   **Zero Error Data Entry**: Riduzione degli errori umani nel carico dei Timesheet.
*   **Real-time Monitoring**: Visione istantanea dello stato delle abilitazioni e della contabilità.

---
*Usa il menu a sinistra per esplorare i moduli funzionali.*
"""

    def _get_scarico_md(self) -> str:
        return """
# 🤖 Workflow Automazioni (Bot)
### Esecuzione di processi Selenium ad alta affidabilità.

I Bot di SyncroJob simulano l'interazione umana per gestire task ripetitivi sul web.

#### ⚙️ Moduli Disponibili
1.  **Scarico TS**: Recupera automaticamente i file excel dal portale per l'elaborazione VBA.
2.  **Dettagli OdA**: Estrae metadati critici dagli Ordini d'Acquisto per alimentare la ricerca globale.
3.  **Carico TS**: Inserisce i dati elaborati nel portale, validando ogni riga in tempo reale.
4.  **Prenota BP**: Gestisce le prenotazioni dei badge permanenti con reportistica immediata.

#### 💡 Best Practices
*   Assicurarsi che la **VPN ISAB** sia attiva prima di avviare un bot.
*   Non interagire con il browser Chrome mentre il bot è in stato `RUNNING`.
*   Utilizzare la **Command Palette (Ctrl+P)** per avvii rapidi.
"""

    def _get_timbrature_md(self) -> str:
        return """
# 📊 Gestione Database & Risorse
### Archiviazione centralizzata e persistente dei dati operativi.

SyncroJob utilizza un motore database SQLite ottimizzato per gestire centinaia di migliaia di record con latenza zero.

#### 📁 Sezioni Database
*   **Timbrature**: Storico completo degli ingressi/uscite con associazione automatica al cantiere.
*   **DataEase**: Integrazione con lo scarico ore cantiere per analisi di resa.
*   **Dipendenti**: Gestione anagrafica, scadenze abilitazioni e badge.

#### 🔍 Ricerca Avanzata
Utilizza la **Ricerca Universale** in alto (Ctrl+F) per trovare istantaneamente un Badge, un Cognome o un numero OdA in tutto l'ecosistema.
"""

    def _get_oda_md(self) -> str:
        return """
# 🏗️ Sincronizzazione PDL & SafeWork
### Automazione dei flussi SafeWork per la programmazione lavori.

Il modulo PDL permette di monitorare l'intero ciclo di vita dei Permessi di Lavoro.

#### 🔄 Ciclo Operativo
1.  **Sync Bot**: Il bot interroga SafeWork e aggiorna il database locale.
2.  **Programmazione**: Gestione settimanale dei flag TCL/TGO per ogni PDL.
3.  **Storico Interventi**: Recupero della cronologia tecnica dai database esterni.

> **Nota**: I dati sono sincronizzati ogni volta che viene eseguito il bot 'Ricerca PDL'.
"""

    def _get_contabilita_md(self) -> str:
        return """
# 📈 KPI & Analisi Strumentale
### La visione economica e produttiva del tuo appalto.

Questo modulo trasforma i dati grezzi in decisioni aziendali.

#### 📉 Funzionalità
*   **Analisi Preventivi**: Monitoraggio degli importi maturati per anno e per OdA.
*   **Controllo Giornaliere**: Verifica quotidiana della produzione strumentale.
*   **Export Enterprise**: Generazione di report Excel pronti per la fatturazione.
"""

    def _get_news_md(self) -> str:
        return """
# 🔔 Notifiche, Audit & News
### Trasparenza totale su ogni operazione eseguita.

#### 📜 Audit Log
Ogni azione rilevante (avvio bot, modifica configurazione, login) viene registrata nel database di Audit per garantire la tracciabilità.

#### 🏥 Health Score
Un algoritmo proprietario valuta la salute del sistema basandosi su:
*   Connettività di rete.
*   Validità delle licenze.
*   Stato dei driver (ChromeDriver).
*   Integrità del Database.
"""

    def _get_license_md(self) -> str:
        return """
# 🔑 Sicurezza & Licenza Digitale
### Protezione dei dati e controllo degli accessi.

SyncroJob Enterprise è protetto da un sistema di licenza hardware univoco.

#### 🛡️ Protocolli di Securrezza
*   **Hardware Binding**: La licenza è legata all'ID del computer per prevenire duplicazioni.
*   **Credential Encryption**: Le password dei portali sono criptate nel database locale.
*   **Session Guard**: Monitoraggio delle scadenze abilitazioni ISAB per evitare blocchi operativi.
"""

    def _get_shortcuts_md(self) -> str:
        return """
# ⚡ Shortcuts di Sistema
### Massimizza la tua velocità operativa.

| Scorciatoia | Azione |
| :--- | :--- |
| **Ctrl + P** | Apri Command Palette (Ricerca Rapida) |
| **Ctrl + F** | Focus su Ricerca Universale |
| **F5** | Refresh dati della pagina corrente |
| **Ctrl + S** | Forza salvataggio impostazioni |
| **Esc** | Chiude dialoghi e modali |
"""

    def _get_troubleshooting_md(self) -> str:
        return """
# 🛠️ Troubleshooting & Risoluzione Problemi
### Guida rapida ai problemi comuni.

#### ❌ Il Bot non parte?
1.  Verifica che **Chrome** sia aggiornato all'ultima versione.
2.  Controlla che la **VPN ISAB** sia connessa.
3.  Assicurati che non ci siano altre istanze di Chrome aperte dal bot.

#### ❌ Errore Login Portale?
*   Verifica le credenziali in `Impostazioni > Account`.
*   Prova ad accedere manualmente dal browser per sbloccare eventuali Captcha.
"""

    def _get_contacts_md(self) -> str:
        return """
# 📞 Supporto Tecnico & Contatti
### Siamo qui per aiutarti.

Per assistenza prioritaria, bug report o richieste di nuove funzionalità:

*   **Lead Developer**: G. Allegretti
*   **Email**: [gianky.allegretti@gmail.com](mailto:gianky.allegretti@gmail.com)
*   **WhatsApp**: [Canale Supporto Interno]

---
*SyncroJob Enterprise è un prodotto sviluppato con passione per l'eccellenza operativa.*
"""
