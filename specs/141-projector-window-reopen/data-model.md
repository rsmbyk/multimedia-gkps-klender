# Data model: reopening the projector window

**Slice**: `specs/141-projector-window-reopen`

**No entity changes.** No model, migration, payload or stored value moves. This file records the
browser-local state the control reads and the DOM contract it joins, so the slice's effect is
readable without running it.

## The display state (read, never written)

`localStorage['gkps-display']`, shared across the browser's tabs by `static/web/display.js`:

| Field | Type | The reopen control's use |
| --- | --- | --- |
| `service` | `number \| null` | compared with this page's `data-project-service`: the control is drawn only on the live service |
| `screen` | `number` | not read by the control — the projector page reads it when it loads, which is what returns the operator to the on-air screen |
| `on` | `boolean` | must be `true` for the control to be drawn |
| `translation` | `'TB' \| 'SIM' \| null` | untouched; the projector wears it as today |
| `at` | `number` | untouched — a reopen writes nothing, so the timestamp does not move |

## The DOM contract (new attribute set, existing group)

| Node | Attribute | Value | Owner |
| --- | --- | --- | --- |
| `.read__project` | `data-project-group` | — | template; the group `display.js` resolves |
| `.read__project` | `data-displaying` | `"true"` / `"false"` | `display.js` `syncButton` — the control's only visibility input |
| `.read__project` | `data-display-channel` | `gkps-service-display` | template (unchanged) |
| `button[data-project-open]` | `data-projector-url`, `data-project-service`, `data-label-project`, `data-label-stop` | as today | template; the Project / Stop toggle |
| `button[data-project-window]` | `data-projector-url` | `/projector` (the bare page) | template — **new** |
| `button[data-project-window]` | `aria-label`, `title` | `Open projector window` | template — **new** |
| `button[data-project-window]` | `data-project-service` | the service id | template — **new**, the same guard the toggle uses |
| `span[data-project-label]` | — | `Project` / `Stop projecting` | `display.js` (unchanged) |

The control carries no new stored value, no class another component selects on, and no server
variable: the URL is written with `{% url 'web-projector' %}`, so the route keeps one definition.

## What changes for an operator

| Case | Before | After |
| --- | --- | --- |
| Window closed while screen 4 is on air | the only control releases; Project restarts at screen 0 | the control reopens the window on screen 4, with no state written |
| Window open | no control reaches it | the control focuses it; the page is not reloaded |
| Display hidden or released | Project only | Project only — unchanged |
| 1280 window, service with media, on air | group 238.4 px in a 240 px pane | group 240 px wrapped over two rows, no spill; header 111 px |
