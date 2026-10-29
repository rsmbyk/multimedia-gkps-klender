# Data Model: a playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md`

Nothing stored changes: no model, no field, no migration, no localStorage key, no channel message.
What this slice adds is a **derived** predicate and the rules that hang off it.

## Entities

### Locked state (derived, never written)

| Part | Source | Constraint |
| --- | --- | --- |
| `audioHost` | `static/web/projector.js:104` — the `.screen__audio-box` of the active screen | non-null only while an audio screen is active and something is showing |
| `audioPlayer` | `:117` — the `GKPSMediaAudio.attach` handle | non-null once the recording's metadata has loaded |
| `audioPlaying()` | `:93` | true iff both are non-null and `audioPlayer.audio.paused === false` |

**Relationships**: one active audio screen → one host → one player → one locked state. The state follows
the screen and the element; it is re-read at each input, never cached.

**Validation**: three invariants.

1. **The state is read, never stored** — every guard calls `audioPlaying()` at the moment of the input,
   so a pause shows up in the guard synchronously, and a screen change cannot leave a stale lock behind.
2. **Clearing the screen clears the lock** — `clearAudioScreen()` (`:105`) nulls the host and the
   player, so display-off, a dock `stop`, a dock screen change or an adopted service all release it
   by the same path that releases the recording.
3. **The lock never reads the fullscreen element** — FR-008's fallback depends on it: the guarded state
   is playback, not the browser's permission.

**State transitions**

| From | Event | To |
| --- | --- | --- |
| unlocked | `Space` / the player's own play while an audio screen is active | locked, audio box fullscreen (or normal screen if refused) |
| locked | `Space` (pause) | unlocked, fullscreen left, position kept |
| locked | browser leaves fullscreen (held `Escape`) | unlocked, recording paused at that point |
| locked | recording ends | unlocked, screen returns, element holds the end |
| locked | dock `hide`/`stop`, or a screen the dock names | unlocked, recording stopped and released (existing rule) |

### Audio screen (unchanged)

The `.screen` markup, the `data-media-audio` sha256 and the player's two times are untouched by this
slice; only the box's fullscreen box-model rule is added.
