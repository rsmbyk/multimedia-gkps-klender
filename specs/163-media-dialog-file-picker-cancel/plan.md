# Implementation Plan: dismissing the file picker leaves the New media dialog open

**Spec**: `specs/163-media-dialog-file-picker-cancel/spec.md`
**Branch**: `fix/163-media-dialog-file-picker-cancel`
**Bump**: `patch` — 1.22.11 → 1.22.12
**Preview**: `live preview at http://localhost:8814/tatib/149/` — the slice's own worktree server, whose
origin the media companion admits (`GKPS_MEDIA_ALLOWED_ORIGINS` carries `http://localhost:8814`), so the
real picker, a real chosen file and the real save path are all reachable there.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript (ES5, no build step) in `static/web/media-entry.js`; Playwright (Python) for the tests |
| Primary dependencies | none added |
| Storage | none |
| Testing | `tests/e2e/test_media_library.py` — four new cases plus the module re-run |
| Target platform | every browser the app supports; the file input's `cancel` is Baseline (MDN: available since May 2023) |
| Project type | server-rendered Django app, vanilla JS |
| Performance goals | none; one comparison per dismissal event |
| Constraints | no markup, CSS, copy, endpoint or geometry change; the 150 ms closing motion and the other editor kinds keep their behaviour; the file input, its `change` path and the save flow are untouched |
| Scale / scope | one guard statement in `media-entry.js`, four E2E cases, one capability requirement (`reading/R32`), one card |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply; the
constraint row above stands in its place.

Re-checked after Phase 1: pass — the design adds no file, no request, no state and no new listener.

## Phase 0 — Research

See `research.md`. Four decisions: guard on the event's target (D001), test the event path rather than the
native picker (D002), keep a case that fails if the fix goes too far (D003), and take the live readout on
this worktree's own server, which the companion admits (D004). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the three things the change touches (the `cancel` event, the file input, the dialog)
  and the invariants the slice adds.
- `contracts/` — `none` (`contracts/none.md`): no interface changes.
- `quickstart.md` — the isolated-DB command for the two cases, the module run, and the live route.

### The design

`static/web/media-entry.js:19` — one statement, before the form check:

```js
editorDialog.addEventListener('cancel', function (event) {
  if (event.target !== editorDialog) return;      // a descendant's cancel is not the dialog's own
  if (editorDialog.querySelector('form[data-entry-form="media"]')) {
    event.preventDefault(); editorDialog.close();
  }
});
```

Everything else stays: the wrapped `close()` above it (`:10-18`), the 150 ms `media-closing` class, the
error dialog's own listeners (`:31-34`), `input.onchange` (`:201`) and the submit path (`:208-243`).

`tests/e2e/test_media_library.py` — four cases beside `test_media_create_picker_defaults_to_upload_and_save_stays_disabled`:

```python
def test_dismissing_the_file_picker_leaves_the_new_media_dialog_open(self):
    page = self.connected_page(reverse('web-tatib-service', args=[self.service.pk]))
    page.locator('[data-entry-open="media"]').first.dispatch_event('click')
    expect(page.locator('form[data-media-create]')).to_be_visible()
    page.locator('form[data-media-create] [name="title"]').fill('Closing hymn')
    page.locator('input[data-media-file]').dispatch_event('cancel', {'bubbles': True})
    page.wait_for_timeout(400)                       # past the 150ms close the defect takes 165ms to finish
    dialog = page.locator('#editorModal')
    self.assertTrue(dialog.evaluate('dialog => dialog.open'))
    expect(page.locator('form[data-media-create]')).to_be_visible()
    self.assertEqual(page.locator('form[data-media-create] [name="title"]').input_value(), 'Closing hymn')
    expect(page.locator('form[data-media-create] .editor__save')).to_be_disabled()

def test_a_dismissed_picker_keeps_the_chosen_file(self):
    page = self.connected_page(...)
    ...  # choose a file through the hidden input, then send the input's `cancel`
    expect(page.locator('[data-media-selected-name]')).to_have_text('swatch.png')
    expect(page.locator('form[data-media-create] .editor__save')).to_be_enabled()

def test_a_picker_dismissal_keeps_the_library_selection(self):
    ...  # a library row selected, the input's `cancel` sent: dialog, tab and row all kept

def test_escape_still_closes_the_new_media_dialog(self):
    ...  # Escape on the dialog itself; gone within 400ms
```

**What is deliberately not done.** No `stopPropagation` on the input (D001), no flag set when the picker
opens, no change to the other dialogs' `cancel` listeners, no change to the 150 ms close, the templates,
the CSS, the companion or `entries.js`.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 a `cancel` closes a dialog only when its target is that dialog | `static/web/media-entry.js:20` | `test` → `…::test_escape_still_closes_the_new_media_dialog` (the dialog's own event still closes) and `…::test_dismissing_the_file_picker_leaves_the_new_media_dialog_open` (a descendant's does not) | both directions of the same rule |
| FR-002 a dismissal leaves the form as it was | `static/web/media-entry.js:20` | `test` → `…::test_dismissing_the_file_picker_leaves_the_new_media_dialog_open` | title kept, prompt still shown, Save still disabled |
| FR-003 Escape and Cancel still close | `static/web/media-entry.js:19-24`, `_entry_form.html:237` | `test` → `…::test_escape_still_closes_the_new_media_dialog`; `inspection` — the `.editor__cancel` path (`data-editor-close`) is untouched | |
| FR-004 nothing else changes | the diff | `inspection` — one statement added; no template, CSS, endpoint or copy change | |
| SC-001 the dialog and its form survive a dismissal | `static/web/media-entry.js:20` | `test` → `…::test_dismissing_the_file_picker_leaves_the_new_media_dialog_open` | asserted 400 ms after the event, past the 165 ms the defect takes |
| SC-002 a re-pick keeps the chosen file | `static/web/media-entry.js:20` | `test` → `…::test_a_dismissed_picker_keeps_the_chosen_file` | the browser reports a re-pick as `cancel` |
| SC-003 Escape still closes | `static/web/media-entry.js:19-24` | `test` → `…::test_escape_still_closes_the_new_media_dialog` | |
| SC-004 the existing suite stays green | `tests/e2e/test_media_library.py` | `test` → the module in full | assertions unchanged |
| US1 AC1 no file chosen | `static/web/media-entry.js:20` | `test` → the dismissal case | |
| US1 AC2 a chosen file survives | `static/web/media-entry.js:20` | `test` → the chosen-file case | |
| US1 AC3 a typed title survives | `static/web/media-entry.js:20` | `test` → the dismissal case | |
| US1 AC4 the library tab's selection survives | `static/web/media-entry.js:20` | `test` → `…::test_a_picker_dismissal_keeps_the_library_selection` | the input is present while the Upload panel is hidden, so the event path is the same |
| US2 AC1 Escape still closes | as FR-003 | `test` → `…::test_escape_still_closes_the_new_media_dialog` | |
| US2 AC2 Cancel still closes | `_entry_form.html:237` → `entries.js` (`data-editor-close`) | `inspection` — the handler is not in this diff and takes no `cancel` event | |
| US2 AC3 other editor kinds unchanged | `static/web/media-entry.js:19-24` | `inspection` — a text, song, scripture or section-break form has no file input, so its `cancel` always targets the dialog | |
| Edge: the same file re-picked | `static/web/media-entry.js:20` | `test` → the chosen-file case | |
| Edge: dismissed mid-inspect | `static/web/media-entry.js:20`, `:175-195` | `inspection` — `choose()` still resolves into the open form or the error dialog; the guard touches neither | |
| Edge: the error dialog is open | `static/web/media-entry.js:31-34` | `inspection` — `#mediaErrorDialog` is a sibling, so its `cancel` never reaches the editor's listener | |
| Edge: reduced motion | `static/web/media-entry.js:12` | `inspection` — the branch that decides the closing motion is above the guard and untouched | |
| Edge: reopened afterwards | `entries.js` (the form fetch on open) | `inspection` — the form is fetched per open; the guard holds no state | |
| Live: the real system picker, dismissed by hand | `http://localhost:8814/tatib/149/` | `manual` — open *New media*, click *Choose file to upload*, press Escape in the picker: the dialog stays; then Escape on the dialog: it closes | the one thing no test can drive |

**Verification split: 13 test · 7 inspection · 1 manual.**

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-004, SC-001…SC-004, US1 AC1…AC4, US2 AC1…AC3 and five edge cases each carry a row |
| Entity coverage | the three entities' fields and the invariants are in `data-model.md`; nothing added |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D004 in `research.md`, each with its measurement or read |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | `13 test · 7 inspection · 1 manual`, counted from the table above |
| `quickstart.md` runnable | yes — both runs were made on this worktree while specifying, and the live route was measured |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/163-media-dialog-file-picker-cancel/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md  fold.md
  contracts/none.md  checklists/requirements.md
```

### Source

```
static/web/media-entry.js                     one guard statement, line 20
tests/e2e/test_media_library.py               three cases in MediaLibraryE2ETests
```
