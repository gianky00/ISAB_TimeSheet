## 2024-05-23 - Visual Feedback for Silent Interactions
**Learning:** Users often distrust silent actions like "Copy to Clipboard". Even when the action works perfectly, the lack of feedback causes uncertainty and repetitive clicking.
**Action:** Always provide immediate, fleeting visual feedback (like a tooltip or toast) for invisible actions. In this case, `QToolTip.showText(cursor_pos, "✨ Copiato!")` provides instant reassurance without interrupting the workflow. Additionally, exposing keyboard shortcuts (like Ctrl+C) via a visible context menu aids discoverability for mouse-first users.

## 2024-05-23 - Motion as "Liveness" Indicator
**Learning:** A static "Running" status indicator (just a color change) can be ambiguous—users may think the app has frozen during long operations.
**Action:** Use subtle motion (like a pulsing animation) to indicate that the application is "alive" and working. A simple opacity pulse on the status dot is less intrusive than a progress bar but effectively communicates ongoing activity.

## 2024-05-23 - Reducing Mouse Travel
**Learning:** Separating list items from their action buttons (e.g., placing "Edit/Remove" buttons far below a list) forces users to move the mouse back and forth repeatedly, increasing cognitive load and physical effort.
**Action:** Implement context menus (Right-Click) directly on list items. This keeps the action (Edit/Delete) spatially connected to the object (the list item), creating a faster and more intuitive workflow.

## 2024-05-23 - Input Field Sizing
**Learning:** Default widget sizes can fail when content density changes (e.g., full date strings).
**Action:** Explicitly set `minimumWidth` for inputs like `QDateEdit` to accommodate the longest expected string (e.g., "DD.MM.YYYY") plus control icons, preventing truncation and usability issues.

## 2024-05-23 - Search Bar Usability
**Learning:** Users in data-heavy views (Database, Accounting) require rapid filtering capabilities. Standard `QLineEdit` search bars lack a quick reset mechanism, forcing manual text deletion.
**Action:** Always enable `setClearButtonEnabled(True)` on filtering inputs to provide a native, accessible "X" button for one-click clearing. This improves efficiency for mouse users and aligns with modern OS search patterns.

## 2024-05-23 - Notification Hierarchy
**Learning:** Frequent success messages via modal dialogs (`QMessageBox`) interrupt user flow.
**Action:** Use "Toast" notifications (translucent overlays) for non-critical feedback (e.g., "Settings saved"), reserving modals only for errors or critical confirmations.

## 2024-05-23 - Self-Contained UI Assets
**Learning:** Relying on external image files for small UI icons (like calendar toggles) complicates deployment and asset management.
**Action:** Embed small UI assets as Base64 strings directly in Python/CSS code. This ensures components like `CalendarDateEdit` are self-contained and render consistently without missing file errors.
