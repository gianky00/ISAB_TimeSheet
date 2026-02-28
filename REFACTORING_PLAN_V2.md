# SyncroJob Enterprise - Piano di Rifatturazione Architetturale (V2.0)

Questo documento estende la strategia di modularizzazione ai componenti Core e alle pagine UI complesse identificate dopo l'analisi di Febbraio 2026.

## 🎯 Obiettivi Core
1.  **Decomposizione Logic-UI**: Estrarre i Controller dai pannelli che gestiscono ancora lo stato internamente.
2.  **Modularizzazione Bridge**: Suddividere i bridge di comunicazione (Telegram, Sentinel) per facilitare il testing.
3.  **Standardizzazione Widget**: Migrare i componenti custom verso il pattern "Component-Widget".

---

## 🏗️ Nuovi Target di Rifatturazione

### 🔴 Priorità Alta (Core Bridge & Sync)
- [ ] `src/core/telegram_bridge.py` (~413 righe)
    - *Criticità*: Gestisce troppi segnali e logica di routing Telegram.
    - *Strategia*: Estrarre `TelegramSignalRouter` e `TelegramUIHandler`.
- [ ] `src/core/data_synchronizer.py` (~380 righe)
    - *Criticità*: Logica di sync multi-dominio (PDL, ODA, Dipendenti) in un unico file.
    - *Strategia*: Creare `src/core/sync/` con sottomoduli per dominio.

### 🟡 Priorità Media (UI Panels Complessi)
- [ ] `src/gui/panels/scarico_ore_panel.py` (~450 righe)
    - *Criticità*: Logica di filtraggio DataEase mescolata alla UI.
    - *Strategia*: Estrarre `ScaricoOreController` e `DataEaseFilterWidget`.
- [ ] `src/gui/panels/settings/pages/lists_page.py` (~436 righe)
    - *Criticità*: Gestione complessa di liste dinamiche (Fornitori, TCL, ecc.).
    - *Strategia*: Estrarre `ListManagementController` e widget generico `EditableListWidget`.
- [ ] `src/gui/panels/health_panel.py` (~390 righe)
    - *Criticità*: Logica di diagnostica integrata nel pannello.
    - *Strategia*: Estrarre `HealthDiagnosticsEngine` in `src/core/`.

### 🔵 Priorità Bassa (Utility & Cleanup)
- [ ] `src/utils/validators.py` (~280 righe)
    - *Strategia*: Suddividere in `document_validators.py` e `data_validators.py`.
- [ ] `src/gui/panels/notifications_panel.py` (~350 righe)
    - *Strategia*: Modularizzare i componenti delle card di notifica.

---

## 📏 Regole d'Ingaggio (Aggiornate)
1.  **Limit 400**: Ogni file che supera le 400 righe deve essere candidato alla scomposizione.
2.  **No Logic in UI**: I pannelli `src/gui/panels/` devono contenere solo `setup_ui`, connessioni ai segnali e chiamate ai Controller.
3.  **Signal First**: Utilizzare `src/core/signals.py` (se esistente) o segnali locali dei Controller per comunicare tra i layer.

---

## 🚀 Prossimo Passo Consigliato
Iniziare con la scomposizione di **`src/core/telegram_bridge.py`** per isolare la logica di notifica dalla logica UI.
