# Preview — spec 212

`index.html` is one static page: the real `<dialog class="editor">` shell, the real
`_editor_form.html` body the server sends for a template (*Model C Indonesia*), the real
`_copy_confirm.html` block with its `hidden` attribute removed, and the product's own
`tokens.css` and `components.css` from this worktree. `candidate.css` is the block this slice
proposes; the page's **Proposed CSS** button toggles it off, which is the state production
serves today.

Open it directly (`file://`) or in the desktop chat's preview frame. **Dark** switches the
theme through `data-theme`, so both token sets can be read on the same page.

```sh
.venv/bin/python specs/212-copy-confirm-layer/preview/probe.py   # prints both states as JSON
```

`probe.py` writes `shots/proposed.png` and `shots/current.png` (gitignored) and reports, per
state: the dialog's box, the layer's box and computed position/display/background, the card's
box and box-model, the heading and body type, the actions row's alignment, both button boxes,
and what `elementFromPoint` returns at the form's own Save button.

The numbers this page produces are the ones quoted in `spec.md`'s `## UI/UX` and asserted by
`tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_covers_the_form`.
