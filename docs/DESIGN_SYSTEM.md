# SyncroJob Design System (V2.0)

Linee guida per mantenere un'interfaccia utente coerente, professionale e "Enterprise".

## 1. Palette Colori (da `src/gui/styles/constants.py`)
*   **Primary**: `#004a77` (Deep Blue)
*   **Success**: `#2e7d32` (Green)
*   **Warning**: `#ed6c02` (Orange)
*   **Error**: `#d32f2f` (Red)
*   **Background**: `#f5f7f9` (Light Grey)

## 2. Componenti Standard (Core Widgets)
Ogni nuovo pannello **DEVE** utilizzare questi widget invece di quelli nativi di PyQt6 per garantire coerenza stilistica:

*   **Pulsanti**: `src.gui.widgets.modern_button.ModernButton`
    *   Supporta icone e animazioni hover.
*   **Dialoghi di Input**: `src.gui.dialogs.standard_input_dialog.StandardInputDialog`
    *   Sostituisce `QInputDialog`.
*   **Conferme**: `src.gui.dialogs.confirmation_dialog.ConfirmationDialog`
    *   Sostituisce `QMessageBox`.
*   **Toast**: `src.gui.widgets.toast.ToastManager`
    *   Per notifiche non invasive (success, error, warning, info).
*   **Empty States**: `src.gui.widgets.empty_state.EmptyStateWidget`
    *   Da mostrare quando una tabella o una lista è vuota.

## 3. Tabelle e Liste
*   Usare `src.gui.widgets.excel_table.ExcelTable` per tabelle che richiedono export/copia-incolla.
*   Le icone di stato devono essere caricate tramite `src.utils.helpers.get_asset_path(Icons.X)`.
*   **Mai usare emoji nel testo dei widget**; usare icone SVG dalla cartella `assets/icons/`.

## 4. Layout e Spacing
*   **Margini Standard**: 10px per i layout principali.
*   **Padding**: 8px per i contenuti interni dei widget.
*   **Alignment**: I pulsanti di azione devono essere centrati o allineati a destra in base al contesto (seguire il pattern dei pannelli esistenti).

## 5. Animazioni
*   Utilizzare `src.utils.animation_helpers` per effetti di fade, slide o pulse.
*   Le transizioni tra le pagine sono gestite automaticamente da `SlidingStackedWidget`.
