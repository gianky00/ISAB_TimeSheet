"""
Bot TS - Help Panel
Pannello Guida rivisitato con stile moderno e coinvolgente.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QFrame, QLabel, QListWidget, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class HelpPanel(QWidget):
    """
    Pannello Guida Tecnico-Operativo.
    Implementa una documentazione strutturata in Markdown con navigazione laterale.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._load_documentation()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header Hero
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4b6cb7, stop:1 #182848);
                border-bottom: 2px solid #0d6efd;
            }
        """)
        header_layout = QHBoxLayout(header)
        
        title = QLabel("📖 Documentazione Tecnica")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; margin-left: 10px;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        version_hint = QLabel("Manuale Operativo v2.1")
        version_hint.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 13px; margin-right: 15px;")
        header_layout.addWidget(version_hint)
        
        layout.addWidget(header)

        # Splitter per Indice e Contenuto
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Indice Laterale
        self.index_list = QListWidget()
        self.index_list.setFixedWidth(250)
        self.index_list.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: none;
                border-right: 1px solid #dee2e6;
                font-size: 14px;
                padding: 10px;
                color: #495057;
            }
            QListWidget::item {
                padding: 12px 8px;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #e9ecef;
            }
        """)
        self.index_list.currentRowChanged.connect(self._on_index_changed)
        
        # Browser Documentazione
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setReadOnly(True)
        self.browser.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border: none;
                padding: 30px;
                font-size: 15px;
                line-height: 1.6;
            }
        """)
        
        self.splitter.addWidget(self.index_list)
        self.splitter.addWidget(self.browser)
        self.splitter.setStretchFactor(1, 1)
        
        layout.addWidget(self.splitter)

    def _load_documentation(self):
        """Inizializza le sezioni della documentazione."""
        self.sections = [
            ("🚀 Introduzione", self._get_intro_md()),
            ("⚡ Scorciatoie", self._get_shortcuts_md()),
            ("🤖 Automazioni", self._get_automations_md()),
            ("🗄️ Database & Filtri", self._get_database_md()),
            ("✨ Lyra AI", self._get_lyra_md()),
            ("🛠️ Risoluzione Problemi", self._get_troubleshooting_md()),
            ("🔑 Licenza & Accesso", self._get_license_md())
        ]

        for title, _ in self.sections:
            self.index_list.addItem(title)
        
        self.index_list.setCurrentRow(0)

    def _on_index_changed(self, row):
        if 0 <= row < len(self.sections):
            _, content = self.sections[row]
            self.browser.setMarkdown(content)

    def _get_intro_md(self):
        return """
# Introduzione a Bot TS

**Bot TS** è una piattaforma di automazione avanzata per la gestione dei flussi di lavoro legati ai Timesheet (TS) e alla Contabilità Cantiere.

### Obiettivi del Sistema
* **Efficienza**: Riduzione del tempo di inserimento dati del 70%.
* **Precisione**: Eliminazione degli errori manuali di trascrizione.
* **Centralizzazione**: Un unico database per timbrature, OdA e consuntivi.

---
### Requisiti di Sistema
* Connessione VPN attiva per l'accesso ai portali ISAB.
* Browser Chrome installato (per l'esecuzione dei Bot).
* Licenza valida rilasciata da Amministrazione.
"""

    def _get_shortcuts_md(self):
        return """
# Comandi Rapidi (Globali)

Utilizza le scorciatoie da tastiera per velocizzare le operazioni comuni.

| Comando | Azione | Contesto |
|:---|:---|:---|
| **F5** | Aggiorna dati / Avvia Bot | Tutte le viste |
| **Ctrl + F** | Focus barra di ricerca | Database |
| **Ctrl + S** | Salva impostazioni | Impostazioni |
| **Ctrl + C** | Copia righe selezionate | Tabelle Database |
| **Canc** | Rimuovi riga selezionata | Tabella Scarico TS |

> **Nota**: Il comando F5 nel pannello **DataEase** avvia l'importazione incrementale automatica dei nuovi record.
"""

    def _get_automations_md(self):
        return """
# Moduli di Automazione

### 1. 📥 Scarico TS (Report Portale)
Scarica massivamente i PDF o Excel dei Timesheet filtrando per Fornitore e Data.
* **Caso d'uso**: Recupero di tutti i TS firmati di un mese per verifica contabile.
* **Suggerimento**: Inserisci i numeri OdA uno per riga.

### 2. 📋 Dettagli OdA
Estrae le informazioni strutturate (posizioni, importi, scadenze) dagli ordini d'acquisto.
* **Database**: I dati vengono salvati localmente per permettere ricerche istantanee senza caricare il portale.

### 3. ⏱️ Timbrature (Isab)
Sincronizza le presenze del personale.
* **Autopilot**: Se abilitato nelle impostazioni, il sistema scarica le timbrature del giorno precedente ogni mattina all'orario prefissato.

### 4. 📤 Carico TS (Input Dati)
Esegue l'upload automatico delle righe TS sul portale ISAB.
* **Attenzione**: Verifica sempre i dati nella tabella di anteprima prima di cliccare su *Avvia*.
"""

    def _get_database_md(self):
        return """
# Gestione Database e Filtri

Il sistema utilizza database SQLite locali per garantire performance elevate anche con migliaia di righe.

### Filtri Avanzati
Nelle tabelle **Strumentale** e **DataEase**, puoi filtrare utilizzando la logica *multi-term*:
* Esempio: `rossi 4041` -> Mostra tutte le righe di Rossi relative all'OdC 4041.
* Esempio: `cantiere sud` -> Filtra per reparti o zone specifiche.

### DataEase (Virtual Table)
Il pannello DataEase gestisce oltre 130.000 righe.
* **ETA Importazione**: Durante l'aggiornamento, il sistema calcola il tempo stimato basandosi sulla velocità di scrittura del disco e sulla dimensione del file Excel.
* **Conteggio Righe**: Visibile in tempo reale nel footer in grassetto blu.
"""

    def _get_lyra_md(self):
        return """
# ✨ Lyra AI - Assistente Intelligente

Lyra è l'intelligenza artificiale integrata che analizza il contesto dei tuoi dati per trovare anomalie o fornire riepiloghi.

### Come interagire con Lyra:
1. **Dalle Tabelle**: Clicca con il tasto destro su una riga -> *Analizza con Lyra*.
2. **Dal Pannello Lyra**: Scrivi una domanda libera (es. *"Quali sono le timbrature senza uscita del mese scorso?"*).
3. **Lyra Sentinel**: Un servizio in background che monitora silenziosamente il database e ti avvisa se rileva anomalie critiche (es. discrepanze tra ore caricate e ore timbrate).
"""

    def _get_troubleshooting_md(self):
        return """
# Risoluzione Problemi

### Errore: Portale non raggiungibile
* Verifica la connessione VPN.
* Controlla se le credenziali ISAB in **Impostazioni > Account** sono corrette.

### Errore: Chrome non si avvia
* Assicurati di non avere istanze "orfane" di Chrome aperte (usa *Gestione Attività*).
* Verifica il timeout nelle impostazioni browser (consigliato: 30s).

### Diagnostica & Log
In caso di crash o comportamenti anomali:
1. Vai in **Impostazioni**.
2. Clicca su **🛠️ Diagnostica & Licenza > Apri cartella Logs**.
3. Invia il file `secure_bot.log` o `crash.log` allo sviluppatore.
"""

    def _get_license_md(self):
        return """
# Licenza e Accesso

L'applicazione è protetta da licenza software legata alla postazione di lavoro.

### Dati Licenza
Visibili nella parte inferiore della sidebar:
* **Cliente**: Nome dell'azienda o utente intestatario.
* **Scadenza**: Data di termine validità del servizio.

### Rinnovo
Al raggiungimento della scadenza, l'applicazione richiederà un nuovo file di licenza (`validity.token`).
Contatta l'amministratore di sistema per generare un nuovo token dopo aver fornito l'ID macchina visualizzato nel popup di errore.
"""

