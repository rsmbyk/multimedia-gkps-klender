# Research: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md`
**Date**: 2026-11-23

| # | Decision | Evidence |
| --- | --- | --- |
| D001 | The gate belongs in `reading/song.html`, not in CSS or JavaScript. | `song.html:45-47` wraps `.verse-add` in `{% if can_edit_verses %}`; `:48-50` separately wraps the invitation in `{% if not verse_rows and can_edit_verses %}`. The server already knows `verse_rows` (`views.py:2426,2446`). |
| D002 | The invitation keeps its button; the after-the-last-verse row is the one hidden. | The request names the row "after the last verse" — with no verses there is no last verse. The invitation's copy already says "Add the first verse". Live measurement shows both buttons are byte-identical, so only the container distinguishes them. |
| D003 | The row's gate is `verse_rows and can_edit_verses` — one condition, not two nested blocks. | `verse_rows` is the view's `is_deleted=False` list, so soft-deleted-only songs read as empty; `can_edit_verses` still keeps hymn and restricted pages clear. |
| D004 | Regression coverage is a targeted Django template test in the existing `multimedia/web/reading/test_verses.py`, not a new browser suite. | The requirement is server-rendered markup; the module already owns the song-page verse rules. The owner asks for targeted verification between push steps. |
| D005 | The visual comparison comes from a static page rebuilt from the live pages' real markup; the current and with-verses routes give the live readouts. | `preview/build.py` captures both route bodies; a `file://` page cannot exercise `{% if %}`, so the live route and `probe.py` carry that evidence. |
| D006 | Bump `patch`: 1.36.9 → 1.36.10; Fold modifies `reading/R40` in place, adds no new requirement. | `VERSION` and `origin/develop` both read 1.36.9; `docs/spec/reading.md` ends at R52, and R40 already owns "one add control after the last verse". The behaviour narrows, it does not add a capability. |
| D007 | Card `ITEM-239` is anchored on issue #590 and moves to `Ready` at gate 1. | Board part: `Ready` is gate 1; the tracker mirror creates the issue on entering that column. Owner accepted gate 1 on 2026-11-23. |

| D008 | The song empty state reuses the Tata Ibadah quarter-band layout, with `padding-top: 0` rather than its 12px floor. | A live CSS probe at 1440×900 put the song title at y=262.9 with 12px, y=255.8 with 2.6px and y=253.9 with 0, against the Tata Ibadah reference y=253.5; at 900×700 the gap is 0.4px, at 390×844 5.5px from the longer wrapped song title. The owner chose to add this as US2 in the same slice on 2026-11-23. |

**Unknowns remaining: 0.**
