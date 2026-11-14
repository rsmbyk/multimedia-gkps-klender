# Fold: a playing recording owns the projector screen until it pauses

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-10-29

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R5` | A playing recording owns the projector screen until it pauses: while an audio entry's recording plays, no page step, entry or bait jump, page boundary, mouse zone, corner-cue control or Go To moves the projector; the recording takes the viewport as a playing video does; the pause that gives the screen back keeps the position; a refused fullscreen still locks; the display channel stays authoritative. |

`R1`–`R4` are unchanged — this behaviour fails alone. It folded as **R5** because develop had already
taken `R3` (image placeholder, spec 157) and `R4` (the audio screen's playback control, spec 156) while
this slice was in flight; `R5` is the reading `R4`'s "the page does not enter fullscreen" leaves room for,
since the takeover is the audio screen's own box.

## Drift guard

- **Files changed in this capability**: `static/web/projector.js`, `static/web/media-audio.js`,
  `static/styles/design/projector.css`, `tests/e2e/test_audio_display.py`
- **Declared no behaviour change**: no — the delta is the behaviour these files add, and the four
  changed files are exactly the ones `plan.md`'s traceability table names for every FR.

**Idempotence**: re-running this fold compares `R3`'s text before adding it; the requirement is added
once, and the header's `last folded` and `slices` fields take 2026-10-29 and
`155-audio-presentation-lock` once.
