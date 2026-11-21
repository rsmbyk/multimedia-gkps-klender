# Quickstart — spec 212

## The change

One block in `static/styles/design/components.css`, immediately after the existing
`.editor__confirm` rule (line 2648). It is the same fifteen lines `preview/candidate.css` carries:

```css
.editor__confirm-layer { position: absolute; inset: 0; z-index: 4; display: grid;
  place-items: center; padding: 16px; border-radius: 14px; background: var(--backdrop); }
.editor__confirm-layer[hidden] { display: none; }
.editor__confirm-layer .editor__confirm { box-sizing: border-box; display: block;
  width: min(468px, 100%); padding: 22px; border-radius: 12px;
  background: var(--canvas); color: var(--ink); box-shadow: var(--shadow); }
.editor__confirm-layer .editor__confirm h3 { margin: 0 0 10px;
  font: 650 18px/1.25 ui-sans-serif, system-ui, sans-serif; }
.editor__confirm-layer .editor__confirm p { margin: 0 0 20px; color: var(--ink);
  font: 400 13.5px/1.55 ui-sans-serif, system-ui, sans-serif; }
.editor__confirm-layer .editor__confirm-actions { display: flex;
  justify-content: flex-end; gap: 8px; }
```

## Preview (no server)

```sh
.venv/bin/python specs/212-copy-confirm-layer/preview/probe.py
```

Prints one JSON object with `proposed` and `current` and writes `shots/{proposed,current}.png`.
Open `preview/index.html` directly to toggle the two states by hand.

## The E2E lane

```sh
DJANGO_DEVELOPMENT_MODE=true .venv/bin/python manage.py test \
  tests.e2e.test_tatib_templates.TataIbadahTemplateE2ETests \
  --keepdb --noinput
```

Against a worktree, point `DATABASE_URL` at a throwaway database so a parallel session cannot hold the
test database:

```sh
export DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:<port>/gkps212"
```

Both new tests live in `TataIbadahTemplateE2ETests`; they open a template's Edit modal through the
sidebar's own row button (`[data-editor-open="tatib"]`), press `[data-copy-open]`, and read the
confirmation's computed layout. They assert no database state, so nothing has to be closed before
asserting.

## What each test proves

| Test | Proves |
| --- | --- |
| `test_the_copy_confirmation_covers_the_form` | the layer's box equals the dialog's, the dialog's height does not change when it opens, `elementFromPoint` at the form's Save resolves inside the layer, the layer's radius is 14px, and `hidden` still hides it after Cancel |
| `test_the_copy_confirmation_card_matches_the_preview` | the card's 448 × 176.3 (± 1), 22px padding, 12px radius, canvas fill and shadow; heading 18px/650; body 13.5px; actions right-aligned, 8px apart, 22px inside the card's right edge |

The existing `test_copy_as_template_asks_and_copies` stays as it is and proves the flow still copies.
