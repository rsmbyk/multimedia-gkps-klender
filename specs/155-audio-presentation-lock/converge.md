# Convergence: a playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-29

Every row of `plan.md`'s traceability table was checked against the code and a run.

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The `is-fullscreen` class `syncAudioFullscreen` toggled on the audio box broke `test_untitled_preview_and_projector_idle_display_off`, which asserts the box's exact class list (`screen__audio-box is-idle`). | `unrequested` | FR-009 | `tests/e2e/test_audio_display.py` ran `screen__audio-box is-fullscreen is-idle`; nothing reads that class (`projector.css` styles `:fullscreen`), so it was removed rather than the assertion widened. |
| `test_projector_space_navigation_and_reset` navigated away from a **playing** audio screen and expected the player to go; FR-001 forbids that navigation. | `contradicts` | FR-001 | The case now pauses before it navigates; its other claims are untouched, and the flip is recorded in the spec's "Pins that flip". |
| The pause case read the clock a fixed 1100 ms after the keypress and saw `0:00` — the fixture's blob, metadata and play take longer than that on this machine. | `partial` | SC-002 | The case now waits for the readout itself (`elapsed !== '0:00'`); the same wait was added to `preview/probe_lock.py`'s `open_audio_screen`. |

Runs in this pass:

- `manage.py test tests.e2e.test_audio_display --keepdb` → 13 cases, **1 failure**:
  `test_untitled_preview_and_projector_idle_display_off`, at its `stop`-broadcast assertion
  (`data-showing` stays `true`).
- `manage.py test tests.e2e.test_video_display --keepdb` → 8 cases, **1 failure**:
  `test_navigation_and_display_off_stop_and_reset_video`, at the same assertion.

Both failures were proved on the base under the same environment — the slice's static changes stashed,
one test each, `DATABASE_URL=…/gkps155 --keepdb` — and both reproduce identically there. They are
card **ITEM-140** ("The projector keeps data-showing=true when display-off is asked for — audio and
video display-off tests never see the projector leave its showing state; identical on develop"). No
`stop` message has a handler (`static/web/projector.js` reads `show`/`hide`/`release`/`flip`/`update`
only), which is the same finding from the code side.

Live route (`preview/probe_lock.py --base http://127.0.0.1:63404`, worktree server on the compose
origin, a real 5:02 MP3): **14/14 checks** read as the spec says — the takeover is
`screen__audio-box` at 1440×900 with the cue outside it, ten key forms and a zone click move nothing,
`g`/`j` stay shut, Space pauses with the clock kept and the keys back, a held `Escape` exits and
pauses, the end returns, and a refused fullscreen still locks.

**Outcome**: three findings. Two were fixed in this pass (the class removal and the clock wait), one
was a pin that the requirement supersedes (rewritten and recorded). No task was appended.

## Pass 2 — 2026-10-29

Re-read after the fixes: the audio module is 12/13 green with the one ITEM-140 red, the video module
7/8 green with the same card's red, the probe 14/14, and every requirement resolves to a green run or
its recorded inspection (FR-010 — the keydown guard names no `c`/`t`, and both handlers sit below it).
The video path's own case `test_projector_fullscreen_play_pause_and_navigation_guard` is green, so the
audio helpers did not move the video's behaviour.

**Outcome**: Converged — nothing remains.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| The full suite has not been run on this branch: the repository carries no workflow (`.github/workflows` is absent on `develop`, and the API's "CI" entry is orphaned), so the full matrix is a manual run at the push step. | `partial` | low | 2026-10-29 — the run belongs to the push step (T015's neighbour), and this record names the known-reds to expect: ITEM-140 (audio + video display-off), ITEM-153 (touch controls), ITEM-144 (five date-picker cases), ITEM-139 (three offline projector), ITEM-141 (bible edition), ITEM-159 (three text-wrap/add-controls), ITEM-156 (media-entry spacing). |

## Cap reached

<!-- not reached: pass 2 converged -->
