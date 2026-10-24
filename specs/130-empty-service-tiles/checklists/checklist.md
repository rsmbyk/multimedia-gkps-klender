# Checklist — 130-empty-service-tiles

Reviewer-owned: the agent writes these and never ticks them.

- [x] The empty block sits in the middle of the reading area, not under the header, at 1440×900.
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

*One of them rests on a different test than the plan names:* "the saved copy matches the server page" is
proved by `test_empty_saved_tatib_shows_add_media_after_sidebar_navigation_offline` and by the tile
comparison written into `test_saved_render_parity.py`, which cannot run to that point because its Kidung step
already fails on `develop` — recorded as G1 in `converge.md`, not as a hidden gap.
