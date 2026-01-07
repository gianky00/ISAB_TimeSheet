"""
SyncroJob - Help Panel
Pannello Guida rivisitato con stile moderno, ricerca integrata e contenuti aggiornati.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


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

        # Header Hero
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4b6cb7, stop:1 #182848);
                border-bottom: 2px solid #0d6efd;
            }
        """
        )
        header_layout = QHBoxLayout(header)

        title = QLabel("📖 Centro Assistenza SyncroJob")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; margin-left: 10px;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        version_hint = QLabel("Documentazione Ufficiale v2.1.26")
        version_hint.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 13px; margin-right: 15px;")
        header_layout.addWidget(version_hint)

        layout.addWidget(header)

        # Splitter per Indice e Contenuto
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sidebar Sinistra
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 15, 10, 15)
        sidebar_layout.setSpacing(10)
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background-color: #f8f9fa; border-right: 1px solid #dee2e6;")

        # Barra di Ricerca
        search_label = QLabel("CERCA NELLA GUIDA")
        search_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #6c757d; margin-left: 5px;")
        sidebar_layout.addWidget(search_label)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔍 Es. Scarico, Lyra, VPN...")
        self.search_edit.setMinimumHeight(35)
        self.search_edit.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 5px 10px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #0d6efd;
            }
        """
        )
        self.search_edit.textChanged.connect(self._filter_index)
        sidebar_layout.addWidget(self.search_edit)

        # Indice Laterale
        self.index_list = QListWidget()
        self.index_list.setStyleSheet(
            """
            QListWidget {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #495057;
            }
            QListWidget::item {
                padding: 12px 10px;
                border-radius: 6px;
                margin-bottom: 2px;
            }
            QListWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
                font-weight: bold;
            }
            QListWidget::item:hover:!selected {
                background-color: #e9ecef;
            }
        """
        )
        self.index_list.currentRowChanged.connect(self._on_index_changed)
        sidebar_layout.addWidget(self.index_list)

        # Browser Documentazione
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setReadOnly(True)
        self.browser.setStyleSheet(
            """
            QTextBrowser {
                background-color: white;
                border: none;
                padding: 40px;
                font-size: 15px;
                line-height: 1.7;
                color: #212529;
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
            ("🚀 Benvenuto", self._get_intro_md()),
            ("🆕 Novità v2.1", self._get_news_md()),
            ("✈️ Configurazione Telegram", self._get_telegram_md()),
            ("📥 Scarico & Elaborazione", self._get_scarico_md()),
            ("📋 Dettagli OdA", self._get_oda_md()),
            ("⏱️ Timbrature & Autopilot", self._get_timbrature_md()),
            ("📊 Strumentale & KPI", self._get_contabilita_md()),
            ("✨ Lyra AI Assistant", self._get_lyra_md()),
            ("⚡ Scorciatoie Veloci", self._get_shortcuts_md()),
            ("🛠️ Risoluzione Problemi", self._get_troubleshooting_md()),
            ("🔑 Sicurezza & Licenza", self._get_license_md()),
            ("📞 Supporto & Contatti", self._get_contacts_md()),
        ]

        for title, _ in self.sections:
            self.index_list.addItem(title)

        self.index_list.setCurrentRow(0)

    def _on_index_changed(self, row):
        if row < 0:
            return

        # Ottieni il titolo visualizzato nell'item
        item = self.index_list.item(row)
        if not item:
            return

        title = item.text()

        # Trova il contenuto originale corrispondente al titolo
        for section_title, content in self.sections:
            if section_title == title:
                self.browser.setMarkdown(content)
                break

    def _filter_index(self, text):
        """Filtra l'indice in base alla ricerca."""
        text = text.lower()
        self.index_list.clear()
        for title, _ in self.sections:
            if text in title.lower():
                self.index_list.addItem(title)

        if self.index_list.count() > 0:
            self.index_list.setCurrentRow(0)

    def open_section(self, section_title: str):
        """Naviga programmaticamente a una sezione specifica."""
        for i in range(self.index_list.count()):
            if section_title.lower() in self.index_list.item(i).text().lower():
                self.index_list.setCurrentRow(i)
                break

    def _get_intro_md(self):
        return """
# Benvenuto in SyncroJob v2.1

SyncroJob è l'ecosistema definitivo per l'automazione dei processi amministrativi e tecnici legati all'appalto ISAB.

### 🌟 Visione del Progetto
L'obiettivo è trasformare ore di lavoro manuale ripetitivo in pochi minuti di supervisione automatizzata, garantendo al contempo una qualità del dato superiore grazie all'integrazione di **intelligenza artificiale** e **database locali ultra-veloci**.

### 🏗️ Architettura
L'applicazione è suddivisa in tre aree principali:
1. **Automazioni (Bot)**: Robot software che navigano sui portali web al posto tuo.
2. **Database & Analisi**: Gestione massiva di dati storici (Contabilità, Timbrature).
3. **Lyra AI**: L'assistente virtuale che ti aiuta a interrogare i dati in linguaggio naturale.

---
### 🚦 Primi Passi
* Assicurati che la **VPN** sia collegata.
* Verifica le tue credenziali in **Impostazioni > Account**.
* Inizia importando i dati base (OdA o Timbrature) per popolare il sistema.
"""

    def _get_news_md(self):
        return """
# 🆕 Novità Versione 2.1.26

L'aggiornamento odierno introduce cambiamenti radicali per migliorare la velocità operativa.

### ⚡ Addio Macro Excel (VBA)
Abbiamo migrato la logica di calcolo e rinomina dei file Timesheet direttamente in **Python**.
* **Più veloce**: Non è più necessario aprire Excel visibilmente per processare i file.
* **Integrato**: Tutto avviene all'interno del pannello "Scarico TS".
* **Senza Errori**: Gestione automatica dei conflitti di nomi e delle cartelle mancanti.

### 🎨 Restyling Interfaccia
* **Date Unificate**: I selettori data ora mostrano un'icona calendario e sono allineati ai fornitori.
* **Layout Compatti**: Parametri più vicini per ridurre i movimenti del mouse.
* **Visualizzazione Fusion**: UI coerente su Windows 10 e 11.

### 🤖 Miglioramenti Bot
* **Scarico TS Batch**: I file vengono elaborati in blocco solo al termine di tutti i download.
* **Resilienza**: Migliorata la gestione dei caricamenti infiniti sul portale ISAB.
"""

    def _get_telegram_md(self):
        return """
# ✈️ Configurazione Bot Telegram

Il controllo remoto ti permette di interagire con SyncroJob ovunque tu sia tramite l'app Telegram. Per garantire il corretto funzionamento in ambienti multi-PC, **ogni installazione deve avere il proprio bot dedicato**.

### 1. Creazione del Bot (Uno per ogni PC)
1. Apri Telegram e cerca **@BotFather**.
2. Scrivi il comando `/newbot`.
3. Scegli un **Nome** (es. `SyncroJob Ufficio Luca`).
4. Scegli uno **Username** univoco che finisca per bot (es. `luca_isab_bot`).
5. BotFather ti fornirà un **API TOKEN** (una stringa lunga di numeri e lettere).

### 2. Collegamento all'App
1. Copia il Token e incollalo in **Impostazioni > Telegram** su questo PC.
2. Clicca su **Salva Impostazioni**.
3. Il servizio si avvierà automaticamente.

### 3. Autorizzazione (Chat ID)
Per motivi di sicurezza, il bot risponderà solo a te (il proprietario).
1. Apri la chat del tuo nuovo bot su Telegram.
2. Premi il tasto **AVVIA** (o scrivi `/start`).
3. L'App SyncroJob riconoscerà il tuo ID e lo salverà come "Autorizzato".
4. Da questo momento, vedrai apparire il menu dei comandi sullo smartphone.

> ⚠️ **Nota Multi-PC**: Non usare lo stesso Token su due PC diversi, altrimenti il bot smetterà di rispondere a causa di conflitti di connessione.
"""

    def _get_scarico_md(self):
        return """
# 📥 Scarico TS & Elaborazione

Questa sezione permette di automatizzare il recupero dei timesheet dal portale ISAB.

### Flusso Operativo
1. Seleziona il **Fornitore** e la **Data Da**.
2. Inserisci i numeri **OdA** nella tabella.
3. Seleziona la **Destinazione** (dove salvare i file).
4. Attiva **"Elabora TS"** se desideri che il sistema esegua i calcoli automatici (ex VBA).

### ⚙️ Cosa fa il flag "Elabora TS"?
Quando attivo, al termine dello scarico, Python apre ogni file Excel scaricato e:
* Analizza il foglio **"Timesheet"**.
* Conta il numero di **POS univoci** presenti.
* Esegue eventuali logiche di controllo congruenza.
* Mostra un riepilogo dettagliato nei log dell'app.

> 💡 **Tip**: Puoi lasciare l'App in background durante lo scarico. Una notifica ti avviserà al termine.
"""

    def _get_oda_md(self):
        return """
# 📋 Gestione Dettagli OdA

Il bot Dettagli OdA è fondamentale per popolare il database interno con le informazioni degli ordini d'acquisto.

### Funzionalità
* Estrae: Posizione OdA, Descrizione, Quantità Residua, Scadenza.
* **Sincronizzazione**: Salva tutto nel DB locale per permettere ricerche istantanee.
* **Filtri Temporali**: Puoi limitare lo scarico a ordini creati in un determinato periodo.

### 🔍 Utilizzo del Database
Una volta scaricati i dettagli, puoi trovarli nei pannelli di ricerca:
* Usa la barra di ricerca globale per trovare un OdA partendo da una parola chiave nella descrizione.
* I dati rimangono disponibili anche offline.
"""

    def _get_timbrature_md(self):
        return """
# ⏱️ Timbrature & Autopilot

Gestisci il flusso delle presenze ISAB in modo professionale.

### 🗓️ Autopilot (Scheduler)
Configura l'App per scaricare le timbrature ogni giorno automaticamente.
* Vai in **Timbrature > Autopilot**.
* Scegli un orario (es. 08:30).
* Il sistema scaricherà le timbrature di "Ieri" ogni mattina se l'app è aperta.

### 📊 Integrazione Database
Le timbrature vengono incrociate con l'anagrafica dipendenti:
* **Reparto/Cantiere**: Assegna una volta sola il reparto a un dipendente per averlo sempre categorizzato correttamente nei report.
* **Alert Uscite**: Il sistema evidenzia le timbrature senza orario di uscita.
"""

    def _get_contabilita_md(self):
        return """
# 📊 Strumentale & KPI

Il modulo Contabilità analizza i dati storici e correnti per fornire una visione economica dell'appalto.

### 📈 Pannello KPI
Visualizza metriche in tempo reale:
* Ore totali caricate per cantiere/reparto.
* Efficienza dei team.
* Alert su budget OdA in esaurimento.

### 🛠️ Gestione Strumentale
Permette di importare il file "Bilancio Strumentale" per incrociare le ore caricate con quelle effettivamente pagate.
* **Importazione Intelligente**: Riconosce automaticamente i nuovi record aggiunti al foglio Excel.
"""

    def _get_lyra_md(self):
        return """
# ✨ Lyra AI Assistant

Lyra non è un semplice chatbot, ma un'estensione intelligente del tuo lavoro.

### 🧠 Capacità di Lyra
* **Analisi Dati**: *"Chi ha lavorato più di 10 ore ieri?"*
* **Riepiloghi**: *"Fammi un sommario dell'OdA 4041"*.
* **Troubleshooting**: Chiedi a Lyra come risolvere un errore del browser.

### 🛡️ Lyra Sentinel
Un guardiano silenzioso che analizza il database in background.
Se Sentinel trova qualcosa di strano (es. un dipendente che ha timbrato ma non ha ore caricate in contabilità), ti invierà una notifica immediata.
"""

    def _get_shortcuts_md(self):
        return """
# ⚡ Scorciatoie e Produttività

Velocizza il tuo lavoro con i comandi rapidi.

### Tastiera
* **F5**: Refresh dati o Start Bot nel pannello attivo.
* **ESC**: Chiude i dialoghi o pulisce la ricerca.
* **Ctrl + C / Ctrl + V**: Copia e Incolla stile Excel nelle tabelle bot.
* **Ctrl + F**: Sposta il cursore sulla barra di ricerca.

### Mouse
* **Tasto Destro**: Menu contestuale su tutte le tabelle (Analizza con Lyra, Elimina, Copia).
* **Doppio Click**: Apre il dettaglio di un record nelle tabelle database.
"""

    def _get_troubleshooting_md(self):
        return """
# 🛠️ Risoluzione Problemi

### 🌐 VPN e Portale
Se il bot fallisce il login:
1. Verifica se riesci ad accedere manualmente a `portale.isab.com` da Chrome.
2. Controlla che le credenziali siano corrette (occhio a scadenze password ISAB).

### 🖥️ Problemi Browser
* **"Chrome non trovato"**: Assicurati che Chrome sia installato nel percorso standard.
* **Bot Bloccato**: Se il portale è molto lento, aumenta il **Timeout** nelle Impostazioni (consigliato 45-60s per connessioni lente).

### 🧹 Pulizia Totale
In caso di problemi persistenti, puoi usare **Impostazioni > Diagnostica > Apri cartella dati** ed eliminare il file `config.json` (Attenzione: perderai le impostazioni salvate).
"""

    def _get_license_md(self):
        return """
# 🔑 Sicurezza e Licenza

SyncroJob adotta standard di sicurezza enterprise.

### Protezione Dati
* **Password**: Salvate nel portachiavi di sistema di Windows (Windows Credentials Manager), mai in chiaro nei file.
* **Database**: Dati criptati a riposo.

### Gestione Licenza
La licenza è associata al tuo **Hardware ID**.
* **Validità**: Controllabile nella barra laterale.
* **Rinnovo**: L'app scarica automaticamente i rinnovi dal server se disponibile una connessione internet.
"""

    def _get_contacts_md(self):
        return """
# 📞 Supporto e Sviluppo

Hai bisogno di assistenza o vuoi richiedere una nuova funzionalità?

### 👤 Sviluppatore
**Giancarlo Allegretti**
* **Email**: support@syncrojob.it
* **Web**: [projectjob-bot.netlify.app](https://projectjob-bot.netlify.app)

### 🐛 Segnala un Bug
Per una risoluzione veloce, invia sempre:
1. Una descrizione dell'operazione che stavi facendo.
2. Uno screenshot dell'errore (se presente).
3. Il file di log (scaricabile da Impostazioni).

*Grazie per aver scelto SyncroJob!* 🚀
"""
