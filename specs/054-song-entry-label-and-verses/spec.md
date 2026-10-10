# Spec 054: Label song entries by their short hymn reference and show the selected verses

- **ID:** 054
- **Status:** Accepted
- **Item:** ITEM-056
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

On the Tata Ibadah stage and in the entry preview, a song from a hymn book should read by its
short reference and title — `HAL 3 — Sai puji Naibata` — the way the section sidebar and the
pickers already do. And when an entry keeps only some of a song's verses, the stage should say
so: `Bait 1, 3` under the entry's heading.

## Scope

### In scope

- The stage heading of a hymn-book song entry: short reference + title (em dash).
- The song preview modal's header: the same string for a numbered hymn song; every other
  song's modal header keeps its present `{book name} — {title}` form.
- A `Bait …` line on the stage when the entry's stored verses differ from the song's current
  verse numbers — any song, hymn or not.

### Out of scope

- The section sidebar's label (spec 039's form, `HAL 3 Sai puji Naibata`, stays).
- Non-hymn songs with a number and hymn songs without one: heading unchanged.
- The song picker labels, the projector screens, the other entry kinds.

## UI details

Approved preview: the live `/tatib/142/` session screenshots of 2026-10-10 (stage and modal,
before / after) that the owner OKed, choosing the with-title serial, the em dash, and the
`Bait 1, 3` verse line (no “dari N”).

- **Heading text:** `{short reference} — {title}`; em dash with spaces; `{short reference}` alone
  when the song has no title; unchanged outside the hymn case.
- **Verse line:** element `.read__sub` (the template hook already in `tatib.html`), rendered under
  the entry's heading, above its words; text `Bait ` + the stored numbers ascending — `Bait 1, 3`.
- **Size / spacing:** `font: 560 12.5px/1.5 ui-sans-serif, system-ui, sans-serif`;
  `letter-spacing: .04em`; `margin: -2px 0 8px` (a ~4px gap under the heading's own 6px bottom
  margin).
- **Colors / typography:** `color: var(--head-ink)` (dims in both themes, quieter than the heading).
- **States:** static — no hover, focus, or active styling of its own.
- **Responsive behavior:** flows with the heading; nothing special.
- **Motion:** none.

## Domain rules

- **A hymn song reads by its short reference.** A song entry from a hymn book whose song is
  numbered resolves to `Song.book_number` + ` — ` + the title; an empty title leaves the
  reference alone, with no stray dash or space. (Amends spec 006's citation for song entries.)
- **Others unchanged.** A non-hymn song, and a hymn song without a number, keep their present
  heading.
- **The modal and the stage agree on the short form.** A numbered hymn song's preview header is
  the same short string as its stage heading; a non-hymn song's header keeps its present form,
  as does an unnumbered hymn's.
- **Partial selection is stated.** When the entry's stored verse numbers differ (as a set) from
  the song's current, not-deleted verse numbers, the stage shows `Bait ` + those stored numbers
  in ascending order, comma separated. An equal set shows nothing.
- **A deleted target shows no selection line.** The existing deleted warning speaks instead.
- **The sidebar keeps its form.** The section list's spec-039 label (`HAL 3 Sai puji Naibata`)
  is untouched.
- **Still filterable.** The stage's filter text carries both the sidebar and the stage wording.

## Acceptance scenarios

### Scenario: A hymn song on the stage

- **Given** an entry for "Kidung Jemaat 152, Ada Kuasa dalam DarahNya" (short name KJ)
- **Then** the stage heading reads `KJ 152 — Ada Kuasa dalam DarahNya`, and the jump link and its
  title carry the same words

### Scenario: Partial verses

- **Given** an entry for HAL 3 "Sai puji Naibata", whose song has verses 1-3, prepared with
  verses 1 and 3
- **Then** the stage shows `Bait 1, 3` directly under the heading

### Scenario: Full selection

- **Given** an entry that includes every current verse of its song (e.g. HAL 1 and all 7 verses)
- **Then** no verse line appears under the heading

### Scenario: A non-hymn song

- **Given** an entry from a non-hymn songbook prepared with verses 1 and 3 of 3
- **Then** its heading is unchanged, `Bait 1, 3` appears under it, and its preview modal's
  header keeps its present form (`{book name} — {title}`)

### Scenario: The preview modal

- **Given** the same HAL 3 entry
- **When** its preview opens
- **Then** the modal's header reads `HAL 3 — Sai puji Naibata`

### Scenario: A title-less hymn song

- **Given** a numbered hymn song with a blank title
- **Then** its heading and modal header show the short reference alone (`KJ 200`)

### Scenario: A deleted target

- **Given** a song entry whose included verse was deleted
- **Then** the deleted warning shows and no verse line appears

### Scenario: The sidebar is untouched

- **Given** a hymn song entry
- **Then** its section-sidebar row still reads `KJ 152 Ada Kuasa dalam DarahNya` (no dash)

## Traceability

- Domain/app tests: `multimedia/tatib/tests.py` (citation), `multimedia/web/tests.py` (stage,
  verse line, modal; the spec-006 long-name assertions updated).
- E2E: `tests/e2e/test_entry_preview.py`.
- Implementation: `multimedia/tatib/models.py`, `multimedia/web/reading/views.py`
  (`_tatib_stage`, `_entry_preview`), `multimedia/web/templates/reading/tatib.html`,
  `static/styles/design/components.css`.
- Amends: spec 006 (a song entry's heading), spec 039 (extends the short reference to the stage
  and the modal).
- Pairs with: spec 032 (the preview modal), spec 050 (picker labels, untouched).
