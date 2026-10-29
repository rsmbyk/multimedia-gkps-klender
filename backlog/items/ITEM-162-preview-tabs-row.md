---
id: ITEM-162
status: in-review
title: 'A song''s verse tabs squeeze the preview title and take the dialog''s first focus'
type: fix
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/153-preview-tabs-row/spec.md
branch: fix/153-preview-tabs-row
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/435
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/434
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-162: A song's verse tabs squeeze the preview title and take the dialog's first focus

## Summary

Opening the Preview of a song shows a focus ring around verse tab `1`, and a long title is squeezed
into the half of the header the tabs leave: the head is a single flex row, so the tab row and the
title compete for its width and the dialog's initial focus lands on the first tab — the first
focusable element in the dialog's DOM order since spec 085 lifted the tabs into the header.

## Notes

Measured on the compose page (develop, 1.22.10) at `/tatib/144/`, 1440×900, dpr 1:

- dialog 704px wide; `.preview__head` 704×59; `#previewTitle` 569.6px of a 730px string — ellipsized;
- `.preview__versetabs` 76.4×30 at x=973.6, sharing the title's row;
- on open `document.activeElement` is `BUTTON.preview__tab` (`1`);
- the same dialog on a **passage** entry is 704×52 and focuses `DIV.preview__body` — the body is what
  the preview focused before the tabs moved into the header, so this is a regression, not a choice.

## Acceptance sketch

- A song preview opens on its reading body: no verse tab carries a ring.
- A long title takes the header's full width; the verse tabs stand on their own row below the header.
- Every preview without verse tabs — passage, text, image, audio, video, PDF — is pixel-identical.

## Links

- Spec: [153](../../specs/153-preview-tabs-row/spec.md)
- Related items: ITEM-034 (spec 032, the preview modal), spec 085 (the identity header), spec 089
