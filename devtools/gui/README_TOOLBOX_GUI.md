# Developer Toolbox GUI - Guida Rapida

## 🚀 Avvio

### Windows
```bash
# Doppio click o esegui da terminale:
scripts\toolbox_gui.bat

# Oppure direttamente con Python:
.venv\Scripts\python.exe admin\developer_toolbox_gui.py
```

### Linux/macOS
```bash
python devtools/gui/developer_toolbox_gui.py
```

## 📋 Funzionalità

### SYSTEM BOOTSTRAP AND SETUP
- **Init System**: Installa/Aggiorna tutte le librerie tramite Poetry

### QUALITY AND SECURITY ENGINE
- **Full Audit**: Analisi totale (Sicurezza, Tipi, Stile e Test)
- **Fast Audit**: Check completo saltando i test (più rapido)
- **Smart Check**: Analisi incrementale (solo file modificati Git)
- **Only Tests**: Esegue solo la suite unitaria di robustezza
- **Auto-Fix**: Sistema automaticamente errori di stile Ruff
- **Dashboard**: Apre il report HTML dell'ultimo Audit

### SECURITY AND ARCHITECTURE
- **Security Scan**: Pip-audit per verificare vulnerabilità CVE
- **Coverage**: Genera report HTML di copertura del codice
- **Architecture**: Genera diagramma delle classi (PNG)

### DOCUMENTATION AND KNOWLEDGE
- **Build Docs**: Compila la documentazione MkDocs (statica)
- **Serve Docs**: Avvia server live per vedere i manuali

### CI/CD, RELEASE AND DEPLOY
- **Commit Wizard**: Guida al commit standard (Conventional Commits)
- **Version Bump**: Incrementa versione e genera Changelog
- **Full Release**: Build EXE totale (con certificazione e test)
- **Fast Release**: Build EXE rapida (salta i test)
- **Full Deploy**: Release + Caricamento su server/distribuzione

### ENTERPRISE POWER TOOLS
- **Secrets Mgmt**: Gestore grafico delle chiavi e credenziali
- **Performance**: Profiling profondo (cProfile) per trovare bottleneck
- **DB Maintain**: Ottimizzazione e Integrity Check SQLite
- **Raw Metrics**: Complessità ciclomatica e indici tecnici
- **Clean Code**: Rimuove codice commentato e dead code
- **Depty Check**: Verifica dipendenze inutilizzate (Deptry)
- **Project Stats**: Statistiche linee di codice e linguaggi
- **Dep Audit**: Verifica isomorfismo dipendenze Sorgente/EXE

### SYSTEM AND RUN
- **Run App (Dev)**: Avvia l'app in modalità Sviluppo (Debug)
- **Clean Cache**: Pulisce .pyc, __pycache__ e temp files
- **Inspector**: Ispezione universale del sistema/log

## 💡 Vantaggi rispetto a toolbox.bat

✅ **Nessun problema di encoding** - Supporta emoji e caratteri Unicode nativamente
✅ **Output in tempo reale** - Vedi i log mentre il comando viene eseguito
✅ **Stop Process** - Puoi interrompere comandi lunghi con un click
✅ **Cross-platform** - Funziona su Windows, Linux, macOS
✅ **Interfaccia moderna** - Pulsanti categorizzati e console integrata
✅ **Multi-threading** - I comandi non bloccano la UI
✅ **Tooltips informativi** - Hover sui pulsanti per vedere descrizioni

## 🎨 Caratteristiche UI

- **Pannello sinistro**: Tutti i comandi organizzati per categoria
- **Pannello destro**: Console di output in tempo reale (stile VS Code)
- **Clear Console**: Pulisce l'output con un click
- **Stop Process**: Termina il processo in esecuzione (utile per mkdocs serve, ecc.)

## 🔧 Note Tecniche

- Basato su **PySide6** (stesso framework dell'app principale)
- Esecuzione comandi in **thread separati** (non blocca la UI)
- Supporta processi **interattivi** (mkdocs serve, cz commit, ecc.)
- Encoding **UTF-8** nativo (nessun problema con emoji)
- Working directory automaticamente impostata su **PROJECT_ROOT**

## 🐛 Troubleshooting

**La GUI non si avvia**:
- Verifica che l'ambiente virtuale sia attivo
- Esegui: `poetry install` o `pip install -e .`

**Il comando non produce output**:
- Alcuni comandi potrebbero richiedere tempo prima di mostrare output
- Usa "Stop Process" se un comando sembra bloccato

**Errore "python.exe not found"**:
- Crea l'ambiente virtuale prima: `python -m venv .venv`
- Oppure usa Poetry: `poetry install`
