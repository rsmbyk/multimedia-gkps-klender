---
id: ITEM-162
status: in-review
title: 'The projector paints its image-unavailable glyph beside every image'
type: fix
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/157-projector-image-missing-glyph/spec.md
branch: fix/157-projector-image-missing-glyph
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/447
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/436
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-162: The projector paints its image-unavailable glyph beside every image

## Summary

An image screen on `/projector` shows the picture and the "image unavailable" glyph side by side. The
glyph is the screen's own placeholder (`screen__image-missing`), which is supposed to appear only when
the bytes fail to load; instead it is painted on every image screen, whether the image arrived or not.

Two faults line up. The template renders that `<svg>` with no `hidden` attribute — the audio, video,
PDF and slides placeholders all carry one — and `renderImageScreen` toggles it with
`missing.hidden = true`, a property SVG elements do not have: the assignment lands as a JS expando, the
attribute the CSS keys on (`.screen__image-missing[hidden] { display: none }`) is never written, and
the glyph stays.

## Notes

- The symptom, measured on the reported screenshot at 1920×1200: the image spans x 520–1319 and the
  glyph's drawing x 1330–1389, both centred on y 583.5/584 — one flex row, `align-items: center`. The
  glyph's 80px box is part of that row, so the picture itself sits **40px left of the page's middle**.
- Verified in Chromium against a real `SVGSVGElement`: `svg.hidden = true` leaves
  `hasAttribute('hidden')` false and `display` `block`; there is no `hidden` descriptor on the element's
  prototype chain.
- `tests/e2e/test_image_display.py::test_missing_preview_and_projector_icon` asserts the glyph *is
  visible* when the bytes 404 — and passes today for the wrong reason, because the glyph is always
  visible. `test_projector_displays_image_only_on_its_screen` reads the `<img>` and never looks at the
  glyph.
- The same file's audio, video, PDF and slides placeholders are correct: they start hidden in the
  template and are toggled with `setAttribute`/`removeAttribute`. The two `.hidden` assignments for the
  image glyph are the only ones in `static/web/` that target an SVG; the preview modal's placeholders
  are `<div>`s.

## Acceptance sketch

- An image screen whose bytes load shows the image alone, centred on the page's middle.
- An image screen whose fetch fails shows the glyph and no image, in the same box.
- The E2E case asserts both states, and is red against the code this card was filed on.

## Links

- Spec: [157](../specs/157-projector-image-missing-glyph/spec.md)
- Related items: ITEM-114 (image media display, the slice that introduced the placeholder), ITEM-119
  (the dock/projector shared state)
