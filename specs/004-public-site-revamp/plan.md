# Plan 004: Public site revamp

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-005
- **Bump:** minor

## Why

The public site currently stops at songs. The accepted direction — captured end-to-end as a
local mockup (`scratch/revamp-mockup/index-search-indonesian-terms.html`) — is
**search-first**: a narrow icon rail, a home page that searches the whole corpus, and a
reading stage for Bible, Kidung, and Tata Ibadah. This plan replaces the earlier draft
(top toolbar + morphing labelled rail + "Coming soon" entries) with that accepted design.

The revamp also finishes the palette work the earlier draft started. Measured against WCAG
AA, the spec 001 palette **fails in five places**:

| Pair | Ratio | Need |
| --- | --- | --- |
| White on `--gkps-green` (primary button) | 2.79 | 4.5 |
| White on `--green-600` (button hover) | 4.09 | 4.5 |
| `--muted` on `--bg` | 4.04 | 4.5 |
| `--muted` on `--surface` | 4.30 | 4.5 |
| `--gkps-green` verse numbers on surface | 2.79 | 4.5 |

The mockup's replacement palette was re-measured for this draft — every text pair ≥ 4.5:1
and every UI/focus pair ≥ 3:1 in **both** light and dark (worst text pair 5.57:1; the
active-fill pair 7.94 light / 6.53 dark) — and the token values are pinned in the spec, so
parity with the mockup and AA hold together.

## Scope / edges

**In:**

- Rebuild `static/styles/design/tokens.css` + `components.css` to the mockup palette and
  metrics, with a contrast regression test keeping both modes AA.
- **Icon rail as primary navigation** (80px; 64px ≤560px): logo, Search / Alkitab / Kidung /
  Tata Ibadah destinations, theme toggle, tooltips with real accessible names.
- **Nested push sidebars** shared across sections — books+chapters (with mini collapse),
  songbooks + wide song list (panel swap below 1272px), Tata Ibadah year+month groups with
  a Templates view and quicklink contents — with one shared duration/easing curve.
- **Search-first home** (96px logo, 56px field, 610px column) and **full-corpus search**
  across Bible (books, references, verse text), Kidung (songbooks, titles, lyrics), and
  Tata Ibadah (titles, public contents) with grouped results and "Show more".
- **Search as a destination**: the rail icon keeps the last result set within the session;
  the logo starts fresh; the current indication is exclusive to closed sidebars.
- **Public reading for the three corpora** — Bible chapters with TB/SIM toggle; songs with
  stanza numbering; Tata Ibadah service orders with quiet end-of-section notes. This
  supersedes the "Bible/Tata Ibadah have no public route" boundary: **new reading views and
  URLs are in scope** (search, bible, tatib), rendering the existing models.
- **Dark mode** (rail toggle, `localStorage`, pre-paint) and **print** (reading content
  only).
- Tests: token contrast; search/reading view tests; E2E for shell, search, reading.

**Out:**

- OBS surfaces, public APIs, the editor (`/manage/`), bookmarks. The existing spec 001/003
  suites must keep passing; the maintenance page is untouched.
- Model/data changes — the views render existing `bible.*`, `songs.*`, `tatib.*` rows.
- The prototype's `*-data.js` sidecars: those are mockup scaffolding; production reads the
  database.
- Fomantic editor surfaces; any framework, font CDN, or third-party request.
- Languages beyond English chrome + Indonesian terms/locale.

**Edges:** TB/SIM affects Bible search-open behavior (open in the current translation unless
the hit came from the other one); the rail is fixed and panels overlay the stage on phones,
so the stage must keep a usable measure at 320px; storage may be blocked (persistence is
the only loss).

## Approach

1. **Tokens first.** Port the mockup's pinned values; write the contrast test first and
   keep it green through both modes.
2. **One shell, one state machine.** The mockup drives everything from `data-*` state
   (`nav` closed/open/mini, `ch` closed/open, `read` on/off, `home` landing/results,
   `section`, `theme`); the production JS keeps that model so the shell behaves as one
   object and every transition has a single source of truth.
3. **Panels push, they don't float (on desktop).** Panel widths are tokens; the stage
   margin and the second column derive from them, so open/close is one coordinated motion.
   Clip-wipe for the wipe; overlay + scrim-free floating panels ≤720px.
4. **Search is server-side, ranked, grouped.** One search view over the three apps' models
   (Postgres full-text where available; ILIKE fallback otherwise), with the mockup's ranking
   rules: exact references and exact titles first, then title matches, then meta, then body
   (lyrics/verses), deduplicated per verse; results grouped Bible → Kidung → Tata Ibadah.
   The reference parser accepts book aliases, `Kidung Jemaat 120`-style full songbook names,
   and case/diacritic-insensitive input; the minimum length rule lives here too.
5. **Reading stage parity.** Chapter/song/service rendering matches the mockup: verse
   numbers, stanza numbers, speaker marks, date-only service eyebrow, citation eyebrow for
   songs, quiet EOS notes. Search targets (a verse, an item) are marked and scrolled into
   view after the panel push settles.
6. **Restoration rules stay.** Reopen from closed navigation or section switch rebuilds the
   sidebar from the stage content (mode-aware for Tata Ibadah), clears a hiding filter, and
   returns focus sensibly on narrow screens.
7. **Language and copy are pinned.** English chrome, Indonesian terms, Indonesian dates —
   the spec's copy table is the checklist; get it from the mockup, not from translation
   instinct.
8. **Dark mode + pre-paint** exactly as the earlier draft described: inline restore script,
   `gkps-*` keys, wrapped storage access.
9. **Build against the mockup, then verify against it.** The mockup's behavior was exercised
   by a browser-check suite (search, sidebar restoration, Tata Ibadah modes, highlight
   exclusivity, 47 scenarios, plus width checks at 320–1440); the implementation's E2E
   scenarios are derived from those checks; before review that same check suite is re-run
   against the implementation as a parity harness — a check that passes on the mockup must
   pass on the shipped site, or the difference is written down. So "the same as the
   mockup" is testable, not a vibe.

## TDD

- Domain/app tests: `tests/test_design_tokens.py` (new — contrast pairs, light + dark);
  `tests/test_web_search.py` (new — reference parsing incl. full songbook names, ranking,
  minimum length); `multimedia/web/tests.py` (updated — new reading views).
- E2E: `tests/e2e/test_reading.py` extended — search-first home, results grouping,
  reference resolution, validation, keep-last-results, sidebar open/close/restore, dark
  mode, print, no overflow.
- Existing `multimedia.web` suite stays green, unchanged in intent; maintenance test kept.

## Risks

- **Scope includes new public views** (bible, tatib, search) — larger than the previous
  draft. Kept in 004 as one concern: the new public site experience. If the reading views
  prove separable, they can split into their own spec before implementation.
- **Search quality across three corpora.** Ranking must reproduce the mockup's feel
  (references first, right-book-first for full names). Unit tests pin the ranking rules;
  the reference parser gets table-driven cases (`KJ 120` ≡ `Kidung Jemaat 120`).
- **Parity drift.** The mockup is the reference; any deliberate deviation must be listed at
  handoff, or the next iteration reintroduces it as a "bug".
- **E2E selector churn.** Accessible names and roles must be preserved while markup changes;
  the E2E suite is updated with the shell, not after it.
- **JS size/complexity.** One `reading.js` carries the shell; keep it state-machine-first
  and dependency-free (no jQuery/RxJS in the public shell — those stay legacy helpers).
