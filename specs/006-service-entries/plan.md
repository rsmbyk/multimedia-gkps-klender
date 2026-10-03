# Plan 006: Service entries

- **Status:** Draft — needs the owner's Accept (SDD gate)
- **Spec:** [./spec.md](./spec.md)
- **Bump:** minor (0.9.0 → 0.10.0)

## Approach

Additive throughout. The new capability lives in new models, new endpoints and new pages, and
every current page, endpoint and row is left as it is. The compatibility promise in the spec is
the first acceptance criterion, not a footnote: the old dock, sources, projection and API are
exercised unchanged before this ships.

## Slices

Each slice is shippable on its own and touches nothing the current app reads.

### Slice 1 — the model

`tatib.ServiceEntry`: one ordered element of a service order.
`kind` (`text`, `scripture`, `song`, `section_break`), the Tata Ibadah it belongs to, its
`order_number`, and the fields its kind needs — all nullable except the ones its kind requires,
with the rules enforced in `clean()` and mirrored in the forms:

- `title`, `text` (text, section break),
- `book_translation`, `chapter`, `verse_start`, `verse_end` (scripture),
- `song`, `verses` (song) — the explicit list of included verse numbers, stored as JSON,
- a `resolve()` that returns the `(title, body)` pair the display consumes, one branch per kind,
  reusing the app's existing citation and lyric formatting rather than inventing a second.

Tests: the field rules per kind, the cascade resets (book/chapter → 1), the "all verses by
default" rule, `resolve()` per kind, ordering and the contiguity of `order_number`.

### Slice 2 — the content pane

The reading app's Tata Ibadah page renders the entries and owns their editing, with per-entry add
controls (scripture, song, text, section break) and one modal each, in the existing design
system. Endpoints: create, update and delete an entry, plus a reorder action following the
conventions the current item API already uses. No sidebar editing of entries.

Tests: the modals' fields and defaults, the cascading dropdowns from the data, the verse
checklist's label, validation errors staying in the modal, and the panes refreshing in place.

### Slice 3 — reorder

Drag to reorder with pointer events, keyboard equivalents (move up / move down) for
accessibility, a reorder mode that hides the add controls and shows Save / Discard, a pending
order held in the page and previewed in the second-level sidebar, and a confirmation modal
before leaving with unsaved changes — covering the in-page switches (contents, another Tata
Ibadah, search) and `beforeunload`.

Tests: the drag and its sidebar preview, Discard restoring the previous order, the guard on each
exit path, and adds being unavailable while reorder mode is on.

### Slice 4 — the new display

New pages for this system: a screen projector and an OBS overlay, with the display rules the
operator relies on (two lines per body, the projector fitting the font, the overlay growing its
box, a blank line holding one line alone), plus the control surface for showing an entry, moving
to the previous or next one, and clearing. Own templates, own scripts, own `BroadcastChannel`
name, so no old dock can reach a new display or the reverse.

Tests: rendering per kind in both pages, the two-line split and the blank-line rule, the sync
channel's isolation, and an e2e pass driving a whole service through the new surface.

### Slice 5 — the old rows (deferred, owner-triggered)

Migrating `TataIbadahItem` rows into entries, and retiring the old path where it is no longer
used. Deliberately not part of this spec's tasks: the owner triggers it once the new system is
finished.

## Risks

- **The old paths.** Mitigated by the compatibility promise: no edits to the current OBS pages,
  API endpoints or model, and a regression pass over them before this is considered done.
- **The in-page shell.** The reading app swaps sections without reloading, so the reorder guard
  has to intercept the shell's own navigation, not just browser navigation. Slice 3 tests each
  exit path.
- **Two display channels.** A new `BroadcastChannel` name is a hard requirement; sharing one
  would let a new dock drive an old source.
- **Verse selection drift.** Storing the included verse numbers explicitly means a later change
  to a song cannot silently alter a prepared service.
