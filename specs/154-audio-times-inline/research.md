# Research: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md` · **Created**: 2026-10-29

Four decisions. Three were settled by reading the product's own code, the fourth by the constraint the
local companion puts on a preview. **Unknowns remaining: 0.**

## D001 — Right-aligned under the bar, not left-aligned beside the total's old place

- **Decision**: the pair ends on the seek bar's right edge; the played time moves to it.
- **Rationale**: the request names the video-player shape, and every one of them puts `current / total`
  at the bar's right end. It also keeps the total — the number that never changes — exactly where it is
  (x 980.2→1004), so the geometry churn is confined to the played time.
- **Alternatives**: left-aligned (`0:00 / 5:02` at the bar's left) would drag the total 457px left, away
  from the bar's end where the projector also puts it; centred would move both numbers.
- **Provenance**: request + `multimedia/web/templates/reading/projector.html:47`, the product's own
  `current / total` line.

## D002 — `justify-content: flex-end` on the existing flex row

- **Decision**: one declaration changes on `.audio-player__times` — `space-between` → `flex-end` — plus
  `gap: 5px` and `align-items: baseline`.
- **Rationale**: the row is already a flex container holding exactly the time spans; every alternative
  (a wrapper div, `margin-left: auto` on the total, absolute positioning) adds markup or a second layout
  rule for the same result. `align-items: baseline` pins the two numbers' baselines to each other even if
  a future child has a different line box.
- **Alternatives**: `margin-left: auto` on the total with `space-between` kept — same picture, but it
  reads as an exception carved into a rule that still claims to spread its children.
- **Provenance**: `static/styles/design/components.css:2134`, measured before/after at 1440×900.

## D003 — The separator is a text node, not a pseudo-element

- **Decision**: `<span class="audio-player__separator">/</span>` between the two time spans.
- **Rationale**: today the line's accessible text is `0:000:10` — two numbers with nothing between them
  (measured in the E2E's DOM). A `::before` would paint a slash and leave that text unchanged; a real
  node makes a screen reader read the value as one.
- **Alternatives**: `content: '/'` on `[data-audio-total]::before` (invisible to assistive technology);
  pasting " / " into the elapsed span's `textContent` (destroyed by the next `update()` call, which
  overwrites exactly that node).
- **Provenance**: `static/web/media-audio.js:39-40` writes `textContent` into the two spans only; the
  separator must therefore live outside them.

## D004 — `media-audio.js` is not touched

- **Decision**: no JavaScript change: the two spans keep their `data-audio-*` selectors and their order in
  the DOM, so `update()`'s two `querySelector` calls keep resolving.
- **Rationale**: the fix is layout. Any JS change would be a second reason for the line to break.
- **Alternatives**: rewriting `update()` to print one formatted string into the row — would delete the
  two spans other selectors (`[data-audio-elapsed]` in `projector.js`, the E2E's own assertions) rely on.
- **Provenance**: `static/web/media-audio.js:31-44`, `static/web/projector.js:108`.

## D005 — The preview's origin must be in the companion's allowlist

- **Decision**: the review window's companion runs with `http://localhost:8814` added to
  `GKPS_MEDIA_ALLOWED_ORIGINS`; nothing about that reaches the repo.
- **Rationale**: `local_media.py:447` refuses a request whose `Origin` is not in the allowlist — the
  browser then blocks the fetch and the player never leaves `hidden` (observed: `Access to fetch at
  'http://127.0.0.1:63174/v1/files' from origin 'http://localhost:8814' has been blocked by CORS
  policy`). Without it the preview cannot show the player at all.
- **Alternatives**: previewing on port 63404 (held by the compose `web` container, which serves
  `develop`); stubbing the file route in the browser (that is how the E2E works, but a preview must run
  the product's real path).
- **Provenance**: `multimedia/local_media.py:441-465`, `docker-compose.yml:57`; the origin was added for
  the review window and removed afterwards.
