# Piano Tecnico Incremento Test Coverage (2026)

**Obiettivo:** Portare il coverage dal 4% attuale a >20% stabili, priorizzando la stabilità e la logica core.

## 1. Analisi Attuale (Baseline)
- **Totale:** ~4%
- **Aree Scoperte Critiche:** 
  - `src/gui/panels.py` (0%) - Logica UI principale.
  - `src/core/excel_importer.py` (17%) - Parsing dati sensibile.
  - `src/bots/base/base_bot.py` (0%) - Fondamenta automazione.
  - `src/core/telegram_manager.py` (0%) - Comunicazione critica.

## 2. Strategia per Modulo

### A. Core Utilities (Target: 90%+)
Questi moduli sono funzioni pure e devono essere testati esaustivamente per garantire fondamenta solide.
- **Target:** `src/utils/parsing.py`, `src/utils/helpers.py`, `src/utils/validators.py`.
- **Tecnica:** Unit test classici con parametri parametrizzati (`@pytest.mark.parametrize`).
- **Azioni:**
  - Coprire tutti i formati data in `parsing.py`.
  - Coprire validazione input (CF, Email, Date) in `validators.py`.

### B. Data & IO (Target: 60%+)
Gestione file e database.
- **Target:** `src/core/excel_importer.py`, `src/core/database.py`.
- **Tecnica:** 
  - `unittest.mock` per simulare file system e contenuti file Excel.
  - DB SQLite `:memory:` per test veloci e isolati del layer dati.
- **Azioni:**
  - Creare fixture che generano Excel validi e invalidi.
  - Testare transazioni DB e rollback in caso di errore.

### C. Bot Logic (Target: 40%+)
Logica di automazione senza browser reale.
- **Target:** `src/bots/base/base_bot.py`, `src/bots/base/login_page.py`.
- **Tecnica:** **Deep Mocking** di Selenium.
  - NON avviare mai Chrome reale.
  - Mockare `driver.find_element`, `WebDriverWait.until`.
  - Verificare che i bot chiamino i selettori corretti e gestiscano le eccezioni `TimeoutException`.

### D. GUI Logic (Target: 20%+)
Testare la logica dietro i pannelli, non il rendering.
- **Target:** `src/gui/panels.py` (metodi non-UI), `src/gui/widgets/bot_parameters.py`.
- **Tecnica:** `pytest-qt` (qtbot).
  - Testare segnali/slot.
  - Verificare che il click su "Avvia" chiami il metodo corretto.
  - Mockare dialoghi (`QMessageBox`, `QFileDialog`) per non bloccare i test.

## 3. Roadmap Esecutiva

1.  **Fase 1: Low Hanging Fruit (Utilities)**
    - Implementare test per `utils/parsing.py` e `utils/helpers.py`.
    - Risultato atteso: +2% coverage totale, +sicurezza su conversioni dati.

2.  **Fase 2: Excel & Configurazione**
    - Implementare test per `config_manager.py` e `excel_importer.py`.
    - Risultato atteso: +5% coverage totale, prevenzione regressioni su I/O.

3.  **Fase 3: Bot Core**
    - Implementare test completi per `BaseBot` (init, login flow, error handling).
    - Risultato atteso: +5% coverage totale, stabilità bot.

4.  **Fase 4: Panel Logic**
    - Testare `ScaricaTSPanel` e `TimbratureDBPanel` (logica salvataggio/caricamento).
    - Risultato atteso: +5% coverage totale.

## 4. Regole d'Oro per i Test
1.  **Nessun I/O Reale:** Usare `tmp_path` di pytest per file temporanei.
2.  **Nessun Browser Reale:** Mockare sempre Selenium.
3.  **Nessuna GUI Bloccante:** Patchare sempre `exec_()` dei dialog.
4.  **Pulizia:** Ogni test deve lasciare l'ambiente come l'ha trovato.
