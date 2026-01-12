# Diario di Analisi e Fix Test (Testing Insights)

## Obiettivo
Analizzare e correggere tutti i test che causano crash quando eseguiti in suite completa.

## Cronologia e Scoperte

### [Data Corrente]
- Inizio analisi.
- File di memoria creato.
- **Collezione Test**: 478 test identificati.
- **Strategia**: Esecuzione completa con `-v -x` per identificare l'ultimo test eseguito prima del crash. Sospetto conflitto Qt/GUI o risorsa non rilasciata.
- **Crash Point**: Il test si interrompe bruscamente durante `tests/unit/test_accessibility_simple.py::TestAccessibilitySimple::test_make_accessible`.
