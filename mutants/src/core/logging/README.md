# SyncroJob - Enterprise Logging System

Sistema di logging strutturato enterprise-grade con support per AI analysis, context propagation, e performance monitoring.

## Quick Start

### Basic Usage

```python
from src.core.logging import get_logger

logger = get_logger(__name__)

logger.info("Operazione completata", items=42, status="success")
logger.error("Errore connessione", retry_count=3)
```

### Context Propagation

```python
from src.core.logging import get_logger, with_context

logger = get_logger(__name__)

# Tutto dentro questo context avrà automaticamente trace_id e bot_type
with with_context(trace_id="bot_123", bot_type="scarico_ts"):
    logger.info("Login started")
    # ... operazioni ...
    logger.info("Download completed", files=3)
```

### Performance Measurement

```python
from src.core.logging import get_logger, measure_time

class MyBot:
    def __init__(self):
        self.logger = get_logger(__name__)

    @measure_time(threshold_ms=1000)  # Alert se > 1sec
    def download_files(self):
        # ... operazioni ...
        self.logger.info("Files downloaded")
```

### Exception Logging

```python
from src.core.logging import get_logger

logger = get_logger(__name__)

try:
    risky_operation()
except Exception as e:
    logger.exception(
        "Operazione fallita",
        exc=e,
        recovery_attempted=True,
        user_action="check_credentials"
    )
```

## Features

### ✅ Structured JSON Logging
Ogni log è un oggetto JSON parsabile:
```json
{
  "timestamp": "2026-01-31T23:00:00Z",
  "level": "INFO",
  "message": "Bot completato",
  "context": {
    "trace_id": "trace_abc123",
    "bot_type": "scarico_ts"
  },
  "data": {
    "files": 3,
    "duration_ms": 1234
  },
  "tags": ["info", "bot:scarico_ts", "success"]
}
```

### ✅ Multi-Sink Output
- **Console**: Output colorato per development
- **JSON File**: `logs/application/app.json` - per AI analysis
- **Human File**: `logs/application/app.log` - per debug manuale
- **Errors File**: `logs/errors/errors.json` - solo ERROR/CRITICAL

### ✅ Context Propagation
- **Trace ID**: Identifica operazione completa
- **Span ID**: Identifica sotto-operazioni
- Thread-safe e async-aware

### ✅ Security & Privacy
- PII masking automatico (password, CF, email, IBAN)
- Multi-layer security
- GDPR compliant

### ✅ Performance Monitoring
- Decorator `@measure_time` per auto-timing
- Alert automatici se supera threshold
- Metriche aggregate

## Configuration

Il sistema usa la directory configurata in `config_manager.CONFIG_DIR`:
```
C:\Users\gianc\AppData\Local\SyncroJob\logs\
├── application/
│   ├── app.json       # Structured logs
│   └── app.log        # Human-readable logs
├── errors/
│   └── errors.json    # Solo errori
├── metrics/
└── bots/
    └── scarico_ts_trace_abc.json  # Log per singola run
```

### Custom Configuration

```python
from src.core.logging import configure_logging
from src.core.logging.config import LoggingConfig

# Custom config
config = LoggingConfig()
config.default_level = "DEBUG"
config.performance_threshold_ms = 3000

configure_logging(config)
```

## Migration da Vecchio Sistema

### Opzione 1: Adapter Compatibile

```python
# PRIMA:
import logging
logger = logging.getLogger(__name__)

# DOPO (backward compatible):
from src.core.logging.migration import get_logger
logger = get_logger(__name__)

# Codice funziona esattamente uguale!
logger.info("Messaggio")
logger.error("Errore", extra={"detail": "value"})
```

### Opzione 2: Full Migration

```python
# PRIMA:
import logging
logger = logging.getLogger(__name__)
logger.info("Bot started")

# DOPO:
from src.core.logging import get_logger, with_context
logger = get_logger(__name__)

with with_context(bot_type="scarico_ts"):
    logger.info("Bot started")  # Auto-tagged!
```

## Advanced Usage

### Bot Integration

```python
from src.core.logging import get_logger, with_context, measure_time

class ScaricoTSBot:
    def __init__(self):
        self.logger = get_logger(__name__)

    def execute(self, cantiere, fornitore):
        # Genera trace ID univoco per questa esecuzione
        from src.core.logging.context import generate_trace_id
        trace_id = generate_trace_id()

        with with_context(
            trace_id=trace_id,
            bot_type="scarico_ts",
            cantiere=cantiere,
            fornitore=fornitore
        ):
            self.logger.info("Bot started")

            try:
                self._login()
                files = self._download()
                self.logger.info("Bot completed", files=len(files))
            except Exception as e:
                self.logger.exception("Bot failed", exc=e)
                raise

    @measure_time(threshold_ms=5000)
    def _login(self):
        # ... login logic ...
        self.logger.info("Login successful")

    @measure_time(threshold_ms=10000)
    def _download(self):
        # ... download logic ...
        return ["file1.xlsx", "file2.xlsx"]
```

### AI Analysis

```python
import json
import pandas as pd

# Carica log JSON
with open("logs/application/app.json") as f:
    logs = [json.loads(line) for line in f]

# Converti in DataFrame
df = pd.DataFrame(logs)

# Query facili:
# 1. Errori per bot type
errors = df[
    (df['level'] == 'ERROR') &
    (df['context'].apply(lambda x: x.get('bot_type') == 'scarico_ts'))
]

# 2. Performance stats
perf = df.groupby('context.function')['data.duration_ms'].describe()

# 3. Ricostruisci timeline bot run
trace = df[df['context.trace_id'] == 'trace_abc123'].sort_values('timestamp')
```

## Best Practices

### 1. Usa Context Propagation
```python
# ❌ BAD
logger.info("Download started", bot_type="scarico_ts")
# ...
logger.info("Download completed", bot_type="scarico_ts")

# ✅ GOOD
with with_context(bot_type="scarico_ts"):
    logger.info("Download started")
    # ...
    logger.info("Download completed")
```

### 2. Log con Metadata Ricchi
```python
# ❌ BAD
logger.info("Files downloaded")

# ✅ GOOD
logger.info(
    "Files downloaded successfully",
    files_count=3,
    total_size_mb=15.4,
    cantiere="ISAB",
    duration_sec=2.3
)
```

### 3. Usa Decorators per Performance
```python
# ❌ BAD
start = time.time()
result = slow_operation()
logger.info(f"Took {time.time() - start}s")

# ✅ GOOD
@measure_time(threshold_ms=5000)
def slow_operation():
    # ... logic ...
    pass
```

### 4. Exception Logging Completo
```python
# ❌ BAD
try:
    operation()
except Exception as e:
    logger.error(f"Failed: {e}")

# ✅ GOOD
try:
    operation()
except Exception as e:
    logger.exception(
        "Operation failed",
        exc=e,
        recovery="retry_recommended",
        user_impact="medium"
    )
```

## Troubleshooting

### Log non vengono scritti
- Verifica che directory esista: `config.ensure_directories()`
- Verifica permessi su `C:\Users\gianc\AppData\Local\SyncroJob\logs`

### Performance lenta
- Riduci `sampling_rate` per log ad alto volume
- Disabilita console output in production: `config.console_enabled = False`

### File troppo grandi
- Rotation automatica già configurata (10MB)
- Verifica retention policy: `config.retention`

## API Reference

### `get_logger(name: str) -> StructuredLogger`
Ottiene logger per modulo.

### `configure_logging(config=None)`
Configura sistema di logging (chiamare all'avvio app).

### `with_context(**context_data)`
Context manager per aggiungere metadata ai log.

### `@measure_time(threshold_ms=None, logger_name=None)`
Decorator per misurare performance.

### `@log_entry_exit(log_args=False, log_result=False)`
Decorator per loggare ingresso/uscita funzioni.

## Support

Per domande o problemi, consulta:
- Piano architetturale: `LOGGING_ARCHITECTURE_PLAN.md`
- Proof of concept: `logging_poc.py`
- Codice sorgente: `src/core/logging/`
