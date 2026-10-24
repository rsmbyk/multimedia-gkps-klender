# Research: Keep a chapter's verse text when the reading page updates in place

**Spec**: `specs/124-bible-edition-block-identity/spec.md`
**Unknowns remaining**: 0

## D001 — Where the fault lives

- **Decision**: the in-place reconciler in `static/web/reading.js` is at fault, specifically
  `nodeIdentity()`, whose fixed attribute list ranks `data-name` above `data-ed`.
- **Rationale**: reproduced on a local server against the real corpus. `/bible/8/1/` (Rut 1) reads
  normally on a direct load: two `#readBody .read__ed` blocks, TB visible with 22 verses, SIM hidden with
  22. Clicking chapter 2 (an in-place move) leaves exactly one block: `data-ed="sim"`, `hidden`, 23 verses —
  the stage is blank and the TB/SIM link does nothing because no TB block exists any more. Reloading
  `/bible/8/2/` renders both blocks again. Browsing Kejadian / 1 Musa the same way keeps both blocks,
  and those two translations name the book differently. In the markup, both blocks carry the same
  `data-name` exactly when the translations share a name (the sidebar shows `Rut — Rut`). Reading the
  reconciler confirms the mechanism: `reconcileChildren` matches a fresh node to the first live node with
  the same key, so the fresh SIM block matches the live TB block — the one just matched — and SIM's verses
  and `hidden` are merged into it.
- **Alternatives considered**: a server-side rendering fault (rejected — a direct load of the same URL is
  correct); a stale saved copy overwriting the stage (rejected — the fault also occurs with the library
  synced and no saved generation for the chapter).
- **Provenance**: research

## D002 — Which identity an edition block carries

- **Decision**: key an edition block by its edition (`data-ed`), placed before the label (`data-name`) in
  the identity list.
- **Rationale**: the label is content, not identity — two translations may legally share it, and this repo
  has many such books. The edition is unique within one stage and is already emitted by both renderers, so
  one ordering change corrects the server page and the saved page together. No markup, CSS, or test fixture
  needs to change.
- **Alternatives considered**: (a) adding a unique `id` to each block in both renderers — two files to keep
  in sync for a value the markup already carries; (b) making `reconcileChildren` refuse to reuse an
  already-matched candidate — it would mask this collision without giving the blocks distinct identities,
  and it changes the reconciler for every keyed node; (c) de-duplicating by position — the existing
  positional fallback cannot tell which block is which when both are present and one is hidden.
- **Provenance**: research

## D003 — Coverage of the saved library

- **Decision**: the saved library is covered by inheritance, not by a new offline fixture.
- **Rationale**: `static/web/offline-render.js` `edition()` emits the same `class="read__ed" data-ed=…`
  markup the server template emits, and the saved view is reconciled by the same script, so the corrected
  identity applies with no separate change. `tests/e2e/test_saved_render_parity.py` is re-run as the guard
  that the saved/server markup did not drift.
- **Alternatives considered**: adding a same-name book to the offline library fixtures — it would test the
  same identity rule a second time at the cost of a synced-library setup; recorded as `inspection` instead.
- **Provenance**: research

## Open

<!-- empty: Phase 0 finished -->
