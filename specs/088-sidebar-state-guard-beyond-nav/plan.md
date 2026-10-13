# Plan 088: A stage-only swap preserves the first panel, not the second

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-091
- **Bump:** patch

## Approach

`applyPage()` already computes `stageOnly` for the four kinds that swap the stage without changing
section. The guard it added in spec 080 covers two statements:

```js
if (!stageOnly) {
  root.dataset.nav = fresh.nav;
  root.dataset.ch = fresh.ch;
}
```

Only the first belongs behind the guard. `nav` is the first-level sidebar — the state the operator owns
and the one spec 080 was reported about. `ch` is the second-level pane, which is a *consequence* of the
arriving page: a service opened from the panel has to arrive with its contents open, and for a chapter
or a song opened from the second-level list the arriving value already matches the live one.

So the guard keeps `nav`, and `ch` is applied for every stage swap, with a comment saying why.

## Why not distinguish the click source

Splitting `chapter`/`song` from `service`/`refresh` would work today but encodes a second rule ("clicks
from a list keep the list") that the code cannot observe: the elements are ordinary links and the same
kind is reached from more than one place. Preserving one state and following the page for the other is
the smaller, testable rule.

## Verification

- Red: `tests/e2e/test_reading.py::ReadingE2ETests.test_service_text_sidebar_shows_two_lines_and_centers_grip`
  fails on `develop` today (`#chList .songrow[data-i="e240"]` resolves but is hidden — the contents pane
  never opened). It passed before #334, which the triage run shows.
- Green: that test plus the whole `SidebarStateOnItemOpenTests` class and the two tests spec 080 adjusted.
- A spike on a throwaway worktree at `develop` (discarded, nothing landed) ran the five 080 cases, the
  regression, and the preview module: 20 tests, OK.

## Risks

- Spec 080's own cases are the guard against over-correcting: if the first-level state stops being
  preserved, they fail.
- The narrow-width case (390px) is in that class too, and it is the one that fails first if `ch` starts
  driving layout.
