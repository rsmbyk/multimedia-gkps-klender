# Research — remove the offline library; the projector fetches on selection

**Slice**: `specs/136-remove-offline-library` · **Date**: 2026-10-26

Every decision below is reachable from the spec's requirements and the owner's answers at Clarify.
Measurements were taken on this machine's compose database (`multimedia`, 66 books × 2 editions) and
the running app on loopback.

## D1 — What "the offline library" is, and every surface it touches

**Decision.** The removal covers the IndexedDB store (`gkps-public-library`), the service worker and
its two page shells, four routes, three scripts, one stylesheet, the rail's status control and
panel, the reading stage's `Saved copy` label, the projector's saved-service fallback, the offline
tests, and ADR 0003 (superseded, not deleted).

**Rationale.** The store is only useful with all of them: a service worker left in place keeps
caching static assets ("no local copies" would be false), the panel and button would report a
library that no longer exists, and the saved-copy paint is the store's only consumer in the reading
path. Removing the store and leaving its UI is a page promising something it cannot do.

**Alternatives.** Keep the service worker for asset caching (rejected: still writes browser storage,
and the owner's request is that the app save nothing); keep the panel as a "download" control
(rejected: nothing to download).

**Provenance.** Code: `static/web/offline-library.js`, `offline-status.js`, `offline-render.js`,
`service-worker.js`, `static/styles/design/offline.css`, `multimedia/web/reading/offline.py`,
`multimedia/urls.py:23-26`, `base.html` (rail button, panel, saved label, three scripts),
`projector.html` (library script), `projector.js` (`reflow`, empty state, `offline:changed`).
Measured: the whole stored library is **16.89 MB** across 215 chunks — bible 11.63 MB, songs
1.47 MB, services 3.78 MB.

## D2 — The Go To lookup stays in the browser, fed by a fetched index

**Decision.** `projector-library.js` keeps its `lookup()` rules and receives its data from a new
index endpoint fetched once when the page loads, held in page memory. No server-side search.

**Rationale.** `multimedia/web/reading/search.py`'s docstring freezes this matcher against the public
page's grammar ("do not touch anything on goto"), and its rules — book aliases, both editions'
abbreviations, chapter prefixes, songbook numbers, numeric tiers, title scoring — are already
implemented and tested in the browser. Re-implementing them server-side would be a second matcher
to keep in step, and a request per typing pause replaces an instant panel.

**Alternatives.** Server search per keystroke, debounced (rejected by the owner in favour of the
index); persisting the index in IndexedDB (rejected: a local copy again); carrying display data with
each result (retracted by the owner: "i think i will take that back. fetch after selection.").

**Provenance.** Code: `static/web/projector-library.js:119-180` (lookup), `search.py:11-13`.
Owner: Clarify, 2026-10-26.

## D3 — The index carries no text, and is exact

**Decision.** The index is `{books: [{id, name, editions: [{v, name, abbr, verses: [count per
chapter]}]}], songbooks: [...], songs: [{id, n, s, t, book_id}]}` — no verse text, no lyric.

**Rationale.** Measured on this database: **126.4 KB raw / 29.4 KB gzipped** (books 15.8 KB, 1,843
songs 110.3 KB, 13 songbooks 0.8 KB). The verse-count array preserves the lookup's exact behaviour —
`passageMatches` only offers a chapter or verse that exists — without storing text, because every
chapter in both editions is contiguous from verse 1 and every book's chapter list is contiguous from
1 (measured: 2,378 chapter-edition pairs, **0** gaps in either direction). `firstVerse` therefore
equals 1, and "does this verse exist" is `1 ≤ v ≤ verses[chapter-1]`.

**Alternatives.** Chapter numbers only (rejected: cannot answer the verse-existence check the lookup
performs, so `Mat 5:999` would list a row the old code refuses); per-verse numbers (rejected: ~62k
ints, and the contiguity measurement makes them redundant).

**Provenance.** Measurement (agent, 2026-10-26); code `projector-library.js:79-113, 212-240`.

## D4 — A selection fetches the whole chapter (both editions) or the whole song

**Decision.** Two content endpoints: a chapter by book and number, carrying both editions' verses;
a song by id, carrying screens and baits.

**Rationale.** The owner's rule: "you fetch the whole chapter when requesting a passage, and the
whole songs when requesting a song", and "the navigation in library passage still valid". A chapter
in hand makes verse steps local and the `T` flip instant; a song in hand makes bait steps local. The
payload is bounded: median **7.4 KB** per chapter both editions, worst **30 KB** (Psalms 119), and a
song's screens are its own lyrics (largest songbook chunk 470 KB for the whole book).

**Alternatives.** One verse per request (rejected: a held arrow becomes ~30 requests/s); the whole
book (rejected: 86 KB median, 743 KB worst, for data most of which is never painted).

**Provenance.** Owner: Clarify, 2026-10-26. Measurement: chapter sizes from the compose database.

## D5 — The loading mode is one flag plus two indicators

**Decision.** A single `gotoBusy` state in `projector.js`, entered by a selection fetch or by a step
that leaves the loaded chapter. While set: the find input is disabled, the chosen row carries a
spinner in place of its count, a spinner appears 8px left of the shortcuts button, the keydown
handler returns early, and click handlers on the mouse zones, cue, dismiss overlay and rows return.

**Rationale.** The owner enumerated the lock ("prevent any navigations, prevent closing the goto
popup, disable the search input"), and one flag is the only way the enumeration stays true when a
new shortcut is added later: the guard sits at the top of the handlers rather than in each branch.
The indicators reuse the app's spinner idiom (`.editor__loading-spinner`: 2px border, 800ms linear,
off under reduced motion) rather than inventing a new one.

**Alternatives.** Disabling controls individually (rejected: a new control would miss the guard);
a blocking overlay (rejected: the owner asked for an indicator, not a modal).

**Provenance.** Owner: Clarify, 2026-10-26. Code: `components.css:670-686` (spinner idiom),
`projector.js:1135` (keydown), `:898-908` (mouse zones), `:1027-1050` (detour).

## D6 — Failure is reported in the panel's own slots

**Decision.** An index failure leaves the panel in its loading state with the row saying the search
is unavailable; a content failure ends the lock, re-enables the field, and puts `Could not load —
try again` in the suggestion slot. Neither adds a control.

**Rationale.** The panel already has one text slot for "nothing to show" (`No matching passage or
song`) and one for "start typing"; a third state belongs there rather than in a dialog or a toast.
`Update` re-fetches the page and the index, which is the recovery path for the index case.

**Alternatives.** A retry button (rejected: a control the request never asked for); silent restore
(rejected: a failed fetch would look like a no-op on a projection surface).

**Provenance.** Code: `projector.js:981-998` (painting the row), preview
`preview/projector-selection-error.html`.

## D7 — The reading path loses its saved-copy branch, nothing else

**Decision.** `reading.js`'s `navigate()` keeps `fromServer()` as its only paint path; the
`GKPSOfflineRender` branch, the direct-boot hydration and the offline failure message are removed.

**Rationale.** The saved-copy paint exists only because the library holds a page; with no library the
branch has no input. History, focus restoration, scroll anchoring and the search snapshot do not
depend on it and stay.

**Alternatives.** Keep `offline-render.js` for a first paint from a cached page (rejected: that is
the local copy being removed).

**Provenance.** Code: `reading.js:1361-1470` (navigate), `:1969-1980` (hydration), `:2066-2070`.

## D8 — The offline tests and their cards

**Decision.** `tests/test_offline_sync.py` and `tests/e2e/test_offline_library.py` are deleted; the
offline cases inside `test_navigation_freshness.py`, `test_projector.py`, `test_pdf_display.py`,
`test_powerpoint_display.py` and `test_saved_render_parity.py` are deleted or rewritten to the
surviving behaviour. Card ITEM-139 (offline projector E2E errors) is retired by the removal.

**Rationale.** Those tests pin behaviour the spec removes; a rewritten test would assert the
opposite of what it was written for. The tests that assert *freshness* survive without their library
setup — they are about the server's answer, which is now the only answer.

**Provenance.** Code: the five test modules, grepped for `offline` (53 references in
`test_projector.py` alone).

## D9 — Version level

**Decision.** `bump: minor`.

**Rationale.** A user-facing capability is removed and a new one (server-fetched Go To content with
a blocking load) replaces part of it. It is not a fix (`patch`) and it breaks no published API
(`major`): the REST API is untouched and the product has no external consumers.

**Alternatives.** `patch` (understates a removed capability), `major` (overstates: no external API
contract breaks; the product is a congregation tool at 1.20.x).

**Provenance.** Neighbouring packs take `patch` for presentation work; this slice changes what the
product can do.

## Unknowns

None. Sizes, contiguity, latency and every removed site were measured or read; the two open
questions were closed at Clarify.
