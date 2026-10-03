---
id: ITEM-005
status: in-review
title: 'Public site revamp'
type: chore
priority: P1
effort: L
created: 2026-10-01
updated: 2026-10-03
spec: ../specs/004-public-site-revamp/spec.md
branch: feat/004-public-site-revamp
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/261
archived_at:
archive_reason:
bump: minor
release_version: 0.8.0
---

# ITEM-005: Public site revamp

## Summary

Rebuild the public site to the accepted **search-first** design: a narrow icon rail as the
primary navigation (logo, Search / Alkitab / Kidung / Tata Ibadah, theme toggle), a home
page whose centered logo and search field lead a **full-corpus search** (Bible, Kidung,
Tata Ibadah), and a reading stage for all three corpora — with an AA-safe palette in light
and dark, English chrome with Indonesian domain terms and date locale, and print that
yields reading content only.

This refreshes the earlier draft: the top-toolbar + morphing-rail design and the "Bible and
Tata Ibadah render as Coming soon" decision are **superseded** by the accepted mockup, which
reads all three corpora. The scope now includes the new public reading views for Bible and
Tata Ibadah and for search.

## Notes

- **Prototype of record (local, not committed):**
  `scratch/revamp-mockup/index-search-indonesian-terms.html`, runnable with its
  `bible-data.js`, `kidung-data.js`, `tatib-data.js`, and `gkps.png` sidecars (a second
  copy lives at `~/.hermes/cache/scratch/rail/`). Where the written spec and the mockup
  disagree, the mockup wins. **Do not delete it until the implementation is verified
  pixel-perfect against it.**
- The mockup was exercised by browser-check suites — search, rail, reader, Tata Ibadah
  modes, sidebar restoration, highlight exclusivity (47 scenarios) plus width checks at
  320–1440 — and the E2E scenarios in the spec are derived from those checks.
- The spec's palette was re-measured from the mockup values: every text pair ≥ 4.5:1 and
  every UI/focus pair ≥ 3:1 in both modes (worst text pair 5.57:1).
- **JavaScript is in scope per owner decision.** The shell (rail, nested sidebars, search
  behaviors, theme) needs runtime state; content stays server-rendered and the enhancement
  degrades rather than gates.
- **UI language:** English chrome; Indonesian terms (*Alkitab*, *Kidung*, *Tata Ibadah*,
  *Perjanjian Lama/Baru*) and Indonesian dates/months (`23 Agu 2026`, `Agustus 2026`).
  Other languages deferred to a later concern.
- No web fonts, no framework: system serif/sans stacks, hand-written CSS, inline SVG icons.
- Search behaviors pinned: references rank first (`Matius 5:13`, `Kidung Jemaat 120` ≡
  `KJ 120`), **any non-empty query searches** — the 3-letter minimum and its inline message
  were dropped in the review round and only an empty submit is inert — the rail search icon
  keeps the last result set (the logo starts fresh), and its current indication is exclusive
  to closed sidebars.
- Shell behaviors pinned (review round): navigation swaps the affected regions in place under
  one URL (the address bar never changes), sidebar picks never scroll their lists (clipped
  rows are nudged only; reveals may centre), and non-hymn song lists carry the *recently
  updated* ↔ *alphabetical* sort backed by `Song.modified` (migration 0012).
- Reveal behaviors pinned (review round 2): a search result and a sidebar opened on the page
  being read both centre the panel tile **and** the list row — for every section, animated —
  with Tata Ibadah contents rows flashed instead of selected; the last result set survives
  sidebar browsing and resumes its scroll offset.
- One concern: this is one spec (004).

## Acceptance sketch

- Search-first home: centered 96px logo and 56px field (610px column), rail present, Search
  as the current destination before any search.
- Search spans Bible (books, references, verse text), Kidung (songbooks, titles, lyrics),
  and Tata Ibadah (titles, public contents); grouped results with counts and excerpts;
  "Show more"; empty state.
- References resolve exactly and rank first; full songbook names and abbreviations are
  interchangeable; matching is case- and diacritic-insensitive.
- Short queries are refused with a visible, announced message and change nothing else.
- Opening a result reads it in the stage; the rail search icon returns to the same result
  set afterwards, from reading or from any sidebar browsing; the logo resets to landing.
- Nested sidebars: parent-first open/close; Bible mini collapse keeps chapters usable;
  Kidung swaps in the wide song list above 1272px; Tata Ibadah groups by year+month with a
  Templates view and unselected quicklinks; restoring from closed navigation or a section
  switch rebuilds from the content on stage.
- Reading: Bible chapters with verse numbers and TB/SIM toggle; songs with numbered
  stanzas; service orders with speaker marks and a date-only eyebrow.
- English chrome + Indonesian terms; Indonesian dates/months.
- Dark mode by rail toggle, persisted, applied before first paint; AA in both modes.
- Print shows reading content only; no horizontal scroll at 320px; rail narrows at 560px.

## Links

- Spec: [../specs/004-public-site-revamp/spec.md](../specs/004-public-site-revamp/spec.md)
- Related items: [ITEM-001](./ITEM-001-public-songs-reading.md) (design foundation),
  [ITEM-004](./ITEM-004-maintenance-page.md) (maintenance page)
