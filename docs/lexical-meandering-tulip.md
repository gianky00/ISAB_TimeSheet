# Piano di Redesign Vista Notifiche - SyncroJob Enterprise

## Obiettivo
Trasformare la vista Notifiche da una lista base di notifiche a un moderno notification center con design migliorato, funzionalità avanzate, e UX ottimizzata.

---

## Analisi Stato Attuale

### Struttura Esistente
- **File principale**: `src/gui/notifications_panel.py` (580 righe)
- **Widget notifica**: `src/gui/widgets/notification_item.py` (140 righe)
- **Backend**: `src/core/notification_manager.py` (singleton, JSON storage)

### Limitazioni Correnti
1. **Visuale**: Design piatto, limitata gerarchia visiva
2. **Organizzazione**: Nessuna categorizzazione, solo 3 filtri base
3. **Contenuto**: Solo testo semplice, no rich content
4. **Interazioni**: Solo delete e mark-as-read
5. **Search**: Non presente
6. **Performance**: Lista verticale non scala bene oltre 100 notifiche

### Data Model Attuale
```python
{
    "id": str,          # UUID
    "title": str,       # Titolo
    "message": str,     # Messaggio
    "level": str,       # info, success, warning, error
    "timestamp": str,   # ISO format
    "read": bool        # Letto/non letto
}
```

---

## Design Vision

### Principi Guida
1. **Consistenza**: Riutilizzare pattern esistenti (ActivityFeed, Toast, ModernButton)
2. **Progressive Enhancement**: MVP → funzionalità avanzate gradualmente
3. **Performance**: Lazy loading, pagination, caching
4. **Backward Compatibility**: Preservare dati esistenti con migrazione graduale

### Pattern da Riutilizzare
- **ActivityFeed**: Gradient backgrounds, 4px colored border, circular icon badges
- **Toast System**: Type-to-color-to-icon mapping, pulse animations
- **Data Tables**: Status-based coloring, toolbar con search/filter
- **Design System**: ColorPalette (success/warning/error/info), Spacing, BorderRadius

---

## Architettura Nuova Struttura

### Gerarchia Componenti

```
NotificationsPanel (main)
├── NotificationToolbar         [NUOVO]
│   ├── Search input (debounced 300ms)
│   ├── Filter chips (All, Unread, Error, Warning, Info)
│   ├── Sort dropdown (Date, Priority, Level)
│   └── Bulk actions menu (when multi-select active)
│
├── NotificationListContainer   [NUOVO]
│   ├── GroupHeader (collapsible) [NUOVO]
│   │   └── "Fissate", "Oggi", "Ieri", "Più vecchie"
│   └── NotificationCard (enhanced) [NUOVO]
│       ├── Header: Pin icon, status badge, title, timestamp, menu (•••)
│       ├── Body: Rich text (markdown support), expandable
│       └── Footer: Category tag, priority badge, action buttons
│
└── NotificationPreferencesDialog [NUOVO]
    └── Settings: grouping, auto-archive, badge config
```

### Data Model Esteso

```python
{
    # Esistenti
    "id": str,
    "title": str,
    "message": str,
    "level": str,        # info, success, warning, error
    "timestamp": str,
    "read": bool,

    # NUOVI CAMPI
    "category": str,     # bot, system, user, database, api
    "priority": str,     # low, medium, high
    "source": str,       # es. "Bot Scarico TS", "Lyra Sentinel"
    "pinned": bool,      # Fissata in alto
    "snoozed_until": str | None,  # ISO timestamp
    "archived": bool,    # Archiviata
    "tags": list[str],   # Tags personalizzati
    "metadata": dict,    # Storage flessibile per rich content
    "actions": list[dict],  # Inline action buttons
    "related_id": str | None  # Link a audit log entry
}
```

**Migrazione**: Campi nuovi con valori default, backward compatible.

---

## Visual Design

### NotificationCard Design

#### Layout Struttura
```
┌─────────────────────────────────────────────────────┐
│ [📌] [●] Title                 [2h ago] [•••]       │ ← Header
│ ──────────────────────────────────────────────────  │ ← Divider
│ Message body con supporto markdown, code blocks,   │ ← Body
│ **bold**, *italic*, e [links](url)                 │
│                                                     │
│ [🏷️ Bot] [🔴 High]              [Retry] [Details]  │ ← Footer
└─────────────────────────────────────────────────────┘
  ↑ 4px colored left border (level-based)
```

#### Proprietà Visive

**Border & Background**:
- Bordo sinistro: 4px accent color (level-based)
- Background unread: Gradient sottile (es. `#fff5f5 → #ffffff` per errori)
- Background read: Bianco puro, opacity 80%
- Border-radius: 12px (BorderRadius.lg)
- Padding: 16px (Spacing.md)

**Icon Badge**:
- Dimensione: 32px circolare
- Background: Bianco
- Icon colorato basato su level

**Color Mapping** (riutilizza Toast/ActivityFeed):
```python
LEVEL_STYLES = {
    "error": {
        "accent": "#F44336",  # error red
        "gradient": "qlineargradient(..., #fff5f5, #ffffff)",
        "icon": Icons.X_CIRCLE
    },
    "warning": {
        "accent": "#FF9800",  # warning orange
        "gradient": "qlineargradient(..., #fffaf0, #ffffff)",
        "icon": Icons.ALERT_TRIANGLE
    },
    "success": {
        "accent": "#4CAF50",  # success green
        "gradient": "qlineargradient(..., #f0fdf4, #ffffff)",
        "icon": Icons.CHECK_CIRCLE
    },
    "info": {
        "accent": "#2196F3",  # info blue
        "gradient": "qlineargradient(..., #f0f9ff, #ffffff)",
        "icon": Icons.INFO
    }
}
```

**Priority Badges**:
- High: 🔴 Red dot + "Alta" label, optional pulse animation
- Medium: 🟡 Orange dot + "Media" label
- Low: 🟢 Green dot (default, no label)

**Animations**:
- Fade-in on load: 400ms, OutCubic easing
- Scale on hover: 1.0 → 1.02, 200ms
- Slide-out on delete: 300ms, InBack easing
- Shadow on hover: `0 4px 12px rgba(0,0,0,0.15)`

### Toolbar Design

**Filter Chips** (Material Design 3 style):
```
[📋 Tutti (12)] [🔔 Da leggere (5)] [❌ Errori (2)] [⚠️ Avvisi (3)] [ℹ️ Info (7)]
```
- Active: Filled con accent color, testo bianco
- Inactive: Outlined, testo grigio
- Hover: Elevation + tinta background
- Badge circolare con count

**Search Bar**:
- Placeholder: "Cerca notifiche..."
- Icon: Search (sinistra)
- Clear button (destra, appare quando text presente)
- Debounce: 300ms
- Real-time filtering mentre si digita

### Empty States

**All Read State**:
```
      ✅ (64px icon, green)
  Tutto a posto!
  Nessuna notifica da leggere

  [Visualizza archivio →]
```

**No Notifications**:
```
      📭 (mailbox icon)
  Nessuna notifica
  Le tue notifiche appariranno qui
```

**No Errors**:
```
      🎉 (celebration)
  Sistema funzionante!
  Nessun errore registrato
```

---

## Funzionalità Avanzate

### 1. Grouping (Raggruppamento)

**Time-Based (Default)**:
- 📌 **Fissate** (pinned=true, sempre in cima)
- 📅 **Oggi** (ultime 24h)
- 📆 **Ieri** (24-48h fa)
- 📂 **Ultimi 7 giorni** (2-7 giorni)
- 🗂️ **Più vecchie** (>7 giorni)

**Alternative Views** (toggle nel toolbar):
- Category-based: 🤖 Bot, 🛡️ Sistema, 📊 Database, 🌐 API, 👤 Utente
- Priority-based: 🔴 Alta, 🟡 Media, 🟢 Bassa

**Group Headers**:
- Collapsible (click per espandere/chiudere)
- Count badge: "(5 notifiche)"
- Subtle divider line

### 2. Filtering & Search

**Basic Filters** (chip buttons):
- Tutti (all notifications)
- Da leggere (unread only)
- Errori (level=error)
- Avvisi (level=warning)
- Info (level=info)

**Advanced Filters** (dropdown menu):
- **Categoria**: Multi-select (Bot, Sistema, Database, API, Utente)
- **Priorità**: Checkboxes (Alta, Media, Bassa)
- **Periodo**: Date range picker o preset (Oggi, 7 giorni, 30 giorni, Custom)
- **Origine**: Dropdown (Bot OdA, Bot TS, Lyra Sentinel, Sistema)

**Search**:
- Full-text search in title, message, tags
- Debounced (300ms) per performance
- Highlight matched terms in results
- Advanced syntax (opzionale): `error:yes priority:high category:bot`

**Sort Options**:
- Data (Più recenti prima) ⬇️ [DEFAULT]
- Data (Più vecchie prima) ⬆️
- Priorità (Alta → Bassa)
- Livello (Errori → Info)

### 3. Rich Content Support

**Markdown Rendering**:
- **Bold**, *italic*, `code inline`
- Code blocks con syntax highlighting
- Lists (bullets, numbered)
- Links (clickable, open in browser)
- Blockquotes

**Implementation**: QTextBrowser con HTML rendering

**Inline Action Buttons**:
```python
"actions": [
    {
        "label": "Riprova",
        "key": "retry_bot_scarico_ts",
        "variant": "primary",  # ModernButton variant
        "icon": Icons.REFRESH
    },
    {
        "label": "Dettagli",
        "key": "open_audit_log",
        "variant": "ghost",
        "icon": Icons.INFO
    }
]
```

Render come ModernButton nel footer, emit signal per handling.

### 4. Interazioni Avanzate

**Context Menu** (right-click):
```
✔️  Segna come letta
❌  Segna come non letta
📌  Fissa / Rimuovi pin
💤  Posponi (submenu: 1h, 3h, Domani, Custom)
───────────────
🔗  Copia link
📋  Copia testo
───────────────
🗑️  Elimina
📂  Archivia
```

**Multi-Select Mode**:
- Trigger: Ctrl+Click o checkbox hover
- UI: Checkboxes visibili su tutte le card
- Toolbar: "X selezionate", bulk action buttons enabled
- Actions: Segna lette, Elimina, Archivia, Fissa

**Keyboard Shortcuts**:
```
j/k      - Navigate down/up
Enter    - Expand/collapse
Space    - Toggle read/unread
p        - Pin/unpin
Delete   - Delete selected
Ctrl+F   - Focus search
Esc      - Clear selection/deselect all
```

**Pin Functionality**:
- Click pin icon in card header
- Pinned cards move to "Fissate" group (top)
- Visual: Pin icon filled (solid) when pinned

**Snooze**:
- Right-click → Posponi → Select time
- Notifica hidden fino a timestamp
- Background timer controlla e mostra quando scade

### 5. Notification Preferences

**Dialog** (trigger: ⚙️ button in header):

**Sezioni**:
1. **Notifiche Toast**:
   - ☑️ Abilita toast per errori
   - ☑️ Abilita toast per avvisi
   - ☐ Abilita toast per info
   - Durata: [3 secondi ▾]

2. **Raggruppamento**:
   - Raggruppa per: [⚪ Data ⚪ Categoria ⚪ Priorità]
   - Comprimi gruppi automaticamente: ☑️

3. **Filtri Predefiniti**:
   - All'apertura mostra: [Da leggere ▾]
   - Nascondi notifiche archiviate: ☑️

4. **Gestione Automatica**:
   - Archivia notifiche lette dopo: [7 giorni ▾]
   - Elimina notifiche archiviate dopo: [30 giorni ▾]

5. **Badge Sidebar**:
   - Conta nel badge: [☑️ Errori ☑️ Avvisi ☐ Info]

**Storage**: `CONFIG_DIR/notification_preferences.json`

---

## Performance Optimization

### 1. Pagination
- Carica 50 notifiche per pagina (default)
- "Carica altre" button in fondo
- Infinite scroll variant: Auto-load quando scroll raggiunge 80% bottom

### 2. Lazy Rendering
- Render solo notifiche visibili + buffer (10 sopra/sotto viewport)
- Reuse widget pool per scrolling fluido

### 3. Search Indexing
- Pre-build search index on load: `{notif_id: lowercase_searchable_text}`
- Invalidate on notifications_updated signal

### 4. Filter Caching
- Memoize filter results con cache key (hash filter state)
- Clear cache on data update

### 5. Virtualized Scrolling (Fase avanzata)
- Alternative a pagination per 1000+ notifiche
- QListView + QAbstractListModel
- Only render visible items (~50-60 max in DOM)

---

## Implementazione a Fasi

### 🔵 Fase 1: MVP - Core Visual Redesign (2-3 giorni)

**Obiettivo**: Feature parity + design moderno

**Tasks**:
1. ✅ Creare `NotificationCard` widget con nuovo design
   - Layout: header + body + footer
   - Border 4px, gradient backgrounds per unread
   - Icon badge 32px circolare
   - Animations: fade-in, hover scale, delete slide-out

2. ✅ Creare `NotificationToolbar` widget
   - Search bar con debounce
   - 5 filter chips (All, Unread, Error, Warning, Info)
   - Sort dropdown (Data desc/asc, Priority, Level)

3. ✅ Implementare time-based grouping
   - Group headers collapsible
   - "Fissate", "Oggi", "Ieri", "Più vecchie"

4. ✅ Integrare in `NotificationsPanel`
   - Replace NotificationItem con NotificationCard
   - Replace filter buttons con toolbar
   - Connect signals (filter_changed, search_query, sort_changed)

5. ✅ Empty states per ogni filtro

**Files da creare**:
- `src/gui/widgets/notification_card.py` (~300 righe)
- `src/gui/widgets/notification_toolbar.py` (~200 righe)
- `src/gui/widgets/notification_group_header.py` (~80 righe)

**Files da modificare**:
- `src/gui/notifications_panel.py` (refactor, ~450 righe finali)

**Testing**:
- Visual regression (screenshot comparison)
- Filters funzionanti
- Performance con 50+ notifications

---

### 🟢 Fase 2: Rich Content & Actions (2 giorni)

**Obiettivo**: Markdown, action buttons, priority badges

**Tasks**:
1. ✅ Estendere data model in NotificationManager
   - Add campi: category, priority, source, pinned, actions, metadata, etc.
   - Migration function: auto-add defaults per backward compat

2. ✅ Markdown rendering in card body
   - QTextBrowser con HTML
   - Support bold, italic, code, links, lists

3. ✅ Priority badge component
   - High: Red dot + pulse animation
   - Medium: Orange dot
   - Low: Green dot

4. ✅ Inline action buttons in footer
   - Render actions list as ModernButton widgets
   - Connect to handler: `_handle_action(notif_id, action_key)`

5. ✅ Context menu (right-click)
   - Mark read/unread, Pin, Snooze, Copy, Delete, Archive

**Files da creare**:
- `src/gui/widgets/priority_badge.py` (~60 righe)
- `src/core/notification_templates.py` (~100 righe)

**Files da modificare**:
- `src/core/notification_manager.py` (+150 righe per nuovi metodi)
- `src/gui/widgets/notification_card.py` (markdown support)

**Testing**:
- Markdown edge cases
- Action button callbacks
- Context menu actions

---

### 🟡 Fase 3: Advanced Filtering & Search (1-2 giorni)

**Obiettivo**: Category filters, date range, advanced search

**Tasks**:
1. ✅ FilterState dataclass per state management
2. ✅ Advanced filters dropdown
   - Category multi-select
   - Priority checkboxes
   - Date range picker (CalendarDateEdit)
3. ✅ Implement category/priority grouping modes
4. ✅ Search highlighting in results

**Files da creare**:
- `src/gui/widgets/advanced_filter_dropdown.py` (~200 righe)

**Files da modificare**:
- `src/core/notification_manager.py` (get_filtered_notifications, search methods)
- `src/gui/notifications_panel.py` (filter logic)

**Testing**:
- Filter combinations
- Search performance (500+ notifications)
- Edge cases

---

### 🟣 Fase 4: Interactions & UX (1-2 giorni)

**Obiettivo**: Multi-select, bulk actions, keyboard shortcuts

**Tasks**:
1. ✅ Multi-select mode con checkboxes
2. ✅ Bulk actions menu
3. ✅ Keyboard shortcuts handler
4. ✅ Notification preferences dialog

**Files da creare**:
- `src/gui/dialogs/notification_preferences_dialog.py` (~150 righe)

**Files da modificare**:
- `src/gui/notifications_panel.py` (keyboard logic, multi-select)
- `src/gui/widgets/notification_card.py` (checkbox mode)

**Testing**:
- Multi-select con 20+ items
- Keyboard navigation flow
- Preferences persistence

---

### ⚪ Fase 5: Performance & Polish (1 giorno)

**Obiettivo**: Pagination, caching, accessibility audit

**Tasks**:
1. ✅ Implement pagination (50 per page)
2. ✅ Search/filter caching
3. ✅ Loading skeletons per async operations
4. ✅ Accessibility audit
   - Keyboard navigation
   - Screen reader labels
   - High contrast mode support
   - Focus indicators

**Files opzionali**:
- `src/gui/models/notification_list_model.py` (se virtualization)

**Testing**:
- Load 1000 notifications, measure FPS
- Screen reader test (NVDA)
- Keyboard-only navigation

---

## Files Summary

### Nuovi Files (da creare)
```
src/gui/widgets/notification_card.py              (~300 righe)
src/gui/widgets/notification_toolbar.py           (~200 righe)
src/gui/widgets/notification_group_header.py      (~80 righe)
src/gui/widgets/priority_badge.py                 (~60 righe)
src/gui/widgets/advanced_filter_dropdown.py       (~200 righe)
src/gui/dialogs/notification_preferences_dialog.py (~150 righe)
src/core/notification_templates.py                (~100 righe)
src/gui/models/notification_list_model.py         (~120 righe, opzionale)
```

**Totale nuovo codice**: ~1,210 righe

### Files Esistenti (da modificare)
```
src/gui/notifications_panel.py          (580 → ~450 righe, refactored)
src/core/notification_manager.py        (130 → ~280 righe, +150)
src/gui/widgets/notification_item.py    (140 righe, deprecato → refactor in card)
```

### Files di Riferimento (leggere per pattern)
```
src/gui/widgets/activity_feed.py        (pattern card, gradients, animations)
src/gui/widgets/toast.py                (color mapping, animations)
src/gui/widgets/data_table.py           (toolbar, filtering)
src/gui/design/colors.py                (design tokens)
src/gui/design/spacing.py               (spacing system)
```

---

## NotificationManager: Nuovi Metodi

```python
# src/core/notification_manager.py

def update_notification(self, notification_id: str, updates: dict) -> None:
    """Update specific fields of a notification."""

def pin_notification(self, notification_id: str, pinned: bool = True) -> None:
    """Toggle pinned state."""

def snooze_notification(self, notification_id: str, until: datetime) -> None:
    """Snooze notification until timestamp."""

def archive_notification(self, notification_id: str) -> None:
    """Move notification to archive."""

def add_tag(self, notification_id: str, tag: str) -> None:
    """Add tag to notification."""

def get_filtered_notifications(self, filter_state: FilterState) -> list[dict]:
    """Apply complex filters and return matching notifications."""

def search_notifications(self, query: str) -> list[dict]:
    """Full-text search with ranking."""

def bulk_operation(self, notification_ids: list[str], operation: str, **kwargs) -> None:
    """Perform bulk operation on multiple notifications."""
```

---

## Design Decisions & Trade-offs

### ✅ Pagination vs Virtualization
**Scelta**: Iniziare con Pagination (MVP), aggiungere Virtualization solo se necessario
**Rationale**:
- Pagination più semplice (1 giorno vs 2 giorni)
- Maggior parte utenti ha <200 notifications
- Virtualization può essere aggiunta dopo senza breaking changes

### ✅ Swipe Gestures
**Scelta**: Defer post-MVP (troppo complesso per desktop)
**Rationale**:
- Mouse swipe detection è finicky
- Context menu già fornisce tutte le azioni
- Better suited for mobile/touch

### ✅ Rich Text Engine
**Scelta**: QTextBrowser + basic Markdown → HTML conversion
**Rationale**:
- No external dependencies heavyweight
- Supporto HTML out-of-box in Qt
- Can sanitize HTML per security

### ✅ Default Grouping
**Scelta**: Time-based come default
**Rationale**:
- Recency è più importante per notifiche
- Category/Priority utile per debugging ma non primario
- Toggle disponibile per power users

---

## Testing Strategy

### Unit Tests
```
tests/unit/test_notification_card.py
tests/unit/test_notification_toolbar.py
tests/unit/test_notification_manager_extended.py
tests/unit/test_filter_state.py
```

### Integration Tests
```
tests/integration/test_notifications_flow.py
```

**Scenarios**:
- Add notification → appears in list → mark read
- Filter by error → only errors shown
- Search → results filtered → highlights
- Multi-select → bulk delete

### Visual Regression
- Screenshot key states (empty, 5 notif, 50 notif)
- Pixel diff before/after

### Performance Benchmarks
```python
def test_render_100_notifications():
    """Ensure 100 notifications render in <500ms"""
    start = time.time()
    panel.setData(generate_test_notifications(100))
    elapsed = time.time() - start
    assert elapsed < 0.5
```

### Manual Checklist
- [ ] Keyboard navigation (Tab, j/k, Enter, Space)
- [ ] Screen reader announces correctly
- [ ] High contrast mode (Windows)
- [ ] 1000+ notifications no lag
- [ ] All animations smooth (60fps)
- [ ] Context menu works
- [ ] Markdown rendering edge cases
- [ ] Action buttons trigger callbacks
- [ ] Preferences save/load

---

## Priority Matrix

### ✅ Must-Have (MVP - Fase 1-2)
- Nuovo design card (border, gradients, icon badge)
- Time-based grouping
- Enhanced toolbar (search, 5 filters, sort)
- Priority badges
- Empty states
- Basic animations (fade-in, hover)

### 🟡 Should-Have (Fase 3-4)
- Advanced filters dropdown
- Multi-select + bulk actions
- Keyboard shortcuts
- Context menu
- Preferences dialog
- Pin/snooze functionality
- Markdown rendering
- Inline action buttons

### 🔵 Nice-to-Have (Fase 5+)
- Virtualized scrolling
- Rich media (images)
- Analytics tracking
- Export to CSV/PDF
- Notification templates

### ❌ Out of Scope
- Mobile app
- Push notifications (requires server)
- AI categorization

---

## Success Metrics

### Quantitative
- Render 100 notifications in <500ms
- Search result in <100ms
- 60fps smooth animations

### Qualitative
- "Notifiche sono più facili da gestire"
- "Design moderno e pulito"
- "Ho trovato subito la funzione che cercavo"

---

## Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Performance degradation con 1000+ notif | Medium | High | Pagination early, virtualization se serve |
| Backward compatibility breaks | Low | High | Migration script, schema versioning |
| Complex state management | Medium | Medium | Dataclasses per state, centralized in panel |
| Animation jank | Low | Medium | Profile, disable se FPS <30 |
| Accessibility regressions | Medium | Medium | Checklist per fase, screen reader tests |

---

## Verification Plan

### Dopo Fase 1 (MVP)
1. Lanciare applicazione: `python main.py`
2. Navigare a Notifiche panel (sidebar)
3. Verificare:
   - [ ] Nuovo design card visibile (border 4px, gradient per unread)
   - [ ] Toolbar presente (search, 5 filters, sort)
   - [ ] Grouping time-based (Oggi, Ieri, ecc.)
   - [ ] Empty states per filtri vuoti
   - [ ] Animations smooth (fade-in, hover scale)
4. Testare filtering:
   - [ ] Click "Da leggere" → solo unread mostrate
   - [ ] Click "Errori" → solo error-level
   - [ ] Search bar → filtra in real-time
5. Performance:
   - [ ] Creare 50 notifiche test → render fluido
   - [ ] Scroll smooth, no lag

### Dopo Fase 2 (Rich Content)
1. Creare notifica con markdown:
   ```python
   NotificationManager.instance().add_notification(
       title="Test Markdown",
       message="**Bold** text con `code` e [link](url)",
       level="info"
   )
   ```
2. Verificare:
   - [ ] Markdown renderizzato correttamente
   - [ ] Priority badge visibile (se priority!=low)
   - [ ] Action buttons nel footer (se actions presenti)
   - [ ] Context menu (right-click)
3. Testare pin:
   - [ ] Pin notifica → move to "Fissate" group
   - [ ] Unpin → torna al group originale

### Dopo Fase 3 (Advanced Filtering)
1. Aprire advanced filters dropdown
2. Verificare:
   - [ ] Category multi-select funzionante
   - [ ] Date range picker
   - [ ] Filter combinations (es. category=bot + priority=high)
   - [ ] Search highlighting in results

### Dopo Fase 4 (Interactions)
1. Testare multi-select:
   - [ ] Ctrl+Click → checkbox mode attivo
   - [ ] Select 5+ notifications
   - [ ] Bulk action "Elimina" → conferma dialog → delete
2. Testare keyboard:
   - [ ] j/k navigation
   - [ ] Space → toggle read
   - [ ] p → pin/unpin
   - [ ] Delete → delete selected
3. Preferenze dialog:
   - [ ] Aprire dialog → settings visibili
   - [ ] Modificare grouping mode → salvato
   - [ ] Riaprire app → preferences persistenti

### Dopo Fase 5 (Performance)
1. Creare 1000 notifications test:
   ```python
   for i in range(1000):
       NotificationManager.instance().add_notification(...)
   ```
2. Verificare:
   - [ ] Pagination attiva (50 per page)
   - [ ] "Carica altre" button funzionante
   - [ ] Search rapido (<100ms)
   - [ ] No UI freeze durante operazioni

### Accessibility Test
1. Tab navigation:
   - [ ] Tab attraverso tutti elementi interattivi
   - [ ] Focus indicator visibile (2px outline)
2. Screen reader (NVDA/JAWS):
   - [ ] Card announced con title + level + timestamp
   - [ ] Buttons have accessible labels
3. High contrast mode:
   - [ ] Colori leggibili
   - [ ] Border visibili

---

## Appendix: Code Snippets

### FilterState Dataclass
```python
# src/gui/notifications_panel.py

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class FilterState:
    levels: list[str] = field(default_factory=lambda: ["all"])
    categories: list[str] = field(default_factory=list)
    priorities: list[str] = field(default_factory=list)
    date_range: tuple[datetime, datetime] | None = None
    show_read: bool = True
    show_unread: bool = True
    show_archived: bool = False
    search_query: str = ""
    sort_by: str = "date_desc"
    group_by: str = "time"  # time, category, priority
```

### Migration Function
```python
# src/core/notification_manager.py

def _migrate_notification(self, notif: dict) -> dict:
    """Add new fields with defaults for backward compatibility."""
    defaults = {
        "category": "system",
        "priority": "low",
        "source": "Sistema",
        "pinned": False,
        "snoozed_until": None,
        "archived": False,
        "tags": [],
        "metadata": {},
        "actions": [],
        "related_id": None,
    }
    return {**defaults, **notif}
```

### Card Animation Example
```python
# src/gui/widgets/notification_card.py

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

def _animate_fade_in(self):
    """Fade-in animation on load."""
    self.opacity_effect = QGraphicsOpacityEffect(self)
    self.setGraphicsEffect(self.opacity_effect)

    self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
    self.animation.setDuration(400)
    self.animation.setStartValue(0.0)
    self.animation.setEndValue(1.0)
    self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    self.animation.start()
```

---

## Conclusione

Questo piano fornisce una roadmap completa e dettagliata per trasformare la vista Notifiche in un moderno notification center. L'approccio a fasi permette di rilasciare valore incrementale mantenendo qualità e performance.

**Timeline stimato**: 7-10 giorni per implementazione completa (Fase 1-5)
**MVP rilasciabile**: 2-3 giorni (Fase 1)

**Next Steps**:
1. Approvare piano
2. Iniziare con Fase 1 (MVP)
3. Iterare basandosi su feedback utenti
