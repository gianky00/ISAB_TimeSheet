# Diario di Analisi e Fix Test (Testing Insights)

## 🛡️ REGOLA MANDATORIA DI TEST (MANDATORY)
**DA ORA IN POI, OGNI OPERAZIONE DI TEST DEVE UTILIZZARE IL RUNNER ROBUSTO.**
- **Comando Preferito**: `scripts/avvio_test.bat`
- **Engine**: `python tests/run_robust_tests.py`
- **DIVIETO**: Non usare più `pytest` direttamente per l'esecuzione dei test. Il runner robusto gestisce l'isolamento dei processi, i timeout e i report necessari per evitare crash della suite causati da conflitti di risorse (Qt/GUI).

## Obiettivo
Analizzare e correggere tutti i test che causano crash quando eseguiti in suite completa, garantendo stabilità tramite l'esecuzione isolata.

## Cronologia e Scoperte

### [Gennaio 2026] - Migrazione a Robust Runner
- **Status**: Migrazione completata.
- **Configurazione**: `scripts/avvio_test.bat` ora include il flag `--reset` di default per garantire il rilevamento di tutti i test.
- **Vantaggi**:
    - Esecuzione isolata per file che falliscono o vanno in timeout.
    - Generazione automatica di `tests/test_report.md`.
    - Persistenza dello stato tramite `.test_session_state.json` (permette di riprendere i test dopo un'interruzione).

### Crash Point Storici (Risolti o Monitorati)
- `tests/unit/test_accessibility_simple.py::TestAccessibilitySimple::test_make_accessible`: Identificato come punto di crash critico in esecuzione seriale standard (risolto tramite isolamento del runner robusto).
