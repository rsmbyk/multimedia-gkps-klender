# Plan 006: Service entries

- **Status:** Accepted (owner, 2026-10-03)
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

### Accepted amendment to slice 3 — ghost under the pointer (owner, 2026-10-04)

Keep the existing live DOM reorder as the single source of truth. After the movement threshold,
show an inert visual copy outside the list at the pointer's grab offset while the actual row
stays in flow but is transparent; never add a second layout slot or delay the copy's movement.
Keep the existing morph, renumbering, release and keyboard paths. Clean the copy up on release
and cancellation; cancellation restores only this gesture's starting order, not earlier unsaved
changes. Verify in a browser with geometry and order assertions for both a normal entry and a
section break. Owner accepted this amendment on 2026-10-04; implement with test-first coverage.

### Accepted amendment to slice 3 — no hover tint while grabbing (owner, 2026-10-05)

Use the active grab state after the movement threshold, not the broader unsaved/reorder mode,
to suppress hover backgrounds on the service-entry list and its ghost. Preserve selected styling
and keyboard focus. Test computed backgrounds before, during and after a pointer drag, including
cancellation. Owner accepted this amendment on 2026-10-05; implement with test-first coverage.

### Accepted amendment — empty Bible header row (owner, 2026-10-05)

The 34px `min-height` on `.read__head-top` supports the Tata Ibadah project button added
in this spec, but it also reserves an empty line above the Bible chapter title and TB/SIM
switcher. On the live reader, the empty eyebrow has `display: none` while its parent still
measures 34px; the stage's separate 40px top padding is intentional. Collapse the parent
when it has no visible child; do not remove the row from song or Tata Ibadah pages. Pin
its geometry from the home click-through route at desktop and phone widths in a browser
test, plus a populated-header control. Owner accepted this amendment on 2026-10-05.

### Accepted amendment to slice 3 — visible destination slot (owner, 2026-10-05)

Style the existing `is-dragging` row's box as a tinted, outlined destination slot while
keeping the row's own text and controls invisible; its inert ghost remains outside the list.
Because `placeRowAt()` already moves that row through the DOM, the indicator follows the
actual previewed order without a second placeholder or a new drop algorithm. Clear it with
the existing drag cleanup on release, pointercancel, blur, and page swap. Test geometry and
computed styling at the beginning, middle, end, and across a section break, plus row count,
list height, selected/hover/focus styling, and keyboard-only reordering. Owner accepted
this amendment on 2026-10-05.

### Accepted amendment to slice 3 — remove the destination slot ring (owner, 2026-10-05)

Remove only the inset `box-shadow` on the existing `is-dragging` slot; retain its tint
and the separate ghost shadow. First update the destination-slot browser test to require
no shadow or outline on that slot and observe it fail, then change the CSS and verify
geometry, ghost, keyboard focus, and cleanup with targeted browser coverage. Owner accepted
this amendment on 2026-10-05.

### Accepted amendment — Bible language switch motion (owner, 2026-10-05)

Keep the TB/SIM anchors and existing edition switching. Give the control one persistent,
non-interactive selected background behind them; move it using a transform tied to the
current pressed state rather than animating layout or painting each anchor separately.
Synchronize that state when the reading stage is replaced or a saved language is restored.
Disable the transform transition under `prefers-reduced-motion: reduce`, avoid an initial
slide on load, and preserve focus, unavailable-language handling, and no-JS fallback.
Before implementation, add browser coverage from home through the Bible chapter: both
directions, mid-transition position, final state, fixed geometry, unavailable and reduced
motion states. Owner accepted this amendment on 2026-10-05.

### Slice 4 — the new display and display mode

Hand-written pages on the public reading app's design tokens: a **projector** (previous, next and
an on/off toggle — and nothing more) and an **overlay** for OBS, both rendering every kind with
the display rules the operator relies on (two lines per body, the projector fitting the font, the
overlay growing its box, a blank line holding one line alone). A **project button** on a Tata
Ibadah opens the projector in a new tab for that Tata Ibadah, together with the **jump-to-it**
controls on scripture and song entries.

Display mode lives in the browser that started it, shared across its tabs over its own
`BroadcastChannel`, and nowhere else — deliberately, so several laptops can project different
things to different screens. One Tata Ibadah at a time within a browser; another browser is
unaffected. While one is displaying, that browser's tabs refuse entry writes (adds, edits,
reorders, deletes) while the Tata Ibadah's own fields stay writable, and the project button
becomes Stop projecting and Update the current state. The endpoints are untouched: the lock is
the shell declining an action, not a server rule, which is also what keeps the compatibility
promise intact.

The OBS overlay is deliberately not in this slice: inside OBS the channel is a different browser
process from the operator's, so what drives the overlay needs an answer of its own. The
projector window — which the project button opens in the operator's own browser, where the
channel does reach — is the whole of this version's display.

Tests: rendering per kind on both pages, the two-line and blank-line rules, prev/next/toggle,
one Tata Ibadah at a time, the entry-write refusal in a second tab, the stop and update buttons,
and the jump-to controls.

### Slice 5 — soft deletion

An `is_deleted` flag (and when, and by whom, for the admin) on Song, Book and Verse, defaulting
to not-deleted so every existing row and every current reading path behaves exactly as it does
now. Deleting from the admin soft-deletes instead, normal lists stop offering the row, and a
service entry that refers to one keeps resolving what it can and says its target was deleted.

The blast radius is the point of care: the flag must be honoured wherever the current app lists
or serves songs, songbooks and verses, and *nowhere else*. That audit is a deliberate part of
this slice, with the compatibility pass over the current pages, docks and API run before and
after.

Tests: deletion marks rather than removes; the public and dock paths skip a deleted row; a
service entry pointing at a deleted song still resolves and warns; the API's responses for
non-deleted data are byte-for-byte what they were.

### Slice 6 — the old rows (deferred, owner-triggered)

Migrating `TataIbadahItem` rows into entries, and retiring the old path where it is no longer
used. Deliberately not part of this spec's tasks: the owner triggers it once the new system is
finished.

## Risks

- **The old paths.** Mitigated by the compatibility promise: no edits to the current OBS pages,
  API endpoints or model, and a regression pass over them before this is considered done.
- **The in-page shell.** The reading app swaps sections without reloading, so the reorder guard
  has to intercept the shell's own navigation, not just browser navigation. Slice 3 tests each
  exit path.
- **Two display paths, no shared channel.** The new projector reads the server's display record
  rather than joining the docks' browser channel, so an old dock and the new projector cannot
  drive each other even by accident.
- **Soft deletion's reach.** Adding the flag is safe; honouring it in the right places is the
  work. Every current list, dock query and API filter is reviewed, and the compatibility pass
  proves the non-deleted data still answers identically.
- **Song sync.** Because a song entry resolves live, editing a song changes services that refer
  to it — intended, and the reason exclusions are stored rather than inclusions.
