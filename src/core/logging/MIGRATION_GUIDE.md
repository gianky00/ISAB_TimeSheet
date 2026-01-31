# Migration Guide - Enterprise Logging System

Guida per migrare codice esistente al nuovo sistema di logging strutturato.

---

## Quick Migration

### Caso 1: Import Semplice (Minimal Change)

```python
# ❌ PRIMA
import logging
logger = logging.getLogger(__name__)

# ✅ DOPO (compatibile al 100%)
from src.core.logging.migration import get_logger
logger = get_logger(__name__)

# Il codice esistente funziona senza modifiche!
logger.info("Messaggio")
logger.error("Errore", extra={"detail": "value"})
```

---

### Caso 2: Full Migration (Raccomandato)

```python
# ❌ PRIMA
import logging
logger = logging.getLogger(__name__)
logger.info(f"Bot {bot_type} started")

# ✅ DOPO
from src.core.logging import get_logger, with_context

logger = get_logger(__name__)

with with_context(bot_type=bot_type):
    logger.info("Bot started")  # Metadata automatici!
```

---

## Bot Migration

Per migrare un bot esistente:

```python
from src.core.logging import get_logger, with_context, measure_time, generate_trace_id

class MyBot(BaseBot):
    def __init__(self):
        super().__init__()
        # BaseBot già fornisce self._logger e self._trace_id

    def run(self, data):
        # Tutto è già in context grazie a BaseBot.execute()
        self.log("Operazione in corso")  # Usa structured logging

        # Per operazioni lunghe, usa measure_time
        self._download_files()

        return True

    @measure_time(threshold_ms=5000)
    def _download_files(self):
        self._logger.info("Download started", file_count=3)
        # ...
        self._logger.info("Download completed")
```

---

## Audit Correlation

Per correlare log con audit entries:

```python
from src.core.audit_manager import AuditManager
from src.core.logging import with_context, set_audit_id

with with_context(trace_id="my_trace", bot_type="my_bot"):
    # Log azione - ritorna audit_id!
    audit_id = AuditManager.instance().log_action(
        "Operazione",
        category="bot"
    )

    # audit_id ora disponibile per correlazione
    # trace_id automaticamente incluso nell'audit entry
```

---

## API Cheat Sheet

| Funzione | Uso |
|----------|-----|
| `get_logger(name)` | Ottieni logger per modulo |
| `with_context(**kwargs)` | Context manager per metadata |
| `@measure_time(ms)` | Decorator per timing |
| `generate_trace_id()` | Genera nuovo trace ID |
| `query_logs()` | Query builder per analisi |
| `view_trace(id)` | Ricostruisci timeline |
| `health_report()` | Report salute sistema |
