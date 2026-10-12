# Spec 066: Always show a song entry's verses on the Tata Ibadah stage

- **ID:** 066
- **Status:** Draft
- **Item:** ITEM-069
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Every song entry on the Tata Ibadah stage states the verses it keeps, under its heading —
`Bait 1-3`, `Bait 1-7`, `Bait 1` — whether the operator kept all of the song's verses or only
some. Today the stage is silent on a full selection (spec 054), while the section sidebar
always shows the line (spec 057), so the operator reads the verses in one place and not the
other.

## Scope

### In scope

- The stage's `Bait …` line under a song entry's heading: shown whenever the entry keeps
  verses, for any song, hymn or not.

### Out of scope

- The sidebar's verse line (spec 057) — unchanged.
- The heading text (spec 054), the song label typography (spec 060), the preview modal, the
  projector screens, and every other entry kind.
- Legacy `TataIbadahItem` rows.

## Domain rules

- **The stage states the kept verses.** A song entry whose target exists and whose stored
  verses are not empty shows `Bait ` + `format_verses(stored verses)` under its heading. The
  comparison with the song's current verses (spec 054's partial-only rule) is removed.
  (Amends spec 054.)
- **The stage and the sidebar agree.** For the same entry, the stage line and the sidebar's
  second line carry the same string.
- **A deleted target shows no verse line.** When the song, its songbook, or an included verse
  is deleted, the existing deleted warning speaks instead (unchanged from spec 054).
- **No verses, no line.** An entry with an empty verse list shows nothing.

## UI details

- **Preview:** no new look. The line reuses spec 054's approved `.read__sub` element and style
  unchanged; this spec only widens when it appears. The owner OKed the change in chat on
  2026-10-12 from the live stage screenshot (songs listed without their `Bait …` line).
- **Element / position:** `<p class="read__sub">` directly under the entry's `h2.read__sec`
  heading, after the deleted warning slot, above any paragraphs — as today.
- **Text:** `Bait ` + the stored numbers in ascending order, runs of three or more collapsed
  (`Bait 1-3, 5, 6, 8-10`); pairs and singles stay comma-separated.
- **Size / spacing:** unchanged — `font: 560 12.5px/1.5 ui-sans-serif, system-ui, sans-serif`;
  `letter-spacing: .04em`; `margin: -2px 0 8px`. The entry box (spec 055, min-height 52px)
  grows by the line's height (~19px + margins) on song entries that previously showed none.
- **Colors / typography:** unchanged — `color: var(--head-ink)` in both themes.
- **States:** static — no hover, focus, or active styling of its own; the entry's hover fill and
  floating controls (specs 033, 034, 065) are unchanged.
- **Responsive behavior:** flows with the heading; no breakpoint changes.
- **Motion:** none.

## Acceptance scenarios

### Scenario: Full selection now shows its verses

- **Given** an entry for HAL 3 "Sai puji Naibata", whose song has verses 1-3, prepared with
  all three verses
- **Then** the stage shows `Bait 1-3` directly under the heading

### Scenario: Partial selection keeps its line

- **Given** the same song prepared with verses 1 and 3
- **Then** the stage shows `Bait 1, 3` under the heading

### Scenario: A single-verse, non-hymn song

- **Given** an entry for "Mars Sekolah GKPS" (not a hymn book) prepared with verse 1
- **Then** the stage shows `Bait 1` under the heading

### Scenario: Stage and sidebar agree

- **Given** a song entry prepared with verses 1, 2, 3, 5, 6, 8, 9, 10
- **Then** the stage line and the sidebar's second line both read `Bait 1-3, 5, 6, 8-10`

### Scenario: A deleted target

- **Given** a song entry whose included verse was deleted
- **Then** the deleted warning shows and no verse line appears on the stage

### Scenario: A verse added to the song after preparing

- **Given** an entry prepared with verses 1-3 of a three-verse song
- **When** verse 4 is added to the song
- **Then** the stage still shows `Bait 1-3` — the entry's own selection, not the song's

## Traceability

- Domain/app tests: `multimedia/web/tests.py` — the spec 054 stage verse-line tests
  (full selection now shows `Bait 1-3`; verse added after preparing; stage/sidebar agreement).
- E2E: `tests/e2e/test_entry_preview.py` (existing `.read__sub` assertion stays green).
- Implementation: `multimedia/web/reading/views.py` (`_tatib_stage`).
- Amends: spec 054 (partial-only verse line). Pairs with: spec 057 (sidebar verse line),
  spec 060 (song label typography).
