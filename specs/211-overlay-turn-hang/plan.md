# Implementation Plan: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`
**Branch**: `feat/211-overlay-turn-hang`
**Bump**: `patch` (1.35.1 → 1.35.2)
**Preview**: `specs/211-overlay-turn-hang/preview/index.html` (static, real sheet, live readout)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, vanilla ES5-style JS, CSS with container units |
| Primary dependencies | Django `StaticLiveServerTestCase`, Playwright (Python) E2E |
| Storage | none — no model, field or payload change |
| Testing | `tests.e2e.test_obs_overlay` at 1280×720, `DJANGO_DEVELOPMENT_MODE=true` (SQLite) |
| Target platform | OBS browser source, the overlay page at `/obs/source/overlay` |
| Project type | server-rendered Django app with a browser-local paint layer |
| Performance goals | one `.some()` over a screen's lines per paint; one CSS `calc()` per continuation row |
| Constraints | no server-side classification, no new DOM node, no change to the mark grid or to voice colours |
| Scale / scope | two production files, five focused E2E cases with small fixtures, one capability block at Fold |

## Constitution Check

No `CONSTITUTION.md` exists in this repo (SDD-01); the check is recorded as not applicable.

Re-checked after Phase 1: not applicable — no principles to violate. The one cross-cutting concern,
the single `--speaker-col` measurement, is preserved by D002 and D006.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity added; one derived screen flag and one CSS class documented.
- `contracts/` — `none` (see `contracts/README.md`): no external interface changes.
- `quickstart.md` — focused E2E command, static preview and the Fold inspection.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/obs-overlay.js`, `static/styles/design/obs-overlay.css` | `test` → `tests/e2e/test_obs_overlay.py::test_a_continuation_hangs_at_the_marked_words` | first glyph at the marked words x |
| FR-002 | `static/styles/design/obs-overlay.css` | `test` → `...::test_a_continuation_hangs_at_the_marked_words` | indent is column + gap; no mark span on the row |
| FR-003 | `static/web/obs-overlay.js` | `test` → `...::test_a_no_mark_screen_keeps_its_continuations_flush` | no class, no variable, no indent |
| FR-004 | `static/web/obs-overlay.js` | `test` → `...::test_a_cue_and_an_ordinary_body_stay_flush` | empty voice stays at the content edge |
| FR-005 | `static/web/obs-overlay.js` | `test` → `...::test_a_continuation_hangs_at_the_marked_words` | `is-leader` and its colour are unchanged |
| FR-006 | `static/styles/design/obs-overlay.css` | `test` → `...::test_a_wrapped_continuation_keeps_every_row_at_the_words_column` | every glyph row at the column, ink inside the plate |
| SC-001 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_continuation_hangs_at_the_marked_words` | x equality within 1 px at 1280×720 |
| SC-002 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_wrapped_continuation_keeps_every_row_at_the_words_column` | row rects and plate content box |
| SC-003 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_no_mark_screen_keeps_its_continuations_flush` | both frames' lines at the same x |
| SC-004 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_liturgy_text_wears_a_plate_with_its_title_and_quieter_leader_lines` | existing plate, mark and colour assertions |
| SC-004 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_wrapped_speaker_line_hangs_under_its_words` | R5's own wrap and widest-column assertions |
| US1/AC1 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_continuation_hangs_at_the_marked_words` | the owner's screenshot case |
| US1/AC2 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_continuation_hangs_at_the_marked_words` | voice class and colour |
| US1/AC3 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_the_widest_mark_sets_the_continuation_column` | continuation and a new `J.` answer share the widest column |
| US2/AC1 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_no_mark_screen_keeps_its_continuations_flush` | mid-turn screen with no mark |
| US2/AC2 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_cue_and_an_ordinary_body_stay_flush` | cue line and its neighbour |
| US2/AC3 | `tests/e2e/test_obs_overlay.py` | `test` → `...::test_a_cue_and_an_ordinary_body_stay_flush` | unmarked body, no speaker |
| UI/UX | `specs/211-overlay-turn-hang/preview/index.html` | `inspection` — the measured readout shows −28.8 px before, 0.0 px after at 1280×720; the no-mark tab stays flush | approved at gate 1 |
| overlay/R5 | `docs/spec/overlay.md` | `inspection` — R5 carries the modified continuation rule and its scenario, with its existing scenarios intact | Fold target |

**Verification split**: 17 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/211-overlay-turn-hang/
  spec.md  plan.md  research.md  data-model.md  quickstart.md
  contracts/README.md  checklists/requirements.md
  preview/index.html  preview/README.md
```

### Source

```
static/web/obs-overlay.js             # screen flag + is-continuation class in plate()
static/styles/design/obs-overlay.css  # one padding-left rule beside .has-mark
tests/e2e/test_obs_overlay.py         # fixtures, nth-screen helper, five new cases
docs/spec/overlay.md                  # R5 modified at Fold
```

### Structure Decision

No new directories. The behaviour lives in the two files that already own the overlay's row
builder and the mark grid; the tests extend the module that already measures that grid. The
preview stays inside the slice as approved at gate 1.
