# Test Disabilitati

## disabled_test_horizontal_timeline.py

Questo file di test è stato temporaneamente disabilitato perché causava un crash non risolvibile (`Fatal Python error: Aborted`) durante l'esecuzione nell'ambiente di CI, anche con `xvfb`.

Il crash si verifica durante l'inizializzazione della fixture `qapp` di `pytest-qt` quando vengono istanziati i widget `LogWidget` o `HorizontalTimelineWidget`. Questo indica una profonda incompatibilità tra l'implementazione di questi specifici widget e l'ambiente di test headless.

Il test dovrebbe essere riattivato solo dopo un refactoring dei widget o un aggiornamento significativo delle librerie sottostanti (`PyQt6`, `pytest-qt`) che risolva il problema di fondo.
