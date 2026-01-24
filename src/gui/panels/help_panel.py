"""
SyncroJob - Help Panel
Pannello Guida rivisitato con stile moderno, ricerca integrata e contenuti aggiornati.
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
    Implementa documentazione strutturata con ricerca e navigazione veloce.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sections = []
        self._setup_ui()
        self._load_documentation()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header Hero Moderno
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E0E0E0;
            }
        """
        )
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

        # Icona Decorativa
        icon_lbl = QLabel()
        icon_lbl.setPixmap(
            get_colored_icon(get_asset_path(Icons.HELP), "#009688").pixmap(48, 48)
        )
        header_layout.addWidget(icon_lbl)

        layout.addWidget(header)

        # Splitter per Indice e Contenuto
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setStyleSheet(
            "QSplitter::handle { background-color: #ECEFF1; width: 1px; }"
        )

        # Sidebar Sinistra
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 20)
        sidebar_layout.setSpacing(15)
        sidebar.setFixedWidth(320)
        sidebar.setStyleSheet("background-color: #FAFAFA;")

        # Barra di Ricerca
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Cerca nella guida...")
        self.search_edit.setMinimumHeight(42)
        self.search_edit.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #CFD8DC;
                border-radius: 8px;
                padding: 0 15px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #009688;
                background-color: white;
            }
        """
        )
        self.search_edit.textChanged.connect(self._filter_index)
        sidebar_layout.addWidget(self.search_edit)

        # Indice Laterale
        self.index_list = QListWidget()
        self.index_list.setIconSize(QSize(20, 20))
        self.index_list.setStyleSheet(
            """
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 12px 15px;
                border-radius: 10px;
                margin-bottom: 4px;
                color: #455A64;
                font-weight: 500;
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #E0F2F1;
                color: #00796B;
                font-weight: 700;
            }
            QListWidget::item:hover:!selected {
                background-color: #F5F5F5;
            }
        """
        )
        self.index_list.currentRowChanged.connect(self._on_index_changed)
        sidebar_layout.addWidget(self.index_list, 1)  # Force stretch to 1

        # Browser Documentazione
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setReadOnly(True)
        self.browser.setStyleSheet(
            """
            QTextBrowser {
                background-color: white;
                border: none;
                padding: 50px 60px;
                font-family: 'Segoe UI', system-ui, sans-serif;
                font-size: 16px;
                line-height: 1.8;
                color: #263238;
            }
        """
        )

        self.splitter.addWidget(sidebar)
        self.splitter.addWidget(self.browser)
        self.splitter.setStretchFactor(1, 1)

        layout.addWidget(self.splitter)

    def _load_documentation(self):
        """Inizializza le sezioni della documentazione."""
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

        for title, _content, icon_key in self.sections:
            item = QListWidgetItem(title)
            item.setIcon(get_colored_icon(get_asset_path(icon_key), "#546E7A"))
            self.index_list.addItem(item)

        self.index_list.currentRowChanged.connect(self._on_index_changed)

    def _on_index_changed(self, row):
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

    def _filter_index(self, text):
        text = text.lower()
        self.index_list.clear()
        for title, _content, icon_key in self.sections:
            if text in title.lower():
                item = QListWidgetItem(title)
                item.setIcon(get_colored_icon(get_asset_path(icon_key), "#546E7A"))
                self.index_list.addItem(item)
        if self.index_list.count() > 0:
            self.index_list.setCurrentRow(0)

    def open_section(self, section_title: str):
        for i in range(self.index_list.count()):
            if section_title.lower() in self.index_list.item(i).text().lower():
                self.index_list.setCurrentRow(i)
                break

    def _get_intro_md(self):
        return f"""
# Benvenuto in SyncroJob v{VERSION}

La piattaforma integrata per la gestione automatizzata dell'appalto ISAB.

### 🚀 Nuova Navigazione
L'interfaccia è stata ridisegnata per massimizzare la produttività:
* **Sidebar Laterale**: Accesso rapido a tutti i database e strumenti. Clicca su **"Database"** per espandere i moduli.
* **Auto-Focus**: La barra laterale si chiude automaticamente quando selezioni uno strumento, lasciando tutto lo spazio ai tuoi dati.
* **Toolbar Unificata**: Cerca, filtra e aggiorna i dati direttamente dalla barra superiore di ogni tabella.

### 🏗️ Moduli Principali
1. **Automazioni**: I Bot che lavorano per te (Portale Fornitori & SafeWork).
2. **Timbrature**: Database presenze incrociato con anagrafiche.
3. **Strumentale**: Controllo economico (Preventivi, Giornaliere, KPI).
4. **DataEase**: Sincronizzazione avanzata per lo scarico ore cantiere.
5. **PDL**: Ricerca e gestione Permessi di Lavoro.
"""

    def _get_news_md(self):
        return f"""
# 🆕 Novità Versione {VERSION}

### ⚡ Navigazione "Clean Line"
Abbiamo eliminato i vecchi tab ingombranti. Ora l'interfaccia è pulita, veloce e reattiva. I dati sono i protagonisti assoluti.

### ☁️ Modulo DataEase
Nuova integrazione completa per lo **Scarico Ore Cantiere**.
* Sincronizzazione diretta dal file Excel DataEase.
* Calcolo automatico dei totali.
* Selezione intelligente per somme rapide.

### 🛡️ Integrazione SafeWork
Il modulo PDL è ora potenziato:
* Scarica massivamente i permessi in PDF.
* Unisci più permessi in un unico file per l'invio.
* Stampa diretta senza aprire il browser.
"""

    def _get_telegram_md(self):
        return """
# 📱 Controllo Remoto Telegram

Gestisci SyncroJob dal tuo smartphone. Ricevi notifiche in tempo reale e invia comandi ai bot.

### Configurazione Rapida
1. Crea un bot con **@BotFather** su Telegram.
2. Incolla il Token in **Impostazioni > Telegram**.
3. Invia `/start` al tuo bot dallo smartphone.
"""

    def _get_scarico_md(self):
        return """
# 📥 Scarico & Carico TS

Gestione completa del ciclo di vita dei Timesheet.

### Scarico TS (Download)
Automatizza il recupero dei file Excel dal portale.
* **Elaborazione Automatica**: Il sistema calcola i totali e rinomina i file secondo lo standard aziendale.

### Carico TS (Upload)
Carica massivamente i dati sul portale compilerà il form web riga per riga.
"""

    def _get_oda_md(self):
        return """
# 📋 Dettagli OdA & Prenotazioni

### Database OdA
Scarica i dettagli completi (descrizioni, quantità residue, scadenze) per alimentare la ricerca globale di SyncroJob.

### Prenota BP
Prenota massivamente i Badge Provvisori inserendo nomi e date direttamente nell'app.
"""

    def _get_timbrature_md(self):
        return """
# ⏱️ Timbrature

Il cuore della gestione presenze.

### Database
Visualizza tutte le timbrature storicizzate con filtri per Reparto o Cantiere.

### Autopilot
Il sistema può scaricare le timbrature ogni mattina in autonomia all'orario desiderato.
"""

    def _get_contabilita_md(self):
        return """
# 📊 Strumentale (Contabilità)

Visione economica completa dell'appalto.

### Sezioni
* **Preventivi**: Elenco preventivi con stato e importi.
* **Giornaliere**: Dettaglio ore lavorate giorno per giorno.
* **KPI**: Grafici interattivi per monitorare l'andamento mensile.
"""

    def _get_lyra_md(self):
        return """
# ✨ Lyra AI

Il tuo assistente analista personale basato su intelligenza artificiale.

### Cosa può fare?
* **Analisi Dati**: Seleziona delle righe e chiedi a Lyra di trovarne le anomalie.
* **Ricerca Intelligente**: Interroga i tuoi database in linguaggio naturale.
"""

    def _get_shortcuts_md(self):
        return """
# ⚡ Scorciatoie

* **F5**: Aggiorna i dati nel pannello corrente.
* **Ctrl + F**: Attiva la barra di ricerca.
* **Ctrl + C**: Copia le righe selezionate.
* **Tasto Destro**: Menu contestuale esteso.
"""

    def _get_troubleshooting_md(self):
        return """
# 🛠️ Risoluzione Problemi

### Il Bot non parte?
1. Controlla che Chrome sia chiuso.
2. Verifica la connessione VPN ISAB.
3. Controlla le credenziali in Impostazioni.
"""

    def _get_license_md(self):
        return """
# 🔑 Licenza

SyncroJob è protetto da licenza digitale legata all'hardware.
Il rinnovo avviene automaticamente alla scadenza.
"""

    def _get_contacts_md(self):
        return """
# 📞 Contatti & Supporto

Per assistenza tecnica, segnalazione bug o richieste personalizzazioni:

### Giancarlo Allegretti
* **Email**: gianky.allegretti@gmail.com
* **Sviluppo**: Python / Qt6 / AI Integration

> Grazie per aver scelto SyncroJob per ottimizzare il tuo lavoro quotidiano.
"""
