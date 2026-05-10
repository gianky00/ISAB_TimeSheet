# TODO QUALITY - SyncroJob

Questo file tiene traccia dei debiti tecnici e dei miglioramenti necessari per mantenere il codice a standard di eccellenza (Senior Level).

## Refactoring Architetturale (Violazioni SRP)
Le seguenti classi/file presentano responsabilità multiple mischiate (UI, Dati, API) e devono essere scomposte in componenti specializzati (Single Responsibility Principle):
- [x] `src/gui/widgets/dashboard/don_ciro_widget.py`
- [x] `src/gui/widgets/dashboard/weather_widget.py`
- [x] `src/bots/base/base_bot.py`
- [x] `src/gui/controllers/navigation_controller.py`
- [x] `src/gui/panels/base.py`
- [x] `src/bots/safework/pdl/bot.py`

## Refactoring Complessità (Xenon Grade C -> B)
Le seguenti funzioni/moduli hanno superato la soglia di complessità desiderata (B) e sono stati spezzettati:

### Bots
- [x] `src/bots/portale_fornitori/prenota_bp/bot.py`: Metodo `run` (Modularizzato V9.1)
- [x] `src/bots/portale_fornitori/scarico_ts/bot.py`: Metodo `_download_excel`
- [x] `src/bots/portale_fornitori/scarico_ts/pages/scarico_ts_page.py`: Metodo `_download_excel` (Modularizzato V9.1)

### Core
- [x] `src/core/audit/manager.py`: Metodi `_generate_notification` e `_get_current_user`
- [x] `src/core/backup_manager.py`: Metodo `detect_cloud_paths`
- [x] `src/core/data_synchronizer.py`: Metodi `sync_giornaliere` e `sync_contabilita_dati`
- [x] `src/core/importers/`: Moduli e metodi complessi (es. `_process_single_sheet` in `contabilita.py`)
- [x] `src/core/sync/smart_sync.py`: Metodi `sync_upsert_smart` e `sync_full_replace_with_metadata` (Refactored V9.1)
- [x] `src/core/dipendenti/anagrafica_controller.py`: Metodo `process_rows` (Refactored V9.1)

### UI & Utils
- [x] `src/gui/widgets/contabilita/helpers.py`: Intero modulo (media C)
- [x] `src/utils/log_humanizer.py`: Intero modulo (media C)
- [x] `src/gui/panels/dipendenti/utils/report_generator.py`: Hook UI integrato in `AnagraficaPage`.
- [x] `src/bots/base/wait_helpers.py`: Metodi `poll_for_new_file` e `poll_for_file` (Refactored V9.1 - Rank B)

## Sicurezza
- [x] Migrazione a `pip-audit` per scansione vulnerabilità (integrato in Toolbox GUI)
- [x] Parametrizzazione SQL in `SmartSyncEngine` (B608 risolto con prepared statements).

## Infrastruttura Test
- [x] Fix doppio conteggio passed/failed in fase isolamento SHOTGUN (V5.1)
- [x] Fix parsing incompleto summary pytest (failed+error)
- [x] SNIPER retry mirato con `--last-failed`
- [x] `sys.exit()` centralizzato, runner utilizzabile come libreria
- [x] Report IA troncato a 2000 char per file (-80% dimensione)
- [x] Suite test per il runner: 34 unit test di regressione
- [x] Allineamento a Poetry e script batch `avvio_test.bat`
- [x] Collection in-process con API pytest (`pytest.main()`) invece di subprocess

## Documentazione (Interrogate)
- [x] Portare la copertura delle docstring dal attuale ~80% al 95%. (Raggiunto 99.6% in V9.1)

## Static Analysis — Industrial Grade (completato 10 Maggio 2026)
- [x] **Ruff: 0 segnalazioni** sull'intera codebase (incluso `scratch/`).
- [x] **MyPy: 0 errori** su 406 file sorgente con strict mode.
- [x] Rimossi tutti i `# type: ignore` e `# mypy: disable-error-code` dall'intera codebase.
- [x] Rimossi override ridondanti in `pyproject.toml` per moduli non installati (`PyInstaller`, `win32api`, `faker`).
- [x] Import pesanti della GUI spostati nel blocco `TYPE_CHECKING` per ottimizzare i tempi di caricamento.

## Stabilità Startup
- [x] **Crash `access violation` al boot risolto (10 Maggio 2026).**
    - Root cause: `NotificationManager` e `AuditSignals` (QObject singletons) venivano istanziati nel `Phase1Worker` thread di background, causando un crash nativo C++ di PySide6 quando il thread terminava e i segnali venivano emessi dal loop `AuditManager`.
    - Fix: Pre-inizializzazione esplicita sul Main Thread in `main.py` prima di `_run_phase1`.

---

## Miglioramenti PySide6 — Feature Specifiche Post-Migrazione

La migrazione da PyQt6 a PySide6 è stata motivata dalla licenza LGPL (vs GPL di PyQt6).
Tuttavia, PySide6 (il binding ufficiale Qt for Python del Qt Project) offre funzionalità **uniche** che PyQt6 non ha. Questa sezione cataloga i miglioramenti adottabili nel codebase.

> **Nota:** Le API di base (signal/slot, widget, threading) sono identiche al 99.9% tra i due binding. I vantaggi qui elencati sono le opportunità *aggiuntive* che solo PySide6 permette.

---

### 1. `@Slot` decorator — Prestazioni Signal/Slot (Priorità: Alta)

**Stato attuale:** L'audit del codice rivela che `@Slot` è usato **solo in 8 slot** su centinaia di connessioni signal/slot presenti nel progetto.

**Vantaggio PySide6:** Il decorator `@Slot` non è solo documentativo — in PySide6 bypassa il lookup dinamico degli argomenti e produce una connessione C++ diretta (analogia con `SLOT()` macro in C++ Qt), riducendo il tempo di dispatch di ogni emissione segnale del 15-30% per slot frequenti.

**Azione:**
- [ ] Applicare `@Slot(...)` sistematicamente agli slot "hot" (chiamati con alta frequenza):
  - Slot connessi a segnali dei timer (`QTimer.timeout`)
  - Slot connessi all'`AuditManager.signals.log_added`
  - Slot del `NotificationManager` (`notification_added`, `notifications_updated`)
  - Slot di aggiornamento UI nei pannelli (es. tabelle, KPI, ActivityFeed)

---

### 2. `__feature__ snake_case` — Leggibilità API Qt (Priorità: Bassa)

**Vantaggio PySide6 esclusivo:** `from __feature__ import snake_case, true_property` trasforma tutta l'API Qt in stile Pythonic:
```python
# Senza feature
button.setEnabled(False)
layout.addWidget(button)

# Con snake_case + true_property
button.enabled = False
layout.add_widget(button)
```

**Decisione:** **Non applicare.** La feature rompe la compatibilità con i type stub di MyPy per PySide6 e aumenta la difficoltà di lettura per sviluppatori che conoscono Qt ma non la feature. Il rischio di regressioni supera i benefici estetici.

- [ ] Documentare questa decisione architetturale in `.gemini/ARCHITECTURE.md`

---

### 3. `QtCore.Property` con `notify` per QML readiness (Priorità: Media)

**Vantaggio PySide6:** Il `QtCore.Property` di PySide6 supporta il parametro `notify` per esporre proprietà a QML. Il progetto usa già `Property` (sidebar button, animation), ma senza `notify`.

**Applicazione pratica — anche senza QML:**
Aggiungere `notify=<signal>` alle proprietà esistenti genera automaticamente la notifica dei change listeners (es. per animation QPropertyAnimation su widget custom), eliminando la necessità di sovrascrivere manualmente i setter per emettere segnali.

```python
# Attuale (senza notify)
_pulse = Property(float, _get_pulse, _set_pulse)

# Migliorato (con notify)
pulse_changed = Signal()
_pulse = Property(float, _get_pulse, _set_pulse, notify=pulse_changed)
```

- [ ] Aggiungere `notify=` alle `Property` dei widget animati (`sidebar_button.py`, `bot_parameters.py`, `shimmer_widget.py`)

---

### 4. `QEnum` / `QFlag` decorator — Enumerazioni type-safe in Qt (Priorità: Media)

**Vantaggio PySide6:** I decorator `@QEnum` e `@QFlag` registrano le enum Python nel meta-system Qt, rendendole accessibili dall'esterno come `MyClass.MyEnum` e supportando `QMetaEnum` introspection. PyQt6 non ha equivalenti diretti.

**Applicazione:** Il progetto usa `Severity` e `Status` in `AuditManager` come enum Python plain. Decorarle con `@QEnum` le renderebbe leggibili da strumenti di diagnostica Qt e interrogabili via meta-system.

```python
from PySide6.QtCore import QEnum
from PySide6.QtCore import QObject

class AuditManager(QObject):
    @QEnum
    class Severity(Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
```

- [ ] Valutare `@QEnum` per `Severity` e `Status` in `src/core/audit/models.py`

---

### 5. `shiboken6` — Validità oggetto C++ (Priorità: Alta)

**Vantaggio PySide6:** `shiboken6.isValid(obj)` permette di verificare se un oggetto C++ Qt sottostante è ancora valido prima di chiamarne metodi. Questo previene i crash `RuntimeError: Internal C++ object already deleted`.

**Pattern utilizzabile:**
```python
import shiboken6

def safe_update(widget: QWidget) -> None:
    if shiboken6.isValid(widget):
        widget.update()
```

**Applicazione:** Il crash `access violation` risolto nel Phase 1 è un caso d'uso diretto. Aggiungere guard con `shiboken6.isValid()` negli slot degli `AuditSignals` e `NotificationManager` per proteggere le emissioni verso widget potenzialmente già distrutti.

- [ ] Aggiungere `shiboken6.isValid()` guard negli slot connessi a segnali cross-thread in `audit_log_widget.py` e `activity_feed.py`
- [ ] Aggiungere `shiboken6.isValid()` in `notification_manager.py` prima di emettere `notification_added` e `unread_count_changed`

---

### 6. Tool CLI PySide6 — Ecosistema Tooling (Priorità: Bassa)

PySide6 include una suite di tool CLI non disponibili con PyQt6:

| Tool | Uso |
|---|---|
| `pyside6-deploy` | Packaging app standalone (alternativa a PyInstaller) |
| `pyside6-android-deploy` | Deploy su Android (non rilevante ora) |
| `pyside6-qml` | Runner QML interattivo per prototipazione rapida |
| `pyside6-metaobjectdump` | Dump meta-object per debug introspection |

- [ ] Valutare `pyside6-deploy` come alternativa a PyInstaller per la build di distribuzione

---

## Backlog Aperto (Prossime Sessioni)

| Priorità | Area | Descrizione |
|---|---|---|
| **Alta** | PySide6 | Applicare `@Slot(...)` agli slot hot (AuditManager, NotificationManager, timer) |
| **Alta** | PySide6 | Aggiungere `shiboken6.isValid()` guard in `audit_log_widget.py` e `activity_feed.py` |
| Media | PySide6 | Aggiungere `notify=` alle `Property` dei widget animati (`sidebar_button`, `bot_parameters`) |
| Media | PySide6 | Valutare `@QEnum` per `Severity`/`Status` in `src/core/audit/models.py` |
| Media | Test | Aumentare la coverage dei test di regressione per i bot (target: >80%). |
| Media | GUI | Ridurre ulteriormente i `# noqa: PLR0913` rimasti (metodi con >5 argomenti). |
| Bassa | PySide6 | Decisione `snake_case` feature — documentare in `.gemini/ARCHITECTURE.md` |
| Bassa | Docs | Mantenere aggiornato `.gemini/ARCHITECTURE.md` con le ultime modifiche architetturali. |
| Bassa | DevOps | Job CI/CD su GitHub Actions: `ruff check` + `mypy src` ad ogni push. |
| Bassa | DevOps | Valutare `pyside6-deploy` come alternativa a PyInstaller. |

---
*Ultimo aggiornamento: 10 Maggio 2026 — Stato: INDUSTRIAL GRADE (Ruff 0 | MyPy 0)*
