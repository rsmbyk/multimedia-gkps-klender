# Feature Specification: a text screen arrives as fast as the entries beside it

**Slice**: `specs/219-projector-fit-cost`
**Branch**: `fix/219-projector-fit-cost`
**Created**: 2026-11-22
**Status**: Accepted (Gate 1, 2026-11-22 · Gate 2, 2026-11-22)
**Input**: the owner's report, 2026-11-22, in two parts — "in projector, when you are advancing to a
text entry, or a screen of the same text entry, there is a delay of the text showing. you can clearly
feel it as it is not as fast as the other entries/screens", and then, with a screenshot of three
overlapping texts, "then screen goes weird when you hold down left/right keys".

The projector fits a screen's words to the stage by walking the font size down from 200 px one pixel
at a time, asking after each step whether the words still fit. Every question reads
`scrollHeight`/`clientHeight`, which lays the page out again, and the page carries **every** screen of
the service at once (R2). So an advance into a screen of words spends 130–280 layout reads between
the key and the frame that paints it, and the number of reads is the distance the body has to come
down: a short lyric settles near 124 px, a text entry comes down to 40 px. That is the reported
defect, and it is worst exactly where the owner reported it — on the longest bodies, which are the
text entries the operator reads from.

Two further faults sit on top of it. The fit runs *after* the arrival morph has started, so it
measures the words 14 px below where they come to rest: the same screen is fitted to 131 px on an
advance and 135 px on a resize (**53 of 126 screens** disagree with themselves), and the arrival
animation is stalled by the fitting while it plays. And the single-screen cut trims the last row's
words one character at a time — 2 992 ms for a 400-row body.

A third is the owner's second report. Every move starts a 240 ms crossfade, and a held arrow key sends
a move every ~35 ms: each move restarted a crossfade the previous one had not finished, so the
part-faded screens piled up behind the new one — **seven painted at once**, their words reading as one
garbled block.

## User Scenarios & Testing

### US1 — A text screen arrives as fast as any other (P1)

**Why this priority**: this is the report. During a live service the operator advances on the beat of
the liturgy; a screen that arrives a tenth of a second late is a visible stumble, and it is the text
entries — the ones the operator is reading from — that stumble.

**Independent Test**: open the projector for a text-heavy service, press ArrowRight once per screen at
a 250 ms beat and time the key's own handling; every screen of words after the first costs one layout
read (the stage's height) instead of ~130, and the advance lands in 3.7 ms median against develop's
16.4 ms.

**Acceptance scenarios**

1. **Given** the projector showing a service of text entries **When** the operator advances at a
   human beat **Then** the arriving screen was already fitted, so the press costs one layout read and
   the frame is painted at 3.7 ms median (worst 7.4 ms) against develop's 16.4 ms (worst 66.9 ms).
2. **Given** the same service **When** the operator advances faster than the page can idle — every
   screen unfitted **Then** the screen is still fitted on arrival, exactly as before, and shows the
   same size.
3. **Given** any screen of words **When** it is fitted **Then** it holds the largest size that fits:
   nothing overflows the stage and one pixel larger does not fit.

### US2 — The size a screen shows does not depend on how it was reached (P1)

**Why this priority**: the fitting measured a moving box, so the same screen showed a different size
on an advance than on a resize. The operator sees a screen at a size the display itself disagrees
with.

**Independent Test**: walk the service on develop and on the slice, recording each screen's size on
arrival and again after a resize; on develop 53 of 126 screens differ, on the slice none do, and the
slice's arrival sizes are exactly develop's at-rest (resize) sizes.

**Acceptance scenarios**

1. **Given** a screen arriving at the end of an advance **When** the fit runs **Then** it measured the
   screen at rest, and a resize immediately afterwards changes nothing.
2. **Given** the bundled display faces arrive after first paint **When** they land **Then** every
   remembered fit is discarded and the screen showing is fitted again in the real face.
3. **Given** a passage whose translation is switched **When** the header text changes **Then** the
   screen is fitted again with the new header.

### US3 — A single-screen text is cut without a per-character layout (P2)

**Why this priority**: the cut is the worst case of the same fault, and it is what a long single-screen
text entry pays on every arrival.

**Independent Test**: give the active screen a 400-row body as a single-screen text and re-fit; the
same rows and characters are kept as before (116 rows, 10 711 characters, 2 px), in 81.5 ms instead of
2 992 ms.

**Acceptance scenarios**

1. **Given** a body that cannot fit at any size **When** it is shown as a single-screen text **Then**
   the same rows are dropped and the same characters trimmed, found by halving rather than one row
   and one character at a time.

### US4 — Holding the arrow key cuts through screens instead of piling them up (P1)

**Why this priority**: reported by the owner, 2026-11-22, with a screenshot — "then screen goes weird
when you hold down left/right keys". The operator holds the key to run down a list quickly; what they
get is a garbled block of three or more overlapping texts, because every move starts a 240 ms
crossfade and a held key sends a move every ~35 ms, so the earlier crossfades are still in flight.

**Independent Test**: hold ArrowRight for a burst of 34 repeats at 35 ms, sampling every frame's
painted screens; on develop up to **7** screens are painted at once and 64 frames carry more than one;
on the slice the worst frame paints **1** (the first move's own crossfade shows 2 for one frame).

**Acceptance scenarios**

1. **Given** the display showing a screen **When** the operator holds ArrowRight or ArrowLeft **Then**
   each move is a cut: exactly one screen is painted at any moment, and the words never overlap.
2. **Given** a held key has just stopped **When** the operator makes one more move after the morph
   window (260 ms) **Then** that move morphs as it always did.
3. **Given** a single move **When** nothing was moving before it **Then** it keeps its crossfade — the
   cut is only for a move that arrives while a morph is still running.

### Edge Cases

- **When** the service has no screens, or a screen carries no words **Then** nothing is fitted and the
  advance costs what it costs today (≈1.5 ms).
- **When** a jump lands on a screen nothing has fitted (Home, End, `Ctrl`+arrow, a Go To) **Then** the
  screen is fitted on arrival exactly as before.
- **When** the window is resized **Then** every remembered fit is void — the stage is in the key — and
  the screen showing is fitted immediately while the neighbours follow in idle time.
- **When** no size fits, down to the 2 px floor **Then** the words are shown at 2 px and a
  single-screen body is cut, as before.
- **When** a Go To detour is on the stage **Then** no neighbour is fitted: the service's own screens
  are not what the operator is about to show.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The fitting SHALL measure the screen at rest: it SHALL run before the arrival morph puts a transform on the screen, so the size a screen shows does not depend on how far into the morph the fit happened to run. | `projector/R14` (added) |
| FR-002 | The screens either side of the one showing SHALL be fitted in idle time, and a screen that has not been fitted ahead of time SHALL still be fitted on arrival — the fit's result SHALL NOT depend on the idle work having run. | `projector/R14` (added) |
| FR-003 | A fitted screen SHALL be remembered by its stage size and its body, so a screen fitted ahead of time costs nothing on arrival; every remembered fit SHALL be discarded when the bundled display faces arrive. | `projector/R14` (added) |
| FR-004 | The fitting SHALL still show the largest size that fits — the walk from 200 px down is kept, because a refusal is not monotone in the size (a larger size re-wraps the words onto more, narrower lines), so a search that halved its range would settle on a smaller size than the screen allows. | `projector/R14` (added) |
| FR-005 | The single-screen cut SHALL find the rows it drops and the characters it trims by halving, keeping the same rows and the same characters as the one-at-a-time cut. | `projector/R14` (added) |
| FR-006 | A resize, the bundled faces arriving, and a header rewritten by the passage translation SHALL each re-fit, as today. | `projector/R14` (added) |
| FR-007 | A move that arrives while a morph is still running — a held arrow key, or two moves in quick succession — SHALL cut rather than morph: the screen leaving SHALL be settled at once and the screen arriving SHALL be painted whole, so exactly one screen is painted at any moment. | `projector/R15` (added) |
| FR-008 | A move that arrives after the morph window has passed SHALL keep its crossfade, and the morph window SHALL be 260 ms — the length of the morph it follows. | `projector/R15` (added) |

### Success Criteria

| ID | Criterion | Verification |
| --- | --- | --- |
| SC-001 | Advancing into a screen of words costs no fitting when the page has had a moment to idle. | Live probe, 1440 × 900, service `Ibadah Minggu` (171 screens, 126 with words): **135.6 → 1.0** layout reads per advance, worst **282 → 1**. |
| SC-002 | A paced advance lands inside a frame. | Live probe, 250 ms between presses: **16.4 → 3.7 ms** median, p90 **34.0 → 5.7 ms**, worst **66.9 → 7.4 ms**. |
| SC-003 | A rapid advance — nothing fitted ahead of time — is no worse than today. | Live probe, no gap: median **13.9 → 2.3 ms**, worst **70.4 → 67 ms** (the fallback path, unchanged in kind). |
| SC-004 | A screen shows the size its own at-rest fit gives. | `preview/verify_sizes.py`: develop's advance disagrees with its resize on 53 of 126 screens; the slice's advance disagrees with develop's resize on **0 of 126**. |
| SC-005 | The fitting contracts still hold: the largest fitting size, the gap between a screen's own lines, a single-screen body on one screen, and a paced advance that fits nothing. | `tests/e2e/test_projector.py` — `test_a_body_too_long_for_the_screen_comes_down_to_fit`, `test_a_gap_opens_between_the_words_own_lines`, `test_a_single_screen_text_fits_its_whole_body_on_one_screen`, and the new `test_a_text_screen_arrives_without_being_fitted`. |
| SC-006 | A single-screen cut keeps its rows and characters, and stops taking a second per arrival. | Live probe: 400-row body **2 992 → 81.5 ms**, same 116 rows / 10 711 characters / 2 px. |
| SC-007 | A held arrow key paints one screen at a time. | `preview/hold_probe.py` (34 repeats at 35 ms, sampled every frame): screens painted at once **7 → 1**; frames carrying more than one screen **64 → 1**. |
| SC-008 | The cut does not reach a single move: after a quiet moment a move still crossfades, and the arriving screen still rises. | `tests/e2e/test_projector.py::…::test_a_single_move_still_morphs`, `test_moving_and_toggling_morph_rather_than_jump`. |

## UI/UX

**live preview at `http://127.0.0.1:8791/projector?service=144`** — the real projector served from
this worktree; the change is the time a screen takes to arrive, so only the live page can show it.
Fixture: the local service **Ibadah Minggu** (16 entries — text, scripture, song, media — 171 screens,
126 of them carrying words), viewport 1440 × 900, dark, 1×. Measured by `preview/probe.py` (fresh
per-page reads; press, then wait 250 ms for the idle work, then press again) and
`preview/verify_sizes.py` (arrival size against the size a resize gives).

| | develop | this slice |
| --- | --- | --- |
| paced advance, median | 16.4 ms | 3.7 ms |
| paced advance, 90th percentile | 34.0 ms | 5.7 ms |
| paced advance, worst | 66.9 ms | 7.4 ms |
| layout reads per advance, mean | 135.6 | 1.0 |
| layout reads per advance, worst | 282 | 1 |
| rapid advance, median | 13.9 ms | 2.3 ms |
| a blank screen (no words) | 1.0–1.8 ms | 1.0–1.8 ms |
| single-screen cut of a 400-row body | 2 992 ms | 81.5 ms |
| screens whose arrival size differs from their resize size | 53 of 126 | 0 of 126 |
| screens painted at once while the key is held | 7 | 1 |
| frames carrying more than one screen, holding the key | 64 | 1 |

- **What the operator sees**: the same arrival morph (240 ms `screenIn`), now starting from the first
  frame that can paint it instead of stalling while the words are measured; the same sizes as the
  display's own at-rest fit; the same corner cue, and the same fit for images, PDFs and slides.
- **What changes on screen**: a screen of words may be one to eight pixels larger than it was, because
  it is now fitted where it rests rather than 14 px below it. That is the fix to US2, not a new look:
  every size equals the one the display already showed after a resize.
- **Holding the key now cuts** instead of crossfading: the screen you land on is painted whole,
  instantly, and the one you left is gone at once. A single move, after a quiet moment, still
  crossfades over 240 ms exactly as before.
- **Reduced motion** (`prefers-reduced-motion: reduce`): the morph is instant; the fitting is the same
  in either build.

## Assumptions

- **The measured service is representative.** It is the only local service that mixes text, scripture
  and song at projector scale (171 screens); a service of songs alone settles at a larger font, does
  fewer reads, and is faster on both builds — the defect is largest exactly where the owner reported
  it, on the longest bodies.
- **250 ms between presses is the operator's beat.** The idle work needs one idle period; the rapid
  run in the probe presses with no gap at all, which is the floor and is reported separately. Both are
  in the table so the claim does not rest on the friendlier number.
- **The search stays a walk from 200 px down.** Halving the range was tried and rejected on evidence:
  the refusal is not monotone in the size (a real screen is refused at 101–105 px and fits again from
  106 px to 137 px, because the words re-wrap onto more, narrower lines), so a halved search settled
  on 90 px where the screen allows 137 px. Exactness costs the reads, so the reads are moved off the
  arrival instead of being reduced.
- **Layout containment on `.screen` was tried and dropped**: `contain: layout size` measured 8.3 ms
  median against 7.8 ms without it on the same advance — within noise, so the CSS change was not
  worth its risk.
- **The stage's own box is read once per fit** rather than on every trial; it cannot move while font
  sizes inside a screen change, and every path that re-fits still measures it afresh.
- **A fitted screen is remembered by stage size and body** (header text, row count, text length). A
  content change the page does not re-render — the Go To detour's own steps — changes that key, and
  the bundled faces arriving clears every key.
- **No cache across stages and no pre-fit of the whole service**: fitting every screen at load would
  cost about a second of idle work for a service this size, and an operator who jumps needs the
  on-arrival fit anyway.
