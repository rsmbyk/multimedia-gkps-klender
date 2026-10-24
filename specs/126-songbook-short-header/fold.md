# Fold: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md` · **Convergence**: `converge.md` (Converged, pass 1)

## Capabilities touched

| Capability | File | Operation | Requirements |
| --- | --- | --- | --- |
| `reading` | `docs/spec/reading.md` | **created** (0 → 2) | `R1` added — a song page's header cites its songbook by its short name; `R2` added — a saved reading page shows its server route's header and title |

## Deltas applied

- **added `R1`** — the header rule with its six scenarios (short name, sub-number, blank short name,
  unnumbered hymn song, ordinary songbook, tab title).
- **added `R2`** — saved-render parity for a reading page's header and title, with its three scenarios
  (hymn, ordinary, offline).

## What was not folded, and why

- **Requirements from specs 001–125.** There was no capability tree when they landed, so this file starts at
  spec 126. The file's header says so; nothing was reconstructed from the slice records, because a Fold that
  rewrites history is not a Fold. Each earlier behaviour will be folded by the next slice that touches it.
- **The `saved-reading` label.** Specs 125 and 126 labelled their saved-render requirements
  `new: saved-reading`; the owner decided at gate 2 that the saved copy is a requirement inside `reading`,
  so the label resolves to `reading/R2` from here.

## Drift guard

Files changed in this capability: `multimedia/web/reading/views.py` (song citation and tab title) and
`static/web/offline-render.js` (`songPage()`). Both have deltas above. `multimedia/web/tests.py` and
`tests/e2e/test_saved_render_parity.py` changed as verification, which is a slice fact and not behaviour.
`docs/spec/reading.md` is the delta itself.

## Idempotence

This is the file's first fold; re-running this slice records `126-songbook-short-header` as already applied
and writes nothing.
