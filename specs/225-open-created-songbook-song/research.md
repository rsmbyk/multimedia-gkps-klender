# Research: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md`

## What the base commit already does

- `multimedia/web/reading/views.py::editor_save` returns `{'ok': True, 'id': saved.pk, 'kind': kind,
  'created': pk is None}`; the create signal and the new id are already on the wire. No server change.
- `static/web/editors.js` dispatches `editor:saved` with that object after a successful save only;
  a 400 re-renders the form and emits nothing.
- `static/web/reading.js`'s `editor:saved` listener branches for a created Normal service
  (`kind='tatib'`, `created`, `record_kind === 0`) and otherwise refreshes the lists in place.
- A panel songbook click calls `navigate(tile.href, {kind: 'lists'})` (`reading.js` bindPanelTiles):
  the row becomes current, the child pane opens, no history entry is pushed and the URL stays
  `/songs/`. A song row click calls `navigate(link.href, {kind: 'song'})` (bindChRows): the stage
  swaps, a history entry is pushed and `data-read` becomes `on`.

## Decisions

| Question | Answer | Source |
| --- | --- | --- |
| Which surface opens? | Songbook: selected row + song list. Song: reading stage. | Owner clarification, 2026-11-23 |
| Which navigation kinds? | `lists` for a songbook, `song` for a song — the same kinds a row click uses. | `reading.js:832-835`, `898-901` |
| How to guarantee fresh data? | `forceServer: true`, as spec 209 uses for a created service; the row exists on the server before the save response returns. | `reading.js:1531`, spec 209 |
| How to keep focus sane? | Reuse the shell's own `navigate` promise; do not add a second focus mechanism. The generic listener's `what`/`focusKind` refresh path stays for edits. | `reading.js:2066-2110` |
| What about other kinds? | Branch only on `created === true` and `kind` in (`songbook`, `song`); everything else takes the existing path. | Spec FR-004/FR-005 |

## Measurement

Live base-commit reproduction (`reproduce.py`, `probe_click.py`) is in the spec folder. The target
values are the measured click-through states, not a new visual design.

**Unknowns remaining: 0.**
