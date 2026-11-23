# Convergence: Verse modal header draws one rule

**Spec**: `specs/226-verse-modal-header-rule/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-11-23

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| none | — | FR-001 … FR-006, SC-001 … SC-003, US1/AC1 … AC7 | Each row checked by its declared method below. |

**Outcome**: zero findings, so no `## Phase N: Convergence` tasks were appended.

### Read-back by declared method

- **test** — `tests.e2e.test_verse_modal_header`, 5 cases at 1366×900 plus a 390×844 resize and
  both colour schemes. Red before the CSS edit: 5 failures, each
  `AssertionError: the title still paints a 1px bottom border` (right reason, no import or timeout
  errors after the pencil click was changed to a DOM click). Green after the edit: 7 tests including
  `tests.e2e.test_song_empty_placement`, `OK` in 20.182s.
- **test** — live probe against the slice worktree's own server at `http://127.0.0.1:8766/songs/1820/`:
  `New verse` and `Edit verse 1` both read title border `0px`, title-to-rule gap `16.5px`, head width
  `840px`, zero ruled descendants inside the head, no page errors.
- **inspection** — `git diff` touches only `static/styles/design/components.css:539–545`,
  `tests/e2e/test_verse_modal_header.py`, the spec pack, the card and the board. Both changed CSS
  selectors require `[data-editor-size="large"]`; the loading skeleton has no such marker.
- **test** — the non-verse `New song` characterisation asserts 18px type, 0px title padding, a
  16px title-to-rule gap and a 16px divider-to-label gap; it stayed green through red and green.

## Pass 2 — 2026-11-23

**Outcome**: Converged — nothing remains.

## Accepted gaps

None.

## Cap reached

Not reached.
