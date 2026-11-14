# Plan 035: Give the section break a clear separation

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-037
- **Bump:** patch

## Why

A section break should divide the service unmistakably, but today there are two shapes and neither
divides strongly: a legacy END_OF_SECTION draws a short centred rule with a diamond, and a
`section_break` entry renders as an ordinary item heading. Give the section break one clear,
consistent separation.

## Scope / edges

**In:**

- One divider treatment for both the legacy END_OF_SECTION row and the `section_break` entry: a rule
  across the reading column, a touch stronger than the plain divider, with the break's label/note
  kept under it.
- The spacing stays generous (the current ~34px top/bottom).
- Keep the entry controls (spec 033) working on the divider.

**Out:**

- The projector's section-break screen (spec 006 keeps its blank screen).
- The TOC / sidebar, and the other panes.
- The other entry kinds.

## Approach

- `multimedia/web/reading/views.py` — in `_tatib_stage()`, make a `section_break` entry produce the
  divider shape the legacy END_OF_SECTION uses (an `eos`-style item) instead of a `.tatib__item`
  heading, carrying its entry pk/controls and its label as the note.
- `multimedia/web/templates/reading/tatib.html` — the divider branch renders the rule and the label;
  the entry controls attach to it (spec 033) as they do for other entries.
- `static/styles/design/components.css` — take `.tatib__eos` full width (drop
  `width: min(220px, 60%)`) and give the rule a little more presence; keep the diamond or remove it
  per review; keep the margins.
- **Amends spec 006**: its pane rendering of a `section_break` entry (a heading) becomes the shared
  divider.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — a `section_break` entry renders the divider with its
  label (not a heading); the legacy END_OF_SECTION renders the same shape.
- E2E: `tests/e2e/test_tatib_section_break.py` — the divider separates the entries around it, in both
  themes.

## Risks

- **Belated controls.** The divider branch is the eos one; its Edit/Delete must still attach or the
  break becomes uneditable (spec 033).
- **Amending spec 006.** The `section_break` pane rendering is pinned there; amend it in the same PR.
