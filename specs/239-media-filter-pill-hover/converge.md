# Convergence: Media Library filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md`
**Plan**: `specs/239-media-filter-pill-hover/plan.md`

## Pass 1 — 2026-11-24

Checked every row against the method it declared. `test` rows were re-assessed from
the actual run, not from their task checkboxes; `inspection` rows were read from the
live probe, the diff and the stylesheet.

| Trace row | Method | Evidence | Result |
| --- | --- | --- | --- |
| US1/AC1 | test | `test_all_unpressed_pills_take_the_hover_pair` — 12 subtests (6 pills × 2 themes); red with rest values on the base, green with the rule | met |
| US1/AC2 | test | `test_pointer_leave_restores_rest_colours` — red on base, green with the rule | met |
| US1/AC3 | test | `test_hover_keeps_box_and_label` — width/height/label unchanged; probe agrees | met |
| US2/AC1 | test | `test_pressed_pill_keeps_its_accent_fill` — red with the guard removed, green with it | met |
| US2/AC2 | test | `test_keyboard_focus_keeps_its_outline` — real Tab press, 2px solid `--focus`, 2px offset | met |
| US2/AC3 | inspection | probe: 63.36 × 30 px in rest, hover and pressed; diff has no geometry declaration | checked by inspection |
| FR-001 | test | same hover-pair test, both themes, six pills | met |
| FR-002 | test | same pressed-pill test | met |
| FR-003 | inspection | `git diff`: one rule, two declarations; no label, dot, filter or focus change | checked by inspection |
| FR-004 | inspection | `git diff --stat`: `components.css` is the only product file changed | checked by inspection |
| SC-001 | test | base run fails 14 subtests with `rgba(0, 0, 0, 0)` where the hover fill belongs | met |
| SC-002 | test | pressed fill/border/text identical under the pointer, both themes | met |
| SC-003 | inspection | probe final readouts: all three states 63.36 × 30 px | checked by inspection |
| SC-004 | inspection | probe final readouts match `spec.md §UI/UX` for light and dark | checked by inspection |

**Findings**: 0 (0 missing · 0 partial · 0 contradicts · 0 unrequested).
**Outcome**: Converged on pass 1. No accepted gaps. T019 stays open for the delivery word.

## Evidence summary

- Red run: `manage.py test tests.e2e.test_media_filter_pill_hover --keepdb` with only the
  gate-1 rule removed — 5 tests, 14 subtest failures, all on missing hover fill/border.
- Green run: same command with the rule restored — 5/5 OK in 12.4s.
- Live probe after the test runs: light hover `rgba(31,31,29,.08)` / `rgb(28,92,60)`,
  dark `rgba(255,255,255,.09)` / `rgb(124,156,240)`, pressed `rgb(28,92,60)` unchanged.
- Number re-check: spec 239 and card ITEM-254 remain free; `origin/develop` VERSION is
  `1.36.23`, so the patch at delivery is `1.36.24`.
