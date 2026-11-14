# Convergence: the active Tata Ibadah lasts only the browser session

## Pass 1 — 2026-11-03

**Checked**: every row of `plan.md`'s traceability table against the code and a run, by the method
the row declares.

### Evidence

| Command | Result |
| --- | --- |
| `manage.py test tests.e2e.test_display_session --keepdb` | 11 tests, **OK** (red before the code: 7 failures and 2 errors, each for its own reason — no marker, a foreign stamp read as a state, the restart's state without a `session`, the cookie-less reload resurrecting the display) |
| `manage.py test tests.e2e.test_obs_dock tests.e2e.test_obs_overlay tests.e2e.test_projector --keepdb` | 85 tests, **OK** |
| `manage.py test tests.e2e.test_reading --keepdb` | 86 tests, 1 failure — `test_the_panel_shows_its_empty_view_when_no_songbook_exists`, the known red on develop (ITEM-137, the songbook empty copy); unrelated to this slice and untouched by it |

### Row status

| Row | Status | Evidence |
| --- | --- | --- |
| FR-001 | converged | `…::test_a_state_from_an_earlier_session_paints_nothing`, `…::test_a_browser_restart_ends_the_session` |
| FR-002 | converged | `…::test_first_paint_never_shows_a_prior_session_state` (a `MutationObserver` from document start sees 0 children) |
| FR-003 | converged | `…::test_the_state_carries_the_session_of_its_writer` |
| FR-004 | converged | `…::test_a_reload_inside_the_session_keeps_the_display`, `…::test_every_surface_closed_and_reopened_keeps_the_display`, and the existing 85 |
| FR-005 | converged | `…::test_the_marker_carries_no_display_data` |
| FR-006 | converged | `…::test_a_surface_without_cookie_storage_still_paints` (no page error; a reload starts idle) |
| FR-007 | converged | existing hide and release tests, green in the 85 |
| FR-008 | converged | `…::test_a_state_with_a_foreign_stamp_reads_as_no_state` |
| FR-009 | converged | `…::test_a_state_written_before_this_slice_reads_as_no_state` |
| FR-010 | converged | `…::test_two_surfaces_minting_together_agree_on_one_session` — two writers agree on the jar's value, and a surface that finds the jar already holding a value takes it instead of its own candidate |
| SC-001 | converged | `…::test_a_browser_restart_ends_the_session` — a real persistent-profile restart: 0 overlay children, 0 pills, the projector not showing |
| SC-002 | converged | `…::test_first_paint_never_shows_a_prior_session_state` |
| SC-003 | converged | the two in-session guards, plus the dock/overlay/projector suites |
| SC-004 | converged | `…::test_the_marker_carries_no_display_data` |
| SC-005 | converged | `…::test_a_state_with_a_foreign_stamp_reads_as_no_state` (both readers) |
| US1/AC1–AC3 | converged | the restart test, the first-paint test, and the existing dock projection cases |
| US2/AC1–AC4 | converged | the two new guards and the existing overlay/dock cases |
| Assumption — OBS restart | **checked by manual — not run in this session** | the steps are in `plan.md`; OBS cannot be driven from this suite. Research D008 records why the cookie cannot survive it (CEF does not persist session cookies; one global context) |

### Findings

Nothing `missing`, `contradicts` or `unrequested`. The one method weaker than ideal is noted, not a
gap: FR-010's instantaneous interleaving cannot be driven from Playwright's synchronous API, so the
test asserts its outcome — one id, and a mint that takes the jar's value — rather than the race
itself.

### Outcome

**Converged, pass 1.** Fold may proceed; the only outstanding verification is the manual OBS restart,
declared in the plan since gate 2.
