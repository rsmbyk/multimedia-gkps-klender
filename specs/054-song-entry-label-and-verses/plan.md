# Plan 054: Label song entries by their short hymn reference and show the selected verses

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-056
- **Bump:** patch

## Why

The stage of a Tata Ibadah still prints a song entry's heading with the long book name —
`Haleluya 3` for HAL 3 — while the section sidebar (spec 039) and the pickers use the short
reference. The preview modal's header does the same (`Haleluya — Sai puji Naibata`). The operator
reads hymns by their short reference (`HAL 3`), so the stage and the modal should too: the owner
asked for `HAL 3 — Sai puji Naibata` while reviewing the live `/tatib/142/` page on 2026-10-10.

The stage also never says which verses of a song the entry carries. With HAL 3 prepared from
verses 1 and 3 of 3, nothing on the page tells the operator that verse 2 was left out; the entry
resolves only the included verses (spec 006), so the page should state the selection: `Bait 1, 3`.

## Scope / edges

**In:**

- The stage heading of a song entry from a hymn book: `HAL 3 — Sai puji Naibata`
  (`Song.book_number`, em dash, title); a title-less song shows the reference alone.
- The preview modal's song header: the same string.
- A selected-verse line under a song entry's heading when the entry's stored verses differ from
  the song's current verse numbers: `Bait 1, 3` (any song, hymn or not; the preview approved
  the form without a “dari N” total).

**Out:**

- The section sidebar's label (spec 039 keeps `HAL 3 Sai puji Naibata`, no dash).
- Non-hymn songs with a number, and hymn songs without one: their heading is unchanged.
- The pickers' labels, the projector screens (a song's screens carry no header), and the other
  entry kinds.

## Approach

- `multimedia/tatib/models.py` — `ServiceEntry.citation()`'s song branch: a hymn book with a
  numbered song returns `f'{song.book_number} — {song.title}'` (the reference alone when the
  title is blank). This moves the stage heading and the filter text with it, and feeds the modal
  header below; the projector is untouched (song screens have no header).
- `multimedia/web/reading/views.py` → `_entry_preview()` — for a numbered hymn song hand the
  modal the entry's citation as one `heading` string; every other song keeps the present
  `{book name} — {title}` composition.
- `multimedia/web/reading/views.py` → `_tatib_stage()` — for a song entry whose stored verses
  differ (as a set) from the song's current, not-deleted verse numbers, set
  `block['subtitle'] = 'Bait …'` (the stored numbers, ascending, comma separated). The template's
  existing `read__sub` hook renders it; the rule gains its CSS in the design system.
- `multimedia/web/templates/reading/tatib.html` — the preview source's `preview__song` line reads
  `{{ item.preview.heading }}`.
- `static/styles/design/components.css` — the `.read__sub` rule from the approved preview.

## TDD

- Domain/app tests: `multimedia/tatib/tests.py` — the hymn citation (with title, without title,
  sub-number, non-hymn unchanged). `multimedia/web/tests.py` — the stage heading, the verse line
  (partial shown / full hidden / non-hymn shown / deleted target none), the modal heading; the
  spec-006 assertions that encode the long name are updated, not kept.
- E2E: `tests/e2e/test_entry_preview.py` — the song modal's header reads the short form; a
  partial selection shows its `Bait …` line on the stage.

## Risks

- **`citation()` is shared.** It feeds the stage heading, the entry filter text, and the modal —
  all intended. Checked consumers: the projector's song screens carry no header; the sidebar
  keeps its own spec-039 label; the pickers build their own labels.
- **Stale assertions.** Six spec-006-era assertions encode the old wording — three in
  `multimedia/tatib/tests.py` (`'Kidung Jemaat 152'` citation resolves), two in
  `multimedia/web/tests.py` (the stage's `'Kidung Jemaat 152'` references), one more there
  (`'Kidung Jemaat'`, the modal header). The tasks list them so the rewrite is deliberate,
  not a surprise of the red run.
- **“Not all verses” is a moving target.** A verse added to a song after the entry was prepared
  makes the selection partial again — the line returns. That matches the stored-verses model
  (“a verse added to the song later has to be added to the service deliberately”) and is stated
  in the spec.
