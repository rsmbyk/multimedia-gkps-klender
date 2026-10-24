# Research: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`
**Unknowns remaining**: 0

## D001 — Where the fault lives

- **Decision**: the saved renderer decides the sort control from the section alone, while the server
  decides it from the book. `static/web/offline-render.js` `songPage()` calls
  `common(doc, 'kidung', …, songListOpen = true)` (line 448), and `common()` then sets
  `#songSort.hidden = section !== 'kidung' || !songListOpen` (line 328).
- **Rationale**: reproduced on a local server against the real corpus (develop plus this draft). With the
  library synced, opening NKB's first song from the sidebar paints the saved page first: frame sampling on
  `requestAnimationFrame` records the control visible from 3130 ms to 3350 ms after the click — 220 ms at
  38 × 38 px, with `#songFilter` narrowing 339 px → 293 px — and then the online refresh applies the server
  page and hides it, returning the field to 339 px. The same comparison run as a document diff
  (`GKPSOfflineRender.render(url)` versus a `no-store` fetch of the same route) reports the mismatch on
  every hymn song of every hymn book in the library — `/songs/1/`, `/songs/508/`, `/songs/1010/`,
  `/songs/1390/` — and no mismatch on the ordinary songbooks' song pages.
- **Alternatives considered**: a fault in `reading.js`'s swap (rejected — the swap copies the arriving
  document's `hidden` value faithfully, so it faithfully reproduces the wrong document); a stale service
  worker (rejected — the JS on disk is what the page runs, and the diff is computed from
  `GKPSOfflineRender.render()` directly).
- **Provenance**: research

## D002 — Which rule the control follows

- **Decision**: the book's hymn flag — `!book.is_hymn_book` — passed as `common()`'s `songListOpen`.
- **Rationale**: that is exactly the server's rule (`multimedia/web/reading/views.py:1820`,
  `show_song_sort = not book.is_hymn_book`), pinned by spec 011 and by `multimedia/web/tests.py`
  (`test_book_detail_lists_its_songs`, `test_non_hymn_book_offers_the_sort_toggle`). The same function
  already reads `book.is_hymn_book` for the citation and the row numbers, so the value is in hand; and
  `listPage()` — the songbook list route — already applies the same rule through
  `selected.is_hymn_book`, which is why the book routes do not mismatch.
- **Alternatives considered**: (a) making the saved renderer offer no sort control at all — it would break
  ordinary songbooks, where the server does offer it; (b) changing the server to offer the control for
  hymn books — it would contradict spec 011 and reverse an accepted behaviour to fix a renderer; (c) hiding
  the control in the swap instead — it would hide the symptom after the wrong frame has already painted.
- **Provenance**: research

## D003 — How the regression keeps the class covered

- **Decision**: add the control's `hidden` state to the fields the saved-parity class compares, and add a
  frame-sampling test for the transient itself.
- **Rationale**: the existing class compares labels, headings, references, rows, eyebrow and stage bodies
  between the saved and server documents, but not this control — which is why spec 122's sweep did not
  catch it. Comparing the value rather than the pixel fixes the class; sampling frames is the only way to
  pin "it never appears", because the defect is a transient between two correct-looking ends.
- **Alternatives considered**: a screenshot-diff test — brittle across fonts and platforms, and the repo has
  no such harness; asserting only the final state — it would pass today, since the flash ends hidden.
- **Provenance**: research

## D004 — The second difference found, deliberately out of scope

- **Decision**: the `/songs/` songbook-list saved page omits the disabled "+ Add song" button that the
  server page renders; this slice does not fix it.
- **Rationale**: measured in the same document diff (`chAdd: saved=false server=true`). It is a different
  control on a different route, it is only visible while editors are enabled, and it is not the reported
  defect. Recorded here so it can become its own card rather than ride along unannounced.
- **Alternatives considered**: folding it into this slice — it would grow the plan's traceability with a
  control no acceptance scenario mentions, and the two changes would ship as one diff with two causes.
- **Provenance**: research

## Open

<!-- empty: Phase 0 finished -->
