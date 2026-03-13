# SyncroJob - Enterprise Logging Standards

Linee guida per un logging efficace, strutturato e sicuro.

## ✅ DO (Best Practices)

### 1. Structured Logging
Usare esclusivamente `src.core.logging.get_logger`. I log devono essere pensati come dati, non come testo libero.
```python
# ✅ GOOD - Metadata strutturati per analisi automatica
logger.info("Files downloaded", count=files_count, duration_sec=time_taken)
```

### 2. Context Propagation
Usare `with_context` per iniettare metadati ricorrenti in tutti i log di un blocco.
```python
with with_context(bot_type="scarico_ts", cantiere="ISAB"):
    logger.info("Session started") # Heredita bot_type e cantiere
```

### 3. Performance Auto-Timing
Decorare funzioni critiche con `@measure_time` per tracciare colli di bottiglia automaticamente.

---

## ❌ DON'T (Errori Comuni)

### 1. Non loggare dati sensibili (PII)
*   **MAI** loggare password, API Key o Codici Fiscali.
*   Il sistema implementa filtri automatici, ma la responsabilità primaria è dello sviluppatore.

### 2. Evitare f-strings nei messaggi base
*   **BAD**: `logger.info(f"User {u} logged in")`
*   **GOOD**: `logger.info("User login", user=u)`
    *   *Perché?* Permette all'IA e agli aggregatori di raggruppare i log per tipo di evento.

---

## Livelli di Log

| Livello | Descrizione |
|---------|-------------|
| `DEBUG` | Dettagli tecnici per dev. Disabilitato in produzione. |
| `INFO` | Milestone operative (es. Login riuscito, Sync completata). |
| `WARNING` | Anomalie recuperabili (es. Retry fallito ma sessione continua). |
| `ERROR` | Errori che richiedono intervento o segnalazione. |
| `CRITICAL` | Crash o fallimenti di sicurezza totali. |
