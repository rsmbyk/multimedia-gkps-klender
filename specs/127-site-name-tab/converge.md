# Convergence: The tab names the site, and the index's tab stops at the name

**Spec**: `specs/127-site-name-tab/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-24

| Requirement | Check | Evidence |
| --- | --- | --- |
| FR-001 | the three index routes read the site name alone | `/`, `/home/`, `/search` measured on the running branch: `Multimedia GKPS Klender`, nothing after it; `ReadingViewTests::test_the_index_tab_names_the_site_and_stops_there` asserts both the context value and the rendered `<title>` |
| FR-002 | every other page appends the name | `/bible/` `Alkitab — …`, `/bible/1/1/` `Kejadian 1 — …`, `/songs/` `Kidung — …`, `/songs/1013/` `PKJ 4 — …`, `/tatib/` `Tata Ibadah — …`, `/search?q=kasih` `Results for “kasih” — …`, `/media-library/` `Media Library — …` |
| FR-003 | leading text unchanged | the existing chapter, song and section title assertions pass unedited except for the suffix: `test_a_section_landing_puts_the_site_name_last`, the `page_title` pins at `multimedia/web/tests.py:167,183,306` |
| FR-004 | saved renderer writes both shapes | the four `document.title` writes in `static/web/offline-render.js` carry the name; the home one is the name alone. The parity regression's expectation was updated to `expected + ' — Multimedia GKPS Klender'` and compares saved against server |
| FR-005 | in-place edition switch | measured in headless Chromium: `/bible/1/1/` reads `Kejadian 1 — …`, and after the SIM switch `1 Musa 1 — Multimedia GKPS Klender` |
| FR-006 | visible and assistive text unchanged | `grep -rn "GKPS Klender" multimedia/web/templates` leaves the rail `aria-label`s, the logo `alt` and the maintenance title only |
| SC-001 | index string exact | the three route readings above |
| SC-002 | one reading per route | the nine readings in T012 |
| SC-003 | saved and server titles equal | the parity expectation; its browser run is the push step (accepted gap) |
| SC-004 | nothing else changed | `multimedia.web` 306 tests OK; `ReadingViewTests` 43 OK |

**Outcome**: no requirement gap. One thing the read caught before the run was the saved renderer's home
title, which would have kept the tagline and renamed the tab when the online update landed — it is T005, not
a line in T008.

## Pass 2 — 2026-10-24

Every requirement re-checked against the shipped diff, and the touched module re-run after the docs and
version changes: `multimedia.web` 306 tests OK. The titles were read a second time on the running branch —
server-rendered and after script — with the same results as Pass 1.

**Outcome**: Converged — nothing remains.

## Accepted gaps

- **The full browser tree was not run.** The touched classes were: `tests.e2e.test_saved_render_parity`
  (5 tests, saved-versus-server titles among its fields), `tests.e2e.test_reading`'s
  `test_reader_can_browse_and_read_a_song` and `test_sim_codes_titles_labels_and_fallback_follow_selected_edition`,
  and `tests.e2e.test_offline_library`'s `test_saved_sim_bible_copy_uses_sim_code_and_heading` — 9 tests, OK
  (2026-10-24). The rest of `tests.e2e/` did not see this change and was left to the merge step; the repo
  carries no CI since #371, so that step is manual.
- **No preview artifact.** The change is text in the browser's tab; the running branch is the reference and
  `quickstart.md` is the reading list.

## Cap reached

not reached
