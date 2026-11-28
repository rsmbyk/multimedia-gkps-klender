# Converge: refit the projector words when fullscreen changes the stage

**Spec**: `specs/247-projector-fullscreen-fit/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-27

**Checked**: the code against `plan.md`'s traceability table, row by row, with each row checked by
the method it declared. `test` rows are the six named cases run on throwaway `test_gkps247`;
`inspection` rows are the diff and the live probe readings; the `manual` row was driven through the
Go To on the live preview.

| Requirement | Method | Result | Evidence |
| --- | --- | --- | --- |
| FR-001 | test | met | `test_fullscreen_signal_refits_the_words_without_a_resize`: stage 804 → 1004 with no `resize`, active lines 42 → 49px, key updated; red on base with `42 not greater than 42` |
| FR-002 | test | met | `test_display_mode_signal_refits_for_browser_fullscreen`: a `change` on the display-mode query with no `fullscreenElement` and no `resize` grows the words; red on base |
| FR-003 | test | met | `test_a_second_fullscreen_signal_does_not_change_the_fit`: repeat at the same stage changes no size or key; green on base too (characterisation guard) |
| FR-004 | test | met | `test_fullscreen_signal_refits_the_neighbours`: neighbour 125 → 168px while it stays off stage; red on base with `125 not greater than 125` |
| FR-005 | inspection | met | `git diff --name-only` shows only `static/web/projector.js` and `tests/e2e/test_projector.py` in source; `fit()`, `setSize()`, CSS, key/click handlers and the cue are untouched; the resize guard case passes |
| FR-006 | inspection | met | no endpoint, model, migration, template or stylesheet in the diff; the listeners are added inside the existing event-registration block (`projector.js:1954–1978`) |
| SC-001 | inspection | met | `preview/probe.py`: base `87 → 87 → 87`, slice `87 → 93 → 87` across stage 804 → 1004 → 804 |
| SC-002 | inspection | met | same probe: heading `53.769 → 57.4772 → 53.769`, base flat; `setSize` still divides by the golden ratio |
| SC-003 | test | met | `test_resize_driven_fullscreen_still_settles_at_87_and_109`: CDP viewport 1440×900 → 1920×1080 → back grows and returns the fit and key; green on base too (guard) |
| SC-004 | inspection | met | every passing case asserts path `/projector?service=…`, `data-current-screen=0` and the same 48-character body prefix |
| US1/AC1 | test | met | shared with FR-001 |
| US1/AC2 | test | met | shared with FR-003 |
| US1/AC3 | manual | met | live preview: Go To `Kis 1` on service 144, detour active; detour lines `87 → 93 → 87px`, key `1376x804|…` → `1376x1004|…` → `1376x804|…` |
| US1/AC4 | test | met | `test_a_fullscreen_signal_with_an_unchanged_stage_does_not_resize_words`; green on base too (guard) |
| US2/AC1 | test | met | shared with SC-003 |
| US2/AC2 | test | met | shared with FR-002 |
| US2/AC3 | inspection | met | the F key, mouse-zone, cue and audio/video takeover blocks are byte-identical to the base; the new listener never calls `render()` |

**Targeted run**: six named cases, `......`, 0 failures, 20.7 s on `test_gkps247`. The full browser
suite is deferred to the push step per the repo's verification split; no full-suite claim is made.

**Findings**: none — `missing` 0 · `partial` 0 · `contradicts` 0 · `unrequested` 0.

**Outcome**: converged on pass 1. No convergence tasks were appended.

## Accepted gaps

None.

## Cap reached

Not applicable — converged before the cap.
