# Converge: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-25

| Requirement | Check | Evidence |
| --- | --- | --- |
| FR-001 | one block per list, centred on the pane | `preview/probe_empty_states.py` at 1440×900: `dvCenter`/`dhCenter` = `0.0` for the empty sections, the filtered sections, the filtered panel and the empty songs states; the E2E asserts both offsets ≤ 1.5px |
| FR-002 | glyph above title above hint | `base.html`: one `span.listempty__icon[data-when]` pair, then `p.listempty__title`, then `p.listempty__hint`; measured ink block 433–547px tall in a 820px pane |
| FR-003 | typed from the rows, not the filter field | `reading.js` `applyFilter`/`applySongFilter` count `total` and `any`; the E2E reads `empty` → `filter` → `hidden` on the same list as the filter changes |
| FR-004 | each section names its own list | `ReadingViewTests` copy tests for books/songbooks/Tata Ibadah and for songs/sections; live read of `/bible/` `No matching books.`, `/songs/` `No matching songbooks.`, `/tatib/` `No matching Tata Ibadah.` |
| FR-005 | section glyph vs magnifier-with-cross | probe reports `iconFor: empty` / `iconFor: filter`; the two SVGs are separate spans, and only one is displayed |
| FR-006 | a page that arrives empty is painted at boot | probe: `/tatib/148/` and `/songs/book/36/` show the empty copy without a keystroke (before the boot paint both read `hidden: true` — research D004) |
| FR-007 | swap keeps the block in step | `reconcileNode` on both blocks; read in the browser: empty service → rail Alkitab → `chEmpty` hidden with `No chapters.` copied, panel copy `No books yet.`; rail Kidung → `No songs yet.`; `tests.e2e.test_targeted_reading_updates` 6 OK |
| FR-008 | saved renderer writes the section's copy and glyph | `offline-render.js` `labelListEmpty` + `paintListEmptyStates` from both renderers; `tests.e2e.test_saved_render_parity` 6 OK |
| FR-009 | deleting the last row shows the empty copy | `entries.js` calls `window.shellListEmpty(node, false, 0)`; inspection of the handler, plus the row-disappearance path covered by the entry-delete suites |
| FR-010 | hidden in the mini panel and beside chapters | probe: collapsed panel `display: none`; `applySongFilter` returns early for `alkitab`, leaving `#chEmpty` hidden |
| FR-011 | the old paragraphs are gone | `grep -rn "panel__empty\|ch__empty\|ch_empty_text\|panel_empty_text"` over the repo → no hits |
| SC-001 | ink centred | the four probe readings, both offsets 0.0px |
| SC-002 | empty and filtered read differently | the six copy pairs in `data-model.md`, read from the served HTML and in the browser |
| SC-003 | one sentence per list per column | the three `ReadingViewTests` copy tests |
| SC-004 | saved copy equals the server's | the renderer writes the same strings by construction; the parity suite proves nothing regressed. **Gap (accepted)**: no assertion compares the two blocks' copy saved-versus-server field by field — see A1 |
| SC-005 | nothing else moves | `manage.py test multimedia.web` 310 OK; `ServiceReorderPaneTests` clean on both branches |

**Outcome**: no `missing`, `contradicts` or `unrequested` gap. Two `partial` items were closed during the run
rather than recorded as gaps:

- **the divider row** — a list holding only a section break counted as empty and printed "No sections yet."
  over the divider. `applySongFilter` now treats a visible `.toc__eos` as a row, and the boot paint counts
  both kinds. Read in the browser on `/tatib/144/` with every section row removed: the block stays hidden;
  filtering it shows the empty copy, since a divider is not a section.
- **the identity of the miss glyph** — the first cut slashed the whole magnifier; the cross now sits inside
  the lens, which the review read as "nothing matched" rather than "search unavailable".

## Pass 2 — 2026-10-25

Every requirement re-read against the shipped diff, then the touched module re-run after the fold, the
changelog entry and the bump: `manage.py test multimedia.web` — 310 OK. The browser test was re-run after the
divider change: 1 OK in 8.4s. The probe was re-run at the same time and still reports `0.0` on all four
states at 38px glyphs.

No requirement moved between the passes; the two `partial` items above were the only ones, and both were
fixed before the fold rather than accepted.
