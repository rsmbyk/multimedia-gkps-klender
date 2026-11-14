# Feature Specification: a converted deck keeps the deck's own layout

**Slice**: `specs/166-slides-render-fidelity`
**Branch**: `fix/166-slides-render-fidelity`
**Created**: 2026-10-30
**Status**: Accepted (owner, gate 1, 2026-10-30)
**Input**: "can you fix the ppt/ppts rendered pdf? most of the positioning are not like the
original" — with six screenshots of *Slide Warta Jemaat GKPS Klender Tgl 25 Oktober 2026.pptx*
(16 slides, 13.333 × 7.5 in) as LibreOffice Impress and PowerPoint draw it.

## What happens today

A PowerPoint is converted to a PDF by the companion's own LibreOffice, and the projector paints that
PDF (`docs/spec/projector.md`, R7). Two things decide whether the result looks like the deck.

**1. The faces the deck names are not in the image.** `Dockerfile` installs `libreoffice-impress` and
`fonts-liberation` only. Read inside the running media container with `fc-match`, every proportional
family this deck asks for resolves to a monospaced one:

| the deck asks for | runs in the deck | the image answers |
| --- | --- | --- |
| `Calibri` | 630 | **Liberation Mono** |
| `Calibri Light` | the theme's minor latin face | **Liberation Mono** |
| `Times New Roman` | 324 | Liberation Serif |
| `Britannic Bold` | 52 | **Liberation Mono** |
| `Berlin Sans FB Demi` | 6 | **Liberation Mono** |

A monospaced face has a different advance for every proportional glyph, so every run re-wraps, every
line box grows, and the composition moves. On the PDF the app serves for this deck today
(`derived-slides/95a90f31…-e073f7c4fb0425d1.pdf`, converted 2026-10-25 by LibreOffice 7.4.7.2):

- page 1's title ink measures **300 × 275 px** — a narrow column — where the deck draws it
  **477 × 199 px**;
- page 3's schedule puts `Warta Jemaat/Tingting` **250.7 pt** from its place (26 % of the page
  width), page 12's table **462.6 pt**, page 10's giving column **240.1 pt**;
- page 2's band holds **12 words** instead of 5: `Duit na masuk Rp.` and its amount fall onto two
  lines each, and the lower amount is clipped by the slide's edge.

**2. The image's Impress is from 2022.** Debian bookworm carries LibreOffice **7.4.7.2**; the machines
that render this deck correctly carry 25.2 or 26.2. The two differ even with the fonts supplied: with
Carlito installed on 7.4 the same page 2 band still wraps its amounts, and per-page pixel distance to
the reference stays at 4,600–12,900 (RMSE, 96 dpi) where 25.2 reaches 0–1,800.

**3. The derived PDF is cached against the LibreOffice version alone.** `slide_pdf()` keys
`derived-slides/<sha>-<key>.pdf` on `libreoffice --version` (`multimedia/local_media.py:362`). Installing
a font, or rebuilding the image with the same LibreOffice, leaves the old PDF in place and the operator
keeps seeing the old render with no way to ask for a new one.

Measured on this machine, converting the reported deck with LibreOffice 25.2 and the faces above
mapped to their metric-compatible equivalents: page 2's table words land on the coordinates the
reference render gives them **to the digit** (`Minggu` at x 641.85, y 8.78 in both; today at y 8.15),
and page 1's title ink is **477 × 199 px** — one pixel from the reference.

## User Scenarios & Testing

### US1 — A converted page lands where the deck draws it (P1)

**Why this priority**: this is the reported defect. A projected bulletin whose table columns and
title have moved is worse than no projection, because the congregation reads it.

**Independent Test**: convert the reported deck and compare each page's word boxes against the same
deck converted by LibreOffice 25.2 on a machine with the same font mapping; every page whose faces
resolve metric-compatibly agrees within 1 pt.

**Acceptance scenarios**

1. **Given** the media image, **When** the font behind each family in the deck is resolved, **Then**
   `Calibri` and `Calibri Light` answer **Carlito**, `Times New Roman` answers **Liberation Serif**,
   `Cambria` answers **Caladea**, `Arial` answers **Liberation Sans**, `Arial Narrow` answers
   **Liberation Sans Narrow**, and no proportional family answers a face whose name ends in `Mono`.
2. **Given** the reported deck, **When** it is converted, **Then** page 1's title ink is 477 × 199 px
   at (95, 90) at 96 dpi, and page 3's table words are within 1 pt of the reference render.
3. **Given** the same deck, **When** page 2 is inspected, **Then** the band holds 5 words — each amount
   on its label's line at x 475.45 and x 785.56 — and nothing is clipped by the slide's edge.
4. **Given** a deck whose text is entirely Calibri and Times New Roman, **When** it is converted,
   **Then** no page embeds a monospaced face.

### US2 — A converter change re-renders what was already converted (P2)

**Why this priority**: the operator has this deck on screen now, already converted. Without this
story the fix ships and the same page keeps showing the same wrong render until the file is removed
and re-uploaded.

**Independent Test**: convert a deck, change the converter's identity (its LibreOffice version, or
its font inventory), and convert again: the second call produces a new PDF instead of returning the
first.

**Acceptance scenarios**

1. **Given** a deck already converted, **When** the image's LibreOffice version changes, **Then** the
   next request converts again and the page shows the new render.
2. **Given** a deck already converted, **When** a font is added or removed, **Then** the next request
   converts again.
3. **Given** neither changes, **When** the same deck is requested twice, **Then** it is converted
   once, as today, and a concurrent request shares that one conversion.
4. **Given** an older derivative, **When** a new one is written, **Then** nothing in the library's
   identity changes: the deck keeps its SHA, its name, its family, its references and its deadline.

### US3 — The operator can supply the faces only their Office has (P3)

**Why this priority**: `Britannic Bold` and `Berlin Sans FB Demi` ship with Office, are not
redistributable, and are absent from every machine here. Two of this deck's pages are set in them
(the cover, and the thank-offering page); the rest of the deck is Calibri and Times New Roman and is
fully served by US1. Closing them is the operator's move, not the build's.

**Independent Test**: drop the two TTFs into the directory the companion reads, restart it, convert
the deck: the cover's ink box matches the deck's own drawing within 1 pt.

**Acceptance scenarios**

1. **Given** a directory of fonts on the host, **When** the companion starts, **Then** the faces in it
   are visible to the converter without rebuilding the image and without a code change.
2. **Given** those faces are supplied, **When** the deck is converted, **Then** the cache key changes
   (US2) and the new render uses them.
3. **Given** the directory is absent or empty, **When** the companion starts, **Then** it starts as
   today and the substitute faces are used.

### Edge Cases

- **When** a deck names a face nobody has and fontconfig would otherwise fall back to a monospaced
  family, **Then** it falls back to the image's default proportional family, never to a mono one.
- **When** LibreOffice is missing from the image at all, **Then** the request fails as it does today
  (*PowerPoint conversion is unavailable*), and the message does not change.
- **When** a conversion fails or times out, **Then** no derivative is cached and the next request
  retries — the timeout, the memory and file-size limits and the private profile stay as they are.
- **When** a `.ppt` (binary) file is converted, **Then** it takes the same path and the same cache
  identity as a `.pptx`.
- **When** an existing derivative was produced by an older converter, **Then** it is not deleted by
  this slice: the new one is written beside it and the old one ages out with the file's own removal.
- **When** the font inventory cannot be read (no `fc-list`), **Then** the key still changes with the
  LibreOffice version and the conversion still runs.
- **When** the operator adds a font while a conversion is running, **Then** that conversion finishes
  under the identity it started with; the next one uses the new inventory.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The media image SHALL resolve each family the decks use to a proportional, metric-compatible face: `Calibri`/`Calibri Light` → Carlito, `Cambria` → Caladea, `Arial` → Liberation Sans, `Arial Narrow` → Liberation Sans Narrow, `Times New Roman` → Liberation Serif, `Courier New` → Liberation Mono; no proportional family SHALL resolve to a monospaced face. | `new: media-library` → R2 |
| FR-002 | The image SHALL carry a LibreOffice whose PowerPoint import places text where the deck places it — 25.2 or newer — and the conversion command, its timeout, its memory and file-size limits and its private profile SHALL stay as they are. | `media-library/R2` |
| FR-003 | The identity that keys a derived PDF SHALL cover everything that changes the render: the LibreOffice version and the font inventory. A change in either SHALL produce a new derivative; an unchanged converter SHALL keep converting once. | `new: media-library` → R3 |
| FR-004 | The converter SHALL read an operator-supplied font directory when one is mounted, so a face that ships only with Office can be added without rebuilding the image. Absent or empty, the behaviour SHALL be exactly today's. | `new: media-library` → R4 |
| FR-005 | A build of the image SHALL fail if a family the decks use resolves to a monospaced face. | `media-library/R2` |
| FR-006 | Nothing else changes: the service's routes, payloads, headers and origin rules; the library's identity, references and deadlines; the projector's painting and fitting; the upload and transfer flow. | `media-library/R1`, `projector/R7` |

### Key Entities

- **Derived PDF** — `derived-slides/<sha>-<key>.pdf`, disposable, rebuilt from the library's own bytes
  when the key changes and removed with the source. `<key>` is the converter's identity, not the
  deck's.
- **Converter identity** — the pair *LibreOffice version* and *font inventory* (the sorted family names
  the renderer can see), hashed. Two renders with the same identity are the same document.
- **Font mapping** — the deployment's answer to "this deck asks for X, we draw Y". It lives in the
  image's fontconfig configuration, not in the application.
- **Operator font directory** — a host directory mounted into the image read-only; whatever faces are
  in it join the inventory, and therefore the identity.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Every word of the reported deck's Calibri and Times New Roman pages lands within 1 pt of the reference render. | word boxes from `pdftotext -bbox`, page by page, against the reference PDF |
| SC-002 | Page 1's title ink is 477 × 199 px at (95, 90) at 96 dpi — the reference's own box, ±1 px. | ink bounding box of the title region, `magick … -trim` |
| SC-003 | Page 2's band holds 5 words, with the amounts at x 475.45 and x 785.56, and nothing clipped. | the same word boxes, filtered to the band |
| SC-004 | The image refuses to build when a family the decks use resolves to a monospaced face. | a build-time check that fails the build; run by hand against the built image too |
| SC-005 | A changed font or a changed LibreOffice version produces a new derivative and shows the new render; an unchanged one converts once. | unit tests on the key, plus the real-converter test |
| SC-006 | The suite is green, with existing assertions unchanged. | `manage.py test multimedia` and the reported E2E set |

## UI/UX

`static preview at specs/166-slides-render-fidelity/preview/index.html` — pages 1, 2, 3 and 10 of the
reported deck, today's PDF beside the proposed one, both at 96 dpi, with the numbers below.

- **Layout / position**: page 1's title ink **300 × 275 px at (177, 53)** → **477 × 199 px at (95, 90)**
  (reference (95, 91)). Page 3's words: worst offset **250.7 pt** → **0.7 pt**. Page 12: **462.6 pt** →
  **0 pt**. Page 10: **240.1 pt** → the reference's own row rhythm.
- **Size / spacing**: page 2's band **12 words** → **5**, amounts at **x 475.45** and **x 785.56**
  (reference the same); the table's rows stop growing by the fallback's line box.
- **Colour / typography**: the deck's `Calibri` is drawn in Carlito — same advance widths as Calibri —
  instead of Liberation Mono; `Times New Roman` in Liberation Serif, as today.
- **States**: one — a converted page. Nothing on any screen has a hover, focus, active, disabled,
  empty, error or loading state that this slice changes; the projector's own empty and error states
  are untouched.
- **Motion**: none. A page that was converted before is converted again on its first request after
  the change; no animation, no spinner, no copy changes.

## Assumptions

- **The reference is LibreOffice, not PowerPoint.** No PowerPoint exists on this machine to render a
  golden set, and the deck is served as a PDF by LibreOffice either way. The reference render is
  LibreOffice 25.2 with the same font mapping; the tolerant target is the deck's own drawing as the
  operator sees it in Impress, which is what the screenshots show.
- **Fonts are the first cause and the version the second.** Measured: adding Carlito to the current
  image moves every page toward the reference but leaves the band wrapped; moving to 25.2 with the
  same fonts lands the words on the reference's coordinates. Both are therefore in the slice, and the
  evidence for each is recorded above rather than asserted.
- **Two faces cannot be shipped.** `Britannic Bold` and `Berlin Sans FB Demi` are Office fonts; the
  slice makes them *suppliable* (FR-004) and substitutes Noto Sans Bold until they are, which is what
  the reference machine does too.
- **A `--convert-to pdf` export is the pipeline.** Rendering the deck any other way (another
  converter, a rasteriser, a browser) is out of scope: the projector already paints a PDF page and
  spec 158 fitted it.
- **The derivative directory is not a cache to police.** Old derivatives are left to age out with the
  source file; adding a sweeper is its own card.
- **No capability number is reused.** `media-library` holds R1 (`docs/spec/media-library.md`), so this
  slice adds R2–R4 and folds R3 and R4 at Fold.

## Clarifications

### Session 2026-10-30

- **Which LibreOffice.** Asked: the media image runs 7.4 (Debian bookworm); how should the converter
  get a current one? **Answered: move the shared image to Debian trixie**, LibreOffice 7.4 → 25.2 for
  both containers. `python:3.12-slim-trixie` exists and the requirements resolve there unchanged
  (checked: Django 4.0.1, psycopg2 2.9.9 and pypdf 5.9.0 install, same Python 3.12).
- **The Office-only faces.** Asked: `Britannic Bold` and `Berlin Sans FB Demi` ship with Office and
  exist on no machine here — supply them here or card them? **Answered: include it** — a host folder
  mounted read-only, re-scanned at start, so the fonts are dropped in once.

Zero open markers remain.
