# Spec 045: Make the passage modal's chapter/verse dropdowns custom

- **ID:** 045
- **Status:** Accepted
- **Item:** ITEM-047
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Give the passage modal one dropdown style: chapter, from-verse and to-verse become the same custom
control as the book picker.

## Scope

### In scope

- Chapter, from-verse and to-verse as custom dropdowns in the add and edit passage modals.
- They keep updating with the chosen book/chapter and keep posting their values.
- The to-verse keeps its disabled state and hover note.

### Out of scope

- The book picker; the song modal and sidebar editors (unless widened).

## Domain rules

- **One style.** Chapter, from-verse and to-verse use the same custom dropdown as the book picker.
- **Values still post.** Each control carries its value into the form unchanged.
- **Still driven.** The controls still refill from the chosen book and chapter.
- **The tip stays.** The to-verse still disables, with its "no verses after the start verse" note,
  when nothing can end the range.
- **Both modals.** Add and edit behave the same.

## Acceptance scenarios

### Scenario: The controls look like the picker

- **Given** the passage modal
- **Then** chapter, from-verse and to-verse are custom dropdowns matching the book picker

### Scenario: They still update

- **Given** a chosen book and chapter
- **Then** the chapter and verse options reflect them

### Scenario: The values post

- **Given** a chapter and verse range chosen
- **When** I save
- **Then** the entry stores the chapter and verses chosen

### Scenario: The to-verse tip

- **Given** the start verse is the chapter's last
- **Then** the to-verse is disabled with its note

### Scenario: Edit modal

- **Given** the edit passage modal
- **Then** the same controls are shown and behave the same

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_entries.py` (`test_adding_and_editing_a_passage_through_custom_pickers`);
  existing picker/translation compatibility coverage in `tests/e2e/test_entry_pickers.py`.
- Implementation: `static/web/entries.js`,
  `multimedia/web/templates/reading/_entry_form.html`,
  `static/styles/design/components.css`.
- Related: spec 042 (picker menus), spec 043 (book picker), spec 044 (translation toggle).
