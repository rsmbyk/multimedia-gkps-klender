# Verse reference notice — preview (spec 232)

One self-contained page: **`index.html`**. Open it directly or in the chat preview frame.

It is assembled from the product's own materials, not drawn to look like them:

| Part | Where it comes from |
| --- | --- |
| tokens, light and dark | `static/styles/design/tokens.css`, inlined verbatim |
| editor dialog, large frame, head/field/buttons/help, narrow-width rule | `static/styles/design/components.css`, 128 lines inlined verbatim by `build.py` |
| form markup | `reading/_editor_form.html` (verse kind, referenced), same classes and button order |
| notice variants and the toolbar | `preview/template.html` — preview-only CSS/JS |

`build.py` reads the two stylesheets plus `template.html` and writes `index.html`. Nothing is fetched
at runtime, so the page works from `file://` and inside the sandboxed chat preview.

## States — all reachable by hand

- **Notice**: `Current` · `A · Callout` · `B · Inline` · `C · Banner`
- **Count**: `1` or `3` Tata Ibadah (checks the copy's number)
- **Theme**: `Light` or `Dark`

The footer reports live measurements of the notice box, the disabled `Delete verse` button and
the dialog: width × height, top offset, computed font, background, ink and button opacity.

## The four notices

- **Current** — shipped behaviour: 12px `--head-ink` line below the action row, disabled button
  faded to `opacity: .5`. It is the control column, kept so the alternatives can be compared.
- **A · Callout** — 476 × 62 at y353; `--rail-bg` panel, 1px `--divider`, 9px radius, 18px info
  glyph, `Delete unavailable` 13px/600 over `Used in 1 Tata Ibadah.` 12px/18. Sits between the
  field and the buttons, 12px above them. Button stays faded.
- **B · Inline** — 215 × 36 at y430, one line in the action row left of the buttons, 15px lock
  glyph, count in 700 weight; button becomes neutral (`--rail-bg` + `--divider` + `--head-ink`,
  no opacity fade). Adds no vertical space.
- **C · Banner** — 476 × 57 at y123, directly under the header; danger-tinted surface
  (`color-mix(--danger 7%, --canvas)`), 3px danger left rule, 17px warning glyph, 12.5px/17.5
  copy naming both the count and what to do. Neutral button.

Nothing here changes the underlying rule: a verse named by a service cannot be deleted, and
the modal still states the count. Only the presentation of that constraint is in question.

```sh
python3 specs/232-verse-reference-notice/preview/build.py
```
