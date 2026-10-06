# Plan 007: The old rows — editable, and one running order

- **Status:** Accepted (owner, 2026-10-05)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-008
- **Bump:** minor (0.11.0 after spec 006 ships as 0.10.0)

## Why

The owner's review of spec 006 (2026-10-04) found two gaps on a service whose rows are old
(`TataIbadahItem`):

- **Edit and Delete are missing on the old rows.** The pane offers them on the new entries only, so
  a typo in an old service can only be fixed in the old OBS dock.
- **A new entry clicked under an old row lands at the end of the service.** The add controls sit
  under every row, but the stage renders the old rows and the entries as two blocks with their own
  numbering, so "after this row" is only honourable for the last old row.

Spec 006 deliberately left the old model alone and deferred moving the old rows into entries (plan
006, slice 6). This spec closes the two gaps in the pane, and leaves both the old OBS pages and the
old API exactly as they are.

## Scope / edges

**In:**

- Editing and deleting an old row (`TataIbadahItem`) from the reading pane, with the same modal the
  entries use and the same danger-coloured Delete.
- One running order per Tata Ibadah, so a new entry lands after the element whose control was used,
  old row or entry; the pane, the contents list and the later projector read that one order.

**Out:**

- Moving the old rows into entries (plan 006, slice 6) — still separate and owner-triggered; this
  spec makes it a smaller cleanup, not a prerequisite.
- Reorder by drag (plan 006, slice 3) — unchanged; old rows join it when it lands.
- Any change to the old OBS dock, sources, projection or API.

## Approach

Slice 1 is additive: two endpoints on the old model (update, delete), one fragment per item kind (a
text row: title and text; an end-of-section row: its note), and the pane revealing Edit and Delete
on an old row the way it does on an entry. Nothing reads differently for the old dock.

Slice 2 is the structural one. Today the stage appends the entries after the old rows, each list
numbered from 1, so "insert after this old row" cannot be represented. Accepted approach: **one
order namespace** — a data migration renumbers the entries after the old rows, keeping today's
visual order exactly (gaps in old rows close first; entries become n+1…n+m), the stage renders the
merged stream sorted by `order_number`, and an insertion after any element shifts the rows below it
in both tables. The old dock still shows the old rows in their sequence; only their numbers may
move. The owner accepted this order, the keep-old-model choice, and the minor bump on 2026-10-05.

Alternative considered: leave the two blocks and ship slice 1 only. That keeps every number
untouched, but leaves the insertion order wrong for every old row that is not the last — which is
the second half of what the owner reported.

## TDD

- Domain/app tests: the update and delete endpoints per item kind (method, permission, validation,
  what the old row reads like afterwards); the migration preserving the rendered order; insertion
  after an old row and after an entry; the old API answering unchanged.
- E2E (Playwright, as in specs 005/006): the controls on an old row, an edit that shows in the
  pane, a delete after its confirmation, and an insertion that lands where it was clicked.

## Risks

- **Renumbering touches production rows.** Only `order_number` changes, and the migration keeps the
  order the pane shows today; tests pin the rendered sequence before and after.
- **The old dock's own reorder** renumbers its table alone; the next pane insertion, deletion,
  or entry reorder normalises again. Stated in the spec and pinned by tests.
- **Two write surfaces on the old model** (the dock's and this pane's). The pane adds no rule of its
  own; both mirror the model.
