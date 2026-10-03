# Spec 007: The old rows — editable, and one running order

- **Status:** Draft — needs the owner's Accept (SDD gate; no implementation before that)
- **Item:** [ITEM-008](../../backlog/items/ITEM-008-old-rows.md)
- **Plan:** [./plan.md](./plan.md) · **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor (to confirm)

## Intent

A Tata Ibadah prepared before spec 006 is made of old rows (`TataIbadahItem`). In the reading pane
those rows can be added to but not edited or deleted, and a new entry added under one of them lands
at the end of the service instead of right after it. The owner asked for both (2026-10-04). This
spec lets the pane maintain an old service fully, while the old OBS pages and the old API keep
working over the same rows.

## Compatibility promise

1. The old OBS pages, sources and API keep their templates, endpoints and behaviour; nothing here
   edits them.
2. `TataIbadahItem` keeps its fields and its meaning; only its `order_number` values may be
   renumbered by the migration so the service can hold one sequence. The order the old dock shows
   for the old rows is preserved.
3. A service with only old rows, or only entries, behaves exactly as it does today.

## Scope

### In scope

- Edit and Delete on an old row in the reading pane, revealed on hover beside the four add controls,
  with the entry controls' styling (icon and label; Delete in the danger colour).
- The old-row modal: a text row's title and text; an end-of-section row's note. The same dialog, the
  same error marking and the same validation discipline as the entry modals.
- One running order per Tata Ibadah: old rows and entries in a single sequence, so a new entry
  inserted after any element lands there; the contents list and the later projector read it.
- The data migration that gives today's services that single sequence without changing the order
  the pane shows.

### Out of scope

- Moving the old rows into entries (plan 006, slice 6) and retiring the old paths — still separate
  and owner-triggered.
- Reorder by drag (plan 006, slice 3).
- Any change to the old dock, the old API, or the OBS sources and projection.

## Domain rules

- **An old row's fields.** A text row: title (optional) and text (required, the same rule the text
  entry gained). An end-of-section row: its note.
- **One running order.** A Tata Ibadah's old rows and entries form one sequence of `order_number`s,
  contiguous from 1 and readable by a single sort.
- **Insertion is after the clicked element, never before it.** The control used decides the place:
  the new entry takes the next number, and everything after it shifts down, in both tables.
- **Editing an old row changes only that row.** No other row's content moves, and the old dock reads
  the edited text.
- **Deleting an old row removes it from the running order and closes the gap.**
- **The rules stay the model's own.** The pane's endpoints add nothing to what the old dock already
  enforces.

## Acceptance scenarios

### Scenario: An old row can be edited from the pane

- **Given** a service whose rows are old items
- **When** I hover a row, choose Edit, change its text and save
- **Then** the pane shows the new text, and the old dock reads the same row with the same text

### Scenario: An old row can be deleted after a confirmation

- **Given** an old row in the pane
- **When** I choose Delete and confirm
- **Then** the row is gone from the pane and from the old dock, and the remaining rows keep their
  order

### Scenario: A new entry lands after the row whose control was used

- **Given** a service with several old rows and some entries
- **When** I add a text entry under the second old row
- **Then** the entry appears immediately after that row, and the rows below it shift down

### Scenario: The order the pane shows is the order it showed before

- **Given** a service prepared before this spec
- **When** the migration has run
- **Then** the pane, the contents list and the sidebar show the rows in exactly the order they
  showed before

### Scenario: The old paths are untouched

- **Given** the OBS dock, its sources and `/api/tatib/items/`
- **When** they are exercised on the same data
- **Then** their responses and behaviour are unchanged

## Traceability

Filled per slice as it lands.

## Open questions for Accept

1. **The order namespace.** I propose one sequence per Tata Ibadah, with a migration that renumbers
   the entries after the old rows while preserving the order the pane shows today. The alternative
   is to leave the two blocks and accept that an insertion under an old row still lands at the end
   of the entry block. Which do you want? (I recommend the first — it is what your report asked
   for.)
2. **Editing an old row versus migrating it.** Editing keeps both systems reading the same row, so
   the old dock never goes stale. Moving the old rows into entries would give everything one model,
   but freezes what the old dock sees. I propose editing, and leaving the migration for later.
3. **Bump.** minor, on top of spec 006's 0.10.0, because of the renumbering migration. Confirm.
