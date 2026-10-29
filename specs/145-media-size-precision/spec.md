# Feature Specification: a media size reads in the unit that still shows its number

**Slice**: `specs/145-media-size-precision`
**Branch**: `feat/145-media-size-precision`
**Created**: 2026-10-28
**Status**: Accepted
**Input**: "the size calculator should detect to the smallest precisions (what does it means 0.0 MB? no size?)" — with a screenshot of the New media card reading `Image · 0.0 MB` for `images (1).jpeg`.

## What the page does today

Two formulas print every media size, and both round a real file down to nothing:

| surface | today's formula | 512 B | 12,345 B | 999,999 B |
| --- | --- | --- | --- | --- |
| New media card — `static/web/media-entry.js:39` | `(bytes / 1000000).toFixed(1) + ' MB'` — always megabytes, one decimal | `0.0 MB` | `0.0 MB` | `1.0 MB` |
| Media Library row and Total — `static/web/media-library.js:13` | `Math.round(bytes / 1000) + ' KB'` below 1 MB | `0 KB` | `12 KB` | `1000 KB` |
| Transfer rail — `static/web/media-handoff.js:19` | the same formula, **defined and never called** | — | — | — |

So every file under **50,000 bytes** reads `0.0 MB` on the card that asks the operator to confirm it, and
every file under **500 bytes** reads `0 KB` in the library. The two live formulas also disagree with each
other: the same 12,345-byte file is `0.0 MB` in the card and `12 KB` in the library, and 346 of its bytes
are invisible in the library.

## User Scenarios & Testing

### US1 — No size reads as zero, and the unit follows the file (P1)

**Why this priority**: this is the report. `0.0 MB` under a file the operator just chose reads as "no
size", and the number is what they check before saving.

**Independent Test**: choose a 12,345-byte file in the New media card and read its line:
`Image · 12.3 KB`. Choose a 512-byte file: `Image · 512 B`.

**Acceptance scenarios**

1. **Given** a chosen file of 12,345 bytes **When** the card draws its line **Then** it reads
   `Image · 12.3 KB`, not `0.0 MB`.
2. **Given** a chosen file of 512 bytes **When** the card draws its line **Then** it reads `Image · 512 B`.
3. **Given** a chosen file of exactly 1,000,000 bytes **When** the card draws its line **Then** it reads
   `Image · 1 MB`.
4. **Given** a library of one 12,345-byte file **When** its row and the Total are drawn **Then** both read
   `12.3 KB`, not `12 KB`.

### US2 — One label, everywhere (P2)

**Why this priority**: three surfaces print sizes and two of them already disagree; a fix applied to one
surface would leave the disagreement, and the next surface to print a size would invent a fourth formula.

**Independent Test**: read the same file's size on the card, the library row and the library Total —
the strings are identical, produced by one function.

**Acceptance scenarios**

1. **Given** a file of 12,345 bytes **When** its size is drawn on the card, in its library row and in the
   library Total **Then** all three read `12.3 KB`.
2. **Given** the transfer rail, which prints no size **Then** its unused formatter is gone rather than
   kept in step.

### Edge Cases

- **When** a file is 999 bytes **Then** the label is `999 B`; at 1,000 bytes it is `1 KB`.
- **When** a value would round to `1000` in its own unit (999,999 bytes → `1000 KB`) **Then** the unit is
  promoted: `1 MB`.
- **When** the byte count is 0 or not a number **Then** the label is `0 B`; the entry path already rejects
  an empty file, so this is a guard, not a state.
- **When** a file is 200,000,000 bytes — the cap **Then** it reads `200 MB`, and the cap is unchanged.
- **When** the library Total sums many files **Then** the bytes are summed first and formatted once, so the
  Total never becomes a sum of rounded strings.
- **When** a size reaches a gigabyte (no surface can today, 200 MB being the cap) **Then** it reads in `GB`
  rather than `1000 MB`.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A media size SHALL be drawn in the largest decimal unit in which its value is at least 1 — `B` · `KB` (1,000 B) · `MB` (1,000 KB) · `GB` (1,000 MB) — and a non-empty file SHALL never read as zero. | `reading/R21` |
| FR-002 | A value SHALL carry one decimal only when it is not a whole number at one decimal (`2 KB`, `12.3 KB`, `868.4 KB`), and SHALL be promoted to the next unit when rounding would print `1000`. | `reading/R21` |
| FR-003 | The New media card, a Media Library row, the Media Library Total and any later size label SHALL be drawn by one function, `window.gkpsFormatSize`, loaded once per page. | `reading/R21` |
| FR-004 | Sizes below 1 KB SHALL be printed as whole bytes with the `B` suffix. | `reading/R21` |

### Key Entities

- **Size label** — the string a surface prints for a byte count: `<value> <unit>`, value `1`–`999.9`, unit
  one of `B`, `KB`, `MB`, `GB`. It is derived, never stored; the byte count stays the source of truth.
- **Formatter** — `window.gkpsFormatSize(bytes)`, defined once in `static/web/media-size.js`, pure, no
  network access.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No non-empty file reads as zero | 1 · 500 · 999 · 1,000 · 1,024 · 12,345 · 50,000 · 123,456 · 868,400 · 999,999 · 1,000,000 · 1,250,000 · 200,000,000 all contain a non-zero digit |
| SC-002 | The unit follows the magnitude | 512 → `512 B`; 1,000 → `1 KB`; 12,345 → `12.3 KB`; 999,999 → `1 MB`; 1,250,000 → `1.3 MB`; 200,000,000 → `200 MB` |
| SC-003 | The surfaces agree | the card, the library row and the Total print the same string for the same byte count |
| SC-004 | Nothing else about the line changes | the card's meta line keeps `12px / 18px`, weight 400, `rgb(100, 99, 87)`; its box grows no more than the string does |

## UI/UX

Text only: no markup, no class, no spacing and no colour changes. Measured on the live branch server at
1440×900, in the real New media card.

- **Layout / position**: the line is unchanged — `[data-media-selected-meta]` under the file name inside
  the upload card, `margin: 0`.
- **Size / spacing**: the line's box measures **17.88px** tall (unchanged) and **87.22px** wide for
  `Image · 12.3 KB`, against **83.83px** for the `Image · 0.0 MB` it replaces — **+3.39px**, inside the
  card's own width.
- **Colour / typography**: inherited and unchanged — `12px/18px`, weight 400, `rgb(100, 99, 87)`.
- **States**: unchanged. `B`, `KB` and `MB` labels appear in the same places the old labels did; nothing is
  hovered, focused or disabled by this slice.
- **Motion**: none.
- **Responsive**: unchanged; the longest new string (`Image · 868.4 KB`, 93.1px) stays inside the card's
  text column at the 720px breakpoint.

## Assumptions

- **Decimal units, not binary.** `1 KB = 1,000 B`, because the product's own cap is written `200 MB`, the
  companion stores `byte_count`, and the shipped formula already divides by 1,000,000.
- **Bytes are shown below 1 KB.** The request asked for the smallest precision; a file under a kilobyte
  is the case where that matters most.
- **`GB` is defined even though nothing can reach it.** The 200 MB cap is unchanged; the unit exists so a
  later cap raise cannot reintroduce a `1000 MB` label.
- **The transfer rail's formatter is removed, not fixed.** `fmt` in `media-handoff.js` has no caller; wiring
  a dead function would add a contract nothing needs.
- **The decimal is trimmed when it is `.0`**, so a whole value reads `2 KB` rather than `2.0 KB`; the chosen
  label style at Clarify is the trimmed one.
- **No server change.** `MediaIdentity.byte_count`, the companion's `/files` and `/inspect` payloads already
  carry exact bytes.

## Clarifications

### Session 2026-10-28

- Q: Which label should the Media Library, the New media card and the transfer rail all use? → A: **the
  smallest unit that still shows a number, with a decimal only when it adds something** — `512 B · 2 KB ·
  12.3 KB · 1 MB` (owner, 2026-10-28).
