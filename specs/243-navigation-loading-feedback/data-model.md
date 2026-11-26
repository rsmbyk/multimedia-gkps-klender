# Data model — spec 243

**Spec**: `specs/243-navigation-loading-feedback/spec.md`

No schema change. The slice reads and writes only data that already exists in the
server-rendered shell and the clicked element's own attributes.

| Entity / field | Role in this slice |
| --- | --- |
| `data-name` on `.book` or `.songrow`, `.rail__name`, `.ch-num` text | source of the title / number / eyebrow seeded into the placeholder |
| `href` on the clicked anchor | URL passed to `navigate()`; unchanged |
| `opts.kind` at `navigate()` | existing classification (`rail`, `lists`, `chapter`, `song`, `search`, `result`, `sync`…); mapped to list-only vs stage-write, not replaced |
| `navBusy`, `pendingNavigation`, `navigationGeneration` | existing client fields in `reading.js`; the queue is replaced by cancel/coexist by stage-write class |
| `pending` (new client record) | `{url, opts, source, writesStage, resolve}`; one live record per fetch, plus an optional coexisting list fetch |
| `locked` (new client set) | clicked elements with `aria-disabled="true"` and the dim-only class; released on success, failure or cancellation |
| `#panel`, `#chapters`, `.stage` | section roots that receive a 3px bar at their very top edge when their content will be replaced |
| `.stage[aria-busy]` | set only for stage writes; cleared on settlement |
| `role="status"` live region | pre-rendered empty, polite, updated once on open and once on settlement |

Invariants: a rail or sidebar item cannot be activated again while its own
request is live; a list-only fetch never sets `aria-busy` on the stage; a stage
write always has exactly one stage bar and one placeholder of the correct
anatomy; a cancelled fetch releases its item immediately; only `navigate()`
starts or clears pending state.
