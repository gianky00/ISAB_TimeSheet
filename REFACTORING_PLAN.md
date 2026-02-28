# SyncroJob Enterprise - Piano di Rifatturazione Architetturale

Questo documento definisce la strategia, i candidati e le regole operative per la decomposizione dei moduli critici della codebase, con l'obiettivo di migliorare la manutenibilità, la testabilità e la leggibilità del sistema.

## 📋 Regole Operative (Protocollo di Avanzamento)

Per garantire la massima sicurezza e stabilità durante il processo di refactoring, ogni intervento deve seguire rigorosamente queste regole:

1.  **Analisi Preliminare**: Prima di ogni modifica, analizzare le responsabilità del modulo e proporre una strategia di scomposizione.
2.  **Modularizzazione**: Estrarre la logica di business dai widget UI, spostandola in controller, helper o service dedicati.
3.  **Integrità Funzionale**: Il comportamento dell'applicazione deve rimanere invariato. Ogni refactoring deve essere validato tramite avvio dell'app.
4.  **Nessun Commit senza Permesso**: **È severamente vietato eseguire commit o push senza l'autorizzazione esplicita dell'utente.** Il lavoro deve rimanere nell'area di stage o essere proposto come modifica locale finché non viene dato il via libera.
5.  **Qualità Totale**: Ogni nuovo modulo creato deve rispettare lo standard "Zero Warnings" (Ruff, MyPy, Refurb).
6.  **Tracciamento**: Una volta completato un modulo, segnarlo come [x] in questo documento.

---

## 🏗️ Candidati Critici (Soglia > 350 Righe)

I seguenti file sono stati identificati come "God Objects" o moduli eccessivamente densi che necessitano di scomposizione.

### 🔴 Priorità Alta (Massima Complessità)
- [x] `src/gui/widgets/contabilita/certificati_tab.py` (~1214 righe)
    *   *Obiettivo*: Scomporre in sotto-widget per i vari tipi di certificati e spostare la logica di calcolo in un helper.
    *   *Sotto-Task*:
        1. Estrarre `ScadenzeAnalysisDialog` in `src/gui/dialogs/certificati_analysis_dialog.py`. (COMPLETATO)
        2. Creare `src/core/contabilita/certificati_engine.py` per logica di business, calcolo scadenze e ricerca PDF. (COMPLETATO)
        3. Creare `CertificatiTreeWidget` per isolare la gestione complessa del QTreeWidget. (COMPLETATO)
        4. Ridurre `CertificatiTab` a un semplice coordinatore di questi componenti. (COMPLETATO)
- [x] `src/gui/panels/pdl/programmazione_tab.py` (~876 righe)
    *   *Obiettivo*: Separare la gestione della griglia dalla logica di pianificazione. (COMPLETATO)
    *   *Sotto-Task*:
        1. Estratto `ProgrammingStatusWidget` in modulo dedicato.
        2. Creato `PDLPeriodManager` per logica temporale.
        3. Creato `ProgrammazioneTableWidget` per gestione griglia dati.
        4. Ridotto `ProgrammazioneTab` a orchestratore.
- [x] `src/gui/panels/dipendenti/pages/anagrafica_page.py` (~774 righe)
    *   *Obiettivo*: Estrarre i moduli di editing (Form, Documenti, Scadenze) in componenti separati. (COMPLETATO)
    *   *Sotto-Task*:
        1. Creato `AnagraficaHeaderWidget` per barra ricerca, azioni e card statistiche.
        2. Creato `EmployeeTableView` per incapsulare la logica della griglia e delegati.
        3. Creato `AnagraficaController` nel core per isolare query SQL e logica di calcolo stati.
        4. Ridotto `AnagraficaPage` a coordinatore dei componenti.
- [x] `src/gui/widgets/excel_table.py` (~707 righe)
    *   *Obiettivo*: Decomporre le funzionalità di filtraggio e formattazione in mixin o controller. (COMPLETATO)
    *   *Sotto-Task*:
        1. Estratto `HoverPulseFrame` in `src/gui/widgets/effects.py`. (COMPLETATO)
        2. Creato `ClipboardMixin` in `src/gui/widgets/mixins/` per logica TSV. (COMPLETATO)
        3. Isolata la logica di integrazione AI Lyra. (COMPLETATO)
        4. Snellito `EditableDataTable` delegando ai nuovi componenti. (COMPLETATO)

### 🟡 Priorità Media (Modularizzazione Necessaria)
- [x] `src/gui/panels/pdl/pdl_panel.py` (~693 righe)
    *   *Obiettivo*: Scomporre l'architettura Master-Detail e isolare la logica SQL. (COMPLETATO)
    *   *Sotto-Task*:
        1. Creato `PDLController` in `src/core/pdl/` per logica query, caching e processing. (COMPLETATO)
        2. Creato `PDLTableView` per incapsulare QTableView, delegati e menu contestuali. (COMPLETATO)
        3. Estratto l'esportatore Excel delegando a Pandas nel pannello. (COMPLETATO)
        4. Ridotto `PDLDBPanel` a coordinatore dei tab e componenti. (COMPLETATO)
- [x] `src/gui/widgets/sidebar_widget.py` (~543 righe)
    *   *Obiettivo*: Estrarre la logica di gestione dei gruppi e del track animato in classi helper. (COMPLETATO)
    *   *Sotto-Task*:
        1. Estratti componenti gerarchici in `src/gui/widgets/sidebar/components.py`. (COMPLETATO)
        2. Creato `SidebarAnimationManager` in `src/gui/widgets/sidebar/animations.py`. (COMPLETATO)
        3. Snellito `SidebarWidget` trasformandolo in un puro orchestratore. (COMPLETATO)
- [x] `src/gui/panels/scarico_pdl.py` (~515 righe)
    *   *Obiettivo*: Scomporre il pannello bot e isolare la logica degli stati riga. (COMPLETATO)
    *   *Sotto-Task*:
        1. Estratto `StatusListWidget` in `src/gui/widgets/safework/status_list.py`. (COMPLETATO)
        2. Snellito `ScaricoPDLPanel` trasformandolo in un puro orchestratore del Bot SafeWork. (COMPLETATO)
        3. Centralizzata la logica di persistenza dei parametri. (COMPLETATO)
- [x] `src/gui/panels/storico_oda/oda_panel.py` (~499 righe)
    *   *Obiettivo*: Scomporre il pannello gerarchico e isolare la logica dei dati. (COMPLETATO)
    *   *Sotto-Task*:
        1. Creato `ODAController` in `src/core/oda/` per raggruppamento e processing. (COMPLETATO)
        2. Creato `ODATreeView` per incapsulare QTreeView e delegati descrizioni. (COMPLETATO)
        3. Ridotto `StoricoOdaPanel` a puro orchestratore Master-Detail. (COMPLETATO)
- [x] `src/gui/widgets/notification_card.py` (~481 righe)
    *   *Obiettivo*: Estrarre la logica di styling e animazione in componenti esterni. (COMPLETATO)
    *   *Sotto-Task*:
        1. Creato `NotificationStylingEngine` in `src/gui/styles/notification_styles.py`. (COMPLETATO)
        2. Snellito `NotificationCard` delegando lo styling al motore esterno. (COMPLETATO)
        3. Ottimizzata la logica di animazione e formattazione. (COMPLETATO)

### 🔵 Priorità Bassa (Rifinitura Stilistica)
- [ ] `src/core/config_manager.py` (~464 righe)
- [ ] `src/gui/main_window/main.py` (~462 righe)
- [ ] `src/bots/base/base_bot.py` (~447 righe)
- [ ] `src/gui/panels/settings/pages/lists_page.py` (~436 righe)
- [ ] `src/core/telegram_bridge.py` (~413 righe)

---

## 🚀 Prossimo Passo Suggerito
Analisi di `certificati_tab.py` per identificare le aree di estrazione prioritarie.
