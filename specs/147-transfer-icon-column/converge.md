# Convergence: a transfer row's icon column

**Spec**: `specs/147-transfer-icon-column/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-10-28

What was checked, row by row, by the method its plan row declared:

| Row | Method | What was looked at | Result |
| --- | --- | --- | --- |
| FR-001 | `test` | `test_every_transfer_row_shares_one_icon_column` — the set of `.media-transfers__mark` widths is `{32.0}` | green |
| FR-002 | `test` | `test_a_long_transfer_name_still_ellipsizes_at_the_pinned_column` — two names truncate, `clientWidth == 482`, height 72px | green |
| FR-003 | `test` | same run as FR-001 — the `strong` and status `span` left spread ≤ 0.5px | green |
| FR-004 | `test` | `test_the_icon_column_holds_in_a_narrow_dialog` — dialog 382px at a 420px window, text column 284px, spreads ≤ 0.5px, no row past the dialog's right edge | green |
| FR-005 | checked by inspection | `git diff` — `static/styles/design/components.css:2753` is the only production file touched; `static/web/media-handoff.js` and `multimedia/web/templates/reading/base.html` are unchanged; `test_sidebar_transfer_session_shows_active_then_finished` passes in the same module run | no gap |
| SC-001 | `test` | glyph spread 0.0px in the module run | green |
| SC-002 | `test` | name/status spread 0.0px in the same run | green |
| SC-003 | `test` | `scrollWidth > clientWidth` on both long names; row height 72px | green |
| SC-004 | `test` | 420px run | green |
| UI/UX numbers | checked by inspection | `preview/preview.html` regenerated after the fix: Now `32 / 21 / 22.75px` and spreads `5.5` / `11.0px`; Fixed `32px` and `0.0` / `0.0`; the 382px panels show three names truncating and the column holding | matches `spec.md` §UI/UX |
| US1 AC1–AC3, US2 AC1–AC2 | `test` | the three tests above | green |
| Edge: every name fits / every name long | `test` + inspection | the nine-row list mixes both; the preview's panels measure all nine | no gap |
| Edge: active percentage label | checked by inspection | `media-handoff.js:62` still writes the label; the mark is `flex: none`, so the label's width cannot reach it | no gap |
| Edge: empty / disconnected, the rail's list | `test` | `test_sidebar_transfer_session_shows_active_then_finished` (empty and completed states) green; `#mediaTransferRail` draws the same rows from the same renderer | no gap |
| Edge: 200% zoom | checked by inspection | the declaration is a CSS px width with no zoom-dependent unit; nothing in the diff changes with zoom | no gap |

**Findings: 0.** No `missing`, `partial`, `contradicts` or `unrequested` gap was found, so no
`## Phase 6: Convergence` task was appended.

**Outcome**: Converged on pass 1.

**One observation, not a gap.** `tests/e2e/test_media_library.py::…::test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`
fails in the same module run (expected 12px ± 1 between a media row and the text row after it, measured
19.98px). It fails identically on unmodified `develop` (measured 19.71px there, run from the main
checkout at `05379336`), so it belongs to the entry spacing shipped by specs 142–143, not to this
slice — carded as ITEM-156. It is recorded here rather than fixed, because fixing it would be
`unrequested` work inside a slice about the Transfers dialog.

## Accepted gaps

None.

## Cap reached

Not reached — pass 1 converged.
