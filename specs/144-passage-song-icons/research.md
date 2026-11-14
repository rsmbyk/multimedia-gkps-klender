# Phase 0 — Research

Slice `specs/144-passage-song-icons`. Every question below was answered by reading the code, measuring
the rendered page, or the owner's gate-1 instruction — no unknowns are carried forward.

## D1 — Where the mark sits in the DOM

**Decision:** the mark is the **first child of the row's heading** (`<h2 class="read__sec">`), before the
`.entry__jump` link — not a child of the section.

**Rationale:** `static/styles/design/components.css:1987` reads
`.read[data-kind="tatib"] .tatib__item--acts > :first-child { margin-top: 0 }`. That rule is what
flattens the heading's 30px pericope margin to the row's 8px padding. A mark placed as the section's
first child takes that seat, the heading stops being `:first-child`, and its margin comes back:
**measured in the preview, a passage row grew 56px → 69.8px**.

**Alternatives rejected:**
- *Mark as the section's last child* — leaves the layout intact but puts a leading visual element after
  the controls in the DOM, and the next `> :last-child` / `> *:has(+ .entry__acts)` rule added to this
  block would then target the mark instead of the content.
- *Patch the shipped selector with `:not(.entry__kind-icon)`* — works, but keeps a fragile
  first-child contract that has to be re-remembered for every future rule in that block.

**Provenance:** `components.css:1987`, `tatib.html:143`, measured row heights on
`specs/144-passage-song-icons/preview/preview.html`.

## D2 — Server-rendered SVG, not script-injected

**Decision:** the SVG is written by the template.

**Rationale:** the entry's kind is known when the page is drawn (`_tatib_stage` carries `kind` per
item), and a mark that exists in the HTML works with script disabled, before `media-stage.js` runs, and
in the targeted-refresh path that swaps nodes from freshly-read server HTML.

**Alternatives rejected:** injecting from `static/web/media-stage.js`, the way the media chip is filled
in. That script exists because the *media family* and its local availability are client-side facts —
neither applies to a passage or a song's kind.

**Provenance:** `multimedia/web/reading/views.py:1012` (`_tatib_stage` builds `kind`), `tatib.html:143`,
`static/web/media-stage.js:1-20`.

## D3 — Geometry: the media row's own columns

**Decision:** the row keeps its 8px padding and gains `padding-left: 64px`; the mark is
`position: absolute; left: 24px; top: 50%; width: 20px; height: 20px; transform: translateY(-50%)`.

**Rationale:** the media row is `padding-left: 64px` and its chip is `left: 13px`, `42 × 42`. The chip's
centre line is `13 + 42/2 = 34px` from the row's edge; a 20px glyph centred on it starts at `34 − 10 =
24px`. The title then begins at the media title's own column, `64px`. Owner's gate-1 instruction: the
mark is centred on the media icons and the title aligned with the media filenames.

**Alternatives rejected:** the preview's original A (own 42px indent, titles off the media column) and
the chip candidates (30px marks, 55px indent) — both shown at gate 1 and not taken.

**Provenance:** `components.css:2008` (`.tatib__item--media { padding: 16px 16px 16px 64px }`),
`components.css:2024` (`.entry__media-icon { left: 13px; width: 42px }`), owner decision 2026-10-28.

## D4 — Colour

**Decision:** `--head-ink` for the glyph stroke.

**Rationale:** it is the stage's own meta ink and it is measurable against the three backgrounds that
matter — **5.57:1** on `--canvas` light, **6.59:1** dark, **4.77:1** / **5.23:1** on the hover fill. The
media chip's `--focus` glyph reads **6.08:1** / **5.89:1** on its tint, so the media chip remains the
heavier mark, which is the distinction the request asks for.

**Alternatives rejected:** `--focus` (the media chip's colour — would make the two read as one family),
`--ink` (equal weight to the title, so the mark would compete with the words).

**Provenance:** `tokens.css:23/34/40/90/102/107`; contrast computed from those hex values.

## D5 — Glyphs

**Decision:** passage = an open book (two pages, centre fold); song = a single flagged note.

**Rationale:** they must be unmistakable next to the media set, where `audio` is already a beamed double
note (`static/web/media-stage.js:5`) and `pdf` is a page. The open book cannot be confused with any file
glyph; a single flagged note is a different silhouette from the audio chip's pair and reads as a hymn,
not a file.

**Alternatives rejected:** the audio note reused for songs (identical silhouette to a media kind),
a hymnbook (a second book — confusable with the passage mark), a text-lines glyph (that is the text
entry's own mark, deliberately not drawn — FR-004).

**Provenance:** `static/web/media-stage.js:4-10`, stroke language of `.entry__media-icon svg`
(`components.css:2031`).

## D6 — Which kinds carry a mark

**Decision:** `scripture` and `song` only — nothing on `text`, `section_break`, `media` or legacy rows.

**Rationale:** the request names passage and song; media already has its chip; a break is a rule, not a
kind; a legacy row has no kind at all (`_tatib_stage` gives legacy items no `kind` key).

**Provenance:** `views.py:1012-1100`, `ServiceEntryKind` (`multimedia/tatib/models.py:89`).

## D7 — The mark states the kind, not the availability

**Decision:** a row whose target was deleted (`target_deleted`) still paints its mark; the mark is
`aria-hidden` and takes no pointer.

**Rationale:** `entry__deleted-warning` already carries the availability in words; a mark that
disappeared would make the row's kind unknown exactly when the row is unusual.

**Provenance:** `tatib.html:144` (`entry__deleted-warning`), `views.py:1050` (`deleted_target`).

## D8 — How it is verified

**Decision:** a new Playwright module, `tests/e2e/test_stage_kind_marks.py`; no unit test, because the
mark changes nothing a Django unit test observes beyond the response body, which the E2E reads anyway.

**Rationale:** the repo's rule — domain/application rules are TDD-governed, user-visible acceptance is
Playwright E2E. The behaviours here are geometry and paint, both invisible to the Django test client.

**Provenance:** `docs/PROCESS.md` TDD repo block ("User-visible acceptance is Playwright (Python) E2E"),
`tests/e2e/test_tatib_entry_controls.py` as the pattern.

## Measured, not assumed

| what | value | where |
| --- | --- | --- |
| the media chip's box | `left: 13px`, `42 × 42`, centre **34px** from the row's edge | `components.css:2024` |
| the media title's column | `64px` (`padding-left`), title at `x = 1030` on a 1440 window | `components.css:2008` |
| a passage/song row today | `padding-left: 12px`, title at `x = 978`, box 56px | measured |
| `HAL 7 — Porini Dong Marribu Hali` | **295.6px** on one line | measured in the preview |
| `HAL 1 — Jahowa Sihol Pujionku` | **270.9px** on one line | measured in the preview |
| title column after the mark | `250px` — the media title's | derived from D3 |
| songs that wrap at the 400px pane | **4 of 4**, +23.8px each | measured in the preview |
| head-ink contrast | 5.57 / 6.59 light/dark; 4.77 / 5.23 on hover | computed from `tokens.css` |

## Unknowns

**Zero.** No `[NEEDS CLARIFICATION]` remains in `spec.md`; the one skipped question (text entries) is
recorded there as FR-004's assumption.
