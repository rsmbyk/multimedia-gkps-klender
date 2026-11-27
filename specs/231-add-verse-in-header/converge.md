# Convergence: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-23

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| — | — | — | No `missing`, `partial`, `contradicts` or `unrequested` finding in the code. |

**Checks against the traceability table**

| Requirement | Method | Result |
| --- | --- | --- |
| US1/AC1 | `test` (E2E written, not executed) + live probe | Add verse 111×34 at x=1157, Project 96×34 at x=1276, gap 8, 1440×900 on `/songs/1880/` |
| US1/AC2 | `test` (E2E written, not executed) + live click | `#editorModal` opens with `New verse` |
| US1/AC3, US1/AC5, US2/AC1–AC3, SC-003–SC-006 | `test` | `test_verse_add_gate`: 5 tests, all green on `gkps231` |
| US1/AC4 | `manual` | 560px probe: Add verse in header, Project hidden by its existing rule |
| FR-001–FR-006 | `inspection` | `song.html` control before Project in `read_actions`; one scoped CSS rule; diff touches no model, endpoint, permission, token or motion |
| FR-007, SC-001, SC-002 | `inspection` | `R56` block written by Fold; probe boxes and null `.verse-add` recorded in `spec.md`/`preview/README.md` |

**Note on the two E2E rows.** The modules are written (`tests/e2e/test_add_verse_header.py`) but
not executed in this pass: the owner's standing instruction defers the heavy browser suite to the
push step. Finding A2, which states that cost, was accepted at gate 2, and the same observable
behaviour was checked live in the approved preview. This is a timing of evidence, not a gap in the
implementation.

**Outcome**: Converged — nothing remains; no Convergence tasks appended.

## Accepted gaps

<!-- none -->

## Cap reached

<!-- not reached -->
