# Ultra Test Runner - Evoluzione Architetturale

## V5.0 — The Apex Runner (Attuale)

### Cambiamenti dalla V4.0
La V4.0 aveva 5 bug critici:
1. `Console.success`/`Console.error` non erano definiti → crash in SNIPER mode
2. `BrokenProcessPool` catch nel posto sbagliato → task residui persi
3. Filtro marker morto (riga 169: `pass` inutile)
4. `QT_QPA_PLATFORM=offscreen` mancante in SNIPER → crash GUI
5. `passed_count` impreciso → contava NodeID per file invece del vero conteggio

### Architettura V5.0

```
┌──────────────────────────────────────────────┐
│            UltraRunner.run()                 │
│                                              │
│    Args parsing + Strategia automatica       │
│    ≤5 target → SNIPER | >5 → SHOTGUN        │
├──────────────┬───────────────────────────────┤
│   SNIPER     │         SHOTGUN               │
│              │                               │
│  subprocess  │  _collect_tests_inprocess()   │
│  .run(live)  │         ↓                     │
│  stdout al   │  ProcessPoolExecutor          │
│  terminale   │  (MAX_WORKERS = CPU-1)        │
│              │         ↓                     │
│  --retry N   │  BrokenProcessPool catch      │
│  loop        │  → recupera task rimanenti    │
│              │         ↓                     │
│              │  Fase Isolamento              │
│              │  (sequenziale + --retry)      │
├──────────────┴───────────────────────────────┤
│              _finish()                       │
│  Report per file (P/F/T) + Coverage (--cov)  │
└──────────────────────────────────────────────┘
```

### Feature
- **Smart Routing**: `≤5 target` → SNIPER (live, debugging), `>5` → SHOTGUN (parallelo)
- **In-Process Collection**: `pytest --collect-only -q` con parsing diretto, niente subprocess per `collect_tests.py`
- **BrokenProcessPool Recovery**: Quando un worker muore (segfault Qt/C++), tutti i task non completati vanno in `isolation_queue`
- **--retry N**: Riesecuzione automatica N volte per flaky test (Selenium/UI)
- **Conteggio Preciso**: Parsing della summary line di pytest (`X passed, Y failed`)
- **Report Strutturato**: Tabella finale per file con pass/fail/duration, ordinati per tempo
- **--cov Opt-in**: Coverage disattivata di default, attivata solo con `--cov`
- **No Emoji**: Output ANSI pulito senza emoji per compatibilità enterprise

### Utilizzo
```bash
# SNIPER: singolo file con debug live
python tests/run_robust_tests.py tests/test_basic.py

# SNIPER: NodeID specifico
python tests/run_robust_tests.py tests/test_basic.py::test_version_exists

# SHOTGUN: full suite parallela
python tests/run_robust_tests.py

# Con retry per flaky tests
python tests/run_robust_tests.py --retry 2

# Con coverage
python tests/run_robust_tests.py --cov

# Con marker
python tests/run_robust_tests.py -m unit
```
