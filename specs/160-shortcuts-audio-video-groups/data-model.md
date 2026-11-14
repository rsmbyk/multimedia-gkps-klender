# Data model: Audio and video name their play/pause key

**Spec**: `specs/160-shortcuts-audio-video-groups/spec.md`

The sheet stores nothing: it is static markup in one template, and every entity below is a DOM
structure the stylesheet draws. The model is written down because the requirements and the test name
these parts.

## Sheet

`#key-list` — the whole shortcuts sheet in `multimedia/web/templates/reading/projector_controls.html`.

| Field | Value |
| --- | --- |
| identity | one element per page, `id="key-list"`, `class="sheet"` |
| shown | `body.projector.keys-open` (set by K or the `.keys` button, `projector.js:750-772`) |
| box | `max-width: calc(100vw - 32px)`, `max-height: calc(100vh - 32px)`, `overflow: auto`, `padding: 20px 24px` |
| height | the tallest column's natural height + padding + borders — never the sum of the columns |
| width | the three columns' widths + 2 × 32px gaps + padding + borders |

## Column

`div.stack` — a flex column of groups, `gap: 24px`. Three per sheet, in document order: the service
keys, the library detours, the display and find keys. **This slice adds two groups to the second
column and moves none.**

| Column | Groups today | Groups after |
| --- | --- | --- |
| 1 | Service, Song, Passage | unchanged — 634.2px natural |
| 2 | Library passage, Library Detour | + Audio, Video — 380 → 539.3px natural |
| 3 | Display, Find, While Finding, Fullscreen | Display loses one row — 609 → 574px natural |

## Group

`section.group` — one `h3` heading and zero or more `.row` paragraphs.

| Field | Value |
| --- | --- |
| heading | 14px, weight 600, `letter-spacing: .02em`, colour `--quiet`, `margin: 0 0 4px` — a 21.5px box |
| height | heading 21.5px + rows at a 34px pitch + 1px per row after the first (its `border-top`) |
| gap to the next group | 24px |

Invariants this slice keeps: every group is drawn (no group is conditional), every group's heading
is its subject, and the sheet's heading set is unique — a heading word appears once.

## Row

`p.row` — a `.fn` label at the left and a `.combo` of `.chord`s at the right; `display: flex; gap:
20px; padding: 3px 0`, with a 1px `#ffffff08` border between consecutive rows.

| Field | Value |
| --- | --- |
| height | 34px (3 + 28 + 3) |
| label | `.fn`, `white-space: nowrap`, colour `--on`, 14px |
| combo | right-aligned (`margin-left: auto`), chords 6px apart, keys 4px apart inside a chord |

## Chord and key cap

- **Chord** (`.chord`) — one alternative for the row; a row with alternatives draws `.or` between
  them. Neither new row has an alternative.
- **Key cap** (`.k`) — 28 × 28px, `border: 1px solid #4a463f`, `border-radius: 5px`, background
  `#2a2722`, the sheet's two-tone shadow. **The Space cap** is `.k.sp.glyph`: 84 × 28px (3 × 28), its
  mark `␣` in `.space-mark` (scaled 1.3 on X), `title="Space"`, `aria-label="Space"`.

## Typed delta (what Fold will write)

| Operation | Entity | Detail |
| --- | --- | --- |
| removed | row | `Audio/Video Play/Pause` leaves the `Display` group |
| added | group `Audio` | one row: `Play/Pause` — the Space chord |
| added | group `Video` | one row: `Play/Pause` — the Space chord |

Nothing else in the model changes: no group is renamed, no column is reordered, no cap, chord or
colour is added.
