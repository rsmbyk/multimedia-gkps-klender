# Convergence: an open modal keeps the scroll to itself

## Pass 1 — 2026-11-28

**Checked**: all 14 rows of `plan.md`'s traceability table, by the method each row declared. Artifacts
read: `spec.md`, `plan.md`, `tasks.md`, `research.md`, `analysis.md`, the shipped CSS diff, the two
probe logs, the red/green test logs and the nested-dialog check.

| Row | Typed finding | Evidence |
| --- | --- | --- |
| US1/AC1 + FR-001 — editor at end | none | `test` green: `test_wheel_at_the_end_of_editor_content_leaves_the_document_still`; probe `tall`: document 600 → 600, content 0 → 617 |
| US1/AC2 — Preview at end | none | `test` green: `test_wheel_at_the_end_of_preview_body_leaves_the_document_still`; base failed the same test on document 1700 |
| US1/AC3 + FR-002 — picker nesting | none | `test` green: `test_picker_options_at_their_end_do_not_scroll_the_editor`; probe `nested`: options 870, editor 0, document 600 |
| US2/AC1 + FR-003 — zero range | none | `test` green: `test_short_editor_does_not_scroll_the_document`; base failed on 2360 |
| US2/AC2 — chrome | none | `test` green: `test_wheel_over_the_editor_header_leaves_the_document_still`; base failed on 2360 |
| US2/AC3 + FR-005 + SC-004 — close | none | `test` green: `test_closing_the_dialog_restores_document_scrolling_at_the_same_offset`; `geometry.py`: 1200/1200/1200 and box 480×100 at (360, 300) on both sides |
| US3/AC1 + FR-004 + SC-002 — all scrollports | none | `test` green: `test_every_named_modal_scrollport_contains_scroll`; probe computed styles `contain` for editor/content/options/dialog and root `hidden` |
| US3/AC2 — nested dialogs | none | checked by inspection: Chromium reported 2 and 1 open dialogs with root `overflow-y: hidden`, and `visible` only after the last close |
| SC-001 — red → green | none | `red.log`: 7 named failures on `1cd9f081` with the test module copied in; `green.log`: `Ran 7 tests … OK` on the slice; base copy removed afterwards |
| SC-003 — no layout shift | none | checked by inspection: `geometry.py` output above, no width or box delta |
| UI/UX values | none | checked by inspection: final `probe.py` run after the last selector edit matches every number in `spec.md` |
| Change scope | none | checked by inspection: behaviour files in `git diff --name-only 1cd9f081` are `static/styles/design/components.css` and `tests/e2e/test_modal_scroll_containment.py` only |
| Research coverage | none | checked by inspection: `research.md` survey lists 13 scrollports with base values; 8 decisions each carry rationale, alternatives and provenance |
| Production confirmation | none (deferred) | checked by inspection of the declared manual row: `tasks.md` T020 is intentionally open until deployment; not executable in a worktree |

**Outcome**: no `missing`, `partial`, `contradicts` or `unrequested` findings. The only open items are
the declared manual row and the declared delivery steps, neither of which is a convergence gap.
**Converged** at pass 1; Fold may run.
