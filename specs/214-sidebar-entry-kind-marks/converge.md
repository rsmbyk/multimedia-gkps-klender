# Convergence: a contents row marks its entry's kind

## Pass 1 — 2026-11-21

**Checked**: every row of `plan.md`'s traceability table, by the method it declared. The code was read
against `contracts/toc-markup.md` and the live page was measured at `/tatib/151/` on the slice server
(127.0.0.1:8778, 1440 × 900, 1×, both themes).

**Evidence**

| Requirement row | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| US1/AC1–AC4, FR-001–FR-004, FR-006, SC-001–SC-002 | test | `ServiceEntryViewTests` (140 tests, green); `tests.e2e.test_sidebar_kind_marks` (12 tests, green) | present |
| US2/AC1–AC3, FR-004, SC-005 | test | E2E `test_row_accessible_name_is_unchanged`, `test_mark_takes_no_pointer`, `test_focus_never_lands_on_the_mark`; markup carries `aria-hidden` and no control | present |
| US3/AC1, FR-005, SC-003 | test | E2E `test_number_centre_and_row_heights_hold`; `test_toc_number_centering` 4/4 green on a fresh DB; live page measured number x 10px, box 24px, mark x 42px, label x 66px | present |
| US3/AC2, SC-004 | test | E2E `test_three_line_clamp_and_pane_wrap_hold`; `test_text_wrap` run — two assertions fail identically on unmodified `origin/develop` (board ITEM-184) | present; two known-red, not this slice |
| US3/AC3, FR-006 | test | `test_deleted_target_keeps_its_mark` | present |
| US3/AC4 | inspection | `components.css`: no `animation`, `keyframes` or `transition` on `.songrow__mark` or `.slot__badge`; the mark is static markup | checked by inspection |
| FR-002, slot modifier | test | E2E `test_slot_rows_keep_the_kind_modifier`; live `/tatib/151/` shows `data-kind-badge="song"` and `"scripture"` on the slot rows | present |
| FR-003, rebuild | test | `test_marks_survive_a_second_render`; view payload keys confirmed in `_tatib_stage` | present |
| FR-007, SC-006 | test | E2E `test_contrast_in_both_themes` (5.57:1 / 6.59:1) | present |
| FR-008 | test | E2E `test_dock_and_projector_keep_their_own_rows`; `test_stage_kind_marks` green | present |
| Edge cases | test | `test_divider_row_has_no_mark`, `test_slot_with_no_kind_draws_no_badge`, `test_mark_column_at_drawer_and_phone_widths` | present |

**Findings**

- No `missing`, `partial`, `contradicts` or `unrequested` gap against the traceability table.
- Two text-wrap assertions are red, but they fail identically on unmodified `origin/develop` and are
  already carded as ITEM-184; three slot-endpoint unit tests and one CI-tagging test are likewise
  pre-existing (ITEM-217 and an untagged companion-page class). None is touched by this slice.
- The repo advanced while the slice was in flight: spec 215 claimed card ITEM-229. The card was
  renumbered to **ITEM-230** (anchor issue #565 retitled) and `origin/develop` was merged into the
  branch with no conflicts; post-merge suites are green apart from the known-red set above.

**Outcome**: **Converged** — 0 CRITICAL, 0 gaps, 3 pre-existing known-red findings recorded, no accepted
gaps from this slice. No further pass needed.
