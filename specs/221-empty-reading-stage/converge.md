# Converge: spec 221 — an empty reading stage after deleting the open record

**Spec**: `specs/221-empty-reading-stage/spec.md` (Accepted, Gate 1 2026-11-22)
**Plan**: `specs/221-empty-reading-stage/plan.md` · **Tasks**: `specs/221-empty-reading-stage/tasks.md`
**Branch**: `fix/221-empty-reading-stage`

## Phase 1: Convergence

Every traceability row was re-assessed by the method it declared, not by its checkbox.

| Row / group | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| US1/AC1 — song delete leaves a nothing-open stage | test | `tests/e2e/test_deleted_stage.py::test_deleting_the_open_song_leaves_a_nothing_open_stage` green; asserts `data-read=on`, `data-home=reading`, parent URL with `stage=empty`, title and hint | checked |
| US1/AC2 — no search surface, song list beside it | test | same test: `#searchHome` hidden, `section=kidung`, `#chList` still rendered | checked |
| US1/AC3 — reload keeps the state | test | `test_reloading_the_empty_stage_keeps_the_reading_view` green | checked |
| US1/AC4 — Back does not revisit the deleted song | test | same test: `history.length` unchanged across replaceState and Back lands on the songbook list | checked |
| US1/AC5 — refused delete leaves the stage alone | inspection | `editor_delete()`/`editor_delete_confirm()` untouched; failure path in `editors.js` still only announces and never navigates | checked by inspection |
| US2/AC6 — service delete | test | `test_deleting_the_open_service_keeps_the_reading_stage` green | checked |
| US2/AC7 — template keeps its mode | test | `test_deleting_the_open_template_keeps_its_mode_and_the_stage` green; URL keeps `mode=template&stage=empty` | checked |
| US2/AC8 — songbook delete | test | `test_deleting_the_open_songbook_keeps_the_reading_stage` green | checked |
| US3/AC9 — off-stage delete unchanged | test | `test_deleting_another_row_keeps_the_open_song_on_stage` green; stage text/URL/datasets byte-identical | checked |
| US3/AC10 — chrome unchanged | inspection | diff touches only the three views' empty branch, the base article, `tatib.html`'s empty guard, the two CSS groups, the delete URL and one comment; `test_reading`, `test_tatib_templates`, `test_navigation_freshness` green apart from the listed baseline failures | checked by inspection |
| FR-001 — stage copy and no search | inspection | `views._empty_stage_context()`, `base.html` article branch, `components.css` rules; E2E asserts the rendered nodes | checked by inspection |
| FR-002 — parent lists and modes | inspection | `parentListUrl()` unchanged; each view's `nav`/`ch` arguments unchanged; E2E asserts section and mode | checked by inspection |
| FR-003 — URL flag, reload, history | test | `test_reloading_the_empty_stage_keeps_the_reading_view` | checked |
| FR-004 — off-stage branch | inspection | `listUrl += ...` lies inside `if (onStage && window.gkpsNavigate)`; off-stage path unchanged | checked by inspection |
| FR-005 — copy uses existing empty-song classes, one icon/centring CSS group | inspection | `base.html` uses `.entry__empty*`; `components.css` adds only icon sizing and the empty-kind stage centring | checked by inspection |
| FR-006 — refusals excluded | inspection | guard endpoints unchanged, no new path to the empty stage on failure | checked by inspection |
| FR-007 — only R41's landing clause superseded | inspection | Fold block below replaces that clause and keeps row removal, neighbour focus, history replacement | checked by inspection |
| SC-001–SC-004 | test | the four behaviours above, 7 tests in the new module, all green | checked |
| SC-005 — geometry | test | `test_the_nothing_open_stage_keeps_the_shell_geometry` green after the stage's existing 320ms fade-up settles: stage 648×900 at (792,0), block 648×108 at y=396, icon 38px; narrow stage 390×844, block y=368; no overflow | checked |
| UI/UX numbers | manual | preview toggles Before/After, dark and 390px; live slice server at 8771 measured the same boxes and the same copy on `/songs/book/36/?stage=empty`, `/tatib/?stage=empty` and `/tatib/?mode=template&stage=empty` | checked |

### Findings

1. **Implementation detail (not a spec conflict)** — `tatib.html` also renders its own
   `.entry__empty` ("This Tata Ibadah is empty.") when a list page has no items. With `read_hint` set
   it would have produced two invitations in the stage, and the shell's node reconciliation kept the
   first title. The guard now includes `and not read_hint`; evidence: the service and template E2E
   tests went from title `This Tata Ibadah is empty.` to `Nothing open.`.
2. **Implementation detail** — the empty article carries `data-kind="empty"`. It scopes the two
   centring CSS rules away from the existing empty-Tata-Ibadah stage, and makes `readKind()` report no
   section so the next on-stage delete is judged correctly.
3. **Test-only adjustment** — the geometry test waits for `document.getAnimations()` to finish;
   the shell's existing `.read__body` fade-up otherwise left the block 6px low at measurement time.
4. **Baseline red, not this slice** — `test_reading::test_the_panel_shows_its_empty_view_when_no_songbook_exists`
   fails identically on unmodified `develop`; five `test_editor` failures (four date-picker cases and
   the pointer row-control case) also fail on `develop`. `test_a_created_service_opens_its_contents_pane`
   failed once in a 178-test batch but passes on both the slice and `develop` in isolation.

No row is missing, partial, contradictory or unrequested against the accepted spec. Outcome: **Converged**.

## Phase 2: Convergence

Not needed — no gaps found in pass 1.
