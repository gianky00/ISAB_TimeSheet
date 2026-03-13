# 🧠 PROMPT: SyncroJob Architecture Generator AI

Questo prompt è progettato per istruire un'IA ad analizzare il progetto **SyncroJob Enterprise** e generare uno script Python (`generate_architecture.py`) basato sulla libreria `diagrams`.

---

## 🎭 Ruolo dell'IA
Agisci come un **Senior Software Architect** esperto in sistemi di automazione e architetture PyQt6/Python.

## 🎯 Obiettivo
Analizzare la directory `src/` del progetto corrente e generare uno script Python che utilizzi la libreria `diagrams` per visualizzare l'architettura reale e aggiornata del sistema.

## 🔍 Fasi di Analisi Richieste

1.  **Core Discovery**: Analizza `src/core/` per identificare i manager (Secrets, Config, Sync, Audit, Telegram, Lyra AI).
2.  **GUI Mapping**: Analizza `src/gui/panels/` e `src/gui/widgets/` per mappare i moduli utente.
3.  **Bot Inventory**: Analizza `src/bots/` per identificare i portali esterni supportati (ISAB, SafeWork).
4.  **Data Flow**: Identifica come i bot scrivono nel DB (`DataSynchronizer`) e come la GUI comunica con il Core.

## 🛠️ Requisiti Tecnici dello Script da Generare

Lo script prodotto deve implementare i seguenti standard:

### 1. Libreria e Setup
- Usare `from diagrams import Cluster, Diagram, Edge`.
- Includere la gestione automatica del PATH per Graphviz su Windows.
- Output dell'immagine in `docs/assets/architecture.png`.

### 2. Attributi Estetici (Alta Risoluzione)
```python
graph_attr = {
    "fontsize": "32",
    "bgcolor": "white",
    "fontname": "Verdana Bold",
    "pad": "2.0",
    "nodesep": "1.8",
    "ranksep": "2.5",
    "dpi": "300",
    "splines": "curved",
    "concentrate": "true"
}
```

### 3. Organizzazione in Cluster
- **Cluster GUI**: Deve contenere Dashboard, KPI e i pannelli principali.
- **Cluster Core**: Deve evidenziare SecretsManager, SyncTracker e la logica di business.
- **Cluster Automation**: Deve mostrare Autopilot e i singoli Bot Selenium.
- **Cluster Persistence**: Database SQLite e DB di Audit.
- **External Systems**: Firewall/Nodi per i Portali ISAB, SafeWork e i servizi AI.

### 4. Mappatura Flussi (Color Coding)
- **Blu**: Interazione Utente -> GUI.
- **Arancione**: Flussi Excel (Import/Export).
- **Verde**: Sincronizzazione Bot -> Database.
- **Rosso (Dashed)**: Automazione Bot -> Portali Esterni.
- **Ciano**: Telegram Bridge -> App Telegram.
- **Viola**: Lyra AI -> Servizi AI Esterni.

## 📤 Output Atteso
Fornisci il codice Python completo, pronto per l'esecuzione, che rifletta fedelmente le dipendenze e i moduli trovati durante la tua analisi del codebase attuale.

---

**Nota per l'IA**: Se trovi nuovi moduli (es. nuovi bot o nuovi servizi core), includili nel diagramma adattando il layout per mantenere la leggibilità.
