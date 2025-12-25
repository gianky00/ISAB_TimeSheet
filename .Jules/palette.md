## 2024-05-23 - Accessibility: Interactive Elements
**Learning:** `QLabel` with `mousePressEvent` is inaccessible to keyboard users and screen readers.
**Action:** Always use `QPushButton` (styled as label/icon if needed) for interactive elements to inherit native keyboard focus (`Tab`, `Space`, `Enter`) and accessibility traits (`role`, `accessibleName`). Add `:focus` styles to stylesheets for visibility.

## 2024-05-23 - UX: Application Map
**Learning:** Users prefer a "Workflow Map" over abstract dashboards.
**Action:** Use a linear, card-based layout on the home screen to guide users through the intended process flow (e.g., Step 1 -> Step 2 -> Step 3). Use arrows and clear numbering to indicate sequence.
