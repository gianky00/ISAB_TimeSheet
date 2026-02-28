# SyncroJob Enterprise - Standard Architetturali (V9.0)

Questo documento definisce le regole ferree per l'estensione e la manutenzione della codebase. Ogni nuovo modulo deve aderire a questi standard per garantire manutenibilità e prestazioni "Zero-Wait".

## 1. Separazione delle Responsabilità (SoC)
L'applicazione segue una variante del pattern MVC/MVVM:

*   **Core (Logica/Dati)**: Resiede in `src/core/`. Non deve importare nulla da `src/gui`. Gestisce DB, API, Bot e algoritmi.
*   **Controllers**: Fungono da ponte. Gestiscono lo stato e orchestrano i componenti Core per conto della UI.
*   **GUI (Pannelli)**: Resiedono in `src/gui/panels/`. Contengono solo layout e connessioni ai segnali.
*   **GUI (Widget)**: Componenti atomici riutilizzabili in `src/gui/widgets/`.

## 2. Regole di Modularità
1.  **Limite 400 Righe**: Nessun file sorgente deve superare le 400-500 righe. Se ciò avviene, va scomposto.
2.  **Lazy Loading**: I pannelli della `MainWindow` devono essere istanziati solo al primo accesso tramite il `NavigationController`.
3.  **Thread Safety**: Ogni operazione di I/O pesante (Bot, scansione cartelle, query SQL massive) **DEVE** essere eseguita in un thread separato (`QThread` o `QTimer` differiti).

## 3. Comunicazione tra Layer
*   **Segnali (PyQt6)**: È l'unico modo permesso per la comunicazione GUI -> Core e il contrario.
*   **Singleton Manager**: Servizi globali come `AuditManager`, `NotificationManager`, `ConfigManager` devono essere acceduti tramite `.instance()`.

## 4. Database & Sync
*   **Schema First**: Le migrazioni devono essere definite in `src/core/database/migrations/`.
*   **Atomicità**: Il salvataggio dei dati deve essere atomico per evitare corruzioni durante i crash.

## 5. Standard di Qualità
*   **Zero Warnings**: `ruff`, `mypy` e `refurb` devono restituire 0 segnalazioni.
*   **UTF-8**: Ogni file deve essere salvato con encoding UTF-8.
*   **Type Hinting**: Obbligatorio per tutti i parametri di funzione e i tipi di ritorno.
