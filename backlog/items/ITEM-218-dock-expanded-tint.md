---
id: ITEM-218
status: done
title: 'An open entry header wears a whisper of a tint'
type: feat
priority: P2
effort: S
created: 2026-11-19
updated: 2026-11-19
spec: specs/206-dock-expanded-tint/spec.md
branch: feat/206-dock-expanded-tint
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/550
issue:
closed_at: 2026-11-20
closed_reason: merged into develop (PR #550)
bump: patch
release_version: 1.34.6
---

# ITEM-218: An open entry header wears a whisper of a tint

## Summary

Since spec 198 a dock header toggles its block and the only mark of the open state is a 15 px
chevron at the far end of the row. The owner asked for a background on an expanded header that is
"really soft as to not actually noticeable by the operator but clearly show that the entry is being
expanded". The header takes one flat wash of the ink colour — 4 % over the rail, exactly half the
8 % the generic hover face already paints — so a closed header still reads as bare rail, an open
one reads as a surface, and the pointer's own feedback stays the loudest state on the row. Hover
replaces the tint rather than adding to it, and the live entry keeps its selected fill.

## Notes

- One CSS rule in `static/styles/design/obs-dock.css`, placed between the base row and
  `.entryrow:hover`; no JavaScript, no new token.
- `.entryrow[aria-expanded="true"]`, `.entryrow:hover` and `.entryrow[aria-current="true"]` all
  weigh (0,2,0), so source order alone decides the cascade: base → open → hover → live.
- The live row is *always* `aria-expanded="true"`, which is why its rule has to stay last.
- The expression follows the sheet's own precedent: `.nextband:hover` is
  `color-mix(in srgb, var(--rail-bg) 92%, var(--ink))`.
- Break rows and entries with an empty block never received `aria-expanded` (spec 198, FR-010), so
  they are untouched without a guard.
- Preview: a static dock at `specs/206-dock-expanded-tint/preview/index.html`, built from the real
  `tokens.css` + `obs-dock.css` and the real rendered dock markup, with 0 / 3 / 4 / 6 % switchable
  and the hover face and the live row on screen for comparison.

## Acceptance sketch

- An open header paints `color-mix(in srgb, var(--rail-bg) 96%, var(--ink))`; a closed one paints
  none. Light `#E5E2DB` (an 8-level step from `#EDEAE3`), dark `#2B2822`.
- The hover face is still stronger (light `#DDDAD3`, a 16-level step): pointing at an open header
  gives the hover face, not a blend of the two.
- The live entry's header keeps `--sidebar-selected-bg` at rest and its own hover tone under the
  pointer, whether its block is open or not.
- The tint arrives and leaves on the row's existing 200 ms `var(--ease)`, chevron included; nothing
  is added to the reduced-motion story.

## Links

- Spec: `specs/206-dock-expanded-tint/spec.md`
- Related items: ITEM-208 (spec 198 — headers toggle, items jump), ITEM-210 (spec 200 — the live
  entry and following)
