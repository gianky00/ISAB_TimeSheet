## 2024-05-23 - Accessibility: Interactive Elements
**Learning:** `QLabel` with `mousePressEvent` is inaccessible to keyboard users and screen readers.
**Action:** Always use `QPushButton` (styled as label/icon if needed) for interactive elements to inherit native keyboard focus (`Tab`, `Space`, `Enter`) and accessibility traits (`role`, `accessibleName`). Add `:focus` styles to stylesheets for visibility.

## 2024-05-23 - UX: Dashboard Hub
**Learning:** When application modules are independent, a sequential "Workflow Map" is confusing.
**Action:** Use a "Hub" layout (Grid) to present modules as equal, independent entry points. Avoid numbering or directional arrows unless a strict dependency exists.
