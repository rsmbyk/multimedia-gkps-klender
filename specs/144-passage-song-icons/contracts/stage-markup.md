# Contract — the stage row's kind mark

The slice exposes no external interface: no endpoint, serializer or form changes. The contract that
matters is between three things that already share the stage — the template, the stylesheet and the E2E
that measures it — so it is written down here.

## Markup

Inside a passage or song row only, as the **first child of the heading**, before the jump link:

```html
<section class="tatib__item tatib__item--entry tatib__item--acts tatib__item--song" …>
  <h2 class="read__sec"><span class="entry__kind-icon" aria-hidden="true" data-kind-icon="song"><svg viewBox="0 0 24 24">…</svg></span><a class="entry__jump" …>HAL 1 — Jahowa Sihol Pujionku</a></h2>
  <p class="read__sub">Bait 1-7</p>
  …
</section>
```

Guaranteed:

| guarantee | why it is a contract |
| --- | --- |
| `.entry__kind-icon` exists **only** on `tatib__item--scripture` and `tatib__item--song` rows | FR-001/002/004; the E2E counts it per kind |
| the mark is the heading's **first child**, never the section's | the section's `> :first-child` rule owns the heading's top margin (research D1) |
| `data-kind-icon="scripture" \| "song"` | lets a test assert which glyph a row got without parsing paths |
| `aria-hidden="true"`, no text content, no `tabindex` | FR-006; the row's accessible name must not change |
| the mark is painted only when the row has a heading | a heading-less row has no line for it to sit on |
| the row carries `tatib__item--scripture` / `--song` | the stylesheet's only selector hook for the mark and its indent |

Not guaranteed (free to change): the SVG path data, the element's tag (`span` today), and the glyph's
internal proportions.

## Geometry

| property | value | source |
| --- | --- | --- |
| `.entry__kind-icon` box | `20 × 20`, `position: absolute`, `left: 24px`, `top: 50%`, `translateY(-50%)` | research D3 |
| its centre line | 34px from the row's left edge — the media chip's own centre | `13px + 42px/2` |
| `.tatib__item--scripture` / `--song` | `padding-left: 64px` — the media row's column | `components.css:2008` |
| glyph paint | `--head-ink`; 1.8 stroke, round caps, no fill | research D4/D5 |

Invariants that must survive the change: a passage row stays **56px** tall; the heading's first line
stays on the row's centre line; nothing else on the stage moves; the only permissible size change is a
song title wrapping because the title column is 250px instead of 302px.

## Test hooks

`tests/e2e/test_stage_kind_marks.py` may rely on: the four class names above, `data-kind-icon`, and
`.entry__media-icon` for the comparison. It may **not** rely on the SVG path data.
