# SyncroJob - Design System & UI Standards

Linee guida per mantenere un'interfaccia utente coerente, professionale e conforme al brand "SyncroJob Enterprise".

## 🎨 Palette Colori (Material 3 Inspired)
Definita centralmente in `src/gui/design/colors.py` e mappata semanticamente in `src/gui/styles/constants.py`.

### Colori Brand
- **Primary**: `#009688` (Teal) - Azioni principali e loghi.
- **Secondary**: `#673AB7` (Purple) - Elementi di supporto e accento.
- **Accent/Deep**: `#004a77` (Deep Blue) - Testate e Sidebar.

### Colori Semantici (Stato)
- **Success**: `#2ecc71` (Green)
- **Warning**: `#f39c12` (Orange)
- **Error/Danger**: `#dc3545` (Red)
- **Surface**: `#FFFFFF` (Bianco Card)
- **Background**: `#FAFAFA` (Grigio chiarissimo)

---

## 🏗️ Componenti UI Standard (Design System)
Ogni nuovo pannello **DEVE** utilizzare i widget specializzati invece di quelli nativi di PyQt6:

*   **Pulsanti**: `src.gui.widgets.modern_button.ModernButton` (Animazioni hover incluse).
*   **Dialoghi**:
    *   Input: `src.gui.dialogs.standard_input_dialog.StandardInputDialog`
    *   Conferma: `src.gui.dialogs.confirmation_dialog.ConfirmationDialog`
*   **Feedback**: `src.gui.widgets.toast.ToastManager` (Notifiche non bloccanti).
*   **Tabelle**: `src.gui.widgets.excel_table.ExcelTable` (Supporto copia/incolla Excel).
*   **Header**: `StatusCard` (Titolo pannello + indicatori bot).

---

## 🔍 Regole di Styling (Audit Findings)

### 1. Centralizzazione QSS
*   Evitare `setStyleSheet` inline con colori HEX cablati.
*   Importare stili da `src.gui.styles.widget_styles.py`.
*   Usare i file QSS in `assets/styles/` (`light.qss`, `overrides.qss`).

### 2. Iconografia & Asset
*   **MAI usare Emoji** nei widget enterprise.
*   Utilizzare icone SVG da `assets/icons/`.
*   Caricamento tramite `src.utils.helpers.get_asset_path(Icons.X)`.

### 3. Layout & Metriche
*   **Margini Standard**: 10px per i layout di pagina.
*   **Padding**: 8px interno ai widget.
*   **Bordi**: Arrotondamento (border-radius) standard: 4px, 8px, o 12px (definito in `constants.py`).

### 4. Animazioni
*   Utilizzare `src.utils.animation_helpers` per effetti di fade o pulse.
*   Le transizioni tra pannelli sono delegate a `SlidingStackedWidget`.
