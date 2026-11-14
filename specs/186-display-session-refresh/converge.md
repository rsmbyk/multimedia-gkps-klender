# Convergence: a surface re-reads the session it shows

**Spec**: `specs/186-display-session-refresh/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-11-04

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The value compare used `JSON.stringify` on two objects whose fields are listed in a different order (`read()` writes `session` before `goto`, `write()` after it), so every focus looked like a change and repainted the list | `contradicts` | FR-005 | `test_a_focus_with_the_state_unchanged_repaints_nothing` counted **19** mutations; the fix is a canonical `fingerprint()` and the count is 0 |
| The notify test counted the subscriber's own first call: `subscribe(fn)` hands the state over immediately, so a fresh count begins after it | `partial` | US2/AC2 | `test_a_changed_reread_notifies_a_subscriber_once` read `2 != 1`; resetting the counter after subscribing makes it 1 |

**Outcome**: both fixed in this pass, neither changed a requirement.

## Pass 2 — 2026-11-04

| Check | Result |
| --- | --- |
| `tests.e2e.test_display_session_refresh` (7 tests) | OK |
| `tests.e2e.test_display_session` (11 tests, untouched module) | OK |
| The dock after the marker is cleared: focus → 0 live rows, 0 live screens, no block, eye `Display this service` | OK (SC-001) |
| The projector after the marker is cleared: 0 `.screen.is-active`, `data-showing="false"` | OK (SC-002) |
| Three focus/visibility pairs with the state intact: 0 mutations | OK (SC-003) |
| Stored keys and the module's exports | unchanged (SC-004) |

**Outcome**: Converged.

## Accepted gaps

None.

## Cap reached

Not reached.
