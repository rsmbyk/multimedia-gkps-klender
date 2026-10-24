# Research: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md` · **Plan**: `specs/126-songbook-short-header/plan.md`

Phase 0. Every unknown in Technical Context is resolved here; **zero `NEEDS CLARIFICATION` remain**.

## D001 — Where the reference is computed: the view, not the model

**Decision**: build the citation in `SongDetailView.get_context_data`
(`multimedia/web/reading/views.py`), with the fallback inline:

```python
if book.is_hymn_book:
    reference = book.short_name or book.name
    citation = (f'{reference} {song.number}{song.sub_number.upper()}'
                if song.number is not None else reference)
else:
    citation = book.name
```

**Rationale**: the citation is a display string for one surface, and the view is the only place that knows
which surface is being rendered (the tab title and the header both come from it; the sidebar already has its
own `book_number` column). The change stays inside the function it replaces.

**Alternatives considered**:

- *Extend `Song.book_number`* — rejected: it is a model property shared with the sidebar rows, `__str__` and
  `Verse.song_name`, and it has no fallback today. Changing it would move every song reference in the app,
  which is more than this slice asks for.
- *Add `Book.reference` / a template tag* — rejected: one call site, and a second abstraction with a single
  consumer is the kind of indirection this codebase avoids.
- *Do it in the template* — rejected: the view already computes `citation` and hands it to both
  `read_eyebrow` and `page_title`; splitting it across the template and the view would leave the tab title
  computing its own version.

## D002 — The saved renderer keeps its own copy of the rule

**Decision**: change `static/web/offline-render.js` `songPage()` the same way, rather than having the saved
page read the server's header.

**Rationale**: this is how spec 122 fixed saved/server parity — two renderers, one rule, compared by a
regression. A saved page is built from the synced library with no request, so it cannot read the server's
header without defeating the point of the saved copy.

**Alternative considered**: *drop the saved renderer's eyebrow and let the online update fill it in* —
rejected: the saved page is the final page when offline, and spec 122 made the saved page carry every label
the server does.

## D003 — The tab title follows the citation because it already shares it

**Decision**: no separate change; `page_title = f'{citation} — GKPS Klender'` picks up the new reference.

**Rationale**: the owner's Clarify answer — the tab names the song the way the page does. Making the tab keep
the full name would mean keeping a second variable in the view purely to disagree with the header beside it.

## D004 — No CSS or template change

**Decision**: none. `.read__eyebrow` already applies `text-transform: uppercase`, so the marked-up text can be
`PKJ 4` and render `PKJ 4`. `base.html` writes the value it is given.

**Rationale**: measured on the running page — the computed `text-transform` is `uppercase` and the element's
type is unchanged (16.5px / 600 / 1.65 / 1.98px). The only visual delta is the string's length and, at narrow
widths, the line count.

## D005 — An unnumbered hymn song shows the reference alone

**Decision**: a hymn book's song with `number is None` gets `short_name or name`, with no trailing number.

**Rationale**: the code already had no number branch (it fell back to the full name); the header should still
name the songbook the way the header does everywhere. The alternative — the full name for exactly this case —
would put two spellings of one songbook on the same page again.

## D006 — Which tests pin it, and what must not break

**Decision**: unit pins in `multimedia/web/tests.py::ReadingViewTests` (the header text for a hymn song, the
blank-short-name fallback, an ordinary songbook carrying a short name, and the tab title) and E2E pins in
`tests/e2e/test_saved_render_parity.py` (the saved hymn paragraph case in the existing per-route table, and
server-vs-saved equality of the header and the title).

**Rationale**: the existing `test_song_detail_shows_lyrics_and_citation` asserts `assertContains('NKB 12')`,
which passes today from the *sidebar row* and would pass after the change from the header — it cannot tell
the difference, so it is not a pin for this rule. The new unit tests assert the paragraph itself.

**Checked and unaffected** (read, not assumed): `test_tatib_date_header_matches_songbook_header` compares
computed styles, not text; `test_saved_documents_use_route_specific_labels_and_markup` expects
`Ordinary Test` from an ordinary book whose `short_name` is `OT` — which is exactly FR-006's rule; the
Bible and Tata Ibadah eyebrows are different code paths and are untouched.

## Evidence gathered

- Live library: the four hymn songbooks carry `HAL`, `KJ`, `NKB`, `PKJ`; every ordinary songbook has an empty
  `short_name` (13 rows, read from the local database).
- The song page's second sidebar already prints `song.book_number` (`PKJ 1`, `PKJ 2`, `PKJ 3`, `PKJ 4`),
  so the header is the only place on that screen with the long name.
- Measured header boxes and the saved/server agreement are recorded in `preview/README.md`.
