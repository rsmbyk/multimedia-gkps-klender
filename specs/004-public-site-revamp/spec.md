# Spec: Public site revamp

- **ID:** 004
- **Status:** Accepted
- **Item:** ITEM-005
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Rebuild the public site to the accepted **search-first** design: a narrow icon rail as the
primary navigation, a search-led home page that searches the whole corpus, and a reading
stage for Bible, Kidung (songbooks), and Tata Ibadah — keeping the palette and contrast
discipline (WCAG AA in light and dark) the revamp started from.

The accepted prototype of record is the local mockup
`scratch/revamp-mockup/index-search-indonesian-terms.html` (not committed; runs with its
`bible-data.js`, `kidung-data.js`, `tatib-data.js`, and `gkps.png` sidecars alongside). It
is the parity reference — **do not delete it until the implementation is verified
pixel-perfect against it**. This spec describes the shipped result it stands for: where
this text and the mockup disagree, **the mockup wins** and this text is corrected.

This **supersedes the earlier draft** (top toolbar + morphing labelled rail + "Coming soon"
Bible/Tata Ibadah entries). Nothing from that direction ships.

## Decisions confirmed by the owner

1. **JavaScript is allowed and expected** for the shell — the rail, nested sidebars, search
   behavior, and theme all need runtime state. Reading content stays server-rendered; the
   shell's enhancement degrades (pages, links, and the search form still work) rather than
   gates.
2. **Bible and Tata Ibadah become full public reading destinations.** The earlier "Coming
   soon" treatment is retired; the accepted mockup reads all three corpora, so this spec
   ships it — including the new public routes for Bible and Tata Ibadah reading and for
   search.
3. **UI language: English chrome, Indonesian domain vocabulary.** Interface copy is English;
   the terms *Alkitab*, *Kidung*, *Tata Ibadah*, *Perjanjian Lama*, *Perjanjian Baru*, and
   all content data stay Indonesian, and dates/months use the Indonesian locale
   (`23 Agu 2026`, `Agustus 2026`). Other languages are a later, separate concern.
4. **No web fonts and no frontend framework.** System stacks only — serif:
   `ui-serif, Georgia, "Times New Roman", serif`; sans: the system UI stack. Hand-written
   CSS, inline SVG icons, no CDN. *(Supersedes the earlier self-hosted Source Serif 4
   decision — the accepted mockup ships without web fonts.)*
5. **The search-first home replaces the old banner home**, and the rail's search icon is a
   **destination** (it keeps the last result set), not a panel.

## Scope

### In scope

- `static/styles/design/tokens.css` + `static/styles/design/components.css` rebuilt to the
  mockup's palette, metrics, and states (tables below), AA in light **and** dark, with a
  contrast regression test.
- **Icon rail as primary navigation** (80px wide; 64px at ≤560px): logo at top, destinations
  in the middle — Search, Alkitab, Kidung, Tata Ibadah — theme toggle at the bottom; hover
  and keyboard-focus tooltips; visible focus rings in both modes.
- **Nested push sidebars**, one column pair shared by the three sections:
  - **Alkitab** — books panel (Old/New Testament groups) + chapters rail; the books panel
    can collapse to a rail-width **mini** strip while the chapter tiles stay usable.
  - **Kidung** — songbook panel + a **wide song list** pane; below 1272px the song list
    replaces the songbook panel.
  - **Tata Ibadah** — service list grouped by year+month, newest first, with a **Templates**
    view for null-dated services; contents rail whose items are **quicklinks**.
  - Opening/closing pushes the reading stage with one shared duration/easing curve;
    panels clip-wipe rather than fade.
- **Search-first home**: centered logo (96px) and search field (56px) on a 610px column;
  landing and results states; a hint line with example queries.
- **Full-corpus search** across Bible (book names/aliases, chapter:verse references, verse
  text), Kidung (songbooks, song titles, lyrics), and Tata Ibadah (service titles, public
  contents): grouped results (Bible, Kidung, Tata Ibadah in that order), per-group counts,
  text excerpts, "Show more"; any non-empty query searches; results open in the reading stage.
- **Reading stage for the three corpora** — Bible chapters with verse numbers and the
  TB/SIM translation toggle; hymn lyrics with numbered stanzas; Tata Ibadah services as
  ordered items (speaker marks L./P./J.; end-of-section notes rendered quietly).
- **Dark mode** via the rail toggle, persisted in `localStorage`, applied before first
  paint.
- **Print**: reading content only.
- New reading views/URLs for Bible and Tata Ibadah reading and for search.
- Tests: token contrast (light/dark), reading + search view tests, E2E for the shell,
  search, and reading flows.

### Out of scope

- OBS surfaces, the public APIs, the editor under `/manage/`, bookmarks.
- Model/data changes beyond `Song.modified` (kept on the model, but no longer the sort
  key -- see the correction below) (migration 0012, added in the review round so
  non-hymn song lists can sort by recency): reading renders the existing `bible.*`,
  `songs.*`, `tatib.*` data.
- The maintenance page (spec 003) — standalone, unchanged.
- Migrating the Fomantic editor surfaces; any third-party frontend dependency.
- Languages beyond English chrome + Indonesian terms/locale (deferred).

## Domain rules

- **The palette is fixed by the accepted mockup** (values below, both modes). Contrast is a
  rule, not a preference: text pairs ≥4.5:1, UI/focus pairs ≥3:1 — re-measured on the
  mockup values (ink/canvas 15.16, head-ink/canvas 5.57, active pair 7.94, tip pair 16.51,
  icon/rail 13.27, focus/canvas 7.29 light; 16.76 / 6.59 / 6.53 / 15.34 / 13.02 / 6.97 dark)
  and kept true by a test.

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--canvas` | `#F7F5F1` | `#14130F` | reading surface |
| `--rail-bg` | `#EDEAE3` | `#232019` | rail and panel surface |
| `--ink` | `#1F1F1D` | `#F5F3EE` | primary text |
| `--head-ink` | `#646357` | `#9C9A91` | meta, group heads, excerpts |
| `--icon` | `#222220` | `#E8E6E0` | rail icons |
| `--active-bg` | `#1C5C3C` | `#7C9CF0` | current/highlight fill |
| `--active-ink` | `#FFFFFF` | `#0D1838` | text/icon on the fill |
| `--divider` | `#D9D6CD` | `#3A362F` | hairlines |
| `--tip-bg` | `#1F1F1D` | `#EDEBE5` | tooltip surface |
| `--tip-ink` | `#FFFFFF` | `#16150F` | tooltip text |
| `--focus` | `#1C5C3C` | `#7C9CF0` | focus rings |

- **The metrics are fixed by the mockup.** Rail 80px (64px ≤560px; rail button 44px→40px,
  logo 40px→34px); books/service panel `18.5rem`; song list `min(26rem, …)`; chapters and
  mini panels are rail-width; search column 610px (field 56px, logo 96px); results 690px.
  Breakpoints: **1272px** (song list replaces the songbook panel), **720px** (panels become
  floating overlays, stage full width), **560px** (rail narrows), **480px** (type/gutter
  trims). Body serif `1.06–1.18rem/1.78`; verse numbers sans 11px tabular in the gutter.
- **The rail is a page margin, not a control panel.** No badge counts, item counts, or
  account block; no shadowed nav rows. The current destination is a filled rail button
  (44px, radius 8, `--active-bg`/`--active-ink`); icons carry `data-tip` tooltips (hover
  after a delay, instantly on focus) and real accessible names.
- **UI copy: English chrome, Indonesian terms.** Pinned strings from the mockup:
  tooltips *Search / Alkitab / Kidung / Tata Ibadah*; theme *Switch to dark mode* ↔
  *Switch to light mode*; search label *Search Alkitab, Kidung, and Tata Ibadah*; placeholder
  *Search Alkitab, Kidung, Tata Ibadah...*; hint *Try Matius 5:13, KJ 152, or pengampunan
  dosa*; status *Results for “q”* /
  *No results for “q”. Try another keyword.*; count *N result(s)*; *Show more*; filters
  *Filter books... / Filter songbooks... / Filter Tata Ibadah... / Filter songs... /
  Filter sections...*; empties *No matching books / songbooks / Tata Ibadah / songs /
  sections.*;
  testament heads *Perjanjian Lama / Perjanjian Baru*; template head *Templates*; mode
  button *Show Tata Ibadah templates* ↔ *Show dated Tata Ibadah*; reader editions *TB* and
  *SIM*; song-list sort control *Sort: by number — switch to alphabetical* ↔
  *Sort: alphabetical — switch to by number* (non-hymn songbooks only; see the
  correction at the end of this document).
- **Search covers the whole corpus.** Bible: every book name and alias, `Book chapter:verse`
  references (ranges included), and verse text (both translations, one hit per verse). Kidung:
  every songbook full name and abbreviation, song titles, and lyric text. Tata Ibadah:
  service titles and public contents — private end-of-section notes are never indexed.
- **References rank first.** `Matius 5:13` (aliases like `Mat`) returns the exact reference
  as the first Bible row and opens straight to the verse. **Song references accept the full
  songbook name and the abbreviation interchangeably** — `Kidung Jemaat 120` and `KJ 120`
  resolve to the same song at the same rank — and matching is case- and diacritic-insensitive
  for all references.
- **Any non-empty query searches.** The owner's review round supersedes the mockup's
  3-letter minimum (and its inline message): a short or punctuation-only query runs like any
  other. An **empty** submission is inert — with results on stage it restores the last result
  set, on the landing it stays on the landing — and there is no `aria-invalid` state or
  validation message anywhere.
- **The search icon and the brand logo are one route** (owner request, supersedes the
  mockup's logo-starts-a-fresh-search). Activating either restores the last result set — the
  query, the rows including those revealed with "Show more", and the **scroll offset** it was
  left at — from the landing page, a reading page, or after browsing the sidebars; with
  nothing stored yet, or with a stored value that is not a result-set URL, it shows the empty
  landing instead. Only the result page itself updates that memory: a reading page reached
  through a sidebar never overwrites it, and nothing clears it. The landing therefore exists
  before the first search of a session.
- **The search indication is exclusive.** The rail Search button is `aria-current` only
  while the search stage is showing **and both sidebar levels are closed**; opening any
  section clears it, closing returns it, and reading keeps it off.
- **There is no back-to-results button.** The rail's Search icon is the return path from
  the reading stage.
- **The shell is one page.** Every pick — a rail destination, a sidebar row (book, chapter,
  song, service, template mode), a search submit, a result open, *Show more* — swaps the
  affected regions in place with the same transitions, so **the address bar never changes**
  and deep links exist only when the server renders them on a direct load. Switching sections
  leaves the reading stage intact; returning to a section rebuilds its lists from it.
- **Sidebar picks do not scroll their lists.** Clicking a fully visible row moves nothing; a
  row clipped at an edge is nudged only enough to become fully visible, never recentred.
- **Reveals centre, and they travel.** In the two reveal cases — opening a search result, or
  opening a sidebar on the page being read — the rows that identify what is on stage are
  centred: the panel tile (book, songbook, service) **and** the list row (chapter, song,
  contents item). The travel is a short eased tween (≈120–180 ms, the shell's easing, so the
  rows just before the target are seen moving past; reduced motion jumps), with a reflow pass
  after the sidebar's push transition that snaps when the correction is under ~48 px and
  travels only when it is larger. Every corpus behaves the same: Tata Ibadah's service row is
  centred like a book or songbook, and the contents row — a quicklink that is never selected —
  is **flashed** (the tint holds half of a 2.6 s animation) so the item in view is
  identifiable.
- **Search and filter fields carry a clear control.** Every search/filter input (the global
  search, the panel filter, the list filter) has a small × at its right edge, shown only while
  the field holds something; activating it empties the field, re-runs what the field drives
  (the filter re-applies, the result set stays), and leaves focus in the field. Its accessible
  name names what it clears, derived from the field's own label (*Clear books*, *Clear
  songbooks*, *Clear songs*, *Clear Tata Ibadah*, *Clear search*).
- **Song lists sort by recency or alphabetically.** A non-hymn songbook (`is_hymn_book`
  false) shows a sort control in the chapters toolbar — *by number* (default: the file's own
  order, number then sub-number then title) ↔ *alphabetical*, whose key drops a title's own
  leading `435. ` — applied in place without a reload. Hymn
  songbooks keep their number order and hide the control.
- **Nested sidebars are parent-first.** A click on a closed or mini section expands the
  parent panel; a click on the open parent closes it and its child; on narrow screens the
  parent trades away the child to keep one usable list, and on wide screens both stay
  visible. Alkitab's inner grip owns the mini collapse and keeps its chapter tiles usable
  beside the mini strip. Tata Ibadah contents items are **quicklinks** — never persistently
  selected.
- **Restoration is content-based.** Reopening a section from fully closed navigation, or
  switching back to it from another section, rebuilds its sidebar from the content on the
  reading stage — book + chapter, songbook + song, or service (including its dated/template
  mode, revealed before the row is looked up). A stale sidebar filter that hides the
  restored row is cleared; the restored row is scrolled into view inside its own panel;
  on narrow screens focus moves to the visible child.
- **Tata Ibadah grouping.** Dated services group by year **and** month, newest first; null
  dates are the *Templates* view; switching modes clears the list filter and re-marks only
  a visible selection.
- **Eyebrows.** A Tata Ibadah service shows **only its date** above the title (styled
  uppercase, e.g. `23 AGU 2026`); a template service shows *Tata Ibadah*. A song shows its
  citation (*Kidung Jemaat 120*). Bible reading shows no eyebrow.
- **Dark mode** follows the system by default, is overridden by the rail toggle, persists in
  `localStorage` (`gkps-*` keys), and is applied before first paint — no flash of the wrong
  theme. Storage access is wrapped so blocked storage cannot throw.
- **Print stays usable.** Printing shows the reading content only — rail, panels, search
  home, translation toggle, and result controls are all absent, for all three corpora.
- **Motion is one object.** Panel push/clip-wipe, stage margin, and tooltips share the single
  `--ease` duration/curve; `prefers-reduced-motion` collapses durations without changing
  behavior (including the close-all path).
- **Server-rendered floor.** With JavaScript unavailable, pages still render content and
  working links, and the search field submits as a normal GET form.
- **Keyboard support.** Escape closes the innermost open layer; focus returns to the trigger
  that opened it; every control has a visible focus ring (including dark mode); tooltips
  appear on focus without hover.
- **No horizontal scrolling** at 320px; layout verified at 320 / 390 / 720 / 721 / 1272 /
  1273 / 1440.
- **Parity with the mockup.** The shipped result reproduces the mockup's structure, states,
  metrics, and copy; the mockup file is the tie-breaker for anything this spec does not
  pin, and its browser-check suite is re-run against the implementation before review,
  with the key views compared pixel-for-pixel at fixed viewports. Any deliberate deviation
  is written down at handoff. **Owner-requested deviations from the mockup (review round,
  2026-10-03):** (1) the mockup's 3-letter minimum and its inline validation message are
  **not** ported — any non-empty query searches; (2) a sidebar click no longer recentres the
  row (it moves a list only to un-clip a row, and centres only in the two reveal cases); the
  mockup's own single-document navigation is now matched by the implementation (one page, no
  address changes); (3) the sort pair originally read *recently updated* /*alphabetical*, which
  could not work on the real corpus (every song imports with one `modified` timestamp, so all
  rows tied and the toggle looked inert) — **corrected in review** to *by number* /
  *alphabetical*, which differ on every songbook; the mockup's own control is unchanged and
  still matches (3) ~~the mockup's *recently updated* sort needs real timestamps —
  `Song.modified` supplies them, and until the first edits land the default order matches
  alphabetical for untouched rows; (4) the collapse control's window glyph is replaced by a
  **double chevron** (`«`), with single chevron and chevron-plus-bar shown as alternatives.

## Acceptance scenarios

### Scenario: Search-first home renders

- **Given** a first visit with no search made
- **When** the home page loads at desktop width
- **Then** the logo (96px) and the search field (56px) sit centered in a 610px column, with
  the example-query hint beneath
- **And** the rail is present with Search / Alkitab / Kidung / Tata Ibadah and the theme
  toggle
- **And** the Search rail button is the current destination

### Scenario: Search spans the whole corpus

- **Given** the corpus is populated
- **When** I search “kasih”
- **Then** results are grouped under **Alkitab**, **Kidung**, and **Tata Ibadah** headings,
  each with a count, title, meta, and text excerpt
- **And** every group can reveal more rows with *Show more*
- **And** a search matching nothing shows *No results for “q”. Try another keyword.*

### Scenario: Bible references resolve exactly

- **Given** Bible text exists
- **When** I search `Matius 5:13`
- **Then** the exact reference is the first Bible row
- **And** activating it opens Matius chapter 5 in the reading stage with verse 13 marked

### Scenario: Song references accept number and full name

- **Given** a numbered songbook (e.g. Kidung Jemaat)
- **When** I search `KJ 120` and separately `Kidung Jemaat 120` (any casing)
- **Then** both queries return the same song as the same first row
- **And** activating it opens that song in the reading stage

### Scenario: Every non-empty query searches

- **Given** I type a short query (e.g. `kj`, `di`) or a punctuation-only one
- **When** I submit
- **Then** results for that query are shown — no minimum length, no invalid state, no message
- **And** submitting an **empty** field is inert: the last result set stays on stage (from the
  landing, the landing stays)

### Scenario: Search keeps its last result set

- **Given** a completed search with results revealed
- **When** I open a result and read, browse a section sidebar, or open another menu, and
  then activate the rail's Search destination
- **Then** the same query and the same result rows (including revealed extras) are shown
  again
- **And** the offset inside the result set is resumed, so the reader continues where they
  left off
- **And** leaving through the logo behaves identically — with no stored result set both land
  on the empty landing page

### Scenario: The shell never leaves the page

- **Given** any stage (landing, results, a reading page)
- **When** I pick a book, chapter, song, service, or search result, or open/close a sidebar
  destination, or press *Show more*
- **Then** the shell swaps the affected regions in place with its normal transitions and the
  **address bar does not change**
- **And** switching sections leaves the reading stage intact, and returning rebuilds that
  section's lists from the page being read

### Scenario: Reveals centre what is on stage

- **Given** the reader is on a page — a chapter, a song, or a Tata Ibadah service (with or
  without an item it was opened at)
- **When** they open the section sidebar, or open a search result
- **Then** the panel tile and the list row that identify that content are centred in their
  scrollports (clamped only at a list's edge), the travel is animated so the rows before the
  target are seen, and a Tata Ibadah contents row is flashed rather than selected
- **And** the same holds for every section, whether the row is already on screen or not

### Scenario: Sidebar picks never scroll the lists

- **Given** an open sidebar list
- **When** I click a row that is already fully visible
- **Then** the list does not scroll at all
- **And** a row clipped at an edge is nudged just enough to become fully visible, never
  recentred
- **And** only the two reveal cases may scroll a list — opening the sidebar on the page being
  read, or opening a search result — and those centre the row (see the reveal scenario above)

### Scenario: Song lists sort by recency or alphabetically

- **Given** a non-hymn songbook whose songs carry `modified` stamps
- **Then** a sort control offers *by number* (default) ↔ *alphabetical* and re-orders
  the list in place
- **And** hymn songbooks keep number order and show no sort control

### Scenario: Search indication is exclusive

- **Given** the search stage is showing
- **When** I open any section sidebar
- **Then** the Search button loses its current state, and regains it when both sidebar
  levels close
- **And** while reading an opened result, the Search button is not current

### Scenario: Alkitab sidebars behave parent-first

- **Given** a reading page
- **When** I open Alkitab
- **Then** the books panel opens beside the rail; choosing a book opens its chapters
- **And** the book panel's inner grip collapses it to a mini strip while the chapters stay
  usable, and expanding restores both
- **And** clicking the open Alkitab rail button closes panel and chapters together

### Scenario: Kidung swaps the song list in at wide widths

- **Given** a viewport wider than 1272px
- **When** I open a songbook
- **Then** the song list appears as a wide pane and the songbook panel stays visible
- **And** below 1272px the song list replaces the songbook panel instead

### Scenario: Tata Ibadah groups, modes, and quicklinks

- **Given** dated and null-dated services exist
- **When** I open Tata Ibadah
- **Then** dated services are grouped by year and month, newest first, and the mode button
  switches to the *Templates* view and back
- **And** tapping a contents item jumps to it without marking the quicklink selected
- **And** opening a service shows its ordered items, with end-of-section notes rendered
  quietly

### Scenario: Sidebar paths restore from the stage

- **Given** a book, song, or service is on the reading stage
- **When** I fully close its sidebar and reopen it — or switch to another section and back —
- **Then** the sidebar rebuilds from the displayed content: the same book/chapter,
  songbook/song, or service (in its correct dated/template mode) is revealed and scrolled
  into view, without rerendering the stage
- **And** a stale filter hiding the restored row is cleared

### Scenario: UI language and date locale

- **Given** any public page
- **When** I read its chrome
- **Then** interface copy is English
- **And** the domain terms are Indonesian — rail tooltips *Alkitab / Kidung / Tata Ibadah*,
  search groups *Alkitab / Kidung / Tata Ibadah*, testament heads *Perjanjian Lama /
  Perjanjian Baru*
- **And** dates and months render in the Indonesian locale (*23 Agu 2026*, *Agustus 2026*)

### Scenario: Reading stage for each corpus

- **Given** each corpus has content
- **When** I open a Bible chapter, a song, and a service order
- **Then** the chapter shows verse numbers and the TB/SIM toggle works
- **And** the song shows numbered stanzas with book citation as its eyebrow
- **And** the service shows its ordered items with speaker marks, dated eyebrow only, and
  template services show *Tata Ibadah* instead of a date

### Scenario: Dark mode persists before paint

- **Given** I choose dark mode from the rail
- **When** I reload any public page
- **Then** the dark palette is applied before first paint with no light flash
- **And** every token pair still meets AA in dark mode
- **And** a storage-blocked browser still works, losing only persistence

### Scenario: Printing yields reading content only

- **Given** a Bible chapter, a song, or a service order is displayed
- **When** the print stylesheet applies
- **Then** only the reading content prints — rail, panels, search home, translation toggle,
  and result controls are absent

### Scenario: Layout holds across viewports

- **Given** viewports of 320, 390, 720, 721, 1272, 1273, and 1440px
- **When** I browse the home, search results, and each reading page
- **Then** nothing overflows horizontally at any width
- **And** the rail narrows (80px → 64px) at 560px, panels become overlays at 720px, and the
  song list swaps in above 1272px

### Scenario: Keyboard and assistive affordances

- **Given** keyboard-only use
- **When** I traverse the shell
- **Then** every control has a visible focus ring in light and dark
- **And** tooltips appear on focus; Escape closes the innermost layer and focus returns to
  its trigger
- **And** `aria-current`, `aria-expanded`, `aria-invalid`, and `aria-describedby` track the
  states above

### Scenario: Motion is opt-out

- **Given** my system requests reduced motion
- **When** I open sidebars, search, or switch theme
- **Then** state changes still happen, with effectively instant transitions

### Scenario: Existing behavior is unchanged

- **Given** specs 001 and 003 are implemented
- **When** their acceptance scenarios run
- **Then** they still pass — the song reading URLs and accessible names keep working, and
  the maintenance page still renders standalone

## Traceability

- Domain/app tests: `tests/test_design_tokens.py` (contrast pairs, light + dark);
  `tests/test_web_search.py` (query rules, reference ranking, any-non-empty queries);
  `multimedia/web/tests.py` (reading views updated)
- E2E: `tests/e2e/test_reading.py` extended — search-first home, grouped results, reference
  resolution, in-place shell navigation, sidebar click scroll rules, the song sort control,
  short-query search, keep-last-results, nested rail open/close/restore, reading flows, dark
  mode, print, no overflow at 320/1440
- Implementation: `multimedia/web/reading/` (views + urls: search, bible, tatib);
  `multimedia/web/templates/reading/` (base, home, search, bible, book_index, book, song,
  tatib, maintenance); `static/styles/design/{tokens,components}.css`;
  `static/web/reading.js` (new)
- Parity (local, 2026-10-03): the mockup's full browser-check suite re-run against the
  implementation — **122/122 green** (geometry, copy, behavior, widths 320–1440, plus the
  review-round checks: in-place navigation under one URL, section switches preserving the
  reading stage, sidebar picks not scrolling their lists, short queries searching) — plus a
  segmented pixel comparison at 1440: home and results byte-identical; bible, song, and
  tatib and song byte-identical below the toolbar band, bible within 0.0026 there (a scroll
  indicator left by the reveal path), whose only toolbar difference is the collapse glyph
  glyph (band 0.0092 — the named deviation). **Owner-requested deviations:** (round 3) the
  mockup's logo starts a fresh search, here the logo takes the same route as the search icon;
  (round 5) the clear control inside search and filter fields, which the mockup does not have.
  Deliberate deviations are listed above and in the pull request.
