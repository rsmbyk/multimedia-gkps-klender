---
id: ITEM-180
status: done
title: The overlay reads by kind: a passage is a quotation card, a liturgy is a script panel
type: feat
priority: P1
effort: S
created: 2026-10-30
updated: 2026-10-30
spec: specs/180-overlay-text-styles/spec.md
branch: feat/180-overlay-text-styles
pr: 472
issue: 471
closed_at: 2026-10-30
closed_reason: merged into develop (#472)
bump: minor
release_version:
---

# ITEM-180: The overlay reads by kind: a passage is a quotation card, a liturgy is a script panel

## Summary

The OBS caption overlay paints every text-bearing screen as a lyric subtitle: white 800-weight ink with a fat black
outline, no plate, and the screen's heading thrown away. That is right for a song, whose lines are the song. It is
wrong for a scripture reading — the stream shows a verse with no idea which passage it is — and for a liturgy, whose
title and speaker cues never reach the stream at all. A passage and a liturgy text should wear a plate: a quiet dark
card that carries the Bible reference and the verse's own title, or the entry's title, above the words.

## Notes

- Measured at 1920×1080 on service 144 (25 Oct 2026): the caption paints 1728×202 at (96, 824), Source Sans 3 800 at
  72 px, transparent fill; `linesOf()` reads `screen.lines` only, so `header` and `lines[].voice` never reach the
  overlay.
- The screen already carries everything a plate needs: `header` (`"Kisah Para Rasul 1:1\nRoh Kudus dijanjikan"` for
  the passage), `lines[].voice` (`leader` · `assembly` · `join`), and `entry_index` into the projector's entry island.
- The overlay already fetches `/projector?service=<id>`; it reads one island from the response and now needs the
  entry island too (one fetch, cached per service).
- Heading data is uneven: 1320 of 2714 legacy text items carry a title, both new-kind `TEXT` entries carry none, and
  one keeps its section heading as its first body line. The plate must not assume a heading — and must not promote a
  body line into one.

## Acceptance sketch

- A song screen is unchanged: caption, 800 weight, outline, no plate, no heading (1728×202 at (96, 824)).
- A passage screen paints a centred card with the reference as its kicker, the verse title under it, a hairline, and
  the verse beneath: 1728×238 at (96, 788), 11.52 px corner, at 1920×1080.
- A liturgy screen paints a left-aligned panel with a 4.07 px bar on its leading edge, its entry title above the
  turns, and a leader line quieter than the assembly's: 1544×201 at (188, 825) with a title.
- A speaker line long enough to wrap hangs under its words: the mark holds its own column, so `Pelayan :` and `L.`
  both leave every wrapped row starting at the words' x.
- Long text takes the frame's full 90 % measure before the panel grows taller: a 467-character verse is five rows
  (373 px) instead of six (423 px) at 78 %.
- The translation flip rewrites the heading and the words together; blank, break and media screens still paint
  nothing; hide and release still empty the stage; nothing on the page is focusable.

## Links

- Spec: [165](../specs/180-overlay-text-styles/spec.md)
- Preview: [overlay-preview.html](../specs/180-overlay-text-styles/preview/overlay-preview.html)
- Related items: ITEM-119 (the dock, projector and overlay under one state), ITEM-002 (projection controls)
