# Data model: the dock fills whatever panel it is given

**Spec**: `specs/164-dock-fluid-width/spec.md`

No entity, no server state, no payload change, no template change: the slice removes two declarations
from one rule, so the only model is the dock's own box tree:

```
body.obs-dock                          the dock page; its viewport IS the panel
└── main.dock#dockPanel                 column flex; width 100%, height 100%, margin 0 (was: max 560, centred)
    ├── section.view#viewPick           the picker
    │   ├── div.dock__head              title row; buttons pushed right by margin-left: auto
    │   └── div.dock__body#pickBody     the scroller, padding 4px 8px 10px; block layout, one column (FR-003)
    │       └── section[data-bucket]    one per non-empty age bucket, stacked
    │           ├── h3.group__head      sticky at the scroller's top (FR-005)
    │           └── ul > li > button.servicerow
    │               ├── span.servicerow__n   flex: 1 — the name, at the row's 10px left padding
    │               ├── span.onscreen / span.servicerow__today   pills, after the name
    │               └── span.servicerow__d   the date, the row's last item (FR-004)
    └── section.view#viewRun            the runner: unchanged by this slice
```

Invariants this slice creates:

1. **The panel's box equals the viewport.** `.dock` has no maximum and no horizontal auto margin, so
   its width is the viewport's at every size from 320px up (FR-001).
2. **Nothing below the panel needs a width.** Every child was already fluid — the head is a flex row,
   the body is a block scroller with 8px side padding, the rows are `width: 100%` — so the row's
   content width is the panel's width less 16px at every size (FR-004, SC-003).
3. **The column count is fixed at one.** `#pickBody` keeps `display: block`; the buckets are sections
   in normal flow, so all of them share one x and one sticky-head line (FR-003, FR-005).

Nothing is persisted; the page is rendered per request and the dock's state stays browser-local
(`web/display.js`), untouched here.
