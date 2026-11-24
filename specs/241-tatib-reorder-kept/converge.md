# Convergence: reordered Tata Ibadah keeps every entry

**Spec**: `specs/241-tatib-reorder-kept/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-24

Every traceability row was re-assessed against the present code, not against its checkbox.

| Requirement | Declared method | Evidence | Result |
| --- | --- | --- | --- |
| US1/AC1 | `test` | `test_a_drop_after_an_edit_is_written_and_the_pane_follows` — base red `[4,1,2,3]` vs `[3,1,2,4]`; present code green, sidebar `3,1,2,4`, stage `3,1,2` | pass |
| US1/AC2 | `test` | same test's reload assertions; a fresh fetch paints the dropped order | pass |
| US1/AC3 | `test` | `test_a_drag_after_an_add_keeps_every_entry_on_the_stage` — base red (stage `[5,3,1,2]`), present code green with every entry once | pass |
| US1/AC4 | `inspection` | `endDrag()` sets `drag = null` before `applyPaneOrder(order())`; the captured base stack `applyPaneOrder <- cancelDrag` cannot fire on a completed drop | checked by inspection |
| US2/AC1 | `test` | `test_an_edit_leaves_the_contents_in_server_order` — rows equal a fresh fetch; base painted `[4,1,2,3]` | pass |
| US2/AC2 | `test` | `tests/e2e/test_song_sort_retained.py` — six tests green (two songs, explicit stamps) | pass |
| US2/AC3 | `test` | `tests/e2e/test_reading.py` chapter-order cases stay green; `applySongOrder()` swaps only song rows among their slots | pass |
| US3/AC1 | `inspection` | `cancelDrag()` still calls `place(current.order)` and never `persist()`; a rewrite-raised cancel is inert once `drag` is null | checked by inspection |
| US3/AC2 | `inspection` | `applyPaneOrder()` calls `readNodes()` itself, so the next gesture sees current sections | checked by inspection |
| FR-001 | `test` | one POST per drop; `written.value.ok` and the reload assertions in both drop tests | pass |
| FR-002 | `test` | both new drop tests assert sidebar order and stage order together | pass |
| FR-003 | `test` | the add-then-drag test asserts every section once in sidebar order | pass |
| FR-004 | `inspection` | `cancelDrag()` restores `current.order` and posts nothing | checked by inspection |
| FR-005 | `test` | `test_an_edit_leaves_the_contents_in_server_order` | pass |
| FR-006 | `test` | six song-sort cases plus the existing toggle case | pass |
| FR-007 | `test` | reload assertions in both drop tests | pass |
| FR-008 | `inspection` | `moving` is built only from pks in `what`, which comes from top-level TOC rows; nested option sections stay inside their choice | checked by inspection |
| SC-001 | `test` | three new E2E tests: red on base, green on this branch | pass |
| SC-002 | `test` | all 32 `tests/e2e/test_reorder.py` cases green | pass |
| SC-003 | `test` | the server-order test and the post-edit drop test | pass |
| SC-004 | `test` | song-sort module green; `test_reading.py` / `test_entries.py` have no new failures and one prior red turns green | pass |

**Outcome**: no gaps — Converged in one pass. The three new tests fail on the base commit for the
two recorded causes and pass here; no new failure appeared in any adjacent suite.

## Mechanical alignment applied during the pass

- The gates were accepted together after implementation, so the card was opened in `Speccing`
  and then aligned to `In progress`; it will carry the `Branch` column until a PR exists. Gate 1
  accepted the spec and gate 2 accepted the plan, including the ten unticked checklist items —
  the agent does not tick reviewer-owned checklists (SDD-15).
- The preview server was started from this worktree against the development database; its URL and
  measurements are recorded in `preview/README.md`.

## Accepted gaps

None. Analysis findings A1–A5 were accepted at gate 2 with their dispositions.

## Cap reached

Not applicable — Converged on pass 1.
