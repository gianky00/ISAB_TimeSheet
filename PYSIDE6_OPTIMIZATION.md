# 🚀 PySide6 Optimization & Architecture Roadmap

Questo documento delinea la strategia di ottimizzazione e refactoring per sfruttare al massimo le potenzialità di **PySide6** e consolidare l'architettura dell'applicazione SyncroJob.

## 🎯 Obiettivi Principali
1. **Refactoring Architetturale (Snake Case):** Allineare l'intera codebase alle best practice Python (PEP 8) sostituendo il `camelCase` con lo `snake_case` per metodi e variabili.
2. **Sfruttamento True Properties PySide6:** Sostituire vecchi getter/setter con le `@Property` native di PySide6, migliorando le performance di rendering e il data-binding.
3. **Ottimizzazione Rendering e Animazioni:** Utilizzare le classi native di animazione di PySide6 in modo più efficiente, riducendo l'utilizzo di memoria e i drop di frame durante la navigazione.

---

## 🛠️ Fase 1: Refactoring e Naming Conventions (In Corso)
**Obiettivo:** Convertire tutti i metodi UI e i nomi delle variabili da `camelCase` a `snake_case`.
- [ ] Mappatura globale dei metodi `camelCase` (es. `updateUI`, `loadData`).
- [ ] Refactoring dei Controller (`service_controller.py`, `bot_controller.py`).
- [ ] Refactoring dei Widget Core (`core_widgets.py`, `dashboard_panel.py`).
- [ ] Verifica dei Signal/Slot connector per evitare regressioni di connessione.

---

## ⚙️ Fase 2: Implementazione True Properties PySide6
**Obiettivo:** Transizione verso il binding reattivo offerto dalle properties di PySide6.
- [ ] Identificazione dei widget custom con stati mutabili (es. progress bar custom, toggle button).
- [ ] Sostituzione dei metodi getter/setter tradizionali con le `@Property` (es. `QPropertyAnimation` compatibili).
- [ ] Ottimizzazione del ricalcolo dei layout: evitare `update()` manuali non necessari.

---

## 🚀 Fase 3: Hardening e Startup Optimization
**Obiettivo:** Snellire il tempo di avvio e ridurre i colli di bottiglia nel Main Thread.
- [ ] Implementare "Lazy Loading" sistematico per tutti i moduli UI non immediatamente visibili all'avvio.
- [ ] Ottimizzare l'uso di `QThread` e `QRunnable` per task I/O (Database, Rete).
- [ ] Gestione proattiva del Garbage Collector in fase di chiusura delle Tab / Widget pesanti (es. Tabelle Dati massive).

---
*Roadmap creata durante la transizione al branch `pyside6-phase3` per la massimizzazione delle feature PySide6.*
