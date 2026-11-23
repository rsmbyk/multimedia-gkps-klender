# Feature Specification: A passage cue carries its current and end verse

**Slice**: `specs/229-cue-verse-counter`
**Branch**: `feat/229-cue-verse-counter`
**Created**: 2026-11-23
**Status**: Draft
**Input**: "in projector, when a bible is displayed, also show the current verse and end verse in cue (or current and last verse of the chapter for goto). put it after the passage reference, separate it with center dot"
**Demand**: `ITEM-244`
**Capability**: `new: projector/R16` (the cue's existing reference-and-flip text is described in `projector/R2`; this adds a counter beside it)

## User Scenarios & Testing

### US1 — A service passage says where it stands (P1)

**Why this priority**: the corner cue is what the operator reads while the congregation sees only the verse. The reference names the passage but never changes as the operator steps through its verses, so a service passage gives no read-out of the current position inside the passage. This is the only behaviour the report asks to change.

**Independent Test**: open `/projector` on a service holding a scripture entry with a start and end verse, step through its verses, and read the counter in `#cue-prefix`: it follows the verse on screen while the end verse holds.

**Acceptance scenarios**

1. **Given** a service passage `Matius 5:3-5` showing verse 3 **When** the cue paints **Then** its prefix reads `Matius 5:3-5 · 3/5 · TB` — the counter after the reference, separated by a centre dot, ahead of the translation flip.
2. **Given** that passage showing verse 4 **When** the operator steps to it **Then** the counter reads `4/5` and the reference, flip and everything else in the cue are unchanged.
3. **Given** a passage with no end verse (`Matius 5:3`) **When** its cue paints **Then** the counter reads `3/3`.
4. **Given** a passage whose translation is missing on screen **When** the cue paints **Then** the counter still reads from the entry's own verse bounds, and no flip is drawn where none was drawn before.
5. **Given** a song, text entry, break or media screen **When** the cue paints **Then** no verse counter appears — only scripture gains it.

### US2 — A passage Go To says where it stands in the chapter (P2)

**Why this priority**: a Go To loads a whole chapter, and its cue reference follows the current verse. It still gives no read-out of the chapter's length, so the operator cannot tell where a verse sits inside the chapter without leaving the cue.

**Independent Test**: open a chapter Go To on the projector, step a verse, then cross into another chapter and read the counter: it follows the verse and the last verse of the chapter currently loaded.

**Acceptance scenarios**

1. **Given** a Go To open on `Matius 5`, first verse of a three-verse chapter **When** its cue paints **Then** the prefix reads `Matius 5:1 · 1/3 · TB`.
2. **Given** that Go To stepped to verse 2 **When** the cue paints **Then** the counter reads `2/3` and the reference reads `Matius 5:2`.
3. **Given** the Go To crosses into another chapter **When** the new chapter paints **Then** the end number is that chapter's last verse, not the old chapter's.
4. **Given** the Go To's edition is flipped or the chapter is reached from a dock or reading-page Go To **When** the cue paints **Then** the counter is identical to one started on the projector.
5. **Given** a song Go To **When** its cue paints **Then** no verse counter appears; baits and Back are unchanged.

### Edge Cases

- **When** the passage's end verse is absent **Then** the end number is the start verse, matching the reference the service already prints.
- **When** the loaded chapter's verse list is empty or absent **Then** no counter is painted rather than a `n/0` or `n/undefined`.
- **When** a screen in a scripture entry is its built-in blank rest **Then** the counter still reads the last scripture verse of the entry; the rest is not a verse.
- **When** the cue's prefix runs a scrolling label (an untitled text entry) **Then** that mechanism is untouched; the counter belongs only to a passage's static label.
- **When** the counter is added at a narrow viewport **Then** the cue's 24px band, its centre alignment and the flip button's hit box are unchanged.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A service scripture entry SHALL carry its start and end verse, and each of its verse screens SHALL carry its verse number, in the projector payload. | `new: projector/R16` |
| FR-002 | The service passage cue SHALL paint a `current/end` counter immediately after the passage reference, separated by a centre dot, before the translation flip. | `new: projector/R16` |
| FR-003 | The counter SHALL follow the verse on the active screen and SHALL keep the entry's end verse while the operator steps through that passage. | `new: projector/R16` |
| FR-004 | The passage Go To cue SHALL paint a `current/end` counter immediately after its reference, where `end` is the last verse of the chapter currently loaded. | `new: projector/R16` |
| FR-005 | The counter SHALL follow a Go To verse step and a chapter crossing, and SHALL be the same for a Go To opened from the projector, the dock or the reading page. | `new: projector/R16` |
| FR-006 | A cue for a song, text, break or media screen SHALL carry no verse counter; a missing end or empty chapter SHALL suppress the counter rather than print an incomplete one. | `new: projector/R16` |
| FR-007 | The counter SHALL reuse the cue's existing text token and box: no new font, colour, height, button or control, and no change to the translation flip's behaviour. | `new: projector/R16` |

### Key Entities

- **Service scripture entry** — the existing `ServiceEntryKind.SCRIPTURE` row: `chapter`, `verse_start`, `verse_end` (nullable), `book_translation`. Its projector entry gains the two bounds; its verse screens gain the verse number already used to build the reference.
- **Passage Go To** — the existing `detour` object: `chapter`, `verse`, `translation` and `editions`, whose `verses` list supplies the chapter's last verse. No new display-state field.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A service passage with verses 3–5 shows `3/5`, then `4/5`, then `5/5`, with the reference unchanged. | Playwright read-back of `.cue-verse` over three arrow steps in `tests/e2e/test_projector.py`. |
| SC-002 | A three-verse chapter Go To shows `1/3`, then `2/3`, then `3/3`, and a chapter crossing changes the end number. | Playwright read-back of `.cue-verse` in `tests/e2e/test_goto_shared_state.py`. |
| SC-003 | No counter is drawn on a song, text, break or media cue, and no `n/0` appears on an empty chapter. | Playwright read-back asserting `.cue-verse` count 0. |
| SC-004 | The existing cue geometry and flip tests stay green: 24px band, centre alignment at 1366×768 and 1920×1080, and a clickable `.cue-translation`. | The 23 pre-existing cue tests in `test_projector.py` and the Go To suite stay green. |

## UI/UX

`static preview at specs/229-cue-verse-counter/preview/index.html` — the real corner-cue markup from
`projector_controls.html` and the real `projector.css`, with the proposed counter text filled in for
the service and Go To states. The data the counter reads is already in the projector payload, so a
static page can show the result; the live route will be measured again after implementation.

- **Before (from the running page)**: cue prefix reads `Matius 5:3-5 ·` then the `TB` flip button;
  a chapter Go To reads `Matius 5:1 ·` then `TB`. No number between the dot and the flip.
- **After**: `Matius 5:3-5 · 3/5 · TB` for the service, `Matius 5:1 · 1/3 · TB` for the Go To.
  The counter is one `<span class="cue-verse">` inside the existing label span, so the flex row
  keeps the same two children and the same `.2em` gap.
- **Measured in the preview (real `projector.css` at 560px)**: the cue resolves to
  `550 16px/16px "CMG Sans", "Source Sans 3", sans-serif`, `rgb(81, 77, 71)`, `letter-spacing: .16px`,
  height 24px; the service prefix box is 166.4 × 24 and the flip button 21.3 × 24, both centred on
  the band. Stepping the button reads `3/5 → 4/5 → 5/5`, and the Go To prefix reads `1/3 → 2/3 → 3/3`.
- **Layout / position**: the cue keeps `left: 32px`, `bottom: 20px`, `height: 24px`, and every part
  stays centred on `viewport height − 32px`; the counters sit between the first centre dot and the
  flip, with the same `' · '` text separators the reference and flip already use.
- **Colour / typography**: inherited from `.cue` — 16px, 550 weight, `line-height: 1`,
  `letter-spacing: .01em`, `#514d47`; the dot is `var(--whisper)`. No new token or face.
- **States**: passage service (start, middle, end verse, single verse), passage Go To (verse step,
  chapter crossing, edition flip, dock-started), song, text, break, media, no service, loading.
- **Motion**: none added or removed.
- **Responsive**: the same DOM at every width; the cue keeps its current `overflow: hidden` and
  ellipsis, and the counter adds four characters at most (`n/nn`).

## Assumptions

- "Current/end counter" was chosen by the owner from three formats on 2026-11-23: `16/18`, not
  `16–18` or `verse 16–18`. The slash form is used for both the service passage and the Go To.
- For a service passage the end number is the entry's `verse_end`, or `verse_start` when it is
  empty — the two numbers the reference already prints, so the counter cannot disagree with it.
- For a Go To the end number is the last verse in the edition being displayed (`translation`, with
  TB then the first edition as fallback), because that is the chapter the operator sees.
- A single-verse passage reads `3/3`; the counter is not hidden for equal numbers.
- The counter is a plain text span, not a button: it adds no control to the cue and no new keyboard
  behaviour.
- The bump is `patch`. The version is applied at delivery, not in the implementation commits.

## Clarifications

### Session 2026-11-23

- Q: How should the added verse text read after the passage reference in the corner cue? → A:
  current/end counter — service `Yoh 3:16-18 · 16/18 · TB`, Go To `Yoh 3:16 · 16/132 · TB`.
