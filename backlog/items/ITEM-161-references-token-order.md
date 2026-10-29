---
id: ITEM-161
status: in-review
title: 'The Media Library''s first refresh writes its references without the token'
type: fix
priority: P1
effort: S
created: 2026-10-28
updated: 2026-10-28
spec: specs/150-references-token-order/spec.md
branch: fix/150-references-token-order
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/430
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/429
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-161: The Media Library's first refresh writes its references without the token

## Summary

Spec 148 made `refresh()` apply the whole state once, but deferred the `/status` response — and with it
the write token — to the end of the refresh. The first `POST /v1/references` of a page load therefore
carries an empty `X-GKPS-Media-Token`, the companion answers 403, the references read is treated as
failed, and the one draw shows `Service uses unavailable` on every row. The next refresh draws the real
list, so the list still jumps 22–68px — the defect 148 was supposed to remove.

## Notes

The E2E stub answers `/references` with 200 for any request, so it never sent a token and never failed:
six green cases while the product was broken. The stub is part of this card.

Measured on the compose page at 1.22.8: two draws 190ms apart, 8 placeholder rows at `#mediaFileList`
800px, then 1 placeholder at 868px; `POST /v1/references` 403 then 200.

## Acceptance sketch

- A page opened after a server restart draws the list once, with its references, and no row moves.
- The E2E stub refuses a references write that carries no token, and the spec-148 cases stay green
  against it.

## Links

- Spec: [150](../specs/150-references-token-order/spec.md)
- Related items: ITEM-158 (spec 148, the slice this completes), ITEM-156 (the spacing-E2E red)
