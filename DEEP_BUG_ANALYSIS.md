# 🦠 DEEP BUG ANALYSIS REPORT

**Data di Generazione**: 13 Marzo 2026
**Esecutore**: Gemini CLI (Architetto Senior / Security Auditor)
**Analisi Eseguita su**: Pytest, Bandit (Sicurezza), Vulture (Codice Morto), Static Analysis.

---

## 1. Regressioni Runtime & Test Failures (Pytest)

Durante l'esecuzione della robust test suite, è emerso **1 errore**:

*   **File**: `tests/integration/test_safework_pdl_flow.py`
*   **Test**: `test_full_pdl_flow_simulation` e `test_pdl_flow_with_search_failure`
*   **Errore Rilevato**: `AssertionError: False is True` a causa di `❌ Validazione fallita: Nessun numero PDL trovato nei dati.`
*   **Root Cause**: Incongruenza di chiavi nei dizionari. Il test mocka i dati passando la chiave `"pdl_number"`, ma il nuovo parser in `SafeWorkPDLBot.validate_data` (o una precedente modifica di conformità alla UI) si aspetta la chiave `"numero_pdl"` (come definito in `get_columns()`).
*   **Stato**: **RISOLTO** (Chiavi normalizzate nel mock del test).

---

## 2. Vulnerabilità di Sicurezza (Bandit)

L'analisi con Bandit ha scansionato `~50.000` righe di codice (Loc) rilevando alcune vulnerabilità di bassa entità, ma nessuna falla grave.

### Risultati Sintetici:
*   `SEVERITY.HIGH`: **0**
*   `SEVERITY.MEDIUM`: **0**
*   `SEVERITY.LOW`: **51**

### Dettaglio (Falsi Positivi / Low Severity):
*   **`B608 (Hardcoded SQL Expressions)`**: Bandit segnala potenziali vulnerabilità di SQL Injection (es. `src/core/database/migrations/*`, `src/core/database/pdl_queries.py`). Spesso questo accade perché si utilizzano f-string o interpolazioni base per query SQL. Nel contesto dell'app, essendo l'accesso confinato a un db SQLite locale offline/interno o con input sanitizzati internamente (es. `validators.py`), l'impatto reale (exploitability) è minimo, ma andrebbe considerato l'uso coerente di Query Parametrizzate (`?`) con la libreria `sqlite3`.
*   **`B106 (Hardcoded Password)`**: Segnalati `2` alert di confidenza bassa legati a funzioni che probabilmente gestiscono password mockate (es. nei test) o logica legata a chiavi predefinite (`test_password`, dummy credentials, ecc.).
*   *Nota*: Nessuna esposizione critica (Hardcoded Credentials reali, Broken Access Control o Esecuzione Remota RCE) rilevata.

---

## 3. Debt Architetturale & Codice Morto (Vulture)

L'analisi condotta con Vulture ha restituito numerosi warning su funzioni, classi e metodi etichettati come non utilizzati (`60% confidence`). Dopo un'ispezione mirata (Grep Search), abbiamo classificato queste segnalazioni in due categorie: **Codice Obsoleto** e **Implementazioni Disconnesse**.

### A. Codice Obsoleto / Over-engineering (Da Eliminare)
*   **`src/bots/base/wait_helpers.py`**: Funzioni come `poll_for_download_complete` o `wait_for_element_staleness` non sono referenziate da nessun bot moderno. Sono residui di vecchie logiche di attesa sostituite da meccanismi più robusti.
*   **`src/core/logging/metrics.py`**: L'intera logica di rilevamento anomalie (`is_anomaly`, `auto_learn_baselines`, `save_baselines_to_file`) è un chiaro caso di over-engineering. Il framework traccia le metriche ma la logica di alerting predittivo non è agganciata a nessun cronjob o worker.
*   **UI Design System (`src/gui/design/spacing.py` / `typography.py`)**: Costanti come `xxs`, `xl`, `overline` definite ma mai usate nei widget.

### B. Implementazioni Disconnesse / WIP (Da Riagganciare o Rimuovere)
*   **`generate_email_report` (`src/gui/panels/dipendenti/utils/report_generator.py`)**: Questa funzionalità complessa di reportistica Excel/HTML via email è completa nel backend. Tuttavia, nella UI (`src/gui/panels/dipendenti/pages/anagrafica_page.py`), il pulsante di generazione richiama una funzione locale `_generate_email_report` che contiene un `pass` e il commento: `# ... logica report delegata al controller ...`. L'architettura è stata predisposta ma l'hook finale è mancante.
*   **Variabili non inizializzate (es. PDF/Excel config)**: Diversi moduli configurano classi per l'esportazione dati che risultano "Unused" semplicemente perché il layer UI non invoca più i controller di esportazione.

*Raccomandazione Architetturale*: Procedere con una PR dedicata esclusivamente all'eliminazione chirurgica della Categoria A (Obsoleto). Per la Categoria B, aprire dei ticket tecnici per decidere se completare il refactoring dei Controller o rimuovere le feature.

---

## 4. Analisi e Prossimi Passi (Next Actions)
1.  **SQL Hardcoded**: Verificare ed eventualmente riscrivere le tuple DB in `src/core/database/pdl_queries.py` passando ai prepared statements standard (`execute(query, params)`).
2.  **Dead Code Removal**: Eseguire uno sfoltimento progressivo delle utilità orfane (come mostrato nel log di Vulture).
3.  **Aumento Coverage**: Molti bot (es. `carico_ts`, `dettagli_oda`) hanno una test coverage < 30%. Sfruttando la stabilità dei nuovi controller, si consiglia di aggiungere unit test mirati alla validazione input e mocking UI.
