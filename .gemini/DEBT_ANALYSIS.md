# SyncroJob - Technical Debt & Code Health

Analisi del debito tecnico rilevato tramite strumenti di analisi statica (Vulture, Xenon).

## 🧟 Codice Morto & Obsoleto (Vulture)

### Categoria A: Da Eliminare (Over-engineering)
- `src/bots/base/wait_helpers.py`: Funzioni di polling obsolete (es. `poll_for_download_complete`).
- `src/core/logging/metrics.py`: Logica di rilevamento anomalie disconnessa.
- `src/gui/design/`: Costanti di spacing/typography non utilizzate.

### Categoria B: Da Completare (Implementazioni Disconnesse)
- `generate_email_report` (`src/gui/panels/dipendenti/utils/report_generator.py`): Backend pronto, hook UI mancante.

---

## 🏗️ Refactoring Complessità (SRP & Xenon)

### Moduli critici (God Objects)
I seguenti moduli violano palesemente l'SRP e devono essere scomposti prioritariamente:
- `don_ciro_widget.py`: Troppe responsabilità (UI + API + Data Processing).
- `weather_widget.py`: Logica di fetch meteo integrata nella vista.
- `base_bot.py`: Accumulo di utility cross-bot che dovrebbero essere in helper separati.

---

## 🛠️ Piano d'Azione (Next Steps)
1.  **Sfoltimento**: Rimuovere le utilità orfane in `wait_helpers.py`.
2.  **Parametrizzazione SQL**: Riscrivere `pdl_queries.py` con prepared statements.
3.  **Modularizzazione UI**: Estrarre i Controller dai widget della Dashboard.
