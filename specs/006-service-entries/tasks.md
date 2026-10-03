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

## Slice 4 — the new display

- [ ] Red: each kind rendered in the new projector and overlay; two lines per body; the blank-line
      rule; the new channel isolated from the old one
- [ ] Green: the new pages, their scripts, the control surface (show, prev, next, clear)
- [ ] e2e: one whole service driven through the new surface

## The compatibility promise

- [ ] A regression pass asserting the current OBS pages, API endpoints and model responses are
      unchanged, run before and after
- [ ] No diff in any current OBS template, script or endpoint

## Done when

- [ ] All acceptance scenarios in ./spec.md hold
- [ ] The tests named above are green, and the compatibility pass is green
- [ ] Traceability in ./spec.md filled; ITEM and board updated in the same PR
- [ ] `VERSION` and the changelog bumped in the same PR
