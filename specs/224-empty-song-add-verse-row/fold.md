# Fold: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md`
**Date**: 2026-11-23

## Capabilities touched

| Capability | Before | After | Operations |
| --- | --- | --- | --- |
| `reading` (`docs/spec/reading.md`) | R40 | R40 modified | `modified` R40's control sentence — the after-the-last-verse add control exists only with a live verse, the song's one control otherwise sits in the empty invitation, which shares the Tata Ibadah quarter-band; two scenarios added; header `last folded` 2026-11-23 and slice prepended |

## Delta

`### R40 — A song's verses are added, edited, removed and reordered on its page` now states the
gate and the placement instead of promising an add control unconditionally. Its two new scenarios
name the one-button empty page and the within-1px title band shared with an empty Tata Ibadah.
No new `R<n>` was taken: the change narrows and refines an existing requirement.

## Drift guard

| File | State |
| --- | --- |
| `multimedia/web/templates/reading/song.html` | changed — `{% if can_edit_verses and verse_rows %}` at line 45 |
| `static/styles/design/components.css` | changed — three `:has(.entry__empty)` song rules beside the Tata Ibadah block |
| `multimedia/web/reading/test_verse_add_gate.py` | added — three template cases |
| `tests/e2e/test_song_empty_placement.py` | added — two targeted geometry cases |
| `docs/spec/reading.md` | changed — R40 and header |
| `static/web/songs_verse.js` | listed to prove the modal and save path are untouched |
| `multimedia/web/reading/views.py` | listed to prove `verse_rows` and the guards are unchanged |
| `backlog/board.md`, `specs/README.md` | changed — Ready row and Accepted index row |

## Not folded

- The static-preview limitation and the 5.5px mobile residual are decisions about this slice's
  evidence, not durable capability behaviour; they stay in `converge.md`.
- The patch version, changelog line, board Done move and PR reference belong to delivery, not to
  the capability tree.
