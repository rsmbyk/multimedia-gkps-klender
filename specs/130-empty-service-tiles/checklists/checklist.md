# Checklist — 130-empty-service-tiles

Reviewer-owned: the agent writes these and never ticks them.

- [x] The empty block's centre sits a quarter of the way down the reading area, clear of the header, at 1440×900.
- [x] The five add actions are one horizontal row, and each is a square.
- [x] A tile shows only a glyph — no visible label anywhere in the row.
- [x] Hovering a tile names it, and the name is `Add Passage`, `Add Song`, `Add Text`, `Add Break`,
      `Add Media` in that order.
- [x] `Add Media` has a glyph like the other four, and it reads as media rather than as one file type.
- [x] Nothing in the row is smaller than 44px, at 1440×900 or in the 240px column both sidebars leave.
- [x] The narrow column takes three and two rather than five tiny tiles.
- [x] Deleting a service's last entry leaves the same centred row behind, without a reload.
- [x] The saved copy of an empty service matches the server page.
- [x] A service that holds items looks exactly as it did before this slice.
- [x] Keyboard focus still shows the same ring on every tile.
- [x] The slice record states what changed in numbers, not adjectives.

*(Items are ticked by the owner at gate 2; the agent does not tick them.)*

**Ticked at gate 2** (owner, 2026-10-25), together with the plan pack's acceptance.

*One of them rests on a different test than the plan names:* "the saved copy matches the server page" was
proved by `test_empty_saved_tatib_shows_add_media_after_sidebar_navigation_offline` while the parity suite
could not run to that point on `develop` — recorded as G1 in `converge.md`, not as a hidden gap. That gap
closed on rebasing onto spec 128: `test_saved_render_parity` now runs the saved-against-server tile comparison
and passes, three runs of three.
