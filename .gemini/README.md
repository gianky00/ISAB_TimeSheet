# 🧠 AI Onboarding & Directory Structure
Benvenuto, agente AI. Se stai leggendo questo file, sei entrato nel "cervello" del progetto ISAB_TimeSheet.
Questa cartella è interamente dedicata a ottimizzare il tuo funzionamento e la tua persistenza.

## 🗂️ Struttura
1. **`knowledge/` (Memoria a Lungo Termine)**
   - Contiene file di know-how profondo (es. guide VBA, spiegazioni architetturali di dominio).
   - Leggi questi file quando hai dubbi su come il business o le tecnologie legacy interagiscono col codice Python.

2. **`prompts/` (Template Esecutivi)**
   - Script e prompt pre-confezionati da utilizzare o espandere per task ripetitivi (es. generazione consuntivi).

3. **`state/` (Memoria di Sessione)**
   - `scratchpad.md`: Usalo liberamente per prendere appunti, segnarti TODO list o passare il testimone ad altre sessioni. Essendo tracciato su Git, il tuo stato si sincronizzerà tra diversi computer.

## 📜 Regole di Sopravvivenza
- Rispetta **sempre** i vincoli scritti nel file `gemini.toml` presente nella root del progetto.
- Prima di toccare il codice, verifica i layer in `GEMINI.md` della root.
- **LEGGI SEMPRE I GEMINI LOCALI:** Il progetto usa un'architettura Clean a domini. Quando lavori in queste cartelle, devi assolutamente leggere il loro `GEMINI.md` locale per non infrangere le regole di dominio:
  - `src/domain/GEMINI.md`: Modelli dati puri e logica di business core.
  - `src/application/GEMINI.md`: Casi d'uso, orchestratori e servizi.
  - `src/infrastructure/GEMINI.md`: DB, API esterne, automazioni Bot e I/O.
  - `src/gui/GEMINI.md`: UI, signal safety e PySide6.
  - `devtools/GEMINI.md`: CLI, build e tool di sviluppo.
- Mantieni la cartella ordinata. Se trovi un file obsoleto, proponi all'Architetto Umano di eliminarlo.
