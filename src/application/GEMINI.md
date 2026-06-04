# 🧠 APPLICATION LAYER - AI ARCHITECT GUIDELINES

Sei all'interno di `src/application/`, il livello di orchestrazione (Use Cases e Services).

## 🚨 REGOLE DEL LAYER (STRICT)
1. **ISOLAMENTO DALLA GUI:** È **tassativamente vietato** importare qualsiasi cosa da `src.gui`. L'applicazione non deve sapere nulla dell'interfaccia utente.
2. **DEPENDENCY INJECTION:** I Service non devono istanziare direttamente i database o i bot. Devono ricevere le dipendenze sotto forma di interfacce/Protocols definiti in `src/domain/`.
3. **ORCHESTRAZIONE PURA:** Un Service qui dentro coordina l'infrastruttura e il dominio. (Esempio: carica dati da DB -> applica logica di dominio -> salva dati -> invia notifica).
4. **ERROR HANDLING UNIFICATO:** Cattura eccezioni tecniche (es. `requests.ConnectionError` o eccezioni di Playwright) lanciate dalla `infrastructure` e traducile in eccezioni di Dominio chiare, da propagare poi in modo sicuro verso la GUI.
5. **THREAD SAFETY:** Molti di questi Service potrebbero essere invocati da QThread asincroni. Progetta le classi senza stato (stateless) o usa lock (es. `threading.Lock`) se gestisci risorse condivise in memoria.
