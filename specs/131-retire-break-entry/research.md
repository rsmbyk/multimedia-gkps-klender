# Research: The Break kind retires, and the breaks already written stay

**Spec**: `specs/131-retire-break-entry/spec.md`

## D001 — The retirement lives in the form map, not in a new branch in the views

**Decision**: remove `'section_break'` from `FORMS`, `KINDS` and `TITLES` in
`multimedia/web/reading/entries.py`, and delete `SectionBreakEntryForm`. Every endpoint that accepts a kind —
the new-entry form, the edit form, the save-new endpoint, the save endpoint — already asks
`build_entry_form()` and answers `Http404('Unknown kind.')` when it gets `None`.

**Rationale**: one map decides what a kind means for writing; the kind is not in it, so nothing can write
one, from any endpoint, with no new condition to keep in step. The `404` is the response an unknown kind has
always produced, and the browser's existing failure handling (a non-OK response → the entry toast) already
covers a stale page.

**Alternatives considered**: (a) an explicit `410 Gone` / `403` branch in `entry_save` — rejected: it writes
the retirement twice (map and view), invents endpoint semantics no client consumes, and would need its own
test to prove it agrees with the map; (b) delete `ServiceEntryKind.SECTION_BREAK` — rejected: existing rows
store `3`, and `kind_name()` and every renderer read the enum (FR-010).

**Provenance**: `multimedia/web/reading/entries.py:18-24` (`KINDS`), `:89-93` (`SectionBreakEntryForm`),
`:187-199` (`FORMS`, `TITLES`), `multimedia/web/reading/views.py:280-306` (`entry_form`),
`:461-474` (`entry_save`, `form is None → Http404`) on `3a360d06`.

## D002 — Each of the three creation surfaces is edited where it lives

**Decision**: the server template, the in-place rebuild and the saved renderer each drop `section_break` from
their own list, and `entries.js` also loses `addBreak()` and its special case in the click handler.

**Rationale**: the three lists are in different layers — a Django template, the reading-shell script, the
saved-page renderer — with no module system between them (no build step; `entries.js` and `offline-render.js`
are separate IIFEs loaded per page). A shared constant would need either a template tag or a global, which is
more machinery than four strings, and the repo's own convention for this trio (spec 130) is to keep the same
markup in all three and check parity in a test.

**Alternatives considered**: (a) a `window.GKPS_ENTRY_KINDS` global — rejected: a new global for four labels,
and the cached-page problem it does not solve (an old cached `entries.js` still has its own list); (b) dropping
the buttons in CSS — rejected: a hidden control is still a control, and it would leave the dead `addBreak`
handler reachable by keyboard/AT.

**Provenance**: `multimedia/web/templates/reading/tatib.html:105-109,178-184,191-209`,
`static/web/entries.js:60-75,144-148,936-948,955-966`, `static/web/offline-render.js:123-148` on `3a360d06`.

## D003 — The empty tile row loses a track with the kind

**Decision**: `.entry__empty-actions` becomes `repeat(4, minmax(0, 52px))`; the narrow-container fallback stays
`repeat(3, 52px)`.

**Rationale**: measured on the branch — the row is a five-track grid (`repeat(5, …)`), so removing one button
leaves an empty fifth track and the four survivors sit 26px left of centre (row 300px wide, tiles 238px
worth). Dropping the track keeps the row centred on the same axis (measured: centre 1176px before and after)
and makes the four-tile row 238px. The container fallback still gives 3 + 1 at 52px, all above the 44px floor.

**Alternatives considered**: `repeat(auto-fit, minmax(0, 52px))` — rejected: on a wide column it would spread
the tiles apart instead of keeping the fixed 10px gap spec 130 approved; a flex row — rejected: the same
measurement would have to be re-derived and the narrow rule re-tested for no gain.

**Provenance**: `static/styles/design/components.css:2219-2234`; probe run at 1440×900 on this branch
(`preview/probe_break_controls.py`).

## D004 — The stored kind and its rows stay; the retirement needs no migration

**Decision**: no model, migration, serializer or renderer change. `ServiceEntryKind.SECTION_BREAK` stays, the
rows stay, and the rendering paths (`views.py` divider block, `_projector_data`, `_toc.html`, `search.py`'s
exclusion, `resolve()`) stay exactly as they are.

**Rationale**: the request retires the *action*, not the data. Every read path already handles the kind
independently of the form map; keeping them untouched is what makes "still view/delete" true without a second
piece of work, and it makes the decision reversible by restoring one map entry.

**Alternatives considered**: a data migration converting stored breaks to blank lines or divider text —
rejected: it would rewrite the operator's past services (and blank lines are projection pauses, not dividers),
which the request explicitly forbids.

**Provenance**: `multimedia/tatib/models.py:89-94,214`; `multimedia/web/reading/views.py:1005-1013`,
`:1192-1194`; `multimedia/web/templates/reading/_toc.html:2-16`; `multimedia/web/reading/search.py:651`.

## D005 — Deletion and reorder are kept, and proven, not touched

**Decision**: add a test that deletes an existing Break from the stage and leaves the delete and reorder paths
untouched.

**Rationale**: the owner's report of being unable to delete was a network fault on the operator's side —
reproduced on the branch, the flow is: hover → Delete → confirm → `POST /editor/entry/<pk>/delete/` → `200` →
row removed and order compacted. Since the request names deletion as the thing that must keep working, the
slice carries the proof rather than a repair, and the existing drag test (`test_reorder.py`) still covers
reorder.

**Alternatives considered**: rebuilding the delete control around the row's 56px box so the divider cannot
move on hover — rejected: that is spec 036/037/052's reveal behaviour for every entry, unchanged by this
slice, and changing it would be an undeclared UI change inside a retirement.

**Provenance**: probe run on the branch at 1440×900 (`POST /editor/entry/18/delete/ → 200`, 7 → 6 dividers);
`tests/e2e/test_reorder.py:263`; `static/web/entries.js:801-870`.

## D006 — The tests that asserted the kind is creatable are replaced, not deleted

**Decision**: `test_creating_a_section_break_without_a_label`, `test_an_instant_break_lands_after_its_add_row…`
and `test_an_instant_break_without_a_position_goes_to_the_end` become refusal tests;
`test_plus_break_adds_the_break_at_once_without_a_dialog` becomes "no Break control is offered"; the label
list in `tests/e2e/test_entries.py` and the opener in `tests/e2e/test_edit_request_feedback.py` are pointed at
the remaining kinds.

**Rationale**: TDD-07 allows deleting a test only when the behaviour is gone — here it is gone by request, so
each test keeps its subject (the kind's write path, the add row's contents) and asserts the retirement
instead of the removed behaviour. Nothing is dropped without its replacement.

**Provenance**: `multimedia/web/tests.py:1237-1240,2064-2084`; `tests/e2e/test_tatib_section_break.py:98-108`;
`tests/e2e/test_entries.py:413`; `tests/e2e/test_edit_request_feedback.py:150`.
