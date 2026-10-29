# Implementation Plan: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md`
**Branch**: `feat/154-audio-times-inline`
**Bump**: `patch` — 1.22.10 → 1.22.11 (VER-10: a fix is a patch)
**Preview**: live preview at `http://localhost:8814/tatib/144/` (entry `e1`'s Preview), slice worktree

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Django template (server-rendered HTML) + hand-written CSS; Playwright (Python) for the test |
| Primary dependencies | none added |
| Storage | none — the line is a view of the `<audio>` element, never persisted |
| Testing | `tests/e2e/test_audio_display.py`: one new case, `_assert_times_are_one_right_aligned_pair`, plus the five existing cases as the regression net |
| Target platform | every browser the app supports (Chromium E2E; `-webkit-`/`-moz-` slider rules already exist and are untouched) |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none — no request, no listener, no paint budget added; one declaration changes |
| Constraints | the two `data-audio-*` spans keep their selectors and their order (D004); the line stays under the bar; the projector's own `.screen__audio-times` is not touched; the dialog, play button, filename and bar keep their boxes |
| Scale / scope | 1 markup line in `tatib.html`, 1 declaration in `components.css`, 1 E2E case + 1 helper, 1 board card, 1 slice pack |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never created automatically), so the check does not apply;
the Constraints row stands in its place.

Re-checked after Phase 1: pass — the design adds no file to the product, no request, no state, and no
script.

## Phase 0 — Research

See `research.md`. Five decisions, each measured or read from the code: right-align the pair (D001), one
declaration on the existing flex row (D002), a real text separator (D003), no JS change (D004), and the
preview origin's place in the companion allowlist (D005). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the line's three children, the two selectors that must survive, and the four
  invariants that keep `media-audio.js` working.
- `contracts/` — `none` (`contracts/none.md`): no external interface.
- `quickstart.md` — the DB-isolated commands, the new case, the module, the preview and its companion
  requirement.

### The design

`multimedia/web/templates/reading/tatib.html:56`:

```html
<div class="audio-player__times"><span data-audio-elapsed>0:00</span><span class="audio-player__separator">/</span><span data-audio-total>0:00</span></div>
```

`static/styles/design/components.css:2134`:

```css
.audio-player__times { display: flex; justify-content: flex-end; align-items: baseline; gap: 5px; margin-top: 7px; font-size: 12px; color: var(--head-ink); }
```

**What is deliberately not done.** No wrapper element, no `margin-left: auto` exception inside a rule that
still says `space-between`, no pseudo-element separator, no change to `media-audio.js`, no change to
`.screen__audio-times`, no move of the line out from under the bar, no new token, no typography change.

### Verification

`tests/e2e/test_audio_display.py` gains
`test_preview_times_read_current_over_total_beside_the_bar`: the times line's text must match
`^\d+:\d\d\s*/\s*\d+:\d\d$`, then `_assert_times_are_one_right_aligned_pair` measures the three boxes —
one line, ≤10px from the played time to the separator and from the separator to the total, played before
total, the pair's right edge on the seek bar's (±1px), and the played time in the bar's right half — and
re-measures after Space + a seek, so the line's stability during playback is asserted, not assumed.

## Traceability

| Row | Requirement | Component | Verified by |
| --- | --- | --- | --- |
| FR-001 | The line reads `current / total` on one line, in that order | `tatib.html:56`, `components.css:2134` | test — `test_preview_times_read_current_over_total_beside_the_bar` (text shape + order) |
| FR-002 | The pair is right-aligned to the bar; the played time is not at the bar's left end | `components.css:2134` (`justify-content: flex-end`) | test — same case (`total.right ≈ seek.right`, `elapsed.left > seek.left + width/2`) |
| FR-003 | Both numbers keep updating in place, the line does not move | `media-audio.js:37-44` (unchanged) + the fixed right edge | test — the same case re-measures after `Space` and a seek `fill('1')` |
| FR-004 | Nothing else changes: dialog, play button, filename, bar, gap, type, states, projector | the slice's diff | inspection — `git diff` touches 2 product lines; the before/after probe table in spec §UI/UX holds every other box identical |
| US1-S1 | An opened Preview reads one pair, 5px either side of the separator | markup + CSS | test — as FR-001 |
| US1-S2 | The pair ends on the bar's edge; the played time starts in the bar's right half | CSS | test — as FR-002 |
| US1-S3 | Playing or seeking keeps both numbers updating in place | `media-audio.js` | test — as FR-003 |
| US2-S1 | Both surfaces read `current / total`, played first | `tatib.html:56` vs `projector.html:47` | inspection — the two templates' times lines read `/` in the same order |
| US2-S2 | The projector's line keeps its own size, colour, margin and alignment | `projector.css:94`, `projector.html:47` | inspection — neither file appears in the diff |
| SC-001 | The pair is one right-aligned group under the bar | live preview | manual — open the preview at 1440×900, read `0:00 / 5:02`, measure the three boxes (spec §UI/UX) |
| SC-002 | The played time left the bar's left end | live preview | manual — same preview: played time at x 941.9, was x 500 |
| SC-003 | The suite can see the shape | the new case | test — red on `develop`'s markup (`0:000:10`, 456.4px apart), green on the branch |
| SC-004 | Nothing else on the dialog moves | before/after probe | inspection — spec §UI/UX table: dialog, player, bar, y positions identical |
| E1 | Unknown duration keeps the shape | markup's initial `0:00` / `0:00` | manual — open the Preview before metadata lands: `0:00 / 0:00`, same alignment |
| E2 | Past an hour stays one line (`62:03`) | `clock()` (`media-audio.js:24`) | inspection — the formatter is untouched and never wraps minutes |
| E3 | Unavailable keeps the player hidden | `.preview__audio-unavailable` | test — `test_missing_audio_states` |
| E4 | Narrow viewport stays right-aligned, clear of the play button | `components.css:2134`, `@media (max-width: 560px)` | manual — 420×820: dialog 382px, pair x 318.9→381, 232px clear |
| E5 | Dark theme keeps `var(--head-ink)` | tokens | manual — `data-theme="dark"`: rgb(156, 154, 145), 12px |

**Verification split**: 8 test · 5 inspection · 5 manual.
