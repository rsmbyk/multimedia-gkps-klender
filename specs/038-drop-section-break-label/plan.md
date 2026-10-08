# Plan 038: Remove the label from section-break entries

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-040
- **Bump:** patch

## Why

A section break is a divider, not a titled entry; the label it carries adds a field the operator must
ignore. Remove it from the `section_break` kind.

## Scope / edges

**In:**

- The section-break editor has no label control.
- A section break stores no label, and the pane shows none for it.
- The label is dropped wherever a `section_break` reads `title` (`resolve()`, the pane block's title
  and note).

**Out:**

- The text entry's title, which shares the `title` column.
- The legacy END_OF_SECTION note (a different model).
- The projector's blank section-break screen.

## Approach

- `multimedia/web/reading/entries.py` — drop `'title'` from `SectionBreakEntryForm.Meta.fields`; keep
  the kind's wording in `TITLES` as needed.
- `multimedia/tatib/models.py` — `resolve()` for a section break returns `('', '')`; the break no
  longer contributes a title. (The `title` column stays — text entries still use it.)
- `multimedia/web/reading/views.py` — `_tatib_stage()` stops using `row.title` as the break's title
  and note.
- `multimedia/web/templates/reading/_entry_form.html` — the section-break branch already shows the
  generic title field for non-scripture/song kinds; exclude `section_break` so it renders no label.
- `static/styles/design/components.css` / `tatib.html` — nothing if the break already renders without
  a label; otherwise stop rendering the heading for it (see ITEM-037).
- **Amends spec 035** (ITEM-037): the shared divider shows no label for an entry break.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — the section-break form has no `title` field; a posted
  `title` is ignored; the pane renders a break with no label; a text entry still has and shows its
  title.
- E2E: covered by the existing pane assertions; no new file.

## Risks

- **Shared field.** `title` is used by text entries; the change must be scoped strictly to
  `section_break`.
- **Stored labels.** Existing breaks may hold a label; decide whether to leave it unused or clear it
  on next save.
