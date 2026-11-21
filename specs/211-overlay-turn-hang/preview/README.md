# Preview: A speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`
**Shape**: `static`
**Open**: `specs/211-overlay-turn-hang/preview/index.html` — open the file directly

## Run

```sh
none: open the file directly
```

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| the owner's case | default tab | the continuation's first glyph sits on the marked line's words x; the plate may widen by the indent |
| a turn that wraps | second tab | every visual row of the long continuation stays on the words x, and no ink passes the plate |
| no mark on the screen | third tab | nothing moves: no speaker column exists, so the lines stay at the plate's content edge |

## Live or static

**Static** — one page assembled from the project's real `obs-overlay.css`, its design tokens and
bundled faces, with the plate's real classes and markup. The frames are laid out at 1280×720 so
container units resolve at the real size; only the paint is scaled. "Before" is today's row;
"After" adds the one declaration this slice proposes. The readout measures the marked words and the
continuation on each frame live.

**What it cannot show:** the row is hand-marked with `is-continuation` in the after frames; the
slice's script adds that class at paint time from `line.voice && !line.mark` and a screen that
paints at least one mark. The live E2E covers that path.
