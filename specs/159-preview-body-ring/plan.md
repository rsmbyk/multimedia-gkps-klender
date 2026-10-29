# Implementation Plan: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md`
**Branch**: `fix/159-preview-body-ring`
**Bump**: `patch` — 1.22.10 → 1.22.11
**Preview**: `static preview at specs/159-preview-body-ring/preview/preview.html` (panel **A** adopted)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript (ES5, `var` + function declarations) in `static/web/preview.js`; CSS in `static/styles/design/components.css`; Python 3.12 / Django for the server, untouched |
| Primary dependencies | none added |
| Storage | none; the only state is a class on one DOM element, for as long as a dialog is open |
| Testing | `tests/e2e/test_preview_body_ring.py` (new, five cases), plus the existing `test_entry_preview.py` and `test_audio_display.py` re-run unchanged |
| Target platform | browsers the app already supports — `<dialog>`, `showModal()` and `:focus-visible` are the mechanism |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none; one `classList` write per space press |
| Constraints | the body keeps focus (FR-003 depends on it); the ring's geometry and colour unchanged; no template change; image and PDF previews untouched |
| Scale / scope | 1 CSS declaration, ~6 lines in `preview.js`, 1 new E2E module, card + spec + board |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
constraint row above stands in its place.

Re-checked after Phase 1: **pass** — the design adds no file to the product, no request, no stored
value and no template hook.

## Phase 0 — Research

See `research.md`. Five decisions, each decided by a code read or a measurement: a state class rather
than a focus move (D001), the class's lifetime across previews (D002), measuring the painted outline
rather than `:focus-visible` (D003), a new E2E module on the audio-display fixture (D004), and
`patch` (D005). **Unknowns remaining: 0.**

One finding is carried to gate 2 rather than fixed here: SC-001's *How it is measured* cell names
`:focus-visible` false, which no correct fix can produce while the body keeps focus (D003).

## Phase 1 — Design

- `data-model.md` — the body's three focus states and the invariants that tie them to the dialog's
  lifetime.
- `contracts/` — `none` (`contracts/none.md`): no interface changes.
- `quickstart.md` — the DB-isolated setup, the new module, the two modules that must stay green.

### The design

`static/styles/design/components.css` — one declaration beneath the body's existing focus rule at
`:2093`:

```css
.preview__body.is-shortcut:focus-visible { outline: none; }
```

`static/web/preview.js` — one helper, and four call sites:

```js
function markShortcut(on) { content.classList.toggle('is-shortcut', Boolean(on)); }
```

- the open path (`:496-517`) clears it, so a preview never inherits the last one's suppression (D002);
- the audio branch (`:579-585`) and the video branch (`:586-592`) set it as they call `player.toggle()`;
- the modal's keydown (`:571`) clears it on `Tab`, which is what makes panel A hold — the indicator
  returns to a reader who navigates, and the body never loses focus;
- the close handler (`:616`) clears it, alongside the other teardown there.

`tests/e2e/test_preview_body_ring.py` — five cases on the `test_audio_display.py` fixture shape (a
`MediaIdentity` per family, one MEDIA entry, `page.route('http://127.0.0.1:63174/v1/files/<sha>')`):

1. `test_a_space_press_leaves_no_ring_on_the_audio_preview` — pointer open, space, click in the body,
   space again: `getComputedStyle(body).outlineStyle === 'none'` at every step, `data-playing` true.
2. `test_a_space_press_leaves_no_ring_on_the_video_preview` — the same for a video identity.
3. `test_a_keyboard_opened_preview_wears_the_ring_until_the_first_space` — focus the opener, `Enter`,
   outline is `2px solid rgb(28, 92, 60)` at offset `-2px`; one space → `none`.
4. `test_tab_brings_the_ring_back_after_a_space_press` — space, then Tab to the body: the outline is
   drawn again, at the same width, colour and offset.
5. `test_the_next_preview_gets_its_ring_back` — suppress in one preview, Escape, open the next by
   keyboard: the ring is painted (D002's trap).

**What is deliberately not done.** No focus is moved or blurred (D001); `.focus-restore-quiet` is not
reused; the body keeps `tabindex="0"`; `media-audio.js`, `media-video.js`, the templates and the
image / PDF preview paths are untouched; the ring's geometry, colour and offset are not touched.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 a key that operates the player leaves no indicator, including clearing one the dialog drew | `components.css` (new rule), `preview.js:496-517`, `:579-592` | `test` → `test_preview_body_ring::test_a_space_press_leaves_no_ring_on_the_audio_preview`, `::test_a_space_press_leaves_no_ring_on_the_video_preview`, `::test_a_keyboard_opened_preview_wears_the_ring_until_the_first_space` | computed outline `none` after every press (D003) |
| FR-002 the ring stays available by Tab, same geometry and colour | `preview.js` Tab clear; `components.css:2093` unchanged | `test` → `::test_tab_brings_the_ring_back_after_a_space_press`; `inspection` — the rule at `:2093` is byte-identical in the diff | `2px solid rgb(28, 92, 60)` at `-2px` |
| FR-003 arrow scrolling and the edge guard | `preview.js:476-484` (untouched) | `test` → `test_entry_preview.py::…::test_clicking_long_preview_text_allows_arrow_key_scrolling`, `…::test_short_preview_arrow_keys_do_not_scroll_the_page` | unchanged cases |
| FR-004 nothing else changes | the diff | `test` → `test_audio_display.py::…::test_preview_plays_seeks_and_closes`, `test_entry_preview.py` module; `inspection` — the diff is one declaration, one helper and four call sites | |
| US1 AC1 audio preview, pointer open + space | as FR-001 | `test` → `::test_a_space_press_leaves_no_ring_on_the_audio_preview` | |
| US1 AC2 video preview, pointer open + two presses | as FR-001 | `test` → `::test_a_space_press_leaves_no_ring_on_the_video_preview` | |
| US1 AC3 keyboard open, then space | as FR-001 | `test` → `::test_a_keyboard_opened_preview_wears_the_ring_until_the_first_space` | panel A |
| US1 AC4 Tab, space, Tab | `preview.js` Tab clear | `test` → `::test_tab_brings_the_ring_back_after_a_space_press` | |
| US2 AC1 Tab draws the ring | `components.css:2093` | `test` → the same case | |
| US2 AC2 arrows scroll an overflowing body | untouched | `test` → the spec-071 cases above | |
| Edge: image and PDF previews unchanged | `preview.js` — the class is set only in the audio and video branches | `inspection` — unreachable there; `test` → `test_image_display.py`, `test_pdf_display.py` re-run | |
| Edge: the seek bar keeps space | `preview.js:581`, `:588` | `test` → `::test_a_space_press_leaves_no_ring_on_the_audio_preview` moves the seek first; `inspection` — the guard is unchanged | |
| Edge: Escape still closes | `preview.js:606-610` | `test` → `test_preview_plays_seeks_and_closes` | |
| Edge: click in the body, then space | `preview.js:470-474` | `test` → `::test_a_space_press_leaves_no_ring_on_the_audio_preview` | the click cannot clear the ring, and no longer needs to |
| Edge: the next preview gets its ring back | `preview.js:496-517`, `:616` | `test` → `::test_the_next_preview_gets_its_ring_back` | D002 |
| SC-001 no indicator after one or two presses, both previews | the compose page after the merge | `manual` — `collectstatic` in `web`, restart, open an audio preview, press space twice, Tab once | the measurement cell is D003's finding |
| SC-002 the player toggles on every press | `media-audio.js`, `media-video.js` (untouched) | `test` → the new cases assert `data-playing`; `test_preview_plays_seeks_and_closes` unchanged | |
| SC-003 Tab draws `2px rgb(28, 92, 60)` at `-2px` | `components.css:2093` | `test` → `::test_tab_brings_the_ring_back_after_a_space_press` | |
| SC-004 otherwise pixel-identical to 1.22.10 | the diff; the dialog's box and padding | `inspection` — no template, no geometry token, no copy change; `manual` — a 1512 × 900 screenshot after the merge | |

**Verification split: 17 test · 5 inspection · 2 manual** across 19 rows — five rows name a second
method, so the three counts do not sum to the row count.

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-004 and US1 AC1–AC4, US2 AC1–AC2 each carry a row; every SC is mapped |
| Entity coverage | the body's three focus states and their transitions are in `data-model.md`; nothing stored |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D005 in `research.md`, each with a code read or a measurement |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 17 `test` · 5 `inspection` · 2 `manual` across 19 rows; every `test` row names its module and function |
| `quickstart.md` runnable | yes — the three commands run on this worktree against `gkps159`; two rows are marked not-yet-runnable with their reason |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/159-preview-body-ring/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md  fold.md
  contracts/none.md  checklists/requirements.md  preview/{preview.html,README.md,build_preview.py,assets/}
```

### Source

```
static/styles/design/components.css          one declaration beside :2093
static/web/preview.js                        markShortcut() + four call sites
tests/e2e/test_preview_body_ring.py          five cases
docs/spec/reading.md                         R31 at Fold
backlog/items/ITEM-171-preview-body-ring.md  card
backlog/board.md                             the card's row
specs/README.md                              the spec's index row
VERSION, CHANGELOG.md                        patch bump and one line, at delivery
```

### Structure Decision

No new product module. The rule lives beside the ring it replaces, the state lives in the script that
owns the shortcut, and the cases live in a module of their own because no existing preview module has
a media fixture.
