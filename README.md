# 🚀 SyncroJob Enterprise

**Piattaforma Integrata di Automazione e Gestione per Portale ISAB**

SyncroJob è una suite software avanzata progettata per automatizzare, monitorare e ottimizzare i flussi di lavoro aziendali sul portale fornitori ISAB e SafeWork.

## 🌟 Funzionalità Principali

### 🤖 Automazione Portali

- **Portale Fornitori ISAB**: Download/upload timesheet, estrazione OdA, timbrature.
- **SafeWork Bot**: Ricerca e sincronizzazione PDL (Piano di Lavoro) in modo completamente automatizzato.
- **DataEase Sync**: Sincronizzazione intelligente differenziale dei dati di cantiere.

### 🛡️ Sicurezza & Affidabilità

- **Audit Trail Certificato**: Registro immutabile (SHA-256 hash chaining) di tutte le operazioni critiche.
- **Crash Detection**: Loguru + faulthandler per catturare e salvare ogni eccezione su `logs/crash.txt`.
- **Licenza Hardware-Bound**: Validazione della licenza legata all'hardware del PC.

### 🎨 Interfaccia Moderna

- **Dashboard Modulare**: Feed eventi real-time, Autopilot scheduler, Quick Actions.
- **Design Premium**: PySide6 con tema HSL dark/light, animazioni fluide, widget personalizzati.
- **Notifiche Smart**: Centro notifiche unificato con filtri per priorità.

---

## 🤖 Moduli Operativi

| Modulo | Descrizione | Stato |
|--------|-------------|-------|
| **📥 Scarico TS** | Download massivo timesheet (PDF/Excel) per commessa/periodo. | ✅ Attivo |
| **📋 Dettagli OdA** | Estrazione e sincronizzazione Ordini di Acquisto. | ✅ Attivo |
| **⏱️ Timbrature** | Gestione, validazione e storicizzazione timbrature dipendenti. | ✅ Attivo |
| **🏗️ SafeWork PDL** | Ricerca e sincronizzazione Piano di Lavoro da SafeWork. | ✅ Attivo |
| **📤 Carico TS** | Upload automatizzato dei timesheet validati. | ✅ Attivo |
| **📊 Contabilità** | Gestione strumentali e certificati campione. | ✅ Attivo |

---

## 📦 Installazione e Requisiti

### Requisiti di Sistema

- **OS**: Windows 10/11 (64-bit)
- **Browser**: Google Chrome (Ultima versione)
- **Rete**: Connessione internet attiva (per Portali e Licenza)

### Installazione Utente

1. Scarica l'ultimo installer da **[projectjob-bot.netlify.app](https://projectjob-bot.netlify.app)**.
2. Esegui `SyncroJob_Setup_vX.X.X.exe`.
3. Al primo avvio, il sistema configurerà automaticamente l'ambiente.

---

## 🛠️ Sviluppo

### Setup Ambiente

```bash
# Installazione dipendenze (Poetry)
uv sync

# Attivazione venv
uv venv
```

### Comandi Utili

```bash
# Avvio app
uv run syncrojob

# Suite di test completa
python -m tests.run_robust_test

# Linting + fix automatico
uv run ruff check --fix

# Type checking strict
uv run mypy --strict src/

# Tutti i quality gate pre-commit
uv run pre-commit run --all-files

# Bump versione (commitizen — non modificare version.py manualmente!)
uv run cz bump
```

Per la documentazione architetturale completa, vedi [`.ai-context.json`](./.ai-context.json) e [`CLAUDE.md`](./CLAUDE.md).

---

## 🔑 Licenza e Supporto

Software proprietario sviluppato da **Giancarlo Allegretti**.
L'uso è consentito solo tramite licenza attiva validata su hardware specifico.

- **Supporto Tecnico**: Integrato nell'app (Tab Help) o via Telegram.
- **Documentazione**: Vedi cartella `docs/`.
