# Convergence: The Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-10-28

Checked every row of `plan.md`'s traceability table by the method it declared, against the code in
the worktree and the run recorded at the bottom.

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The divider's 9px top margin no longer collapses through the list's top edge, because `overflow-y: auto` makes the list a block formatting context — in the first-child case the line now sits 23px under the title instead of 14px | `unrequested` | FR-002 | measured on `preview/preview.html` with the divider moved to the top of the list: `titleToLine` 14px today, 23px after; `lineToRow` 9px in both. Accepted: the line keeps its own 9px in that state too, which is what FR-002 asks, and the state is not reachable from the rail flow (the newest transfer is always the one that started the session, so it is always above the seam) |

**Outcome**: 1 finding, accepted as recorded above; nothing appended as a task.

### Per-row verification

| Row | Method | Evidence |
| --- | --- | --- |
| FR-001, FR-002, FR-003, SC-001 | `test` | `test_the_session_seam_draws_one_line` (row above reports `0px`, divider `2px`, `near` 1) and `test_the_seam_keeps_equal_space_either_side` (9px above / 9px below) — green |
| FR-004, FR-005, SC-002, SC-003, US2/AC1–AC3 | `test` | `test_a_long_transfer_list_scrolls_inside_the_dialog` — green: the list scrolls, the dialog does not, 0px past the inner bottom edge, 22px at the end of the scroll, the title's rect unchanged |
| FR-006, SC-004, US2/AC4, Edge — one row | `test` | `test_a_short_transfer_list_keeps_its_natural_height` — green. **A pin, not a red-first test**: it also passed before the change, which is what it is for |
| US1/AC4 | `test` | the same test asserts no `.media-transfers__divider` when the dialog is opened from `#mediaTransfersButton`; the existing `test_sidebar_transfer_session_shows_active_then_finished` still passes unchanged (active transfer → no divider) |
| US1/AC1 | `inspection` | preview, `9 rows`, light and dark: one 2px line where the report had a 1px line 10.5px above a 2px one (pixel scan of `shots/nine-light-detailNow.png` vs `…detailAfter.png`: 2 boundaries at 319/339 against 1 at 337) |
| US1/AC3, Edge — divider first | `inspection` | preview with the divider moved to the top of the list: 2px line, the row below keeps its 1px border, 23px under the title (see the finding above) |
| Edge — failed / cancelled rows | `inspection` | `git diff` touches `.media-transfers__row`'s border, the dialog's `display` and the list's overflow only; `.media-transfers__main span` (the status text) is untouched |
| Dark theme | `inspection` | preview with `Dark` pressed: `--divider` `#3A362F`, the same counts and distances in the metrics table |

### Where the implementation went beyond the plan

One rule the plan did not name was needed: `.media-transfers__dialog[open]` rather than
`.media-transfers__dialog`. A bare `display: flex` out-ranks the UA's `dialog:not([open]) { display:
none }`, so a closed dialog stayed visible — caught by the existing
`test_sidebar_transfer_session_shows_active_then_finished`, not by the new tests. Recorded here
because the plan's traceability row for FR-004 now points at a selector that carries `[open]`.

### Run

- `tests.e2e.test_media_library` (31 tests after the rebase onto `develop` @ `954dee75`): the four new tests green; the module's one red is
  `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`, which fails identically on
  `develop` under the same command, database and browser — already carded there as ITEM-156, so this
  slice needs no card of its own. The rebase also renamed this slice's page helper to
  `transfer_list_page`, because spec 147's tests own `transfers_page`.
- `test_sidebar_transfer_session_shows_active_then_finished`: green after the `[open]` correction.
- Preview probe re-run after the rules landed: seam `2 · 1px + 2px` → `1 · 2px`, list past the edge
  `19px` → `0px` (nine rows) and `451px` → `0px` (fifteen).

## Pass 2

Not needed — pass 1 left no actionable gap.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| The first-child seam sits 23px under the title instead of 14px | `unrequested` | LOW | 2026-10-28 (agent, recorded; not reachable from the rail flow) |

## Cap reached

Not reached — one pass, nothing actionable.
