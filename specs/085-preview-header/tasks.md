# Tasks 085: Show the entry's identity in the Preview dialog's header

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/085-preview-header`)
- [x] Red — E2E: `tests/e2e/test_entry_preview.py` (6 of its 11 cases failed before the change)
      - [x] a titled Text entry shows its title in the header and not in the body
      - [x] an untitled Text entry shows no header and keeps the `Preview` label
      - [x] a passage shows its reference in the header
      - [x] a song shows its heading and verse tabs in the header, and the tabs still swap verses
      - [x] the header does not scroll with the body
- [x] Green — `_preview_modal.html` gains the header shell; `preview.js` lifts the payload's own
      identity (`.preview__ref` / `.preview__song`) and its `.preview__tabs` into it, wires the tabs
      dialog-wide, clears the header on close, and points `aria-labelledby` at the title;
      `components.css` gains the header rules. **`tatib.html` needed no change** — lifting the
      payload's own nodes keeps one source of truth instead of copying the strings into JS.
- [x] Confirm the footer suites stay green: `tests/e2e/test_text_screen_breaks.py`,
      `tests/e2e/test_unified_text_screen_mode.py`, `tests/e2e/test_single_screen_text_breaks.py`
- [x] Confirm `tests/e2e/test_tatib_hover.py` stays green (origin highlight behind the backdrop)
- [x] Run the targeted suites only: `tests/e2e/test_entry_preview.py` plus the four modules above
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open;
      Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
