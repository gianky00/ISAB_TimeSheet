# 🧠 GUI LAYER - AI ARCHITECT GUIDELINES

Sei all'interno di `src/gui/`, il livello di presentazione basato su PySide6.

## 🚨 REGOLE DEL LAYER (STRICT)
1. **SINGLE RESPONSIBILITY & ZERO BUSINESS LOGIC:** I widget UI si limitano a: 1) Mostrare dati, 2) Raccogliere input, 3) Emettere segnali. Qualsiasi calcolo o salvataggio deve essere delegato a un Controller o un Service di `src/application`.
2. **THREADING (CRITICAL):**
   - **REGOLA D'ORO:** L'interfaccia utente (Main Thread) NON DEVE MAI BLOCCARSI.
   - Tutte le operazioni I/O (database, web scraping, API, caricamento file pesanti) DEVONO essere eseguite in un `QThread` o tramite `QThreadPool` / `QRunnable`.
3. **SIGNAL SAFETY:** 
   - Fai molta attenzione alle `lambda` nei `.connect()`. In PySide6, le lambda che catturano variabili di ciclo o componenti dinamici possono causare crash o memory leak.
   - Disconnetti sempre i segnali se elimini o rimpiazzi un widget dinamicamente.
4. **GESTIONE CRASH (C++ / Python):**
   - I crash nativi di Qt abbattono l'interprete Python in modo silente. Assicurati che le firme degli `Slot()` corrispondano esattamente ai tipi inviati dal `Signal()`.
   - Proteggi i punti di ingresso UI (click dei bottoni) usando decoratori come `@logger.catch`.
5. **UI RESPONSIVA:** Implementa loader asincroni e indicatori visivi ("Caricamento in corso...") per dare sempre feedback all'utente.
