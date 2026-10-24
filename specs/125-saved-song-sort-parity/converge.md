# Convergence: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-24

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The existing field comparison (`test_saved_reading_routes_match_server_fields`, 15 routes) did not compare the sort control; the dedicated parity test covered only the four song/book routes. FR-004 asks for the state to be compared on every route the regression already covers. | `partial` | FR-004 | `tests/e2e/test_saved_render_parity.py` — the `fields()` map had no `sortHidden` entry |

**Outcome**: 1 finding appended as T013 — `sortHidden` added to the existing comparison's `fields()`, so
all fifteen routes now compare it; the class passes (5 tests) with both new tests.

## Pass 2 — 2026-10-24

Checked every requirement against the shipped code and re-ran the class:

| Requirement | Evidence |
| --- | --- |
| FR-001 | saved hymn song `#songSort.hidden` true, equal to the server page (dedicated parity test) |
| FR-002 | frame sampler records no visible control online or offline |
| FR-003 | ordinary songbook's song page keeps the control (measured live: `hidden=false`, 38 px) |
| FR-004 | `sortHidden` in the field comparison over 15 routes, plus the dedicated test over 4 |
| FR-005 | the class's other fields and the two offline classes are unchanged |

**Outcome**: Converged — nothing remains.

## Accepted gaps

none

## Cap reached

not reached
