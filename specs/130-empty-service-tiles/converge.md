# Convergence — pass 1

Code read against `plan.md`'s traceability table. Every row reconsidered from the code, not from the task
boxes.

| Requirement | Code found | Type | Action |
| --- | --- | --- | --- |
| FR-001 | `.read[data-kind="tatib"]:has(.entry__empty)` + `.read__body:has(> .entry__empty)`, margins dropped in the state | met | — |
| FR-002 | `.entry__empty-actions` five-column grid; `.entry__empty-btn` `aspect-ratio: 1` | met | — |
| FR-003 | `title` + `.sr` span in all three renderers | met | — |
| FR-004 | media glyph in `tatib.html`, `offline-render.js`, `entries.js` | met | — |
| FR-005 | `@container (max-width: 300px)` → `repeat(3, 52px)` | met | — |
| FR-006 | `offline-render.js::emptyAddButtons`, `entries.js::emptyAddButton` | partial | see G1 |
| FR-007 | all rules scoped to `.entry__empty`/`:has(.entry__empty)`; `/tatib/144/` measured identical | met | — |

## Gaps

**G1 — `partial`: FR-006's parity test cannot run end to end.** The saved row is verified on its own
(`test_empty_saved_tatib_shows_add_media_after_sidebar_navigation_offline`) and the tile content comparison
exists in `test_saved_render_parity.py`, but that test dies earlier — at its *song page* step — on unmodified
`develop` too (three runs of three). The saved renderer's tile markup is therefore verified, its box-for-box
parity is not. Not repairable inside this slice: the failing step is a Kidung page's `#readEyebrow`, which
this slice does not touch. Reported for the owner.

**G1 closed — 2026-10-25, on rebasing onto `develop`.** The branch now sits on `04b085a2` (spec 128, the hymn
separator), and `tests.e2e.test_saved_render_parity` runs green three times of three: the Kidung step that
failed here failed because of what 128 fixes, not because of this slice. FR-006 is therefore verified end to
end — the five tiles' labels, glyph counts and square sizes now compare saved-against-server and match. The
gap above is kept rather than rewritten: it was real when it was written, and it closed for a reason outside
this slice.

**G2 — `unrequested`: none.** The media glyph is the only addition the request did not name, and it is
recorded as an assumption in `spec.md`.

## Pass 2

No code changed in response to pass 1 except the test-side additions noted above (the rebuild assertions in
`test_editing_an_entry_and_deleting_it_after_a_confirmation`); pass 2 re-read the table and found no new gap.
Converged with G1 accepted as an open report, not a silent gap.

## Pass 3 — after gate 2, the owner's revision

The accepted placement (middle of the reading area, equal gaps) was replaced by the quarter mark: an
`unrequested` change had it stayed unrecorded, so it is recorded instead. Code (`grid-template-rows:
minmax(min-content, 50%)` with a 12px floor pad, replacing the flex centring), the E2E test, FR-001, SC-001,
US1, §UI/UX, `quickstart.md`, R6 and the changelog line moved together; the spec carries the delta as
Revision 1. Re-assessed after the change: no new gap, and the 1024×700 overlap that the first attempt
introduced was found and fixed in the same pass (12px clear instead of 12.7px over). Still converged with G1
accepted.
