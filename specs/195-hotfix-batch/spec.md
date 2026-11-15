# Feature Specification: Production hotfixes — 2026-11-15

**Slice**: `specs/195-hotfix-batch`
**Branch**: `fix/195-hotfix-batch`
**Created**: 2026-11-15
**Status**: Accepted (Gate 1, 2026-11-15)
**Input**: six production defects reported on `multimedia-gkps-klender.vercel.app` with screenshots (2026-11-15): the Today badge under the row actions, the Copy as template button unstyled in the edit modal, the dead date picker in create-from-template, the song-entry verses save refusal, the overlay lyric painting past two lines, and the overlay not catching saved entry changes.

## User Scenarios & Testing

### US1 — The Today badge steps aside while a row's actions are revealed (P1)

**Why this priority**: on a Today row the revealed edit/delete controls paint on top of the badge, so the row's most important mark is obscured exactly when the operator acts on it.

**Independent Test**: hover a dated Tata Ibadah row that carries the Today badge; the badge is not painted while the controls are up, and returns when the pointer leaves.

**Acceptance scenarios**

1. **Given** a Today row at rest, **When** it is inspected, **Then** the badge paints exactly as accepted by spec 132 (same position, colours, size).
2. **Given** the row is hovered, **When** the edit/delete controls are revealed, **Then** the badge is not painted, the way spec 190 already hides the row's date.
3. **Given** the pointer leaves the row, **When** the controls hide, **Then** the badge paints again.
4. **Given** a keyboard user focuses a row's control, **When** the controls are revealed by focus, **Then** the badge is not painted for the same reveal.
5. **Given** a touch device (no hover), **When** the actions are shown by the existing touch rules, **Then** the badge follows the same reveal the date does.

### US2 — Copy as template stands in the edit modal's header, right of the title (P1)

**Why this priority**: the button currently falls below the title as an unstyled element — it reads as broken, and spec 167's accepted design put it in the header at measured size.

**Independent Test**: open a Tata Ibadah's Edit modal; the title and the button share one header row with the button right-aligned at 34px tall; the confirmation flow still works.

**Acceptance scenarios**

1. **Given** the Edit Tata Ibadah modal, **When** it renders, **Then** the header is one row: title left, Copy as template right, with the hairline rule under the row as the preview drew.
2. **Given** the button, **When** measured, **Then** it is 34px tall with the preview's padding, border, radius and type.
3. **Given** the button is hovered or focused, **When** the state applies, **Then** the preview's hover and focus states paint (border and background on hover, the standard focus ring).
4. **Given** the button is clicked, **When** the confirmation opens and is accepted, **Then** the copy proceeds exactly as before (behaviour unchanged).

### US3 — The date picker opens in the create-from-template dialog (P1)

**Why this priority**: the dialog's second step cannot be completed by hand — the date field is dead, so creating from a template via the dialog fails on the click path people actually use.

**Independent Test**: on a template page reached by clicking through the sidebar, open New Tata Ibadah, step to Name and date, click the Date field; the calendar opens and a chosen day fills the field.

**Acceptance scenarios**

1. **Given** the dialog arrived with a stage swap (the sidebar click path), **When** the Date trigger is clicked, **Then** the calendar opens.
2. **Given** the calendar is open, **When** a day is chosen, **Then** the field shows the chosen date in the dialog's wording and the Create step accepts it.
3. **Given** the dialog arrived by full page load (deep link), **When** the Date trigger is clicked, **Then** the calendar opens as before — no regression on the already-initialised path.
4. **Given** the editor modal's own date fields, **When** a form fragment is swapped, **Then** their pickers still initialise (the existing `date-picker:initialize` path is preserved).

### US4 — A new song entry saves with the verses that were picked (P1)

**Why this priority**: the checklist submits verse numbers while the server validates verse IDs (the spec 189 storage change), so no fresh pick can be saved; and after a refusal the re-rendered checklist reads verse IDs as its numbers.

**Independent Test**: in a New song dialog, pick a song, check verses, save; the entry is created and the stage names the picked verse numbers; the summary names numbers in both the fresh and the re-rendered checklist.

**Acceptance scenarios**

1. **Given** a fresh song entry, **When** verses are picked and Save is pressed, **Then** the entry is created — no "Select a valid choice" and no "Keep at least one verse" refusal.
2. **Given** the verses summary, **When** it renders from a fresh pick or a re-rendered checklist, **Then** it names verse numbers ("Verses 1, 3"), never verse IDs.
3. **Given** the server-rendered checklist (edit modal, or the re-render after a refusal), **When** it is inspected, **Then** it carries the same row styling as the client-rendered checklist — same checkbox look, same number beside each box.
4. **Given** a song entry being edited, **When** its stored verses are rendered, **Then** the checklist checks the stored verses and names their numbers.
5. **Given** an empty checklist submitted, **When** the form validates, **Then** the existing refusal ("Keep at least one verse in the service.") still applies.

### US5 — A song lyric never paints more than two lines on the overlay (P1)

**Why this priority**: the overlay's caption was designed as a two-line block (a two-line lyric at 1080p paints 1728×202); long lines currently wrap the block to three or more rows, breaking the design and covering more of the stream than accepted.

**Independent Test**: paint a song screen whose lines wrap at the caption's box; the block stays within two visual lines by shrinking its type, and no screen paints a third line.

**Acceptance scenarios**

1. **Given** a two-line lyric whose lines fit at the accepted size, **When** it is on air at 1920×1080, **Then** the caption paints exactly as accepted by spec 183's numbers (1728×202 at (96, 824), 72px) — no shrink on screens that already fit.
2. **Given** a lyric line that would wrap, **When** the screen is painted, **Then** the type shrinks until the whole block fits two visual lines.
3. **Given** the shrunken caption, **When** the screen steps to another lyric, **Then** the next screen's type is fitted for its own words, not carried over.
4. **Given** a lyric so long that even the smallest fitted size cannot reach two lines, **When** it is painted, **Then** the type stops at the floor the stylesheet already declares (11px) and the block may exceed two lines — recorded as the one accepted edge.

### US6 — A saved change reaches the on-air surfaces (P1)

**Why this priority**: editing the on-air service leaves the OBS overlay (and the dock) painting old entries; the projector already re-reads, so the operator sees three surfaces disagree mid-service. The overlay and dock live in OBS's own browser, separate from the browser the site is edited in (owner, 2026-11-15), so no channel message can reach them — they must discover the change themselves.

**Independent Test**: with a service on air in the overlay, edit one of its entries in a separate browser; the overlay repaints the changed words within one poll interval, without a manual reload, and the dock's step list follows.

**Acceptance scenarios**

1. **Given** a service on air in the overlay, **When** one of its entries is edited (add, edit, reorder, delete), **Then** the overlay repaints the screen it is showing with the new words within one poll interval.
2. **Given** the same act, **When** the dock is open, **Then** its step list and its painted screen follow the change the same way.
3. **Given** the projector page, **When** the same change lands, **Then** it keeps its existing re-read behaviour (no regression).
4. **Given** a change that does not alter the painted screen, **When** the re-read returns the same words, **Then** the overlay does not repaint (no flicker).
5. **Given** a same-browser surface, **When** the re-read message arrives, **Then** the surfaces drop their per-service cache and re-read at once — the message path stays the fast path.

## Edge Cases

- **US1**: a Today row on a touch device follows the same reveal rules the date does today (`hover: hover` guard).
- **US1**: the badge stays in the row's accessible label — only the painting steps aside.
- **US2**: a modal whose record offers no copy (non-tatib kinds) renders no button — the header layout must not shift anything for them.
- **US3**: a dialog opened while its picker is mid-initialisation must not double-bind (the existing ready guard holds).
- **US4**: a song with no verses keeps its existing named state ("This song has no verses", spec 162).
- **US4**: verse IDs remain the stored contract — nothing writes verse numbers into `ServiceEntry.verses`.
- **US5**: `prefers-reduced-motion` is untouched; the fit applies before the entrance animation runs.
- **US6**: the poll runs only while a service is on air and the page is visible; a backgrounded tab does not fetch. The poll fetches the same projector data the projector page itself re-reads (`no-store`), so no write path can be missed — the islands are the painted truth.
- **US6**: a stale re-read that lands after the state moved on must not paint for the old state (the existing guard holds).

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | While a Tata Ibadah row's actions are revealed (hover or focus), the Today badge is not painted; it returns when the reveal ends. | `reading` (row actions, spec 190's reveal; badge, spec 132) |
| FR-002 | The Edit Tata Ibadah modal renders its header as one row — title left, Copy as template right — at the sizes spec 167 accepted, styled per its preview. | `reading` (R37) |
| FR-003 | The create-from-template dialog's date picker initialises whatever path the dialog arrived by, and opens on its trigger's click. | `reading` (R36) |
| FR-004 | The song entry's verse checklist submits verse IDs (the spec 189 contract), rendering verse numbers as its labels; the verses summary names verse numbers in both the fresh and the server-rendered checklist. | `reading` (song entry form, spec 189) |
| FR-005 | The server-rendered verse checklist carries the client-rendered checklist's row styling. | `reading` (song entry form) |
| FR-006 | The empty-verses refusal, the no-verses named state and the stored-ID contract are preserved. | `reading` (R30 + spec 189's storage contract) |
| FR-007 | A song screen's caption shrinks its type until the block fits two visual lines, keeping the accepted look (weight, outline, inset, centring); a screen that already fits paints at the accepted size. | `overlay` (R2 modified) |
| FR-008 | A saved entry change re-reads what is on air on every painted surface — overlay and dock included — and repaints only when the words changed. A surface in another browser (OBS's own) discovers the change by re-reading the service's screen data on a timer while a service is on air; a same-browser surface also drops its cache when the re-read message arrives. | `overlay` (R1) / `display-state` |

### Key Entities

- **ServiceEntry.verses** — stays a list of verse IDs; only the picker's submitted values change.
- **Display state (`gkps-display`)** — unchanged shape; the re-read is a read act, not a state write.
- **The overlay's per-service cache** — gains invalidation so a re-read fetches fresh screens.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A hovered Today row shows controls over no badge. | preview state + DOM check |
| SC-002 | The edit modal's header lays out as one row at the accepted numbers. | preview state + computed-style check |
| SC-003 | The dialog's calendar opens on the swap path and the deep-link path. | live click-through |
| SC-004 | A fresh song entry saves with its picked verses; summaries name numbers. | live click-through + view test |
| SC-005 | A wrapping lyric paints ≤ 2 visual lines at every screen. | overlay fixture + measurement |
| SC-006 | An edited on-air entry repaints the overlay and the dock. | live two-surface check |

## UI/UX

- **US1** — no new geometry: the badge keeps `components.css` 1432–1446 exactly; the hide mirrors the date hide at 1425–1428 (`hover: hover` guard, `:hover` + `:focus-within`).
- **US2** — ported from spec 167's preview: `.editor__head` flex, space-between, 16px gap, 16px bottom margin, 14px bottom padding, hairline rule; `.editor__copy-btn` 34px tall, 13px horizontal padding, 1px `--divider` border, 8px radius, 13px/560 type, transparent background, hover border `--focus` + `--icon-hover-bg`, focus ring 2px `--focus` offset 2.
- **US4** — the checklist keeps the client-rendered row anatomy (`.editor__verses > div` inline-flex, labels per 2623+); the server-rendered `<ul>` gets the same box model so both renders read alike; the summary wording stays "Verses 1, 3".
- **US5** — the caption keeps its accepted rest state (72px at 1080p, weight 800, outline, 5% inset, centred, `text-wrap: balance`); the fit only ever changes `font-size`, measured per paint, never below the 11px floor.
- **US6** — no visual change; surfaces repaint through their existing animations.

Preview reference: `specs/195-hotfix-batch/preview/index.html` (static: US1 row states, US2 modal header, US5 caption fit). US3, US4 and US6 are previewed live: `python manage.py runserver 0.0.0.0:8765 --noreload` in the slice worktree, then the click paths named in `preview/README.md`.

## Assumptions

- US1's reveal set is the existing one (`:hover` and the control's own focus reveal, hover-capable pointers only) — the badge follows the date's already-accepted rule rather than inventing a new one.
- US2's numbers come from spec 167's accepted preview, which was never ported; the product CSS receives that block verbatim (tokens for the values the preview took from the design tokens).
- US4's fix is client-contract alignment: the picker submits IDs end to end. The server keeps refusing a genuinely empty checklist.
- US5's fit targets the song caption only; passage and liturgy plates are untouched.
- US6's mechanism: the overlay and the dock poll the service's screen data on a timer (10 s interval — recorded as a default the owner can move at gate 2) while a service is on air, and drop their per-service cache whenever the re-read message arrives. No model changes, no new endpoint: the poll reads the projector page's own islands, so every write path that changes what is painted shows up.

## Clarifications

### Session 2026-11-15

- Q: "when a service is on air and you edit its entries, do you edit in the same browser that runs OBS's dock and overlay, or in a separate browser window?" → A: **separate browser** — the site is edited in Firefox/Chrome while OBS runs its own dock and overlay sources. No channel message can reach OBS, so the overlay and the dock discover changes themselves (a timed re-read of the projector data); the message path stays for same-browser surfaces. Recorded in FR-008, US6 and Assumptions; no `[NEEDS CLARIFICATION]` markers remain.
