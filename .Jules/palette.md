## 2024-05-23 - Accessibility: Interactive Elements
**Learning:** `QLabel` with `mousePressEvent` is inaccessible to keyboard users and screen readers.
**Action:** Always use `QPushButton` (styled as label/icon if needed) for interactive elements to inherit native keyboard focus (`Tab`, `Space`, `Enter`) and accessibility traits (`role`, `accessibleName`). Add `:focus` styles to stylesheets for visibility.
