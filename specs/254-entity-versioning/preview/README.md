# Preview: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`
**Shape**: `static`
**Open**: `specs/254-entity-versioning/preview/index.html`

## Run

none: open the file directly. It links the repo's real `tokens.css`, `fonts.css` and `components.css` by relative path.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Song referenced | default, or click `Song · 2 services` | 480×157 confirmation; note reads `Used in 2 Tata Ibadah — delete unavailable`; Delete disabled at 0.5 opacity |
| Songbook referenced | click `Songbook · 1` | Same frame; count 1; `Delete songbook` disabled |
| Verse modal | click `Verse modal` | 840×760 large frame; note leads the action row; Delete verse disabled |
| Unreferenced control | click `Unreferenced control` | No note; Delete enabled at full opacity |
| Dark | click `Dark` | All four states with the product's dark tokens |

Each state is a native `<dialog>` opened with `showModal()`, so the backdrop and centring match the product.

## What is not a preview

A static page cannot show server-rendered context: the count is hard-coded here, and the delete POST is not made. The markup, class names, stylesheet, tokens, fonts, disabled state and `aria-describedby` wiring are the product's own.

## Measured with the repo's Playwright

`probe.py` (run with the main checkout's `.venv/bin/python`) writes `shots/probe.json` and screenshots:

- 1440×900: toolbar 1440×53; confirmation dialog at (440, 372), 560×157; verse modal at (300, 70), 840×760.
- Note: `12px / 18px ui-sans-serif, system-ui, …`; colour `rgb(100, 99, 87)` light and `rgb(156, 154, 145)` dark; one line 265×18 in both frames.
- Action buttons: 38px high; disabled Delete at opacity 0.5; note is the first child of `.editor__actions` and is the button's `aria-describedby`.
- Candidate rule shown in this preview: delete confirmations are `min(560px, calc(100vw - 32px))` wide, the minimum at which both the song and songbook notices stay on one line with the default action buttons.
