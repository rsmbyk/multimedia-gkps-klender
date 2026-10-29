# Convergence — the rail's marks and the stage's own

**Spec**: `specs/151-rail-icons/spec.md` · **Date**: 2026-10-29

## Pass 1

Checked every row of `plan.md`'s traceability table against the working tree, by the method each row
declares.

| Row | Method | Result |
| --- | --- | --- |
| FR-001 · rail Alkitab and the panel's empty state | `test` | **met** — `test_the_rail_bible_and_a_passage_draw_one_path` reads three nodes, the book, its gutter and the cross (stem `M12 2.6v4.6`, bar `M10.1 4.5h3.8`); both places draw it. |
| FR-002 · passage mark and Add Passage tile | `test` | **met** — the same test asserts string equality across the rail, the 20px row mark and the 24px tile. |
| FR-003 · rail Tata Ibadah is a clipboard | `test` | **met** — two `rect`s and the three rules, and the shipped `M8.6 8.8h6.8` page is gone; the mark differs from `gkpsMediaIcon('pdf')`. |
| FR-004 · rail Kidung = song mark = Add Song tile | `test` | **met** — `test_the_rail_note_and_a_song_draw_one_path`. |
| FR-005 · audio is a waveform everywhere | `test` | **met** — `window.gkpsMediaIcon('audio')` and the stage's chip both return the five-bar path. |
| FR-006 · the other families and `missing` unchanged | `test` | **met** — compared against the shipped strings. |
| FR-007 · every box unchanged | `test` | **met** — 44/24 at the same x, 20px mark at +24, title at +64, 42/23 chip, rows 56 and 80. |
| FR-008 · inline SVG, `currentColor`, `aria-hidden`, no pointer | `test` + `inspection` | **met** — the diff adds no `fill`, `style`, `width`/`height` on a mark, `tabindex` or event attribute; every mark keeps `aria-hidden="true"`. |
| FR-009 · five destinations; Search and Media Library unchanged | `test` | **met** — five buttons in rail order, five distinct path sets, no node shared with a media family. |
| US1 AC4 / SC-005 · one ink in both themes | `test` | **met** — each rail glyph's computed colour equals its button's, in both themes. |
| US3 AC3 / SC-004 · song and audio differ at 1:1 | `manual` | **checked by inspection** — on `/tatib/144/` from the slice's server: the song row draws the beamed pair, the audio chip the five-bar waveform, one above the other. |
| Edge · ≤560px rail, 20px marks | `inspection` | **checked** — at 425px the rail is the menu drawer (spec 138) and the stage marks keep their box; the row's mark is drawn from the same 24-unit grid. |
| Edge · missing / unavailable audio chip | `inspection` | **checked** — `renderRow` still chooses `missing` over the family, and the chip keeps `--danger`. |
| Edge · phone menu drawer | `inspection` | **checked** — the drawer is closed by default at 425px, and it renders the same rail markup. |

**Findings: 1 partial.**

- **`partial` — the responsive note named the wrong breakpoint.** `spec.md` said the rail drops to
  64px at 1272px; `tokens.css:114-116` narrows it at **560px** (1272px is where the sidebars become
  drawers, spec 138). The spec, plan and the manual task were corrected to 560px. No requirement
  changed: FR-007 pins each mark's box by name, and the marks scale with their own 24-unit grid at
  every width. Recorded here rather than reopened at Specify because the requirement never depended on
  the sentence — the sentence was wrong about the product, not the product about the requirement.

**Evidence run**: `tests.e2e.test_rail_marks` — 7 tests, OK. `tests.e2e.test_stage_kind_marks` —
11 tests, OK, with no edit to that file.

**Outcome: converged.** No missing, contradicting or unrequested behaviour; the one partial is a
corrected sentence.

## Pass 2

Not run. Pass 1 found no gap to re-check, and the evidence run is the same code the first pass
measured.

## History

- 2026-10-29 — pass 1: 14 rows checked (9 `test`, 4 `inspection`, 2 `manual`), 1 partial (breakpoint
  text), 0 missing, 0 contradicts, 0 unrequested. Converged.
