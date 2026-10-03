# Tasks 006: Service entries

- **Status:** Accepted (owner, 2026-10-03) — needs the owner's Accept (SDD gate). No implementation before that.
- **Spec:** [./spec.md](./spec.md) · **Plan:** [./plan.md](./plan.md)

## Before starting

- [ ] Spec Accepted by the project owner
- [ ] The open questions in ./spec.md answered (model name, control surface, stack, URLs)
- [ ] Branch from the current base (`feat/006-service-entries`)
- [ ] Confirm the compatibility promise's regression pass exists before touching anything

## Slice 1 — the model  (done)

- [x] Red: field rules per kind; at least one verse kept; `resolve()` per kind; ordering
      (`multimedia/tatib/tests.py`, `ServiceEntryTests`)
- [x] Green: `tatib.ServiceEntry` + migration `0005_serviceentry` + admin; `TataIbadahItem`
      untouched
- [x] The book/chapter cascade reset to 1 is a form/UI rule: slice 2
- [x] Verified: 130 tests green, the 116 that existed before among them, with no edit to any
      current template, endpoint or model

## Slice 2 — the content pane  (endpoints done; the pane itself to come)

- [x] Red: create/update/delete endpoints per kind; validation errors; what the pickers need
      (`ServiceEntryViewTests`, 17 tests, red before the wiring existed)
- [x] Green: the per-kind forms (`multimedia/web/reading/entries.py`), the six endpoint views,
      their URLs, and the two fragments (`_entry_form.html`, `_entry_song_options.html`)
- [x] Two bugs the tests caught: `editor/<str:kind>/new/` was swallowing `editor/entry/new/`
      (the entry routes must come first), and a second `kind` input shadowed the form's own,
      making every create invalid
- [ ] The content pane itself: entries rendered in the Tata Ibadah page, the per-entry add
      controls, and the modals' behaviour (the cascading dropdowns, the song pick, the verse
      checklist's label)
- [ ] E2E: each modal, the cascading dropdowns, the verse checklist's label, the panes
      refreshing in place

## Slice 3 — reorder

- [ ] Red: drag and keyboard moves; the sidebar preview; Discard restoring; adds hidden; the leave
      guard on every exit path (contents, another Tata Ibadah, search, tab close)
- [ ] Green: reorder mode, Save/Discard, the confirmation modal, the reorder endpoint

## Slice 4 — the new display and display mode

- [ ] Red: each kind rendered on the new projector and overlay; two lines per body; the
      blank-line rule; prev/next/toggle
- [ ] Red: entry writes refused while the Tata Ibadah is displaying in this browser, in its other
      tabs too, while the Tata Ibadah's own fields stay writable; one Tata Ibadah at a time in
      this browser; a second browser unaffected
- [ ] Red: the project button becomes Stop projecting and Update the current state; Update
      re-reads a song whose lyrics changed
- [ ] Green: the in-browser display state on its own channel, the hand-written pages on the
      reading app's tokens, the project button, the jump-to controls on scripture and song entries
- [ ] e2e: a whole service driven through the new projector, plus the two-tab lock
- [ ] Deferred: the OBS overlay, which needs its own answer for reaching inside OBS

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
