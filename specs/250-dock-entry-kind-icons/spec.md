# Feature Specification: entry-kind icons in the OBS dock

**Slice**: `specs/250-dock-entry-kind-icons`
**Branch**: `feat/250-dock-entry-kind-icons`
**Created**: 2026-11-28
**Status**: Accepted
**Input**: the owner's request — "add the respective icons for each entry headers in dock. put it to the left of chevron icon on each row"

## Current behaviour (read, not assumed)

- `static/web/obs-dock.js` `entryRowContent()` builds a header per service entry; `renderList()` appends one `.entrychev` only when the entry has an expandable inner block (FR-001 of spec 198), and `aria-current="true"` hides that chevron on the live row.
- A section break renders a hairline (`.entryrow__break`) with no chevron and no inner.
- Entry kinds come from `projectorEntryData`: `text`, `passage`, `song`, `media`, `break`.
- The product already owns four 24-unit kind glyphs in `multimedia/web/templates/reading/_toc_mark.html` (book, note, play-frame, text rules), drawn at 16px in the contents rows.
- The pinned header clones the whole `.entryrow`, so anything added to the header is carried into both pins without another writer.

## User Scenarios & Testing

### US1 — Each header names its kind in shape (P1)

**Independent Test**: open a service covering text, passage, song, media and break; read the mark on every header and the chevron beside it.

1. **Given** a text/passage/song/media entry **When** its runner header renders **Then** one 16px mark of that kind renders immediately to the left of its chevron.
2. **Given** a section break **When** the list renders **Then** the hairline row carries no mark and no chevron.
3. **Given** any mark **When** assistive technology reads the row **Then** the mark is `aria-hidden`, takes no pointer and adds no text — the header's own words still name the entry.

### US2 — The chevron and the existing row anatomy keep their states (P2)

**Independent Test**: measure the mark, chevron and title boxes in both themes and on the live row; run the chevron state and header-wrap modules.

1. **Given** a collapsed or open header **When** it is clicked **Then** the chevron still rotates 90° and stays vertically centred in the row.
2. **Given** the live header **When** the chevron is hidden **Then** the kind mark stays at the trailing edge in the live ink.
3. **Given** both pinned clones **When** they stand at the scrollport edge **Then** each carries the same single mark as its source header.

## Requirements

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Every non-break entry header SHALL render one kind mark — book for `passage`, note for `song`, play-frame for `media`, rules for `text` — with the same paths as the product's contents-row marks. | `dock/R20` (added) |
| FR-002 | The mark SHALL sit immediately left of the header's chevron at the trailing edge, with the row's own 10px gap, and SHALL stay in the row when the header wraps. | `dock/R20` |
| FR-003 | The mark SHALL be decorative: `aria-hidden="true"`, `pointer-events: none`, no accessible name. A break row SHALL carry none. | `dock/R20` |
| FR-004 | The chevron's presence, rotation, centring and live-row hiding SHALL be unchanged; the live mark SHALL use the live ink. | `dock/R3`, `dock/R14` (unaffected) |

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Four distinct glyph sets render on the four kinds, one mark per eligible row, zero on the break. | E2E kind/placement probe |
| SC-002 | Mark and chevron share the row centre line; their gap is 10px; neither spills from the row. | Playwright box measurements |
| SC-003 | Chevron state, wrap and pin modules stay green apart from separately recorded machine-local reds. | Targeted E2E |

## UI/UX

Measured on the live slice server at 420×800, dark theme, 1×:

- Mark: **16×16px**, 24-unit viewBox, `stroke-width: 1.8` (1.2px painted), `--head-ink` **rgb(156,154,145)**; live row `--ink`.
- Placement on a 420px dock: mark **361–377px**, chevron **387–402px**, gap **10px**, both vertically centred in a **38px** row (0px off its centre).
- Long-song row: the mark takes **26px** from the song title column (315.41 → 289.41px); the row height stays **77px** and the title keeps its **61.59px** left edge — no new wrap.
- A break row keeps its hairline with no mark; the live row keeps the mark with no chevron.

## Assumptions

- The mark is a copy of the product's own contents-row glyphs, not a new icon vocabulary; no new dependency, endpoint or migration.
- A break is a divider, not a header, so it is unmarked (FR-003).
- The live row keeps its mark even though its chevron is hidden, because the request says every entry header.

## Clarifications

- None on behaviour. The checkout was chosen through the native question UI (new slice worktree off develop); that is a process choice, not a requirement.
