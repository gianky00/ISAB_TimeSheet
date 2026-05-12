# TODO QUALITY - SyncroJob

Questo file tiene traccia dei debiti tecnici e dei miglioramenti necessari per mantenere il codice a standard di eccellenza (Senior Level).

## Refactoring Architetturale (Violazioni SRP)
Le seguenti classi/moduli hanno troppe responsabilità e devono essere scissi:

- [x] `AnagraficaPage`: Separare gestione tabella da logica di caricamento/import (Scomposto in `DipendentiController`).
- [x] `NavigationController`: Separare la logica dello stack dalla creazione fisica dei widget (Scomposto in `PanelFactory`).
- [x] `AutopilotWidget`: Scomporre il widget gigante in componenti atomici (EventCard, ConfigCards).

---

## Hardening PySide6 (Industrial Grade Optimization)
Sfruttamento delle feature native di PySide6 per performance e stabilità.

### 1. `@Slot` — Tipizzazione Segnali (Priorità: Alta)
- [x] Applicato `@Slot(...)` a tutti gli slot "hot" (timer, log updates, progress bars).
- [x] Riduzione lookup dinamico Python e miglioramento dispatch segnali.

### 2. `Property` con `notify` — Binding Reattivo (Priorità: Media)
- [x] Aggiunto parametro `notify` a tutte le `Property` animate.
- [x] Permette fluidità nativa per `QPropertyAnimation`.

### 3. `shiboken6.isValid()` — Prevenzione Crash (Priorità: Alta)
- [x] Aggiunte guardie di validità in tutti gli slot asincroni e callback differiti.
- [x] Eliminazione definitiva dei crash `RuntimeError: Internal C++ object already deleted`.

### 4. `@QEnum` — Introspezione Meta-System (Priorità: Media)
- [x] Registrate enum `Severity` e `Status` tramite `@QEnum`.
- [x] **Nota Tecnica:** Richiede `IntEnum`. Implementato mapping `.to_str()` per compatibilità DB.

### 5. Rendering & Caching (Priorità: Alta)
- [x] Implementato **Icon Caching** globale per icone SVG colorate.
- [x] Implementato **Path Caching** (`QPainterPath`) per widget grafici 60 FPS.

---

## Backlog Aperto (Prossime Sessioni)

| Priorità | Area | Descrizione |
|---|---|---|
| Media | Test | Aumentare la coverage dei test di regressione per i bot (target: >80%). |
| Media | GUI | Ridurre ulteriormente i `# noqa: PLR0913` rimasti (metodi con >5 argomenti). |
| Bassa | DevOps | Job CI/CD su GitHub Actions: `ruff check` + `mypy src` ad ogni push. |
| Bassa | DevOps | Valutare `pyside6-deploy` come alternativa a PyInstaller. |

---
*Ultimo aggiornamento: 10 Maggio 2026 — Stato: INDUSTRIAL GRADE (Ruff 0 | MyPy 0 | PySide6 Optimized)*
