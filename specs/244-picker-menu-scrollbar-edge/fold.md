# Fold: picker popout scrollbar edge

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-26

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `R59` | The complete R59 block now adds: the options scrollport reaches the menu's inner right and bottom borders (only the 1px border between the scrollbar lane and the menu edge), the menu clips that lane to its radius, option rows/group headings/in-menu filter keep their boxes, and a non-overflowing list draws no bar; new scenario `The menu's scrollbar is its edge`. The accepted search, filter, keyboard and cascade rules are unchanged. |

Header: `last folded` moved to 2026-11-26 and `244-picker-menu-scrollbar-edge` was prepended to
`slices`.

## Drift guard

- **Files changed in this capability**: `static/styles/design/components.css`,
  `tests/e2e/test_picker_menu_scrollbar_edge.py`, `specs/244-picker-menu-scrollbar-edge/`,
  `docs/spec/reading.md`, `backlog/items/ITEM-259-picker-scrollbar-edge.md`, `backlog/board.md`.
- **Declared no behaviour change**: no — the change moves the painted scrollbar lane to the menu's
  border while preserving every other behaviour; R59 records the modification.
- `CHANGELOG.md` and `VERSION` are written in the delivery commit, after the push has given the
  card its PR number; they are not part of this Fold commit.

## Before / after

| | Before | After |
| --- | --- | --- |
| reading `R<n>` count | 60 | 60 (`R59` modified, no new number) |
| `slices` entries | 60 | 61 |
| spec packs under `specs/` (this branch) | 243 max (in flight) | 244 added |
| scrollport right/bottom gap from menu (Book/Chapter) | 9px / 9px | 1px / 1px |

## Number retake

The plan and tasks first named `ITEM-258`; the navigation slice claimed that ID in an unmerged
worktree before the card was created. Every worktree was re-scanned, `ITEM-259` was taken, and the
plan, tasks, card and board row were updated. The plan also first named patch `1.37.1`; the
navigation slice merged to `develop` with that number after this branch was cut, so the next free
patch is `1.37.2` and the plan/tasks were updated. No spec number or capability ID was retaken:
`244` and the `R59` modification remained free.

## Not folded

No requirements were excluded — Converge reported no accepted gaps. The pre-existing
`test_hidden_and_muted_states` failure in `tests.e2e.test_song_entry_pickers` is identical on the
unmodified base and is not a behaviour change from this slice; it is recorded in `converge.md`,
not folded.
