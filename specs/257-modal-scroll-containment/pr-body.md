Refs #653

An open modal used to pass a wheel to the page behind it once its own view reached the end — and
immediately when that view had nothing to scroll. A nested picker also moved the editor content
under it.

- Hold the document while any native `<dialog>` is open.
- Contain the ten named modal scrollports so each keeps its own range without chaining outward.
- Inner scrolling, focus, layout and the opening scroll offset stay unchanged.

Seven Playwright behaviours fail by name on unmodified `1cd9f081` (7/7) and pass on the slice (7/7).
The final live A/B probes match every value frozen in the spec's `## UI/UX`. `reading/R66` was folded
with four scenarios.

Board: `ITEM-277` is **In review** on this PR and moves to Done before the merge. The `patch` bump
and changelog line land in the pre-merge delivery commit.

Verification split: 7 test · 6 inspection · 1 manual (the manual production check remains after
deployment).
