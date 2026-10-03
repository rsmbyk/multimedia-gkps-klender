# Tasks 006: Service entries

- **Status:** Draft — needs the owner's Accept (SDD gate). No implementation before that.
- **Spec:** [./spec.md](./spec.md) · **Plan:** [./plan.md](./plan.md)

## Before starting

- [ ] Spec Accepted by the project owner
- [ ] The open questions in ./spec.md answered (model name, control surface, stack, URLs)
- [ ] Branch from the current base (`feat/006-service-entries`)
- [ ] Confirm the compatibility promise's regression pass exists before touching anything

## Slice 1 — the model

- [ ] Red: field rules per kind; the book/chapter cascade resets to 1; all verses by default and
      at least one kept; `resolve()` per kind; ordering and contiguous numbers
- [ ] Green: `tatib.ServiceEntry` + migration + admin, `TataIbadahItem` untouched

## Slice 2 — the content pane

- [ ] Red: create/update/delete endpoints per kind; validation errors; the modals' defaults
- [ ] Red: e2e — each modal, the cascading dropdowns, the verse checklist's label, the panes
      refreshing in place, hymn-free behaviour where relevant
- [ ] Green: entry rendering in the Tata Ibadah page, the per-entry add controls, the four modals

## Slice 3 — reorder

- [ ] Red: drag and keyboard moves; the sidebar preview; Discard restoring; adds hidden; the leave
      guard on every exit path (contents, another Tata Ibadah, search, tab close)
- [ ] Green: reorder mode, Save/Discard, the confirmation modal, the reorder endpoint

## Slice 4 — the new display and display mode

- [ ] Red: each kind rendered on the new projector and overlay; two lines per body; the
      blank-line rule; prev/next/toggle
- [ ] Red: entry writes refused while the Tata Ibadah is displaying, in a second tab too, while
      the Tata Ibadah's own fields stay writable; one Tata Ibadah at a time
- [ ] Red: the project button becomes Stop projecting and Update the current state; Update
      re-reads a song whose lyrics changed
- [ ] Green: the server-held display record, the hand-written pages on the reading app's tokens,
      the project button, the jump-to controls on scripture and song entries
- [ ] e2e: a whole service driven through the new projector, plus the two-tab lock

## Slice 5 — soft deletion

- [ ] Red: deletion marks rather than removes; normal lists and the current dock/API paths skip a
      deleted row; a service entry referring to a deleted song still resolves and warns
- [ ] Green: the flag on Song, Book and Verse, the admin path, the warning on the entry
- [ ] Audit every current query site for songs, songbooks and verses — the compatibility pass
      before and after

## The compatibility promise

- [ ] A regression pass asserting the current OBS pages, API endpoints and model responses are
      unchanged, run before and after
- [ ] No diff in any current OBS template, script or endpoint

## Done when

- [ ] All acceptance scenarios in ./spec.md hold
- [ ] The tests named above are green, and the compatibility pass is green
- [ ] Traceability in ./spec.md filled; ITEM and board updated in the same PR
- [ ] `VERSION` and the changelog bumped in the same PR
