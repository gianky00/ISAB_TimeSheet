# Best Practices - Enterprise Logging

Linee guida per un logging efficace in SyncroJob.

---

## ✅ DO

### 1. Usa Context Propagation

```python
# ✅ GOOD - Context automatico per tutti i log
with with_context(bot_type="scarico_ts", cantiere="ISAB"):
    logger.info("Download started")
    logger.info("Download completed")
```

### 2. Log con Metadata Ricchi

```python
# ✅ GOOD - Metadata utili per analisi
logger.info(
    "Files downloaded",
    files_count=3,
    total_size_mb=15.4,
    duration_sec=2.3
)
```

### 3. Usa Decorators per Performance

```python
# ✅ GOOD - Auto-timing
@measure_time(threshold_ms=5000)
def slow_operation():
    pass
```

### 4. Exception Logging Completo

```python
# ✅ GOOD - Context + exc per stack trace
try:
    operation()
except Exception as e:
    logger.exception(
        "Operation failed",
        exc=e,
        recovery="retry_recommended"
    )
```

---

## ❌ DON'T

### 1. Non Ripetere Context

```python
# ❌ BAD - Ripete bot_type ogni volta
logger.info("Start", bot_type="scarico_ts")
logger.info("End", bot_type="scarico_ts")

# ✅ GOOD - Una volta nel context
with with_context(bot_type="scarico_ts"):
    logger.info("Start")
    logger.info("End")
```

### 2. Non Usare f-strings per Dati Variabili

```python
# ❌ BAD - Difficile da parsare
logger.info(f"Downloaded {count} files in {time}s")

# ✅ GOOD - Strutturato
logger.info("Files downloaded", count=count, duration_sec=time)
```

### 3. Non Loggare Dati Sensibili

```python
# ❌ BAD - Password in chiaro
logger.info(f"Login with password: {password}")

# ✅ GOOD - PII filter automatico
logger.info("Login attempt", username=username)
# Password automaticamente mascherata dal security filter
```

### 4. Non Misurare Tempo Manualmente

```python
# ❌ BAD - Boilerplate
start = time.time()
result = operation()
logger.info(f"Took {time.time() - start}s")

# ✅ GOOD - Decorator
@measure_time(threshold_ms=5000)
def operation():
    pass
```

---

## Log Levels

| Level | Quando Usare |
|-------|--------------|
| `DEBUG` | Dettagli di sviluppo (disabilitato in prod) |
| `INFO` | Eventi normali (start, complete, milestone) |
| `WARNING` | Situazioni anomale ma recuperabili |
| `ERROR` | Errori che richiedono attenzione |
| `CRITICAL` | Errori fatali che bloccano operazione |

---

## Query Tips

```python
# Errori ultime 24h
query_logs().level("ERROR").time_range(
    start=datetime.now() - timedelta(hours=24)
).execute()

# Timeline completa di un'esecuzione
view_trace("trace_abc123")

# Health check
report = health_report()
if report['error_rate_percent'] > 5:
    alert("Error rate alto!")
```
