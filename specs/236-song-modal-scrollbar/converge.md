# Convergence: song entry modal scrollbar

**Spec**: `specs/236-song-modal-scrollbar/spec.md`
**Plan**: `specs/236-song-modal-scrollbar/plan.md`
**Traceability rows checked**: 16 (12 `test`, 4 `inspection`)

## Phase 1: Convergence

**What was checked**: the working tree against every row in `plan.md` §Traceability — the one
declaration in `static/styles/design/components.css`, the new E2E module, the self-contained
preview and its verifier, the board card and the inspection observables. No diff against history
was used as evidence.

**Typed findings**:

| Type | Finding | Evidence / disposition |
| --- | --- | --- |
| `missing` | none | all 16 rows have an implementing component and a verification |
| `partial` | none | US1/US2/US3, FR-001–004 and SC-001–004 each have a named test or an inspection observable |
| `contradicts` | none | code and spec agree: dialog non-scrollport, content wrapper unchanged |
| `unrequested` | none | product diff is four lines: three of comment and one declaration; no JS, template or endpoint change |

**Test evidence**: `manage.py test tests.e2e.test_song_modal_scrollbar --keepdb` — base:
3 failures (`'auto' != 'clip'` twice, wheel `10 != 0`); after the declaration: **7 tests, OK**.
The other four tests were green on both sides as regression guards (menu position, settled edit
box, tall-form inner scrolling at 1366×900 and 900×600).

**Inspection rows recorded** (T009):

- **FR-002** — computed `overflow-y: clip`; gutter `0px`; `scrollHeight` may still read 256px
  because clipped overflow still counts. Asserted in `test_new_song_dialog_has_no_scrollbar_gutter`.
- **FR-004** — `git diff` shows only `overflow: clip` plus its comment in `.editor`; 480px width
  asserted in both entry modes; 14px radius, the verse-panel animation and fixed menu rules are
  untouched; `test_new_song_results_menu_still_escapes_the_dialog` checks `position: fixed` and an
  unchanged dialog box.
- **SC-004** — preview readouts before `246/256px, 5px, auto` and after `246/256px, 0px, clip`;
  Edit song `410/410px, 0px` in both. The self-contained page passes the chat-frame verifier.
- **US3/AC3** — the date picker is a top-layer popover with no selector change in this slice, so
  the dialog's overflow declaration cannot clip it.

**INFO**: task T007 says "large text form" while the implemented fixture is a verse-heavy Edit
song form. Both exercise the same `.editor__content` scrollport; the wording is kept as the
approved task text, and the test module documents the fixture. No change.

**Outcome**: converged — zero CRITICAL, zero typed gaps, 16/16 rows checked. Unchecked tasks
T013/T014 belong to delivery after the push, not to Convergence.

## History

- 2026-11-24 — pass 1: 16/16 rows checked, no typed findings, one INFO wording record.
