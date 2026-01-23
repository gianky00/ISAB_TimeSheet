# Prompt per Gemini: Piano Strategico di Refactoring

**Ruolo:**
Agisci come un Senior Software Architect specializzato in Python, PyQt6 e Automazione Desktop.

**Contesto:**
Ho analizzato il repository di "BotTS", un'applicazione desktop per la gestione di automazioni su portali web. L'applicazione è funzionale e basata su uno stack moderno (PyQt6, Selenium 4, Pandas), ma soffre di debiti tecnici strutturali che ne minacciano la manutenibilità a lungo termine.

**Problemi Identificati (Analisi Tecnica):**

1.  **Violazione del Principio di Responsabilità Singola ("God File"):**
    *   Il file `src/gui/panels.py` è diventato un monolite di oltre 1600 righe.
    *   Contiene la definizione di *tutti* i pannelli della GUI (`ScaricaTSPanel`, `DettagliOdAPanel`, `TimbratureDBPanel`, ecc.) mischiati insieme.
    *   Contiene la classe `BotWorker` (gestione thread), che dovrebbe essere isolata.

2.  **Debito Tecnico "Nascosto" (Deprecazioni):**
    *   Il file `pytest.ini` sopprime esplicitamente i warning per `datetime.utcnow()`, che è deprecato nelle versioni recenti di Python.
    *   Vengono soppressi warning di `openpyxl`.
    *   Questo approccio "nascondi la polvere sotto il tappeto" è rischioso per aggiornamenti futuri dell'interprete.

3.  **Gestione Dipendenze e Rete Incoerente:**
    *   Il progetto ha `httpx` installato nel `requirements.txt`, ma il codice usa esclusivamente `requests` in modo sincrono (bloccante) all'interno dei `QThread`.
    *   Questo crea una dipendenza inutile ("bloat") e perde l'opportunità di usare l'asincronicità nativa moderna.

4.  **Strategia di Deployment "Fragile":**
    *   Lo script `scripts/restart.bat` esegue un "reset nucleare" ad ogni avvio problematico: cancella `.venv`, `__pycache__` e la cache dei driver `.wdm`.
    *   Questo indica instabilità di fondo nella gestione dell'ambiente e aumenta drasticamente i tempi di ripristino/avvio.

---

**Richiesta:**
Elabora un **Piano Strategico di Refactoring** dettagliato e diviso in fasi incrementali. Il piano deve permettere di sanare questi debiti senza bloccare lo sviluppo di nuove feature.

**Struttura richiesta per il Piano:**

1.  **Fase 1: Modularizzazione (Priorità Alta)**
    *   Come splittare `src/gui/panels.py`? Proponi una nuova struttura di directory (es. `src/gui/panels/package`).
    *   Dove spostare `BotWorker`?

2.  **Fase 2: Modernizzazione del Codice (Qualità)**
    *   Strategia per sostituire `datetime.utcnow()` con `datetime.now(datetime.UTC)` in tutto il progetto.
    *   Analisi costi/benefici: Migrare a `httpx` (asincrono) o rimuoverlo e tenere `requests` (pulizia)?

3.  **Fase 3: Stabilizzazione Environment (DevOps)**
    *   Come riscrivere `restart.bat` per essere meno distruttivo? (Es. check integrità pip invece di cancellare tutto).

4.  **Fase 4: Testing & Sicurezza**
    *   Come garantire che il refactoring della GUI non rompa i collegamenti dei segnali PyQt?

Per ogni fase, fornisci una stima della complessità e i passaggi operativi chiave.
