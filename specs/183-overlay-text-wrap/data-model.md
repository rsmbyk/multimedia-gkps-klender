# Data model: the overlay's text wraps inside the box that owns it

**Spec**: `specs/183-overlay-text-wrap/spec.md`

No stored entity, no payload and no endpoint changes. What the slice governs is a computed property
and the boxes it moves; they are recorded here so a reader can tell which measurement is the
behaviour's and which is a consequence of it.

| Object | Where it comes from | Before | After |
| --- | --- | --- | --- |
| `.obs-overlay__stage` (the rule's home) | the overlay template's single child div | `overflow-wrap: normal` (inherited default) | `overflow-wrap: break-word` |
| `.obs-overlay__plate` | `static/web/obs-overlay.js` `plate()` | inherits `normal` | inherits `break-word` |
| `.obs-overlay__kicker` | the plate's heading, first line | inherits `normal` | inherits `break-word` |
| `.obs-overlay__title` | the plate's heading, remaining lines | inherits `normal` | inherits `break-word` |
| `.obs-overlay__line` (a body row) | one `<p>` per screen line | inherits `normal` | inherits `break-word` |
| `.obs-overlay__words` (a marked row's text) | the row's second grid cell | inherits `normal` | inherits `break-word` |
| `.obs-overlay__speaker` (the mark) | the row's first grid cell | `white-space: nowrap` (own declaration) | unchanged |
| `.obs-overlay__caption` (a song) | the caption builder | inherits `normal` | inherits `break-word` |
| The plate, report state (1080p) | | 1728×240.72 | 1728×240.72 |
| The plate, pasted-URL state (1080p) | | 1728×251.52 | 1728×301.91 (one more row) |
| The plate, passage state (1080p) | | 1728×326.22 | 1728×364.03 (title and body rows) |
| The caption, song state (1080p) | | 1728×302.39 | 1728×403.19 (one more row) |
| The plate, 64-character kicker (1080p) | | 963.44×139.94 | 963.44×139.94 |

The panel boxes are a *consequence*: the rule changes where a run breaks, and a panel's height follows
the rows that result. The panels' width, anchor and padding are unchanged — FR-003 is the requirement
that keeps it that way — and the kicker's plate does not move at all, because its own run already fits.
