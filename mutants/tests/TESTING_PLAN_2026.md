# Piano Tecnico Incremento Test Coverage (Aggiornato 2026)

**Obiettivo:** Portare il coverage dal 4% attuale a >20% stabili.
**Stato Attuale:** 11% (Incremento notevole su moduli core).

## 1. Analisi Attuale (Baseline Post-Intervento)
- **Totale:** ~11%
- **Moduli Migliorati:**
  - `src/utils/parsing.py`: 92% (era 13%)
  - `src/bots/base/base_bot.py`: 57% (era 0%)
  - `src/core/config_manager.py`: 42% (era 20%)
  - `src/core/excel_importer.py`: 28% (era 17%)
  - `src/gui/panels.py`: 25% (era 0%)

## 2. Prossimi Passi (Priorità Alta)

### A. Bot Specifici (Low Coverage)
I bot specifici (`scarico_ts`, `prenota_bp`, `safework`) ereditano da `BaseBot` ma hanno molta logica custom non testata.
- **Target:** `src/bots/portale_fornitori/scarico_ts/bot.py` (14%).
- **Azione:** Creare `test_scarico_ts_bot_logic.py` usando i mock di `BaseBot` già collaudati.

### B. Core Managers
- **Target:** `src/core/audit_manager.py` (49%).
- **Azione:** Completare i test su rotazione log e scrittura DB.
- **Target:** `src/core/telegram_manager.py` (0%).
- **Azione:** Mockare `python-telegram-bot` per testare la gestione comandi senza rete.

### C. GUI (Pannelli Rimanenti)
- **Target:** `ScaricaTSPanel` in `src/gui/panels.py`.
- **Azione:** Replicare il pattern di test usato per `TimbratureDBPanel` (testare `_save_data`, `validate_ready`).

## 3. Strategia di Mantenimento
1.  **Eseguire `run_robust_tests.py` prima di ogni commit.**
2.  **Non accettare PR che abbassano il coverage.**
3.  **Continuare a usare `mock` per isolare I/O e UI.**
