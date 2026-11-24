# Data Model: song entry modal scrollbar

**Spec**: `specs/236-song-modal-scrollbar/spec.md`

## Entities

No persisted entity is added, removed or changed. The slice changes one CSS declaration on the
shared dialog; no model, migration, form or serialiser is involved.

## Existing boxes the rule relies on

| Box | Current rule | Role in this slice |
| --- | --- | --- |
| `.editor` | `display: flex; flex-direction: column; max-height: min(86vh, 46rem)`; UA `overflow: auto` | the fault: a second scroll container at the dialog edge |
| `.editor__content` | `overflow-y: auto; min-height: 0` | the intended scrollport; unchanged |
| `.editor__verse-panel[hidden]` | `display: grid; grid-template-rows: 0fr; opacity: 0` | animated collapse; its clipped descendants cause the 10px overflow; unchanged |

**Relationships**: `.editor` contains `.editor__content`, which contains the entry form and the
collapsed verse panel. **Validation**: none. **State transitions**: none — the rule applies in
every editor state and does not key on the form's mode.

## Invariants

- The dialog's own edge has no scrollbar in any song-entry state (FR-001, FR-002).
- Overflow scrolls in `.editor__content` when a form is taller than the cap (FR-003).
- The verse panel's collapse animation and fixed-position picker menus are unchanged (FR-004).

## Not modelled

- No new CSS custom property: the change is a single declaration using no design tokens.
- No new state flag: the rule is unconditional on `.editor`.
