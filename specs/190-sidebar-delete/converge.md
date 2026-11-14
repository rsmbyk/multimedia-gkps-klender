# Converge: spec 190 — sidebar delete buttons

**Pass**: 1 · **Date**: 2026-11-14
**Artifacts checked**: `spec.md`, `plan.md`, `tasks.md`, `analysis.md`, `checklists/requirements.md`, `preview/index.html`, code under `multimedia/web/` and `static/`
**Outcome**: Converged (1 pass; one `partial` resolved in-pass; one pre-existing observation).

| Requirement | Declared | Checked by | Finding | Disposition |
| --- | --- | --- | --- | --- |
| FR-001/002/003 (controls on eligible rows, guards, placement) | inspection | inspection | Live pages: 273 dated tatib rows + 22 template rows + 10 non-hymn songbook rows carry `.row-delete` beside `.row-edit`; hymn/restricted rows draw none (template guards + panel counts); same 26px box/reveal at `right: 38px` (pencil) / `right: 6px` (trash) — swap requested by owner 2026-11-14, measured | OK |
| FR-004 (dated row hides date on hover/focus) | inspection | inspection | Rule served and correctly scoped (CSSOM on live page: `@media (hover: hover) { li[data-editor-kind]:hover/focus-within .book__s }`); the hover mechanism itself proven live (hover drives the reveal the controls depend on). The `display: none` match itself is not observable in this environment: headless Chromium reports `hover: none`/`pointer: none`, so the media query correctly never matches there; headed launch unavailable. The state was demonstrated in the preview and accepted at Gate 1. | OK (checked by inspection; live-match limitation recorded) |
| FR-005/006/012 (confirm in shared modal, kind noun, reused classes) | inspection | inspection + test | Confirm fragment renders in the shared modal with `editor__danger`/`editor__cancel`; nouns verified live (`Delete template: …`) and by test. Header removed per owner revision 2026-11-14 (sr-only accessible name kept for `aria-labelledby`) | OK |
| FR-007 (`data-editor-kind` distinguishes templates) | test | test + inspection | Rows carry `data-editor-kind="tatib"` (273) / `"template"` (22) live; `nounFor`/delete kind ride it; cross-kind deletes refused by test | OK |
| FR-008/009 (POST delete + CSRF; GET confirm + POST delete endpoints) | test | test | `SidebarRecordDeleteTests` (10 tests): method enforcement (405s), unknown kind/kind mismatch 404s, hymn + deleted-songbook refusal, soft-delete and deactivate outcomes, fragment noun. Green with the editors and reading suites (91 tests) | OK — see F-001 |
| FR-010 (row removed from the correct panel) | test | test | Live Playwright flow on a throwaway record: hover → confirm → POST 200 → row gone, modal closed, neighbour focus | OK |
| FR-011 (on-stage delete replaces history) | test | test | Live Playwright: delete while `/tatib/<pk>/` on stage → POST 200, URL → `/tatib/`, `history.length` 4 → 4 (replaced, not appended) | OK |
| FR-013 (responsive/touch preserved) | inspection | inspection | Phone grid gains 74px clearance for rows with actions; touch/coarse rule covers both controls; no gesture rules touched | OK |

## Findings

- **F-001 — `partial` (resolved in-pass)**: the plan's traceability declared `test` for FR-008/009, but no tests existed when Converge entered. T014 appended (Converge's appended task) and implemented: 10 endpoint tests, green. Residual: none.
- **F-002 — observation (pre-existing, not this slice)**: `ServiceEntryViewTests` carries 3 failing song-entry verse tests (`test_creating_a_song_entry_stores_the_verses_it_includes`, `test_a_deleted_saved_song_remains_available_when_editing_its_existing_entry`, `test_the_song_fragment_checks_every_verse_of_its_song`). Verified red on clean `develop` (a11b35e2) in a throwaway worktree against a fresh database — identical failures, so not introduced by 190. Left as-is; fresh demand for the owner to card if wanted.

## Owner revisions during review (2026-11-14, all folded into the implementation)

- Swap the edit and delete button positions (delete takes the trailing edge).
- Remove the confirm modal's header (sr-only `#editorTitle` keeps the accessible name).
- Fix the confirm POST: `FormData` is read before `setDialogBusy` disables the fields — the CSRF token was being dropped, which produced the false "restricted" 403s.
- Map 403s honestly: the server's own "restricted" body keeps the restricted message; any other 403 (a refused CSRF check) reads "The change was refused. Reload the page and try again."

## Phase 1: Convergence

- Pass 1 (this file) — traceability walk against code, live probes (three throwaway records, cleaned up), and the new endpoint suite. Outcome: **Converged**; no `missing`/`contradicts`/`unrequested` gaps outstanding; cap not hit (1 pass).
