# Feature Specification: Project Button on the Song and Bible Pages

**Slice**: `specs/193-reading-project-button`
**Branch**: `feat/193-reading-project-button`
**Created**: 2026-11-14
**Status**: Accepted (Gate 1, 2026-11-14)
**Input**: "i want you to add project button on songs and bible verses pages. it open the bible chapter and song as goto detour. it also opens projector window if none open."

## User Scenarios & Testing

### US1 — Project the open song (P1)

**Why this priority**: The song page is the surface an operator reads from during worship; putting its song on the projector without leaving the page is the core of the request.

**Independent Test**: Open a song page, click its Project control with the projector window closed, and verify the projector shows that song's first screen as a Go To detour; press Back on the projector and verify whatever was on air before returns untouched.

**Acceptance scenarios**

1. **Given** a song on stage (`/songs/<id>/`) **When** its Project control is clicked **Then** the projector puts that song on air as a Go To detour at its first screen, and any detour that was on air is replaced.
2. **Given** the projector window is closed **When** the control is clicked **Then** `/projector` opens in the browser's `gkps-projector` window already showing the song detour; no second window is ever opened while one exists.
3. **Given** the projector window is already open **When** the control is clicked **Then** the same window is brought to the front showing the new detour, without reloading the page.
4. **Given** the projector already shows THIS song as its detour (started here or at the dock) **When** the control is clicked again **Then** nothing changes on the projector: no fetch, no repaint, and the detour keeps its current place; the window is still opened or brought forward.
5. **Given** an in-page navigation from one song to another (the stage swapped in place) **When** the arriving page renders **Then** its Project control works without a reload.

### US2 — Project the open chapter (P1)

**Why this priority**: The same one-click act for the Bible reader; it ships in the same slice because it is the same control, the same window act, and the same Go To pointer with a passage shape.

**Independent Test**: Open a chapter page (`/bible/<book>/<chapter>/`), click its Project control, and verify the projector detours to that chapter at its start verse in the edition the page is showing; the projector's TB/SIM flip reaches the other edition.

**Acceptance scenarios**

1. **Given** a chapter on stage **When** its Project control is clicked **Then** the projector puts that chapter on air as a Go To detour starting at verse 1, in the edition the page shows (TB by default, SIM when the page is reading SIM).
2. **Given** the page is reading SIM **When** the control is clicked **Then** the detour paints SIM, and the projector's edition flip reaches TB.
3. **Given** a book page with no chapter on stage (`/bible/<book>/`) **When** it renders **Then** no Project control is drawn.
4. **Given** the control drawn **When** the header lays out **Then** the control sits in the title row, right of the TB/SIM switch — title left, switch and control at the right end.
5. **Given** the projector already shows THIS chapter as its detour **When** the control is clicked again **Then** nothing changes on the projector — no fetch, no repaint, place kept — and the window is still opened or brought forward (US1 scenario 4's rule on a passage).
6. **Given** the projector window closed or open **When** the control is clicked **Then** the window behaves exactly as US1 scenarios 2–3.

### Edge Cases

- **When** the song has no verses **Then** no control is drawn — a detour with nothing to paint would blank the projector.
- **When** a detour from any surface (dock find band) is already on air **Then** the click replaces it; the existing Go To rules govern.
- **When** a service is on air **Then** the service, its screen and its translation are preserved underneath the detour; Back on the projector returns to them.
- **When** the browser blocks the popup **Then** no window opens and the Go To still goes on air.
- **When** a saved (offline) reading page renders **Then** no control is drawn — the saved renderer draws no project controls today (Tata Ibadah included), and the Go To payloads are server reads.
- **When** a hymn song (numbered, cited `PKJ 4`) or an ordinary songbook song is on stage **Then** both get the control; the detour is keyed on the song's id, not its citation.
- **When** the page is narrower than 720px **Then** the control is not drawn, on the same terms as reading/R14's rule for the Tata Ibadah project controls.
- **When** the display state belongs to another browser session **Then** spec 184's session boundary governs as today; the control writes fresh state and is unaffected.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The song page SHALL draw a Project control in the stage header's actions group, in the same anatomy and slot as the Tata Ibadah page's project group (`.read__project` / `.read__project-btn`). | `reading/R42` (new) |
| FR-002 | The Bible chapter page SHALL draw the same control whenever a chapter is on stage, in the title row at its right end, immediately right of the TB/SIM switch. | `reading/R42` (new) |
| FR-003 | Clicking the control on a song page SHALL start a Go To of that song at its first screen: the display state gains `{kind: 'song', song_id: <id>, index: 0}` while the adopted service, its screen, its translation and the on-air flag are left untouched, and `{type: 'goto'}` is broadcast on the display channel. When the stored state already opens this song, the pointer is left untouched — the control never resets a detour it already opened. | `dock/R12` (new) |
| FR-004 | Clicking the control on a chapter page SHALL start a Go To of that chapter: `{kind: 'passage', book_id: <book>, chapter: <chapter>, verse: 1, translation: <the edition the page shows>}`. When the stored state already opens this chapter, the pointer is left untouched, on the same terms as FR-003. | `dock/R12` (new) |
| FR-005 | The click SHALL also bring the projector window forward: a closed `gkps-projector` window is opened on `/projector`, an open one is focused without being reloaded. A popup the browser blocks opens nothing and leaves the Go To on air. The control always shows "Project" — it never displays Stop projecting. | `reading/R42` (new) |
| FR-006 | A Go To started from these pages SHALL compose with the existing Go To rules (`dock/R1`): it replaces any detour on air from any surface, it never adopts or releases a service, and Back on the projector ends it exactly as a dock-started Go To ends. | `dock/R12` (new) |
| FR-007 | The control SHALL NOT be drawn on a book page with no chapter on stage, on a song with no verses, on any saved (offline) page, or below 720px. | `reading/R42` (new) |
| FR-008 | The projector SHALL fetch and paint a Go To only when it differs from the detour already open: an identical pointer — the same detour at the same position, from any surface — neither fetches nor repaints, so the open detour keeps its place. The projector's own verse/screen navigation and a genuinely different pointer are unaffected. | `projector/R1` (modified) |

**Non-goals**: the dock and the OBS overlay are unchanged. The projector page changes only by FR-008's guard; everything else it does today — applying a stored Go To on boot and over the channel (specs 136/185), the payload endpoints `/projector/goto/song/<id>/` and `/projector/goto/chapter/<book>/<chapter>/` — is unchanged. The saved renderer is unchanged (it draws nothing new).

### Key Entities

- **Display state** (`gkps-display`) — `{service, screen, on, translation, at, session, goto}`; the Go To is a pointer into it, written by `display.js`'s `goTo` verb (spec 185) and read by the projector page, the dock and the overlay.
- **Go To pointer** — `{kind: 'song', song_id, index}` or `{kind: 'passage', book_id, chapter, verse, translation}`; the projector fetches what it paints from the goto endpoints.
- **Projector window** — the browser's named `gkps-projector` window (spec 141's named window); opening focuses an existing one rather than spawning a second.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | One click from a song page puts that song on air at its first screen; an adopted service keeps its place and returns after Back. | Targeted E2E on the running app |
| SC-002 | One click from a chapter page puts that chapter on air at its start verse in the shown edition; the projector's flip reaches the other edition. | Targeted E2E on the running app |
| SC-003 | With no projector window the click opens one already showing the detour; with one open the click focuses it; a second window never opens. | Targeted E2E (window handle count) |
| SC-004 | The control survives in-page navigation — no dead button after the stage swap. | Targeted E2E: navigate song→song, chapter→chapter, click each time |
| SC-005 | A Go To started here is indistinguishable on the projector from one started at the dock's find band — same state shape, same payloads, same Back. | Inspection against `dock/R1` scenarios |
| SC-006 | Clicking Project for the detour already open changes nothing on the projector (no fetch, no repaint, place kept) and still brings the window forward. | Targeted E2E: click twice, assert identical screen and no second paint |

## UI/UX

- **Layout / position**: **Song page** — the control sits in `read__head-top` (flex, `justify-content: space-between`, gap 12px) at its right end, inside a `.read__project` group — flex, wrap, `justify-content: flex-end`, `align-items: center`, gap 8px, margin 0. The eyebrow stays left, the control right: the same slot the Tata Ibadah page uses. **Bible chapter page** — the control sits in the title row (`read__row`) at its right end, immediately right of the TB/SIM switch (title left; switch, then control).
- **Size / spacing**: `.read__project-btn` — height 34px, padding 0 14px, border-radius 9px, icon 15×15px (20×20 viewBox), icon-to-label gap 6px, font 600 13px/1.
- **Icon**: the projector glyph already in use on the Tata Ibadah page (body rect, lens circle, three waves), copied verbatim — no new icon.
- **Colour / typography**: rest — border `--divider`, ink `--head-ink`, background none; hover — ink `--ink`, border `--focus`, background `--icon-hover-bg`; focus-visible — 2px `--focus` outline, offset 2px. All existing tokens.
- **States**: rest · hover · focus-visible. No toggle, no pressed state: the control is one act, and ending the detour stays the projector's Back (assumption A1).
- **Motion**: none beyond the button's existing `--ease` transition on border-color/color/background.
- **Labels**: accessible name and tooltip "Project".
- **Breakpoints**: the group wraps inside a narrow pane (row-gap 8px, as the tatib header does); below 720px the control is not drawn (FR-007).

Preview reference: `specs/193-reading-project-button/preview/index.html` (static, assembled from the real header markup and stylesheet).

## Assumptions

- **A1 — No Stop state.** The control always reads "Project" and never displays Stop projecting. The Tata Ibadah button toggles because it owns the service display; this control starts a detour the projector's Back ends, so a second state would name an act this page cannot see.
- **A2 — Verse-less songs draw no control** (FR-007): the page already says "This song has no verses yet", and a detour with an empty screen set would paint a blank.
- **A3 — The detour takes the edition the page shows** (TB default, SIM when reading SIM); the projector's edition flip reaches the other, which is the existing passage-detour behaviour.
- **A4 — Saved pages draw nothing** — matching today's saved renderer, which draws no project controls on any page.
- **A5 — The control is a reader control**: not editor-gated, like the Tata Ibadah Project control.
- **A6 — The Go To goes on air even when the window cannot open** (popup blocked): the two acts are independent, and the operator can open the projector window by hand.
- **A7 — The song detour starts at index 0** (first screen), the same start the dock's find band writes.
- **A8 — Hidden words resume in place.** If the operator has hidden the words (`hide`) while this detour is open, the click resumes rather than restarting: the pointer is untouched and the display comes back on at the place it kept.

## Clarifications

### Session 2026-11-14

- Q: Which verse should the projector's detour start on when Project is clicked on a chapter page?
  → A (owner): **Verse 1** — the chapter from the top; the arrow keys walk down from there. The
  scrolled/`?v=` position was declined. Recorded in US2/AC1 and FR-004.
- Revision at gate 1 (owner, 2026-11-14): on the Bible chapter page the control belongs in the
  **title row, right of the translation switch** — not in the top row beside the hidden eyebrow.
  Recorded in FR-002, US2/AC4 and UI/UX; preview re-drawn.
- Ruling at gate 1 (owner, 2026-11-14, second showing): unlike the service page's Project button,
  these controls **never display Stop projecting** — always Project, and every click opens or
  reuses the projector window; and **the projector window only fetches the Go To content when it
  differs from the detour already open**. Recorded in FR-003, FR-004, FR-005, FR-008,
  US1/AC4, US2/AC5 and A1.
- Zero `[NEEDS CLARIFICATION]` markers remain.
