# Plan 046: Show the first two text lines for untitled service entries

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-048
- **Bump:** patch

## Why

An untitled Text entry currently reads "Text" in the Tata Ibadah sidebar, while a titled entry has a
useful operator-provided title. Quote the first two literal body lines for untitled Text and
Single-Screen Text entries, preserving titles when present so the running order is more informative
without discarding the operator's label.

## Scope / edges

**In:**

- The service-entry sidebar label for `text` and `single_screen_text` kinds: when the title is empty,
  use the first two literal lines of the body, split on `\n`; blank lines count and are not skipped.
- When either kind has a title, keep the title as the sidebar label.
- Cap the final label (retained title or body preview) at 60 characters overall, preserving the current
  service-entry cap.
- Keep the reorder grip vertically centered on a two-line row.

**Out:**

- Legacy `TataIbadahItem` text rows.
- Passage, song and break rows.
- The reading pane (spec 031 clamps it separately).
- The projector.

## Approach

- `multimedia/web/reading/views.py` `_tatib_stage()` — keep a non-empty title for both text kinds;
  otherwise join the first two literal lines from `resolve()[1]`, then apply the 60-character cap.
  For an empty body, preserve the current kind-label fallback and keep the TOC filter text in step
  with the row content.
- `multimedia/web/templates/reading/_toc.html` — render the selected body lines as separate spans and
  keep an explicit blank-line row visible; `static/styles/design/components.css` gives the lines a
  consistent height and verifies the existing `.toc__grip` `top: 50%` positioning stays centered.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — untitled Text and Single-Screen Text use the first two
  literal lines (including blank lines); titled entries retain their title; the combined label is
  capped at 60 characters; legacy and other entry kinds are unchanged.
- E2E: `tests/e2e/test_reading.py` — the untitled sidebar row shows the two-line label, its grip is
  centered, and a titled row still shows its title.

## Risks

- **Line-break collapse.** Whitespace collapses unless markup/CSS preserves it; verify literal blank
  lines and the second line render as intended.
- **The grip.** A taller row must keep the grip at its vertical middle.
- **Long lines.** The two-line label remains capped at 60 characters total, matching the current
  service-entry cap.
