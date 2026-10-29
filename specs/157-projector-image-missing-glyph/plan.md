# Implementation Plan: the projector's image placeholder waits for the image to fail

**Spec**: `specs/157-projector-image-missing-glyph/spec.md`
**Branch**: `fix/157-projector-image-missing-glyph`
**Bump**: `patch` — `1.22.10` → `1.22.11` (re-read immediately before the merge, VER-04)
**Preview**: `specs/157-projector-image-missing-glyph/preview/preview.html` — static, two boards from the
frozen stylesheet

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Django template (Django 4.0) and JavaScript (ES5) in `static/web/projector.js`; Playwright (Python) for the tests |
| Primary dependencies | none added |
| Storage | none; the state is the DOM's and the object URL's |
| Testing | `tests/e2e/test_image_display.py` — two new cases; the module's existing cases, including the 404 one, unchanged |
| Target platform | every browser the app supports; the projector is a display page (dark, fixed) |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none; the same request, the same one paint |
| Constraints | no CSS change (D004); no route, payload or copy change; the 404 case keeps its assertion; the four sibling placeholders keep their behaviour |
| Scale / scope | one template line, three lines in `projector.js`, two E2E cases, one capability requirement at Fold |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply; the
constraint row above stands in its place.

Re-checked after Phase 1: pass — the design adds no file to the product, no request and no state.

## Phase 0 — Research

See `research.md`. Six decisions, each read or measured: the attribute (D001), the markup ships hidden
(D002), leaving a screen clears the failed state (D003), no CSS change (D004), one new case per state
(D005), `bump: patch` (D006). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the image screen's three states, the placeholder's two fields, three invariants.
- `contracts/` — `none` (`contracts/none.md`): no interface changes.
- `quickstart.md` — the isolated database, the two cases, the module, the preview probe and the manual
  live row.

### The design

`multimedia/web/templates/reading/projector.html:46` — the image box's placeholder starts hidden, like the
four below it:

```django
<svg class="screen__image-missing" viewBox="0 0 48 48" aria-hidden="true" hidden>…</svg>
```

`static/web/projector.js` — `renderImageScreen` (`:211`) toggles the attribute, not the property:

```js
var missing = host.querySelector('.screen__image-missing');
image.hidden = true;
missing.setAttribute('hidden', '');          // was: missing.hidden = true
…
}).catch(function () {
  if (token === imageToken && host === imageHost) missing.removeAttribute('hidden');   // was: = false
});
```

and `clearImageScreen` (`:198`) drops a failed state with the screen it belongs to, as `clearVideoScreen`
(`:137`) already does:

```js
if (imageHost) {
  var image = imageHost.querySelector('.screen__image');
  if (image) { image.hidden = true; image.removeAttribute('src'); }
  imageHost.querySelector('.screen__image-missing').setAttribute('hidden', '');
}
```

`tests/e2e/test_image_display.py` — two cases beside the existing ones, both driven by `_page` and the
same Space/`Control+ArrowRight` reach:

```python
def test_projector_loaded_image_shows_no_placeholder(self):
    page = self._page(f'/projector?service={self.service.pk}')          # 200, a real PNG
    …reach the image screen…
    expect(page.locator('.screen.is-active .screen__image')).to_be_visible()
    expect(page.locator('.screen.is-active .screen__image-missing')).to_be_hidden()

def test_a_pending_image_screen_paints_nothing(self):
    page = self._page(..., pending=True)                                # the route never fulfils
    …reach the image screen…
    expect(page.locator('.screen.is-active .screen__image')).to_be_hidden()
    expect(page.locator('.screen.is-active .screen__image-missing')).to_be_hidden()
```

`_page` grows one keyword: `pending=True` registers a handler for the file URL that returns without
fulfilling, so the screen stays in its pending state without touching the product.

**What is deliberately not done.** No CSS change (D004), no class, no `style.display`, no new element or
wrapper, no change to `media-image.js`, to the audio/video/PDF/slides paths, to the preview modal's
placeholders (`<div>`s that already work) or to the 404 case's assertion.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 a loaded image screen paints no placeholder | `multimedia/web/templates/reading/projector.html:46`, `static/web/projector.js:219-233` | `test` → `tests/e2e/test_image_display.py::ImageDisplayE2ETests::test_projector_loaded_image_shows_no_placeholder` | red before the change: the glyph computes `block` |
| FR-002 a failed load paints the placeholder, not a picture | `static/web/projector.js:231-233` | `test` → `…::test_missing_preview_and_projector_icon` | the existing case, assertion untouched |
| FR-003 leaving a screen drops its failed state | `static/web/projector.js:198-209` (`clearImageScreen`) | `inspection` — the reset sits in the clear path, mirroring `clearVideoScreen` (`:137-143`) | no E2E can see it: the screen is `aria-hidden` while it is off-active — *checked by inspection* |
| FR-004 one mechanism, five placeholders | `projector.html:46` against `:47-49`; `projector.js:220`, `:232` | `test` → `…::test_a_pending_image_screen_paints_nothing` (the markup's own `hidden` carries it) | the four siblings read as `inspection` in the same task |
| FR-005 the E2E asserts both outcomes | `tests/e2e/test_image_display.py` | `test` → the two new cases plus the untouched 404 case | a fix without them would leave the blind spot |
| FR-006 nothing else changes | the diff | `inspection` — one template attribute, three script lines, no CSS | `static/styles/design/projector.css` untouched — *checked by inspection* |
| SC-001 loaded: placeholder `display: none`, picture centred | `preview/probe.py` | `inspection` — `loaded`: right board `none` / `960 ÷ 960`; left `block` / `920 ÷ 960` / `−40px` | the numbers the spec's UI/UX quotes — *checked by inspection* |
| SC-002 failed: glyph 80×80 on the middle, no picture | `preview/probe.py` | `inspection` — `failed`: `80×80 at x 920–1000` on both boards | *checked by inspection* |
| SC-003 pending: neither painted | `static/web/projector.js`, `projector.html:46` | `test` → `…::test_a_pending_image_screen_paints_nothing` | `preview/probe.py`'s `pending` row shows the same |
| SC-004 the module is red before, green after | `tests/e2e/test_image_display.py` | `test` → the recorded red run, then the module's own run | the red run is quoted in `analysis.md` |
| SC-005 audio, video, PDF and slides untouched | `projector.js:111`, `:159`, `:286`; their modules | `test` → `tests.e2e.test_audio_display`, `tests.e2e.test_video_display`, `tests.e2e.test_pdf_display` re-run | |
| US1 AC1 loaded: picture, no placeholder | as FR-001 | `test` → `…::test_projector_loaded_image_shows_no_placeholder` | |
| US1 AC2 failed: placeholder, no picture | as FR-002 | `test` → `…::test_missing_preview_and_projector_icon` | |
| US1 AC3 pending: neither | as SC-003 | `test` → `…::test_a_pending_image_screen_paints_nothing` | |
| US1 AC4 a screen that failed is drawn afresh on return | `projector.js:198-209`, `:213-214` | `inspection` — the clear resets it, and the next visit's render hides it before the fetch | *checked by inspection* |
| US2 AC1 loaded: placeholder not visible, picture is | as FR-001 | `test` → the loaded case | |
| US2 AC2 404: placeholder visible, picture is not | `tests/e2e/test_image_display.py:87-105` | `test` → the 404 case, unre-written | |
| Edge: the object URL is revoked on a move | `projector.js:202-207` | `inspection` — the arriving screen starts from its own hidden pair | *checked by inspection* |
| Edge: 200 with bytes that are not an image | `static/web/media-image.js:22`, `projector.js:231` | `inspection` — `mime()` throws, the catch paints the glyph | no case stubs it; `test_missing_preview_and_projector_icon` covers the rejection path it shares — *checked by inspection* |
| Edge: the fetch is aborted by a move | `projector.js:221-227` | `inspection` — the abort resolves through the catch and the token guard refuses the stale host | *checked by inspection* |
| Edge: an image wider than the stage | `preview/probe.py` at 1280×720 | `inspection` — picture 1109×624 at x 45–1154 (today) and 85–1194 (after): same 40px | *checked by inspection* |
| Live: the picture alone, then the glyph on a failed load | `/projector?service=<id>` from this worktree | `manual` — `preview/README.md`'s Live check: run, press Space and step to the image screen; then stop the `media` container and step back | |
**Verification split: 12 test · 9 inspection · 1 manual.**

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-006 each carry a row; all five SC and both stories' scenarios are mapped |
| Entity coverage | the image screen and the placeholder are in `data-model.md`; nothing persisted is added |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D006 in `research.md`, each read or measured |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 22 rows: 12 `test` · 9 `inspection` · 1 `manual` |
| `quickstart.md` runnable | yes — both cases and the module run on this worktree; the live row is the one `manual` |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/157-projector-image-missing-glyph/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/none.md  checklists/requirements.md
  preview/preview.html  preview/probe.py  preview/build_preview.py  preview/README.md  preview/assets/*.css
```

### Source

```
multimedia/web/templates/reading/projector.html   one attribute on the image box's placeholder (:46)
static/web/projector.js                           the attribute toggle (:220, :232) and the clear (:198-209)
tests/e2e/test_image_display.py                   two cases, and one keyword on _page
docs/spec/projector.md                            R3 at Fold
backlog/items/ITEM-164-projector-image-missing-glyph.md   card
backlog/board.md                                  the card's row
specs/README.md                                   the spec's index row, at Accept
VERSION, CHANGELOG.md                             patch bump and one line, at delivery
```

### Structure Decision

No new module, file or asset in the product: the defect is one attribute and one property in the function
that owns the screen, and the cases live in the module that already covers image display.
