# Converge: focus only the empty search landing

**Pass**: 1 · **Date**: 2026-11-22 · **Against**: `spec.md` `b3a9560c5c20` (Accepted) and `plan.md` `acadce10471d`

## What was checked

Every traceability row, by the method it declared.

| Row | Method | Evidence | Result |
| --- | --- | --- | --- |
| FR-001 (load, five landing routes) | `test` | `test_the_empty_search_landing_takes_focus` — 5 subtests, each types without clicking | checked by test — pass |
| FR-001 (in-page arrival) | `test` | `test_the_search_rail_opens_a_focused_landing` | checked by test — pass |
| FR-002 (value, selection, scroll) | `test` | `test_focusing_the_landing_keeps_the_page_still` (`scrollY` 0, selection 0–0, value empty, `scrollHeight == innerHeight` at 390×844) | checked by test — pass |
| FR-003 (submit hands focus back; results never focus) | `test` | `test_the_landing_hands_focus_over_when_results_open` (direct results, then landing → submit) | checked by test — pass |
| FR-004 (reading routes unfocused) | `test` | `test_reading_routes_never_take_search_focus` — chapter, song, service | checked by test — pass |
| FR-005 (no CSS, template, view or route change) | `inspection` | `git diff --stat -- static/ multimedia/ docs/` → `static/web/reading.js`, 35 insertions, nothing else | checked by inspection — pass |
| FR-006 (only 139's no-focus clause superseded) | `inspection` | `spec.md` §Clarifications keeps the superseded decision; `docs/spec/reading.md` `R15` geometry, no-scroll and no-transition sentences survive untouched | checked by inspection — pass, with C1 |
| UI/UX numbers | `manual` | live probe on this worktree's own server (8765): landing field 610×56 at top 422 (1440×900) and 354×56 at top 394 (390×844); results bar 46; `scrollY` 0; `scrollHeight == innerHeight`; preview agrees | checked by inspection of the probe output — pass |

Acceptance scenarios AC1–AC3 → the landing test; AC4 → the rail arrival test; AC5 → the submission
half of the results test; AC6 → the direct-results half; AC7 → the reading-routes test.

The edge case "an invalid query still paints a focused landing without clearing or selecting the
value" was measured separately: `/search?q=`, `?q=%20%20` and `?q=%20%20%20` all render the landing
with focus, an empty value and selection 0–0 (the server trims the query).

## Regression check

Eleven existing tests that touch search or the shell's focus activity, run against this branch: all
pass. `test_search_first_home_renders`, `test_search_finds_a_song`, `test_search_keeps_last_result_set`,
`test_short_query_searches_and_empty_submit_returns_to_index`,
`test_index_is_empty_but_search_restores_tab_local_state`,
`test_search_state_survives_sidebar_browsing`, `test_search_icon_never_opens_a_stale_stored_url`,
`test_clear_controls_in_search_and_filter_fields`, `test_sidebar_timeout_waits_while_filter_has_focus`,
`test_panel_scroll_restarts_sidebar_idle_timeout`, `test_search_page_reads_the_query_grammar`.

The idle-timeout pair matters because the sidebar's activity list includes `focusin`: a landing that
focuses its field must not arm or break the sidebar's timer, and it does not.

## Findings

| # | Type | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | `contradicts` — spec at fault, bookkeeping only | The spec's capability line says this slice "modifies `reading/R15` (focus clause only)", but `R15` carries no focus clause: `specs/139-home-search-center/fold.md` maps that slice's FR-006 onto the geometry paragraph, and `docs/spec/reading.md` mentions focus only in other requirements. There is no clause in the capability tree to supersede — the clause lives in spec 139's own `spec.md`. | **Folded as `added R50` only**, with the discrepancy written into `fold.md`. The behaviour is unchanged either way; reopening Specify to correct a capability line would invalidate a plan for a bookkeeping error. Reported to the owner in the closing report. |
| C2 | `unrequested` — none | No behaviour beyond the spec was added: the blur is limited to the `landing → results` transition, and a background refresh deliberately does not touch focus. | none |

## Outcome

**Converged** — every row holds by its declared method, one bookkeeping finding (C1) recorded and
folded honestly, no accepted gaps.