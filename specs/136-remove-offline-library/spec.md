# Feature Specification: Remove the offline library; the projector fetches on selection

**Slice**: `specs/136-remove-offline-library`
**Branch**: `feat/136-remove-offline-library`
**Created**: 2026-10-26
**Status**: Accepted (owner, 2026-10-26). Gate 1 accepted after Clarify retracted the carry-the-data
design in favour of fetch-on-selection, the page-memory index, and the blocking loading mode with its
two indicators; gate 2 accepted — "accept" — on the delivered slice's Converge and Fold report.
**Input**: "i wanna remove the offline library completely. the app no longer save local copies. for
projector's goto search, when returning search results, it has to carry along the data it is going
to display so that upon enter/selecting the search result item, the data is displayed instantly
without having to fetch the contents again."
**Input (revised by the owner during Clarify, 2026-10-26)**: "i think i will take that back. fetch
after selection. when the app is requesting the selected data: prevent any navigations, prevent
closing the goto popup, disable the search input and add loading indicator on the result selection.
restore again after the data is displayed. also, the navigation in library passage still valid. you
fetch the whole chapter when requesting a passage, and the whole songs when requesting a song.
navigating to the next chapter will make the same loading mode: all shortcuts are disabled, all
click are disabled and display a loading indicator to the left of keyboard icon."

## User Scenarios & Testing

### US1 — The app keeps no local copy of the library (P1)

**Why this priority**: this is the request's fixed point. Today the reading pages and the projector
keep a revisioned IndexedDB library (16.89 MB of chunks, measured) and a service worker holding two
page shells; a reading navigation paints the saved copy first and replaces it when the server's page
arrives, and the projector falls back to a saved service when its screens are missing. Every one of
those paths goes with the store.

**Independent Test**: browse the reading pages and the projector in a fresh profile, then inspect
the browser's storage: no service-worker registration, no cache entry, no `gkps-public-library`
database. The rail has no offline control, and every page is the server's.

**Acceptance scenarios**

1. **Given** a fresh browser profile **When** `/home/` opens and the reader moves through Alkitab,
   Kidung and Tata Ibadah **Then** the browser registers no service worker, holds no cache entry and
   creates no IndexedDB database.
2. **Given** the same session **When** any reading page opens **Then** it is painted from that
   navigation's own response, and no saved copy precedes it.
3. **Given** a reading page **When** the rail is inspected **Then** it carries no offline status
   button, and the offline panel is not in the document.
4. **Given** the projector page for a service **When** it opens **Then** its screens come from that
   response alone; no saved service is read and no library-change listener exists.
5. **Given** a projector page with no screens **When** it draws its empty state **Then** the copy
   promises no saved copy and no offline sync.

### US2 — Go To searches an index held in the page (P1)

**Why this priority**: the removed store is what answered the panel's lookup, and the operator
types into it between songs. A search that waits for the server on every pause would be a slower
panel than the one being replaced; the index measured for exactly this lookup is 126.4 KB raw,
29.4 KB gzipped — 0.75% of the library — and it carries no text, so it cannot paint anything.

**Independent Test**: open the projector, type in `G` while the network panel records requests: the
suggestion and `n / n` count change without a request per keystroke, and the projector made one
index request when it loaded.

**Acceptance scenarios**

1. **Given** the projector page **When** it loads **Then** it requests the Go To index once, and no
   other request is made by typing in the panel.
2. **Given** the index has arrived **When** a query is typed **Then** the suggestion row and the
   `n / n` count update as the query changes, with no request.
3. **Given** the page has just loaded **When** `G` is opened before the index arrives **Then** the
   panel is in its loading state — input disabled, suggestion replaced by a loading indicator — and
   it leaves that state when the index arrives.
4. **Given** a session **When** the index is inspected in browser storage **Then** nothing was
   written: the index lives in page memory only.
5. **Given** a song added to the database after the page loaded **When** `Update` re-reads the page
   **Then** the index is re-fetched and the new song is findable.

### US3 — Choosing a result fetches its whole chapter or song behind a loading mode (P1)

**Why this priority**: with nothing stored, the text must come from the server at the moment it is
chosen. The owner's rule is that the panel cannot be dodged while that happens — no navigation, no
close, no typing — and that it says it is working.

**Independent Test**: choose a passage row and a song row while throttling the network: the row
shows a loading indicator, the input is disabled, nothing in the page navigates, and the text
appears when the response lands.

**Acceptance scenarios**

1. **Given** a listed passage result **When** Enter (or a click on the row) chooses it **Then** the
   panel shows a loading indicator on that row, keeps the input disabled, refuses Escape and the
   dismiss overlay, and paints the passage when the chapter arrives.
2. **Given** a listed song result **When** it is chosen **Then** the same loading mode runs, and the
   whole song is painted — every bait's screens and its bait buttons — when the response lands.
3. **Given** a passage fetch **When** the chapter arrives **Then** the panel closes as it does today —
   its own close animation, then the page regains focus.
4. **Given** a fetch in flight **When** any key is pressed **Then** no shortcut fires: no
   next/previous entry, no bait step, no show/hide, no fullscreen, no `K`, no `J`, no `G`.
5. **Given** a fetch in flight **When** the mouse zones are clicked **Then** the screen does not
   change and fullscreen is not entered.
6. **Given** a passage fetch **When** both editions of the chapter are in hand **Then** the `T` flip
   repaints between them with no request.
7. **Given** a song fetch **When** bait keys or clicks are used **Then** every bait is already in
   hand and steps with no request.

### US4 — Chapter and book navigation inside a passage detour share the loading mode (P2)

**Why this priority**: the owner kept the detour's own navigation ("the navigation in library
passage still valid"). Verse steps inside a loaded chapter are local; a step that leaves the
chapter — next/previous chapter, or a book change — is a fetch, and it must look and lock the same
way as a selection.

**Independent Test**: open a passage detour, step to the chapter's last verse and one step further:
the corner cue shows a loading indicator to the left of the keyboard icon, every shortcut and click
is refused, and the next chapter paints when it arrives.

**Acceptance scenarios**

1. **Given** an open passage detour **When** an arrow steps a verse within the chapter **Then** the
   verse paints with no request and no loading state.
2. **Given** the detour's last verse of a chapter **When** the next-verse step is pressed **Then**
   the next chapter is fetched under the loading mode, and paints at its first available verse.
3. **Given** the detour's first verse **When** the previous-verse step is pressed **Then** the
   previous chapter is fetched under the loading mode and paints at its last verse.
4. **Given** the detour **When** Shift+arrow steps a chapter, or Ctrl+arrow steps a book **Then**
   each move is a fetch under the loading mode, opening at the chapter's first verse or the book's
   chapter 1.
5. **Given** Home or End with a modifier **When** it jumps to the first or last verse, chapter or
   book **Then** it fetches as the same loading mode and lands where it lands today.
6. **Given** the loading mode **When** it is showing **Then** the corner cue carries the indicator
   to the left of the keyboard icon, and it is gone once the chapter paints.

### US5 — Go To's lookup rules survive (P2)

**Why this priority**: `multimedia/web/reading/search.py`'s docstring freezes this matcher against
the public search page's grammar ("do not touch anything on goto"). Moving its data source from
IndexedDB to page memory is a change of source, not of behaviour.

**Independent Test**: for a fixture library, the same query list returns the same labels in the same
order as the current browser lookup.

**Acceptance scenarios**

1. **Given** a reference (`Mat 5:4`) or a chapter (`Mat 5`) **When** it is searched **Then** the row
   is the reference, labelled with the translation's book name and the verse.
2. **Given** a book abbreviation of either edition (`Kej`, `1Mu`) **When** it is searched **Then**
   the matching chapter rows list, one per edition, with the edition suffix when two rows share a
   label.
3. **Given** a songbook reference (`KJ 2`) **When** it is searched **Then** every song whose number
   starts with that run lists in number order.
4. **Given** a bare number (`012`) **When** it is searched **Then** exact numbers come first, then
   prefix matches, then substring matches, across every hymn book, with the same tie order as today
   (number, songbook, sub-number, title, id).
5. **Given** a title fragment (`Ada Kuasa`) **When** it is searched **Then** the best-scoring title
   matches list, capped at the same twelve rows.
6. **Given** a query that matches nothing **When** it is searched **Then** the row reads `No matching
   passage or song` and the count reads `0 / 0`.

### Edge Cases

- **When** the index request fails **Then** `G` opens in the loading state and the row reports that
  the search is unavailable; it never lists an index it does not have, and the page's `Update`
  re-fetches it.
- **When** a selection fetch fails **Then** the loading mode ends, the panel stays open with its
  rows, the row reads `Could not load — try again`, the field is usable again, and the corner
  spinner is gone; the operator can choose again or retype.
- **When** the query is empty or whitespace **Then** the panel reads `Start typing to find a match`
  and Enter does nothing.
- **When** a passage's verse is missing in one edition **Then** that edition is absent from the flip
  and the other edition paints.
- **When** a song has no verses **Then** its detour paints nothing new, as today.
- **When** the network is down before a reading navigation **Then** the browser's own error stands;
  no saved page is painted and no offline message replaces it.
- **When** the Update key is pressed **Then** the page is re-read from the server (`no-store`) and
  the index is re-fetched; no library sync runs.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Every reading page SHALL be painted from the response to its own navigation; no saved copy SHALL be painted first. | `reading/R2`, `reading/R3`, `reading/R5` (removed) |
| FR-002 | The browser SHALL hold no library copy: no service-worker registration, no Cache Storage entry and no IndexedDB database for the public library. | — (never folded: no `R<n>`) |
| FR-003 | The reading rail's offline status control, its panel and the reading stage's `Saved copy` label SHALL be removed from every reading page. | — (never folded: no `R<n>`) |
| FR-004 | `/offline/manifest/`, `/offline/chunk/<kind>/<pk>/`, `/offline/projector-shell/` and `/service-worker.js` SHALL answer 404. | — (never folded: no `R<n>`) |
| FR-005 | The projector SHALL fetch a Go To lookup index once when the page loads and hold it in page memory; no browser storage SHALL be written. | `new: projector` |
| FR-006 | The index SHALL carry what the lookup needs and nothing paintable: books with their names, aliases, editions and chapter lists, songbooks, and each song's number, sub-number, title and songbook. | `new: projector` |
| FR-007 | A Go To query SHALL be answered from the in-memory index, producing the same rows, labels and order as the current lookup. | `new: projector` |
| FR-008 | The Go To's matcher SHALL remain the current lookup's rules — references, book abbreviations of both editions, songbook numbers, numeric tiers and title matches — not the public search page's grammar. | `new: projector` |
| FR-009 | Choosing a result SHALL fetch the whole chapter (both editions) for a passage, or the whole song (screens and baits) for a song, and paint it when the response lands. | `new: projector` |
| FR-010 | While a selection or chapter fetch is in flight the panel SHALL hold a loading state: a loading indicator on the chosen row, the search input disabled, Escape and the dismiss overlay refused, every keyboard shortcut suppressed and every click refused. | `new: projector` |
| FR-011 | Verse stepping inside the loaded chapter SHALL be local; a step that leaves the chapter (next/previous chapter, or a book change) SHALL fetch under the same loading mode, with its indicator to the left of the keyboard icon in the corner cue. | `new: projector` |
| FR-012 | The projector page SHALL render from its own response alone: no saved-service fallback, no library-change listener, and an empty state that names no saved copy. | `new: projector` |

### Key Entities

- **Go To index** — the page-memory payload: `books` (id, name, editions with version, translation
  name, abbreviation and chapter list), `songbooks` (id, name, short name, hymn flag) and `songs`
  (id, number, sub-number, title, songbook id). No verse text and no lyric.
- **Go To result** — one row the panel lists: `kind` (`passage` or `song`), `label`, and the target
  (`book_id`/`chapter`/`verse`/`edition`, or `song_id`).
- **Chapter payload** — `book_id`, `chapter`, the translation labels, and both editions' verses
  (number, title, text) in order; the reference label per verse.
- **Song payload** — `label`, `screens` (each with `bait`, `split`, `split_total`, lines) and
  `baits` (`number`, `start`, `end`).
- **Offline library** — retired: the browser database, the two page shells, the status control and
  their routes. Nothing replaces it.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A browsing session leaves nothing stored | `navigator.serviceWorker.getRegistrations()` empty, `caches.keys()` empty, `indexedDB.databases()` names no `gkps-public-library` |
| SC-002 | Search costs one request per page load, not per query | the request list stays unchanged while typing ten queries after the index has loaded |
| SC-003 | The Go To lists what it lists today | for a fixed query list, every label, its order and the row count equal the pre-change lookup's |
| SC-004 | The removed routes are gone | the four paths answer 404 |
| SC-005 | The index is small | the payload is ≤ 130 KB raw / ≤ 30 KB gzipped for this database |
| SC-006 | Selection is locked while it loads | during a throttled fetch, no key or click changes the screen, the panel stays open, and the row and corner cue show their indicators |
| SC-007 | A reading navigation is one request and one paint | one document request per navigation, and the stage's content arrives with it |

## UI/UX

Static previews at `specs/136-remove-offline-library/preview/`, each built from the pages this
worktree's own server serves: `after.html` (the reading shell without the offline control) and four
projector states — `projector-index-loading.html`, `projector-selection-loading.html`,
`projector-selection-error.html`, `projector-chapter-loading.html`. Measured at **1440×900**, and at
**390×844** where noted.

- **Layout / position**: the reading rail's foot loses one button and keeps its stack — the theme
  button stays where it was, the transfer button stays hidden. The Go To panel does not move: at
  `left: 32px; bottom: 58px`, **396px** wide (its 400px cap less two 2px borders) and **149.4px**
  tall, its one suggestion row **30.75px**. The row's spinner sits at the row's right end, in the
  count's slot; the corner spinner sits **8px** left of the shortcuts button (`right: 74px` = 32px
  page inset + 34px button + 8px gap), its vertical centre level with the button's (delta **0px**).
- **Size / spacing**: rail foot **96px → 44px** at 1440×900 (three foot buttons → two, one hidden),
  and **40px** at 390×844. Row spinner **12×12px**, 2px border; corner spinner **14×14px**, 2px
  border. The count is hidden while the row loads, so the suggestion's start does not move. The
  spinner's layout box stays 12px; its bounding box reads up to ~16.4px mid-rotation, which is the
  square turning, not a size change.
- **Colour / typography**: unchanged — the panel's 11px type, `--on` text and `--quiet` count; the
  spinners take the projector's own quiet pair, `--whisper` (#6E6A62) track and `--quiet` (#8E8A80)
  head. A disabled field keeps its colours, with `cursor: not-allowed`.
- **States**: **loading** — index (`Loading search…`, field locked, row spinner), selection (query
  and row shown, field locked, row spinner, corner spinner), chapter crossing (panel closed, corner
  spinner only); **error** — the panel keeps its rows, the row reads `Could not load — try again`,
  the field is usable and the corner spinner is gone; **empty** — the panel's existing `No matching
  passage or song`; **hover / focus / disabled** — the row's, field's and button's existing rules are
  untouched.
- **Motion**: the spinners turn `800ms linear infinite`; under `prefers-reduced-motion: reduce` they
  do not turn (`animation-name: none`, verified in a reduced-motion context).
- **Responsive**: at 390×844 the Go To panel is **326px** wide (its `calc(100vw - 64px)` cap), the
  shortcuts button stays at `right: 32px`, and the corner spinner keeps its 8px gap and its centre;
  the reading rail foot stays one visible button.

## Assumptions

- **"Completely" is the whole feature** — library script, status control and panel, `offline.css`,
  the service worker, the four routes, the saved-copy paint, the offline tests and ADR 0003
  (recorded as superseded, not deleted).
- **The index is page memory, not storage** — it is fetched with the page and re-fetched by
  `Update`; a song added while the page is open is not findable until then.
- **The matcher moves source, not rules** — `projector-library.js`'s lookup logic is kept; only
  `load()` changes, from IndexedDB to the fetched index.
- **A selection always fetches**, even a passage the operator saw a moment ago; nothing is cached
  between selections.
- **No replacement for the removed fallback** — the app is online-only, and a network failure is
  the browser's to report.
- **The projector's live paths are untouched** — reflow, service adoption, the display channel, the
  entry list and the find panel's visuals keep their behaviour.
- **The reading page's in-page navigation keeps everything else** — history, focus restoration,
  scroll position and the search snapshot — and only its saved-copy branch is removed. That
  behaviour was never folded into an `R<n>`, so it is protected here rather than in the tree.
- **The offline feature never entered the capability tree** (the tree starts at spec 126), so its
  removal cites no `R<n>`; `docs/spec/reading.md`'s R2, R5 and R3's saved-copy scenario are the only
  entries it removes. The Go To's new requirements open a `projector` capability, because the
  behaviour area is not reading.
- **Bump is declared in the plan**, not here.

## Clarifications

### Session 2026-10-26

- Q: How much passage data should each result carry? → SKIPPED as a design point, then **retracted
  by the owner**: "i think i will take that back. fetch after selection."
- Q: What does the fetch block, and what shows while it runs? → A: every navigation is prevented,
  the Go To cannot close, the search input is disabled, and a loading indicator sits on the chosen
  row; the state restores once the content is displayed. A chapter change inside a passage detour
  uses the same mode, with the indicator to the left of the keyboard icon (owner).
- Q: How much content does a selection fetch? → A: the whole chapter for a passage (both editions)
  and the whole song for a song (owner); the detour's verse/bait navigation stays valid.
- Q: When is the search request made? → SKIPPED in favour of a local index, then decided: the index
  is fetched when the projector page opens, and while it loads the Go To is in the same loading
  state (owner).
- Q: How large is that index? → A: measured on this database — 126.4 KB raw / 29.4 KB gzipped
  (66 books with chapter lists 15.4 KB, 1,843 songs 110.3 KB, 13 songbooks 0.8 KB); it carries no
  text, so selecting still fetches (agent, owner asked).
