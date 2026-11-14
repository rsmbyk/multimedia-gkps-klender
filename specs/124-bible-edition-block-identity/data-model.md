# Data Model: Keep a chapter's verse text when the reading page updates in place

**Spec**: `specs/124-bible-edition-block-identity/spec.md`

## Entities

`n/a — the slice adds, removes and changes no stored entity, field, relationship or payload; the edition block is rendered markup only.`

## Invariants

- A rendered chapter carries at most one block per translation that has text for it, and exactly one of them is visible. (FR-001)
- Each block's identity within the stage is its translation, not its label. (FR-001, FR-002)
- The selected translation survives an in-place chapter move. (FR-002)

## Not modelled

- The translation switch's remembered choice — client state in `document.documentElement.dataset.bibleEdition`, already existing and unchanged.
- The saved library's copy of the chapter — same markup, produced by `static/web/offline-render.js`, already existing and unchanged.
