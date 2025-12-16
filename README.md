# Bot TS

**Sistema di Automazione per Portale ISAB**

Applicazione desktop per l'automazione delle operazioni sul portale fornitori ISAB, sviluppata da Giancarlo Allegretti.

## 🚀 Funzionalità

### Bot Disponibili

| Bot | Descrizione |
|-----|-------------|
| **📥 Scarico TS** | Download automatico dei timesheet per commessa/mese/anno |
| **📋 Dettagli OdA** | Login automatico per consultazione Ordini di Acquisto |

### Caratteristiche

- ✅ Interfaccia grafica moderna (PyQt6)
- ✅ Gestione multi-commessa con tabelle editabili
- ✅ Menu contestuale per gestione righe (tasto destro)
- ✅ Sistema di licenze con validazione hardware
- ✅ Aggiornamenti automatici via Netlify
- ✅ Configurazione credenziali e percorsi
- ✅ Log dettagliato delle operazioni

## 📦 Installazione

### Utente Finale

1. Scarica l'installer da [bot-ts.netlify.app](https://bot-ts.netlify.app)
2. Esegui `BotTS_Setup_x.x.x.exe`
3. Inserisci i file di licenza nella cartella indicata
4. Avvia l'applicazione

### Sviluppatore

```bash
# Clone repository
git clone https://github.com/gianky00/bot-ts.git
cd bot-ts

# Crea virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Installa dipendenze
pip install -r requirements.txt

# Avvia applicazione
python main.py
```

## 🛠️ Build & Release

### Build Locale (senza deploy)

```batch
release_patch_no_Deploy.bat [major|minor|patch]
```

### Release Completa (con deploy Netlify)

```batch
release_patch.bat [major|minor|patch]
```

### Struttura Output

```
admin/Crea Setup/Setup/
├── BotTS_Setup_x.x.x.exe    # Installer
└── netlify/
    ├── version.json         # Info versione
    └── index.html           # Redirect download
```

## 📁 Struttura Progetto

```
bot-ts/
├── main.py                  # Entry point
├── requirements.txt         # Dipendenze Python
├── src/
│   ├── core/               # Moduli core
│   │   ├── version.py      # Versione app
│   │   ├── config_manager.py
│   │   ├── license_validator.py
│   │   ├── license_updater.py
│   │   └── app_updater.py
│   ├── bots/               # Bot modulari
│   │   ├── base/           # Classe base
│   │   ├── scarico_ts/     # Bot Scarico TS
│   │   └── dettagli_oda/   # Bot Dettagli OdA
│   ├── gui/                # Interfaccia grafica
│   │   ├── main_window.py
│   │   ├── panels.py
│   │   ├── widgets.py
│   │   └── settings_panel.py
│   └── utils/              # Utility
├── admin/
│   ├── bump_version.py     # Script versioning
│   ├── Crea Licenze/       # Tool generazione licenze
│   └── Crea Setup/         # Build scripts
├── assets/                 # Icone (generate)
└── tests/                  # Unit tests
```

## 🔑 Sistema Licenze

### Generazione (Admin)

```bash
python admin/Crea\ Licenze/admin_license_gui.py
```

### File Licenza

```
%LOCALAPPDATA%\Programs\Bot TS\Licenza\
├── config.dat        # Dati licenza cifrati
└── manifest.json     # Checksum integrità
```

### Repository Licenze

Le licenze vengono distribuite tramite repository GitHub privato:
`github.com/gianky00/intelleo-licenses/tree/main/licenses`

## ⚙️ Configurazione

### Percorso Dati

- **Windows**: `%LOCALAPPDATA%\Programs\Bot TS\`
- **Linux**: `~/.local/share/Bot TS/`

### File Configurazione

`config.json`:
```json
{
    "download_path": "",
    "isab_username": "",
    "isab_password": "",
    "browser_headless": false,
    "browser_timeout": 30,
    "last_ts_data": [],
    "last_oda_data": []
}
```

## 🧪 Testing

```bash
pytest tests/ -v
```

## 📋 Requisiti

- Python 3.10+
- Google Chrome (per automazione Selenium)
- Windows 10/11 (target principale)

## 📄 Licenza

Software proprietario - Giancarlo Allegretti

## 👤 Autore

Giancarlo Allegretti
