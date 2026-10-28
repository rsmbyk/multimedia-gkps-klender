---
id: ITEM-155
status: ready
title: 'A long transfer name ellipsizes instead of moving the icon column'
type: fix
priority: P2
effort: S
created: 2026-10-28
updated: 2026-10-28
spec: specs/147-transfer-icon-column/spec.md
branch: feat/147-transfer-icon-column
pr:
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/416
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-155: A long transfer name ellipsizes instead of moving the icon column

## Summary

In the Transfers dialog, the rows whose name is long enough to be ellipsized sit 5.5px left at the
glyph and 11px left at the name and status label. The cause is `components.css:2753`: the 32px mark
is a flex item, so it shrinks — from 32px to 21px and 22.75px on the two long rows — and everything
after it starts sooner. Measured on the owner's nine-row list.

## Notes

- Owner report with a screenshot of `/media-library/`: "why do some items alignments are off from the
  others". Two of nine rows affected.
- `.media-transfers__main` already ellipsizes correctly (`nowrap` + `text-overflow`); only the icon
  column pays for the overflow. The service-media status dialog has the same look but a grid with a
  38px column, so it does not collapse.
- The proposed fix is one declaration, `flex: none` on `.media-transfers__mark`; the fixed preview
  measures a 0.0px spread on all nine rows at a 580px and at a 388px dialog.

## Acceptance sketch

- Every row's glyph shares one left edge and every name/status label shares one, in a list that
  mixes short and long names.
- The long names still end in an ellipsis, and the row stays 72px tall.
- Unchanged: the rows drawn, their order, the divider, the rail.

## Links

- Spec: [147](../../specs/147-transfer-icon-column/spec.md)
- Preview: [preview.html](../../specs/147-transfer-icon-column/preview/preview.html)
