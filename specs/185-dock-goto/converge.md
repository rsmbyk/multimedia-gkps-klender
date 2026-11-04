# Convergence: the dock's Go To

**Spec**: `specs/185-dock-goto/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-11-04

The suite was run against a throwaway database (`gkps185`), and every traceability row was
checked against a test that exercises the running product.

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| FR-007 says the block's header carries "its `On screen` marker and `Back`"; FR-017 says that header "SHALL NOT carry it either" | `contradicts` | FR-007 / FR-017 | `spec.md` FR-007 vs FR-017. FR-017 is the later rule and matches the approved preview (`preview/index.html`, the block's header carries no pill); the code follows FR-017, and FR-007's phrase is read as "the block itself is the marker". No code change. |
| Opening `/projector?service=<id>` while the service stands on screen 2 writes `screen: 0` — the projector's own boot adopts the URL's service "at its start" | `unrequested` | FR-008 | `static/web/projector.js:1833-1836` (`if (adoptId) { … write({service: adoptId, screen: 0 …}) }`). Pre-existing and untouched by this slice (the same block exists on `develop`); it only matters to the round-trip when the projector window is opened mid-service. Out of scope here — proposed as a follow-up card, not fixed silently. |
| The dock's block renders every song screen, including a bait's built-in rest, as a row labelled `Rest` | `partial` | FR-007 | A rest row is a real screen the projector can stand on and steps like any other; the preview showed it as an italic `Rest`. Kept — the alternative is a row the arrows can land on without a way back to it. |

**Outcome**: 3 findings; no task appended — two are readings of the accepted text and one is
pre-existing behaviour outside the slice.

## Pass 2 — 2026-11-04

| Check | Result |
| --- | --- |
| `tests.e2e.test_dock_goto` (14 tests) | OK |
| `tests.e2e.test_goto_shared_state` (8 tests) | OK |
| `tests.e2e.test_display_session` (12 tests, untouched module) | OK |
| `tests.e2e.test_entries` (14 of 26 in the module ran; 3 failed) | 3 failures — **identical on unmodified `develop`** (worktree `../multimedia-gkps-klender-attr185`, base `d51d9288`): `test_an_empty_service_invites_the_first_item` (TimeoutError), `test_an_empty_service_places_its_tiles_a_quarter_of_the_way_down` (`6 != 4`), `test_the_add_controls_wait_for_a_hover` (`'1' != '0'`). Pre-existing, not caused by this slice. |
| Preview probes | `probe.py`, `probe_sync.py`, `probe_frame.py` — all green |

A third pass was not needed: nothing actionable remained.

**Outcome**: Converged.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| The projector's boot resets the service's screen to 0 when its window is opened with `?service=` | `unrequested`, pre-existing | MEDIUM — costs the operator the place mid-service, and Back then lands on screen 0 | not accepted here; proposed as a follow-up card |

## Cap reached

Not reached.
