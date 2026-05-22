# Miglioramento Sistema Impostazioni - Implementation Plan

Questo piano descrive gli step per evolvere il sistema di configurazione attuale (`SettingsPanel` e `ConfigManager`) verso una soluzione piùù robusta, user-friendly e portabile.

## Analisi Stato Attuale

* **Backend (`config_manager.py`)**: Solido. Usa JSON atomico, `platformdirs`, thread-safe.
* **Frontend (`settings_panel.py`)**: Ricco ma potenzialmente dispersivo (`QToolBox` verticale). Gestisce molte liste manualmente.
* **Mancanze**: Nessuna validazione proattiva dei file, nessun modo facile per esportare/importare configurazioni complete (backup/restore), navigazione lenta tra le sezioni.

## Proposte di Miglioramento

### 1. UX & Navigazione

- [ ] **Ricerca Rapida**: Aggiungere una barra di ricerca in alto nel pannello impostazioni per trovare rapidamente un'opzione (es. "token", "timeout") senza aprire tutti i tab.
* [ ] **Indicatore Validità**: Aggiungere icone di stato (✅/❌) accanto ai campiù percorso (File Path) che verificano in tempo reale se il file/cartella esiste.

### 2. Gestione Dati (Import/Export)

- [ ] **Export Configurazione**: Permettere all'utente di esportare l'intero JSON (o una parte) in un file `.zip` o `.json` per backup o condivisione.
* [ ] **Import Configurazione**: Permettere di ripristinare le impostazioni da un file.
* [ ] **Reset Selettivo**: Aggiungere un pulsante "Ripristina Default" per ogni singola sezione, non solo globale.

### 3. Validazione & Robustezza

- [ ] **Validazione Schema**: Introdurre uno schema di validazione (es. usando `pydantic` o validazione manuale piùù stretta) per evitare che stringhe corrotte rompano l'app.
* [ ] **Self-Repair**: Se un file di configurazione è corrotto all'avvio, offrire di rigenerarlo o caricarne una versione precedente (backup automatico interno).

## Piano Operativo (Step-by-Step)

### Fase 1: Validazione Visuale (Low Effort / High Impact)

Modificare `SettingsPanel` per aggiungere feedback visivo immediato sui percorsi file.
* **Files**: `src/gui/settings_panel.py`
* **Azione**: Aggiungere `textChanged` signal ai `QLineEdit` dei path che controlla `os.path.exists` e colora il bordo di rosso/verde.

### Fase 2: Import/Export (Medium Effort)

Implementare la logica di backup e ripristino configurazione.
* **Backend**: Aggiungere `export_config(path)` e `import_config(path)` in `config_manager.py`.
* **UI**: Aggiungere pulsanti "Esporta Impostazioni" e "Importa" nel footer del pannello o in un menu "Avanzate".

### Fase 3: Ricerca (Optional / High Polish)

Aggiungere una barra di filtro che nasconde/mostra i widget nel `QToolBox` o evidenzia i match.

## User Action Required

Quale di queste fasi ha la prioritàà per te?

1. **Validazione Visuale** (evita errori di percorso file)
2. **Import/Export** (sicurezza dati e portabilitàà)
3. **UX/Ricerca** (comodità d'uso)

Personalmente raccomando di iniziare dalla **Fase 2 (Import/Export)** per garantire la sicurezza della configurazione prima di fare altre modifiche, oppure la **Fase 1** per un feedback immediato.
