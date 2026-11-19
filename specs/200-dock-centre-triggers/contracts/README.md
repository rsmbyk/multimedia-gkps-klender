# Contracts: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md`

## Interfaces exposed by this slice

none — client-only. The dock gains one DOM control and one page-memory flag; no HTTP endpoint,
channel verb, storage key or display-record field changes. The internal IDs (`#centreBtn`,
`#prevBtn`, `#nextBtn`, `#runBody`, `.nextband`) are one document's own markup and are recorded in
`data-model.md` and `plan.md`, not offered as an interface.

## Not exposed

- The following mode is not broadcast: the projector and overlay have no list to follow.
- The idle clock is not persisted and has no debug query parameter in the product (the `?idle=`
  override exists only in the static preview).
- The centre control writes no display state; it only moves the list.
