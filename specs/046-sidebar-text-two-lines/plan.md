# Plan 046: Show the first two text lines in the service sidebar

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-048
- **Bump:** patch

## Why

An untitled text row in the Tata Ibadah sidebar reads "Text", and a titled one reads only its title,
so the running order does not show what the reader will actually meet. Quote the entry's own opening
lines instead — the first two — for both text kinds.

## Scope / edges

**In:**

- The sidebar label for `text` and `single_screen_text` entries: the first two literal lines of the
  entry's text, shown as up to two lines.
- The reorder grip staying vertically centered on a two-line row.

**Out:**

- Passage, song and break rows.
- The reading pane (spec 031 clamps it separately).
- The projector.

## Approach

- `multimedia/web/reading/views.py` `_tatib_stage()` — for `kind_key in ('text',
  'single_screen_text')`, build the TOC label from the first two lines of `resolve()[1]` (split on
  `\n`), and keep the row's `txt` filter text in step.
- `multimedia/web/templates/reading/_toc.html` — render the label so a literal line break survives
  (`white-space: pre-line`, or split the two lines into spans).
- `static/styles/design/components.css` — let `.songrow__t` take up to two lines; confirm
  `.toc__grip`'s `top: 50%` centering holds for a taller row (the `li` is already positioned).
- Keep the `titled` flag / `songrow--cont` behaviour as the owner decides (open question).

## TDD

- Domain/app tests: `multimedia/web/tests.py` — a multi-line text entry's TOC label is its first two
  lines; a single-screen text entry's too; a passage/song/break is unchanged.
- E2E: `tests/e2e/test_reading.py` — the sidebar row shows two lines and the grip is centered.

## Risks

- **Line-break collapse.** Whitespace collapses unless the markup/CSS preserves it; the two lines must
  actually render as two.
- **The grip.** A taller row must keep the grip at its vertical middle.
- **Over-long lines.** A long first line can still dominate; the label cap is an open question.
