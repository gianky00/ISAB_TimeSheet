# Graphical Styling Audit - SyncroJob Enterprise

## 📋 Executive Summary
L'architettura grafica di SyncroJob non utilizza librerie "standard" di terze parti (come Qt-Material o Fluent-UI), ma implementa un **Design System proprietario** altamente customizzato. Il sistema è stratificato per garantire coerenza visiva e facilità di manutenzione.

---

## 🏗️ Architettura dello Stile
Il sistema si basa su tre pilastri fondamentali coordinati dal `ThemeManager`:

### 1. Palette Core (`src/gui/design/colors.py`)
Definisce l'identità visiva di base utilizzando il paradigma **Material Design 3**.
*   **Primary Color**: Teal (`#009688`) - derivato dal logo aziendale.
*   **Secondary Color**: Deep Purple (`#673AB7`).
*   **Supporto Temi**: Esistono definizioni sia per `LIGHT` che per `DARK`, sebbene il sistema sia attualmente forzato sul tema Light per coerenza operativa.

### 2. Costanti Operative (`src/gui/styles/constants.py`)
Mappa i colori semantici simili allo standard **Bootstrap**:
*   **Success**: `#2ecc71` / `#198754`
*   **Error/Danger**: `#dc3545`
*   **Warning**: `#f39c12`
*   **Text Hierarchy**: Definisce `text_dark` (`#212529`), `text_muted` (`#6c757d`), etc.
*   **UI Metrics**: Centralizza border-radius (4px, 8px, 12px), spaziature e font sizes.

### 3. Widget Styles (`src/gui/styles/widget_styles.py`)
Contiene stringhe QSS riutilizzabili per i componenti comuni:
*   **Buttons**: Definizioni per `BUTTON_PRIMARY`, `SUCCESS`, `DANGER`, `TRANSPARENT`.
*   **Inputs**: Stili custom per `QComboBox`, `QLineEdit`, `QTimeEdit`.
*   **Containers**: Effetti gradiente per le `Card` e stili per `QScrollArea`.

---

## 🎨 File di Stile (QSS)
Oltre agli stili definiti nel codice Python, vengono caricati file esterni in `assets/styles/`:
*   `light.qss`: Stile base del tema.
*   `overrides.qss`: Correzioni globali applicate sopra ogni tema.
*   `main_window.qss`: Specifico per la struttura principale.
*   `message_box.qss`: Per le finestre di dialogo.

---

## 🔍 Analisi dell'Implementazione (Inline vs Centralizzato)
Dall'audit del codice emerge un utilizzo misto:
1.  **Stili Centralizzati**: Molti widget importano variabili da `widget_styles.py` (approccio consigliato).
2.  **Stili Inline (Hardcoded)**: In diversi file (es. `security_dashboard.py`, `pdl_timeline.py`) sono presenti chiamate `setStyleSheet` con colori HEX cablati direttamente nel codice.
    *   *Rischio*: Questi componenti non reagirebbero correttamente a un cambio di tema (es. passaggio a Dark Mode).

---

## 🛠️ Raccomandazioni Tecniche
1.  **Refactoring Colori Hardcoded**: Sostituire i colori HEX fissi nei widget con riferimenti alle costanti in `COLORS` o `STATUS_COLORS`.
2.  **Unificazione Glass Effect**: L'effetto "Glass" della sidebar è codificato manualmente. Potrebbe essere estratto in una funzione helper in `widget_styles.py` per essere riutilizzato in altri pannelli.
3.  **Abilitazione Dark Mode**: La struttura è pronta per il tema scuro (grazie a `DARK` in `colors.py`), ma richiede la rimozione dei vincoli "forzati" nel `ThemeManager`.

---

**Audit completato il:** 26 Febbraio 2026
**Stato:** 🟢 Design System Solido e Coerente.
