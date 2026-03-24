# Piano di Remediazione Linting e Typing (Strict Mode)

Questo documento traccia la strategia per la rimozione progressiva e sicura dei commenti `# noqa` introdotti durante l'abilitazione delle configurazioni *strict* di Ruff e MyPy.
L'obiettivo è raggiungere lo "Zero Warning" reale senza rompere il codice in produzione, affrontando i ~1800 warning disattivati.

## Principi Fondamentali
1. **Contesto prima di tutto:** Mai risolvere un warning in modo "cieco" (es. estrarre costanti senza capirne il senso di business o forzare un tipo errato).
2. **Prevenzione Regressioni:** Ogni fix deve essere accompagnato dall'esecuzione della test suite (`pytest`) prima del commit.
3. **Refactoring SRP (Single Responsibility Principle):** Se un metodo ha troppi statement (`PLR0915`) o troppe dipendenze condizionali (`PLC0415`), la soluzione non è fare a pezzi il codice a caso, ma estrarre la logica in classi dedicate o servizi separati.

---

## Fasi di Remediazione

### Fase 1: Quick Wins & Config Tuning (Basso Rischio)
In questa fase ridurremo drasticamente il rumore (eliminando centinaia di `# noqa`) agendo sulla configurazione e sui test, senza toccare la logica core.

*   **1.1 Naming PyQt (`N802`, `N803`):** I metodi ereditati da PyQt (es. `paintEvent`, `mousePressEvent`) non possono seguire il PEP8 (`snake_case`). Invece di avere `# noqa` sparsi in tutte le viste, aggiungeremo un'eccezione globale su Ruff per il pattern matching di PyQt.
*   **1.2 Magic Numbers nei Test (`PLR2004`):** I file di test abbondano di magic numbers (es. `assert calcolo() == 1234.56`). È perfettamente lecito nei test. Disabiliteremo globalmente `PLR2004` nella cartella `tests/`.
*   **1.3 Type Annotations (`ANN*`) nei Test:** Analogamente, annotare esaustivamente fixture e mock (`mock_driver`, `mock_file`) rallenta lo sviluppo. Disabiliteremo `ANN` sui test.

### Fase 2: Core e Utils Typing (Rischio Moderato)
Focus sulle fondamenta (i layer senza dipendenze). Sistemare qui i tipi bloccherà a cascata gli errori nei layer superiori.

*   **2.1 Utils (`src/utils/`):** Risolvere le regole `ANN` (missing types) e `Any` impliciti. Rendere 100% type-safe i file come `parsing.py`, `helpers.py`, `formatters.py`.
*   **2.2 Model & DTOs:** Assicurarsi che ogni Data Transfer Object e Dataclass sia tipizzata rigidamente.
*   **2.3 Tryceratops (`TRY*`):** Rivedere i blocchi `try...except` in `utils` e `core`. Molti catturano eccezioni loggandole senza re-raise o ritornando valori non gestiti. Sistemare il flusso degli errori (Custom Exceptions).

### Fase 3: Architettura Modulare e Import (`PLC0415`, `PLR0915`)
Questa fase è cruciale. L'uso di `import` dentro le funzioni (`PLC0415`) indica solitamente problemi di dipendenze circolari.

*   **3.1 Risoluzione Dipendenze Circolari:** Spostare le logiche comuni in file condivisi (es. `interfaces.py` o file di costanti/tipi) per permettere import puliti a top-level.
*   **3.2 Scomposizione Moduli (`PLR0915`, `PLR0913`):** Metodi troppo lunghi o con troppi argomenti nella GUI devono essere snelliti estraendo la Business Logic nei `Controller` (`src/core`).

### Fase 4: GUI Typing e Completamento (Rischio Alto)
Il layer della GUI (`src/gui`) interagisce massicciamente con PyQt, rendendo la tipizzazione rigorosa molto tediosa e potenzialmente instabile se MyPy non deduce bene i parent types.

*   **4.1 Eventi e Segnali:** Tipizzare correttamente tutti i tipi di ritorno dei signal e degli slot.
*   **4.2 Finalizzazione MyPy:** Una volta rimosso `Any` dalla GUI, potremo attivare `disallow_untyped_defs = true` globalmente in `pyproject.toml` per chiudere l'anello.

---

## Log delle Esecuzioni
*(Questa sezione verrà aggiornata iterativamente dall'AI durante le sessioni)*

*   **[Completata]** Fase 1: Riduzione rumore test e GUI tramite configurazione e auto-fix. (~1800 warning rimossi).
*   **[Completata]** Fase 2 (Parte 1): Remediazione completa `src/utils/`. Tutti i file in questa directory sono ora 100% Type-Safe (MyPy Strict) e Ruff-compliant.
*   **[In corso]** Fase 2 (Parte 2): Remediazione `src/core/models/` e DTOs.
